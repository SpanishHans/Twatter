from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import Text, String, Boolean, DateTime, ForeignKey, func
from shared.models.user import Base

class Twatt(Base):
    __tablename__ = "twatts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_reshare: Mapped[bool] = mapped_column(Boolean, default=False)
    original_twatt_id: Mapped[int | None] = mapped_column(
        ForeignKey("twatts.id", ondelete="SET NULL"), nullable=True
    )

    media_files: Mapped[list["Media"]] = relationship(
        back_populates="twatt", cascade="all, delete-orphan"
    )

class Media(Base):
    __tablename__ = "media_files"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    twatt_id: Mapped[int] = mapped_column(ForeignKey("twatts.id", ondelete="CASCADE"))
    media_type: Mapped[str] = mapped_column(String(50), nullable=False)
    media_url: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    twatt: Mapped["Twatt"] = relationship(back_populates="media_files")
