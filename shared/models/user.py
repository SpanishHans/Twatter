from typing import TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from datetime import datetime
from typing import Optional

from shared.models.base import Base
if TYPE_CHECKING:
    from shared.models.twatt import Twatt

class User_on_db(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        unique=True,  # Automatically creates index
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        nullable=False
    )
    profile_picture: Mapped[Optional[str]] = mapped_column(
        nullable=True
    )
    biography: Mapped[Optional[str]] = mapped_column(
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    twatts: Mapped[list["Twatt"]] = relationship(back_populates="user")