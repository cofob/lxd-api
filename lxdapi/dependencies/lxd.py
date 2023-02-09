"""Module containing LXD dependency."""

from aiolxd import LXD
from fastapi import Request


def get_lxd(request: Request) -> LXD:
    """Get AioLXD session from request.

    Returns:
        LXD: Prepared AioLXD session.
    """
    return request.state.lxd
