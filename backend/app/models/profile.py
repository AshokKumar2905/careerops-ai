from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.session import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    education_level: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    degree: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    field_of_study: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    graduation_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    experience_level: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    career_goal: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
