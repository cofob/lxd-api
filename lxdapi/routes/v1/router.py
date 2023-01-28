"""Version 1 API."""
from fastapi import APIRouter

from . import ping

router = APIRouter(tags=["v1"])
router.include_router(ping.router)
