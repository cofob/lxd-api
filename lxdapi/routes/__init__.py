"""Module containing all FastAPI routes."""
from fastapi import APIRouter

from .v1 import router as v1_router

router = APIRouter()
router.include_router(v1_router.router, prefix="/api/v1")
