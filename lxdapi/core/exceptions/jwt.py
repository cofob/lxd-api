"""JWT-related exceptions."""

from .abc import AbstractException, UnprocessableEntityException


class JWTException(AbstractException):
    """Base JWT exception."""


class TokenInvalidException(JWTException, UnprocessableEntityException):
    """JWT token is invalid."""

    detail = "JWT token is invalid"
