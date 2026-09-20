from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AIProvider(ABC):
    """Base interface for CareerOps AI providers."""

    @abstractmethod
    def analyze_career(
        self,
        profile: dict[str, Any],
        recommendations: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Generate personalized career analysis."""
        raise NotImplementedError


class LocalAIProvider(AIProvider):
    """
    Local fallback provider.

    This version does not call an external AI service.
    It creates structured guidance from the recommendation
    engine results.
    """

    def analyze_career(
        self,
        profile: dict[str, Any],
        recommendations: list[dict[str, Any]],
    ) -> dict[str, Any]:
        if not recommendations:
            return {
                "summary": (
                    "We could not find a strong career match "
                    "from the information provided."
                ),
                "strengths": profile.get("skills", []),
                "priority_skills": [],
                "next_steps": [
                    "Add more interests.",
                    "Add more current skills.",
                    "Describe your career goals in more detail.",
                ],
            }

        top = recommendations[0]

        matched_skills = top.get("matched_skills", [])
        missing_skills = top.get("missing_skills", [])
        career_title = top.get(
            "title",
            "this career path",
        )

        return {
            "summary": (
                f"Your profile currently aligns with "
                f"{career_title}. The recommendation is based "
                "on your interests, skills, education, experience "
                "and career goal."
            ),
            "strengths": matched_skills,
            "priority_skills": missing_skills[:5],
            "next_steps": [
                f"Explore the {career_title} career path.",
                "Build projects that demonstrate relevant skills.",
                "Develop the highest-priority missing skills.",
                "Review suitable certifications and learning resources.",
                "Compare this path with other recommended careers.",
            ],
        }


def get_ai_provider(provider_name: str) -> AIProvider:
    """Return the configured AI provider."""

    normalized = provider_name.strip().lower()

    if normalized == "local":
        return LocalAIProvider()

    raise ValueError(
        f"Unsupported AI provider: {provider_name}"
    )