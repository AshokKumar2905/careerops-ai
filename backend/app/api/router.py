from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.dependencies import get_database
from backend.app.models.career import Career
from backend.app.models.career_skill import CareerSkill
from backend.app.models.industry import Industry
from backend.app.models.skill import Skill
from backend.app.schemas.career import CareerAnalysisRequest
from backend.app.services.ai.provider import get_ai_provider
from backend.app.services.career_engine import (
    recommend_careers,
    recommendation_to_dict,
)


router = APIRouter(prefix="/api/v1")


@router.get("/system/health")
def system_health():
    return {
        "status": "ok",
        "service": "careerops-ai-api",
    }


def load_career_catalog(db: Session) -> list[dict]:
    """Load careers and their required skills from PostgreSQL."""

    rows = db.execute(
        select(
            Career.id,
            Career.title,
            Career.description,
            Career.experience_level,
            Industry.name.label("industry"),
            Skill.name.label("skill"),
        )
        .join(
            Industry,
            Industry.id == Career.industry_id,
        )
        .outerjoin(
            CareerSkill,
            CareerSkill.career_id == Career.id,
        )
        .outerjoin(
            Skill,
            Skill.id == CareerSkill.skill_id,
        )
        .order_by(Career.id)
    ).all()

    careers: dict[int, dict] = {}

    for row in rows:
        if row.id not in careers:
            careers[row.id] = {
                "title": row.title,
                "industry": row.industry,
                "description": row.description or "",
                "experience_level": row.experience_level or "",
                "skills": [],
            }

        if row.skill:
            careers[row.id]["skills"].append(row.skill)

    return list(careers.values())


@router.post("/career/analyze")
def analyze_career(
    request: CareerAnalysisRequest,
    db: Session = Depends(get_database),
):
    """Analyze a career profile using rules plus the configured AI provider."""

    profile = request.model_dump()

    careers = load_career_catalog(db)

    recommendations = recommend_careers(
        profile=profile,
        careers=careers,
        top_n=5,
    )

    recommendation_data = [
        recommendation_to_dict(recommendation)
        for recommendation in recommendations
    ]

    ai_provider = get_ai_provider(settings.ai_provider)

    ai_analysis = ai_provider.analyze_career(
        profile=profile,
        recommendations=recommendation_data,
    )

    return {
        "status": "success",
        "message": "Career analysis completed",
        "recommendations": recommendation_data,
        "ai_analysis": ai_analysis,
    }