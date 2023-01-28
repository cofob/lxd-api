"""Worker module."""
import logging
from asyncio import create_task, sleep
from dataclasses import dataclass
from time import time
from typing import Any, Callable, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession

from lxdapi.core.config import Config
from lxdapi.dependencies.database import get_db_deprecated

log = logging.getLogger(__name__)


@dataclass
class Cron:
    """Cron class."""

    func: Callable[..., Coroutine[Any, Any, None]]
    every: float | int
    current: int = 0


class Worker:
    """Worker class."""

    def __init__(self, debug: bool = False) -> None:
        """Initialize worker."""
        self.task_counter = 0
        self.debug = debug
        self.cron = [
            Cron(self.function_proxy(self.test_job), every=60 * 5),
        ]
        self.interval = 5
        self.config = Config.from_env()
        log.debug("Worker initialized")

    async def run(self) -> None:
        """Run worker."""
        log.info("Worker started scheduled tasks.")
        # Prepare tasks
        for cron in self.cron:
            if cron.every % self.interval != 0:
                old = cron.every
                cron.every = cron.every - (cron.every % self.interval) + self.interval
                log.warning("Interval is not a divisor of every. Fixing from %s to %s", old, cron.every)
        if self.debug:
            log.info("Debug mode enabled. Starting all tasks...")
            for cron in self.cron:
                await cron.func()
        else:
            while True:
                for cron in self.cron:
                    diff = cron.every / self.interval
                    log.debug(f"Current: {cron.current}, every: {cron.every}, interval: {self.interval}, diff: {diff}")
                    if cron.current >= diff:
                        create_task(cron.func())
                        cron.current = 0
                    else:
                        cron.current += 1
                log.debug(f"Sleeping for {self.interval} seconds...")
                await sleep(self.interval)

    def function_proxy(
        self,
        func: Callable[..., Coroutine[Any, Any, None]],
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> Callable[[], Coroutine[Any, Any, None]]:
        """Proxy function.

        Pass to it essential dependencies and catch errors.

        Essential dependencies are:
        - Database session (AsyncSession, first positional argument)

        Args:
            func (Callable): Function to proxy.
            *args: Arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.
        """

        async def function_proxy_inner() -> None:
            task_id = self.task_counter
            self.task_counter += 1
            try:
                db = get_db_deprecated(self.config)
                log.info(f"Running task {func.__name__}#{task_id}...")
                start_time = time()
                await func(db, *args, **kwargs)
                elapsed_time = time() - start_time

                if elapsed_time > self.interval:
                    log.warning(
                        f"Task {func.__name__}#{task_id} took {elapsed_time} seconds, but it should take"
                        + f"less than {self.interval} seconds. Increase interval or split task."
                    )
                else:
                    log.debug(f"Task {func.__name__}#{task_id} took {elapsed_time} seconds.")
            except Exception as e:
                log.error(f"Error in task {func.__name__}#{task_id}")
                log.exception(e)

        return function_proxy_inner

    async def test_job(self, _db: AsyncSession) -> None:
        """Test job."""
        log.debug("Test job started")
        await sleep(10)
        log.debug("Test job finished")
