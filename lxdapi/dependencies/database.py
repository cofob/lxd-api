"""Module containing database setup and dependency."""

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from lxdapi.core.config import Config


def get_db_deprecated(config: Config) -> AsyncSession:
    """Get async database session instance with current engine.

    *Deprecated*: Use get_db instead.

    Returns:
        AsyncSession: Prepared database session.
    """
    engine = create_async_engine(config.DATABASE_URL, future=True)
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)()  # type: ignore


def get_db(request: Request) -> AsyncSession:
    """Get database session from request.

    Returns:
        AsyncSession: Prepared database session.
    """
    return request.state.db
