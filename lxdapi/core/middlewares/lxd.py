"""Database middleware."""

import logging

from aiolxd import LXD
from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.types import ASGIApp

log = logging.getLogger(__name__)


class AioLXDMiddleware(BaseHTTPMiddleware):
    """Database session middleware."""

    def __init__(self, app: ASGIApp, lxd: LXD) -> None:
        """Initialize."""
        super().__init__(app)
        self.lxd = lxd
        self._is_initialized = False

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Dispatch."""
        if not self._is_initialized:
            await self.lxd.start()
            self._is_initialized = True
        request.state.lxd = self.lxd
        return await call_next(request)
