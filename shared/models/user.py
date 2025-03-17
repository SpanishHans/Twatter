from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime

from shared.models.base import Base


class User_on_db(Base):
    __tablename__ = "users"  # changed from 'usuarios' to 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    profile_picture: Mapped[str] = mapped_column(nullable=True)
    biography: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)
