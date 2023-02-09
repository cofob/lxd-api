"""Default exception handlers for the intape package."""
from aiolxd import exceptions as lxd_exceptions
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .abc import AbstractException


class ErrorSchema(BaseModel):
    """Error response for AbstractException."""

    ok: bool = False
    status_code: int = 500
    detail: str | None = None
    error_code: str = "Exception"
    exception_chain: list[str] = ["Exception"]


def register_exception_handler(app: FastAPI) -> None:
    """Register exception handlers."""

    @app.exception_handler(AbstractException)
    async def abstract_exception_handler(request: Request, exc: AbstractException) -> JSONResponse:
        """Exception handler for AbstractException.

        Returns:
            JSON serialized ErrorModel.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorSchema(
                error_code=exc.__class__.__name__,
                detail=exc.detail,
                status_code=exc.status_code,
                exception_chain=exc.exception_chain,
            ).dict(),
            headers=exc.headers,
        )

    @app.exception_handler(lxd_exceptions.AioLXDException)
    async def lxd_exception_handler(request: Request, exc: lxd_exceptions.AioLXDException) -> JSONResponse:
        """Exception handler for AioLXDException.

        Returns:
            JSON serialized ErrorModel.
        """
        return JSONResponse(
            status_code=500,
            content=ErrorSchema(
                error_code=exc.__class__.__name__,
                detail=str(exc),
                status_code=500,
                exception_chain=["AioLXDException", exc.__class__.__name__],
            ).dict(),
        )
