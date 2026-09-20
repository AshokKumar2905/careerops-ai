from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.session import Base


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("career_assessments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    results: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
