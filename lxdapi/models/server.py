"""Server model."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .abc import AbstractModel

if TYPE_CHECKING:
    from .user import UserModel


class ServerModel(AbstractModel):
    """Server model."""

    __tablename__ = "servers"

    id: int = Column("id", Integer, primary_key=True)
    user_id: int = Column("user_id", Integer, ForeignKey("users.id"))
    user: "UserModel" = relationship("UserModel", back_populates="servers", lazy="joined")
    name: str = Column("name", String(255), nullable=False)
    cpu: float = Column("cpu", Float, nullable=False)
    memory: int = Column("memory", Integer, nullable=False)
    disk: int = Column("disk", Integer, nullable=False)
    system: str = Column("system", String(255), nullable=False)
    ip: str = Column("ip", String(255), nullable=False)
    is_deleted: bool = Column("is_deleted", Boolean, nullable=False, default=False)
    is_active: bool = Column("is_active", Boolean, nullable=False, default=False)
