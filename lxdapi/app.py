"""Module containing main FastAPI application."""
import logging
from os.path import isfile

from aiolxd import LXD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from .core.config import Config
from .core.exceptions.handler import register_exception_handler
from .core.middlewares import (
    AioLXDMiddleware,
    ConfigMiddleware,
    DBAsyncSessionMiddleware,
)
from .routes import router

log = logging.getLogger(__name__)

VERSION = ""

# Read git commit hash from file, if it exists
if isfile("version"):
    try:
        with open("version") as f:
            VERSION = f.read().strip()[:6]
    except Exception:
        pass

VERSION = "0.1.0" + (f"-{VERSION}" if VERSION else "")


class App:
    """FastAPI application."""

    def __init__(self, config: Config, app: FastAPI | None = None) -> None:
        """Initialize FastAPI application."""
        self.config = config

        if app is None:
            self.app = FastAPI(
                title="LXD API",
                description="""**LXD API** is a REST API for LXD. It provides a way to manage LXD containers.""",
                version=VERSION,
            )
        else:
            self.app = app

        self.setup_app()

    @classmethod
    def from_env(cls) -> "App":
        """Create application from environment variables."""
        return cls(Config.from_env())

    def setup_app(self) -> None:
        """Add middlewares and routers to FastAPI application."""
        self.app.include_router(router)

        # lxd
        self.lxd = LXD.with_async(self.config.LXD_URL, cert=(self.config.LXD_CERT, self.config.LXD_KEY))

        # cors middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        # middlewares
        self.app.add_middleware(DBAsyncSessionMiddleware, config=self.config)
        self.app.add_middleware(ConfigMiddleware, config=self.config)
        self.app.add_middleware(AioLXDMiddleware, lxd=self.lxd)
        # exception handler
        register_exception_handler(self.app)
