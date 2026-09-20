from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


@dataclass
class CareerRecommendation:
    title: str
    industry: str
    description: str
    match_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    reasons: list[str]


# -------------------------------------------------------------------
# COMMON TERM NORMALIZATION
# -------------------------------------------------------------------

TERM_ALIASES: dict[str, list[str]] = {
    # Technology
    "tech": ["technology"],
    "it": ["technology"],
    "information technology": ["technology"],
    "software": ["technology", "programming"],
    "software development": ["technology", "programming"],
    "web development": ["technology", "programming", "javascript"],
    "frontend": ["programming", "javascript"],
    "front end": ["programming", "javascript"],
    "backend": ["programming", "python"],
    "back end": ["programming", "python"],

    # Cloud / DevOps
    "aws": ["cloud computing"],
    "amazon web services": ["cloud computing"],
    "azure": ["cloud computing"],
    "gcp": ["cloud computing"],
    "google cloud": ["cloud computing"],
    "cloud": ["cloud computing"],
    "devops": ["automation", "cloud computing", "linux", "git"],
    "devops engineer": [
        "automation",
        "cloud computing",
        "linux",
        "git",
    ],
    "ci/cd": ["automation", "git"],
    "cicd": ["automation", "git"],
    "continuous integration": ["automation", "git"],
    "continuous delivery": ["automation", "git"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes"],

    # Data
    "data": ["data analysis"],
    "analytics": ["data analysis"],
    "data analytics": ["data analysis"],
    "business intelligence": ["data analysis", "business analysis"],
    "bi": ["data analysis", "business analysis"],
    "machine learning": ["machine learning", "python", "statistics"],
    "ml": ["machine learning", "python", "statistics"],
    "artificial intelligence": [
        "machine learning",
        "python",
        "data analysis",
    ],
    "ai": ["machine learning", "python", "data analysis"],

    # Cybersecurity
    "cyber security": ["cybersecurity"],
    "information security": ["cybersecurity"],
    "security": ["cybersecurity"],
    "ethical hacking": ["cybersecurity", "networking"],

    # Design
    "design": ["ui/ux design", "creativity"],
    "ui": ["ui/ux design"],
    "ux": ["ui/ux design"],
    "ui/ux": ["ui/ux design"],
    "user experience": ["ui/ux design", "user research"],
    "graphic design": ["graphic design", "creativity"],

    # Business
    "business": ["business analysis"],
    "management": ["leadership", "project management"],
    "project management": ["project management"],
    "marketing": ["marketing"],
    "sales": ["sales"],
    "operations": ["operations"],

    # Finance
    "finance": ["financial analysis", "accounting", "excel"],
    "banking": ["financial analysis", "accounting"],
    "accounting": ["accounting", "excel"],
    "investment": ["financial analysis", "financial modeling"],

    # Healthcare
    "healthcare": ["healthcare knowledge"],
    "medical": ["healthcare knowledge"],
    "medicine": ["healthcare knowledge"],
    "biology": ["biology"],
    "biotech": ["biology", "research"],
    "biotechnology": ["biology", "research"],

    # Education
    "education": ["teaching"],
    "teaching": ["teaching", "public speaking"],
    "training": ["teaching", "public speaking"],
    "research": ["research"],

    # Media
    "content": ["content writing"],
    "writing": ["content writing"],
    "media": ["communication", "creativity"],
    "journalism": ["journalism", "research"],
    "video": ["video editing", "creativity"],
    "video editing": ["video editing", "creativity"],
    "social media": ["social media", "communication"],

    # Law
    "law": ["legal research", "legal writing"],
    "legal": ["legal research", "legal writing"],
    "public service": ["civic knowledge", "communication"],
    "government": ["civic knowledge", "communication"],
    "policy": ["policy analysis", "research"],

    # Hospitality
    "hospitality": ["hospitality operations", "customer service"],
    "hotel": ["hospitality operations", "customer service"],
    "travel": ["travel planning", "customer service"],
    "tourism": ["travel planning", "customer service"],
    "events": ["event management", "customer service"],

    # Skilled trades
    "electrical": ["electrical maintenance", "electrical systems"],
    "electrician": ["electrical maintenance", "electrical systems"],
    "mechanical": ["mechanical maintenance", "mechanical design"],
    "welding": ["welding"],
    "plumbing": ["plumbing"],
    "construction": ["construction"],
}


EDUCATION_ALIASES: dict[str, list[str]] = {
    "computer science": [
        "technology",
        "programming",
        "data analysis",
        "problem solving",
    ],
    "computer engineering": [
        "technology",
        "programming",
        "networking",
        "problem solving",
    ],
    "information technology": [
        "technology",
        "programming",
        "cloud computing",
    ],
    "software engineering": [
        "technology",
        "programming",
        "problem solving",
    ],
    "data science": [
        "data analysis",
        "statistics",
        "machine learning",
        "python",
    ],
    "artificial intelligence": [
        "machine learning",
        "python",
        "data analysis",
    ],
    "commerce": [
        "accounting",
        "financial analysis",
        "business analysis",
        "excel",
    ],
    "business administration": [
        "business analysis",
        "project management",
        "operations",
    ],
    "management": [
        "leadership",
        "project management",
        "operations",
    ],
    "finance": [
        "financial analysis",
        "accounting",
        "excel",
    ],
    "economics": [
        "financial analysis",
        "statistics",
        "data analysis",
    ],
    "biology": [
        "biology",
        "research",
        "healthcare knowledge",
    ],
    "biotechnology": [
        "biology",
        "research",
        "statistics",
    ],
    "medicine": [
        "healthcare knowledge",
        "research",
        "clinical documentation",
    ],
    "design": [
        "ui/ux design",
        "graphic design",
        "creativity",
    ],
    "law": [
        "legal research",
        "legal writing",
        "policy analysis",
    ],
    "education": [
        "teaching",
        "public speaking",
        "curriculum development",
    ],
    "mechanical engineering": [
        "engineering fundamentals",
        "mechanical design",
        "autocad",
    ],
    "electrical engineering": [
        "engineering fundamentals",
        "electrical systems",
        "electrical maintenance",
    ],
}


EXPERIENCE_GROUPS: dict[str, set[str]] = {
    "entry": {
        "student",
        "fresher",
        "entry level",
        "entry-level",
        "graduate",
        "new graduate",
    },
    "junior": {
        "1-3 years",
        "1 to 3 years",
        "junior",
        "early career",
    },
    "mid": {
        "3-5 years",
        "3 to 5 years",
        "mid level",
        "mid-level",
        "mid career",
    },
    "senior": {
        "5+ years",
        "5 years",
        "senior",
        "lead",
        "principal",
    },
}


# -------------------------------------------------------------------
# TEXT HELPERS
# -------------------------------------------------------------------

def normalize(value: str) -> str:
    """Normalize text for safe comparison."""
    return re.sub(r"\s+", " ", str(value).strip().lower())


def tokenize(values: list[str]) -> set[str]:
    """Create normalized phrase and word tokens."""
    tokens: set[str] = set()

    for value in values:
        normalized = normalize(value)

        if not normalized:
            continue

        tokens.add(normalized)

        for token in re.findall(
            r"[a-z0-9+#./-]+",
            normalized,
        ):
            if len(token) >= 2:
                tokens.add(token)

    return tokens


def expand_terms(values: list[str]) -> set[str]:
    """
    Convert user language into canonical concepts.

    Example:
        AWS -> cloud computing
        DevOps -> automation, cloud computing, linux, git
        Tech -> technology
    """
    expanded: set[str] = set()

    for value in values:
        normalized = normalize(value)

        if not normalized:
            continue

        expanded.add(normalized)

        aliases = TERM_ALIASES.get(normalized, [])

        for alias in aliases:
            expanded.add(alias)

        # Also preserve useful individual words.
        for token in tokenize([normalized]):
            expanded.add(token)

    return expanded


def expand_text(values: list[str]) -> set[str]:
    """Expand a list of phrases and their aliases."""
    return expand_terms(values)


def related_terms(
    user_values: list[str],
    career_values: list[str],
) -> bool:
    """Check whether normalized concepts overlap."""
    user_terms = expand_text(user_values)
    career_terms = expand_text(career_values)

    if not user_terms or not career_terms:
        return False

    if user_terms.intersection(career_terms):
        return True

    # Partial phrase matching for longer terms.
    for user_term in user_terms:
        for career_term in career_terms:
            if (
                len(user_term) >= 4
                and len(career_term) >= 4
                and (
                    user_term in career_term
                    or career_term in user_term
                )
            ):
                return True

    return False


# -------------------------------------------------------------------
# EDUCATION
# -------------------------------------------------------------------

def education_concepts(
    field_of_study: str,
    degree: str,
) -> set[str]:
    """Convert education information into career concepts."""
    concepts = expand_text(
        [
            field_of_study,
            degree,
        ]
    )

    field = normalize(field_of_study)
    degree_text = normalize(degree)

    for source, aliases in EDUCATION_ALIASES.items():
        if source in field or source in degree_text:
            concepts.update(aliases)

    return concepts


# -------------------------------------------------------------------
# EXPERIENCE
# -------------------------------------------------------------------

def normalize_experience(value: str) -> str:
    """Map experience descriptions into broad groups."""
    normalized = normalize(value)

    if not normalized:
        return ""

    for group, values in EXPERIENCE_GROUPS.items():
        if normalized in values:
            return group

    return normalized


# -------------------------------------------------------------------
# SKILL MATCHING
# -------------------------------------------------------------------

def match_skills(
    user_skills: list[str],
    required_skills: list[str],
) -> tuple[list[str], list[str]]:
    """
    Match user's skills against career requirements.

    The returned matched list uses the career's canonical skill names.
    """
    user_concepts = expand_text(user_skills)

    matched_skills: list[str] = []
    missing_skills: list[str] = []

    for required_skill in required_skills:
        required_normalized = normalize(required_skill)

        if not required_normalized:
            continue

        required_concepts = expand_text([required_skill])

        matched = bool(
            user_concepts.intersection(required_concepts)
        )

        if matched:
            matched_skills.append(required_skill)
        else:
            missing_skills.append(required_skill)

    return matched_skills, missing_skills


# -------------------------------------------------------------------
# CAREER SCORING
# -------------------------------------------------------------------

def score_career(
    profile: dict[str, Any],
    career: dict[str, Any],
) -> CareerRecommendation:
    """
    Calculate a transparent career-match score.

    Maximum score:
        Interests:     35
        Skills:        35
        Education:     10
        Experience:    10
        Career goal:   10
        -----------------
        Total:        100
    """

    interests = [
        str(item)
        for item in profile.get("interests", [])
        if str(item).strip()
    ]

    user_skills = [
        str(item)
        for item in profile.get("skills", [])
        if str(item).strip()
    ]

    field_of_study = str(
        profile.get("field_of_study", "") or ""
    )

    degree = str(
        profile.get("degree", "") or ""
    )

    experience_level = str(
        profile.get("experience_level", "") or ""
    )

    career_goal = str(
        profile.get("career_goal", "") or ""
    )

    career_title = str(
        career.get("title", "") or ""
    )

    career_description = str(
        career.get("description", "") or ""
    )

    industry = str(
        career.get("industry", "") or ""
    )

    career_experience = str(
        career.get("experience_level", "") or ""
    )

    required_skills = [
        str(skill)
        for skill in career.get("skills", [])
        if str(skill).strip()
    ]

    score = 0
    reasons: list[str] = []

    # ---------------------------------------------------------------
    # 1. INTEREST MATCH — 35
    # ---------------------------------------------------------------

    career_text = [
        career_title,
        career_description,
        industry,
    ]

    if related_terms(interests, career_text):
        score += 35

        reasons.append(
            "Your interests overlap with this career area."
        )

    # ---------------------------------------------------------------
    # 2. SKILL MATCH — 35
    # ---------------------------------------------------------------

    matched_skills, missing_skills = match_skills(
        user_skills,
        required_skills,
    )

    if required_skills:
        skill_ratio = (
            len(matched_skills) / len(required_skills)
        )

        skill_score = round(skill_ratio * 35)

        score += skill_score

        if matched_skills:
            count = len(matched_skills)
            suffix = "" if count == 1 else "s"

            reasons.append(
                f"You already have {count} relevant skill{suffix}."
            )

    # ---------------------------------------------------------------
    # 3. EDUCATION MATCH — 10
    # ---------------------------------------------------------------

    education_concepts_set = education_concepts(
        field_of_study,
        degree,
    )

    career_concepts = expand_text(career_text)

    if education_concepts_set.intersection(
        career_concepts
    ):
        score += 10

        reasons.append(
            "Your education is related to this career area."
        )

    # ---------------------------------------------------------------
    # 4. EXPERIENCE MATCH — 10
    # ---------------------------------------------------------------

    user_experience = normalize_experience(
        experience_level
    )

    required_experience = normalize_experience(
        career_experience
    )

    experience_matches = (
        user_experience
        and required_experience
        and (
            user_experience == required_experience
            or user_experience == "entry"
            and required_experience in {"entry", "junior"}
            or user_experience == "junior"
            and required_experience in {"entry", "junior"}
        )
    )

    if experience_matches:
        score += 10

        reasons.append(
            "Your experience level aligns with this career."
        )

    # ---------------------------------------------------------------
    # 5. CAREER GOAL MATCH — 10
    # ---------------------------------------------------------------

    if career_goal and related_terms(
        [career_goal],
        career_text,
    ):
        score += 10

        reasons.append(
            "This career relates to your stated career goal."
        )

    score = max(0, min(score, 100))

    if not reasons:
        reasons.append(
            "This career is a potential path worth exploring."
        )

    return CareerRecommendation(
        title=career_title,
        industry=industry,
        description=career_description,
        match_score=score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        reasons=reasons,
    )


# -------------------------------------------------------------------
# RECOMMENDATION ENGINE
# -------------------------------------------------------------------

def recommend_careers(
    profile: dict[str, Any],
    careers: list[dict[str, Any]],
    top_n: int = 5,
) -> list[CareerRecommendation]:
    """Return the strongest career matches."""

    if top_n <= 0:
        return []

    recommendations = [
        score_career(
            profile=profile,
            career=career,
        )
        for career in careers
        if str(career.get("title", "")).strip()
    ]

    recommendations.sort(
        key=lambda recommendation: (
            recommendation.match_score,
            len(recommendation.matched_skills),
        ),
        reverse=True,
    )

    return recommendations[:top_n]


# -------------------------------------------------------------------
# API SERIALIZATION
# -------------------------------------------------------------------

def recommendation_to_dict(
    recommendation: CareerRecommendation,
) -> dict[str, Any]:
    """Convert recommendation object into JSON-ready data."""

    return {
        "title": recommendation.title,
        "industry": recommendation.industry,
        "description": recommendation.description,
        "match_score": recommendation.match_score,
        "matched_skills": recommendation.matched_skills,
        "missing_skills": recommendation.missing_skills,
        "reasons": recommendation.reasons,
    }