"""Global application configuration."""
import logging
from dataclasses import dataclass
from os import environ

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Config:
    """Global application configuration."""

    DATABASE_URL: str
    SECRET: str
    LXD_URL: str
    LXD_CERT: str
    LXD_KEY: str
    ORIGINS: tuple[str, ...] = ("*",)

    @staticmethod
    def _get_env(name: str, default: str | None = None) -> str:
        """Get environment variable.

        Args:
            name (str): Name of the environment variable.
            default (str | None): Default value if environment variable is not set.

        Returns:
            str: Value of the environment variable.

        Raises:
            ValueError: If environment variable is not set and default value is not provided.
        """
        val = environ.get(name)
        if val is None:
            if default is None:
                raise ValueError(f"Environment variable {name} is not set")
            return default
        return val

    @classmethod
    def from_env(cls) -> "Config":
        """Create application from environment variables."""
        origins = cls._get_env("ORIGINS", "undefined")
        if origins == "undefined":
            log.warning("ORIGINS environment variable is not set. Using default ('*') value.")
            ORIGINS = ("*",)
        else:
            ORIGINS = tuple(origins.split(","))  # type: ignore

        return cls(
            DATABASE_URL=cls._get_env("DATABASE_URL"),
            SECRET=cls._get_env("SECRET"),
            LXD_URL=cls._get_env("LXD_URL"),
            LXD_CERT=cls._get_env("LXD_CERT"),
            LXD_KEY=cls._get_env("LXD_KEY"),
            ORIGINS=ORIGINS,
        )
