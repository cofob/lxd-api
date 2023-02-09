"""User model."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .abc import AbstractModel

if TYPE_CHECKING:
    from .server import ServerModel


class UserModel(AbstractModel):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    is_banned = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    servers: list["ServerModel"] = relationship("ServerModel", back_populates="user")
    _permission_groups: str = Column("permission_groups", String(255), nullable=False, default="user")

    @property
    def permission_groups(self) -> list[str]:
        """Return the list of permission groups."""
        return self._permission_groups.split(",")

    @permission_groups.setter
    def permission_groups(self, value: list[str]) -> None:
        """Set the list of permission groups."""
        value = list(set(value))
        self._permission_groups = ",".join(value)
