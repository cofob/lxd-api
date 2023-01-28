"""Common exceptions for the LXD API."""

from .abc import InternalServerErrorException


class DatabaseException(InternalServerErrorException):
    """Exception raises when a database error occurs."""
