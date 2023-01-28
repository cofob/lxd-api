"""Config dependency."""
from fastapi import Request

from lxdapi.core.config import Config


def get_config(request: Request) -> Config:
    """Get config."""
    return request.state.config
