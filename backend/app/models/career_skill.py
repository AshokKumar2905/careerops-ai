from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.session import Base


class CareerSkill(Base):
    __tablename__ = "career_skills"

    __table_args__ = (
        UniqueConstraint("career_id", "skill_id", name="uq_career_skill"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    career_id: Mapped[int] = mapped_column(
        ForeignKey("careers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    importance: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
