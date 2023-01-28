"""Authorization utils."""

from calendar import timegm
from datetime import datetime, timedelta
from logging import getLogger
from typing import Any

from jose import JWTError, jwt

from lxdapi.core.config import Config
from lxdapi.core.exceptions.jwt import TokenInvalidException

ALGORITHM = "HS256"
JSON_TYPE = dict[str, str | int | float | bool | None | dict[str, "JSON_TYPE"] | list["JSON_TYPE"]]

logger = getLogger(__name__)


def timegm_delta(**delta: Any) -> int:
    """Get timegm from timedelta."""
    return timegm((datetime.utcnow() + timedelta(**delta)).utctimetuple())


def timegm_now() -> int:
    """Get timegm from now."""
    return timegm(datetime.utcnow().utctimetuple())


def generate_iat_ts() -> int:
    """Get JWT iat field."""
    return timegm_now()


def encode(config: Config, data: JSON_TYPE) -> str:
    """Encode provided data to signed JWT token.

    Args:
        data: JWT data.

    Returns:
        str: JWT string.
    """
    return jwt.encode(data, config.SECRET, algorithm=ALGORITHM)


def decode(config: Config, token: str, options: dict[str, bool] = {}) -> JSON_TYPE:
    """Decode JWT token and return its data.

    Args:
        token: JWT token string.

    Raises:
        TokenInvalidException: If token is invalid.

    Returns:
        dict: Parsed JWT data.
    """
    # jose raises exception if jti field is not int, so we disable jti
    # check globally
    options["verify_jti"] = False
    try:
        return jwt.decode(
            token,
            config.SECRET,
            algorithms=[ALGORITHM],
            options=options,
        )
    except JWTError:
        logger.exception("JWT exception")
        raise TokenInvalidException(detail="JWT decode/verification error")
