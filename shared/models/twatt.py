from typing import TYPE_CHECKING, Optional, List
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, DateTime, ForeignKey, func, Integer, Enum as PgEnum

from shared.models.base import Base
if TYPE_CHECKING:
    from shared.models.user import User_on_db





class TwattType(str, Enum):
    ORIGINAL = "original"
    REPLY = "reply"
    RETWEET = "retweet"  # quotes y retweets

class Twatt(Base):
    __tablename__ = "twatts"

    #AUTOMATICO
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    #AUTOMATICO
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    #OBLIGATORIO
    twatt_type: Mapped[TwattType] = mapped_column(PgEnum(TwattType), nullable=False)
    #OBLIGATORIO
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE")
    )

    #OPCIONAL
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Nullable for pure retweets
    #OPCIONAL
    parent_twatt_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("twatts.id", ondelete="SET NULL"),
        nullable=True
    )

    # Count fields for perf
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    comments_count: Mapped[int] = mapped_column(Integer, default=0)
    retweet_count: Mapped[int] = mapped_column(Integer, default=0)
    bookmarks_count: Mapped[int] = mapped_column(Integer, default=0)
    views_count: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    user: Mapped["User_on_db"] = relationship(back_populates="twatts")
    media_files: Mapped[List["Media"]] = relationship(
        back_populates="twatt", cascade="all, delete-orphan"
    )
    parent_twatt: Mapped[Optional["Twatt"]] = relationship(
        "Twatt", remote_side=[id], backref="replies"
    )

class Media(Base):
    __tablename__ = "media_files"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True, 
        default=uuid.uuid4
    )
    twatt_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("twatts.id", ondelete="CASCADE"),
        unique=True,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    media_type: Mapped[str] = mapped_column(nullable=False)

    twatt: Mapped["Twatt"] = relationship(back_populates="media_files")
