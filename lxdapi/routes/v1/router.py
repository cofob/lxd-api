"""Version 1 API."""
from fastapi import APIRouter

from . import ping, server

router = APIRouter(tags=["v1"])
router.include_router(ping.router)
router.include_router(server.router)
