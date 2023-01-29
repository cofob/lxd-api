"""Abstract base classes for exceptions."""
from abc import ABCMeta
from typing import Type, TypeVar

from fastapi import status

T = TypeVar("T", bound="AbstractException")


class AbstractException(Exception, metaclass=ABCMeta):
    """Abstract exception.

    All custom exceptions must inherit from this class.

    Example:
    ```
        @exception
        class MyException(AbstractException):
            status_code = status.HTTP_400_BAD_REQUEST
            detail = "My custom exception"
            headers = {"X-Error": "There goes my error"}

        @exception
        class MyExceptionWithInit(AbstractException):
            def __init__(
                self,
                detail: str = "My custom exception",
                status_code: int = status.HTTP_400_BAD_REQUEST,
                headers: dict[str, str] = {"X-Error": "There goes my error"},
            ) -> None:
                # In __init__ we can do more complex logic, like setting status_code
                # based on some condition.
                super().__init__(detail, status_code, headers)
    ```
    """

    _http_exception: bool = False

    detail: str | None = None
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    headers: dict[str, str] | None = None
    exception_chain: list[str] = []

    def __init__(
        self,
        detail: str | None = None,
        status_code: int | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Exception init method.

        Args:
            detail: Short error description.
            status_code: HTTP status code that will be returned.
            headers: Dict with HTTP headers that will be returned.
        """
        # The logic here is a bit tricky with variable scopes: if the argument is not None
        # then we set it to `self`, otherwise we do nothing. This works because child-class
        # already declares variable, in case it is not passed to `__init__`. This is needed
        # for more customization possibilities, because the caller can overwrite any parameter,
        # but the class can also declare a standard value.
        if detail is not None:
            self.detail = detail
        if headers is not None:
            self.headers = headers
        if status_code is not None:
            self.status_code = status_code

        # If detail is specified, then pass it to Exception() constructor.
        # This logs the exception with detail to the console.
        if self.detail is not None:
            super().__init__(detail)
        else:
            # If detail is not specified, then pass the class name to Exception() constructor.
            # Example: "NotFoundException (404)."
            super().__init__(f"{self.__class__.__name__} ({self.status_code}).")

        # Build exception chain.
        #
        # Example: ["MyDomainException", "DomainException", "NotFoundException"]
        #
        # This is used to determine the exception type in the API response.
        # For example, if the exception is NotFoundException, then the frontend
        # can show a 404 icon. Or if the exception is DomainException, then the
        # frontend can show a generic error icon.
        #
        # Order is important here, because we want to show the most specific
        # exception first.
        if not self.exception_chain:
            for class_type in self.__class__.__mro__:
                if getattr(class_type, "_http_exception", False):
                    self.exception_chain.append(class_type.__name__)


def exception(exception_class: Type[T]) -> Type[T]:
    """Make exception class.

    This decorator is used to set the `_http_exception` attribute to True.
    """
    exception_class._http_exception = True
    return exception_class


# Define base exceptions for specific HTTP status codes.
# Usage: class MyDomainException(DomainException, NotFoundException): pass
# Order is important here, please see the comment in AbstractException.__init__.


@exception
class BadRequestException(AbstractException):
    """400 Bad Request."""

    status_code = status.HTTP_400_BAD_REQUEST


@exception
class UnauthorizedException(AbstractException):
    """401 Unauthorized."""

    status_code = status.HTTP_401_UNAUTHORIZED


@exception
class ForbiddenException(AbstractException):
    """403 Forbidden."""

    status_code = status.HTTP_403_FORBIDDEN


@exception
class NotFoundException(AbstractException):
    """404 Not Found."""

    status_code = status.HTTP_404_NOT_FOUND


@exception
class MethodNotAllowedException(AbstractException):
    """405 Method Not Allowed."""

    status_code = status.HTTP_405_METHOD_NOT_ALLOWED


@exception
class ConflictException(AbstractException):
    """409 Conflict."""

    status_code = status.HTTP_409_CONFLICT


@exception
class UnprocessableEntityException(AbstractException):
    """422 Unprocessable Entity."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


@exception
class InternalServerErrorException(AbstractException):
    """500 Internal Server Error."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@exception
class NotImplementedException(AbstractException):
    """501 Not Implemented."""

    status_code = status.HTTP_501_NOT_IMPLEMENTED


@exception
class ServiceUnavailableException(AbstractException):
    """503 Service Unavailable."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
