from pydantic import BaseModel, Field

class CareerAnalysisRequest(BaseModel):
    education_level: str = Field(min_length=1, max_length=100)
    degree: str = Field(default="", max_length=150)
    field_of_study: str = Field(default="", max_length=150)
    graduation_year: int | None = None
    experience_level: str = Field(default="", max_length=100)
    career_goal: str = Field(default="", max_length=500)
    interests: list[str] = Field(default_factory=list, max_length=30)
    skills: list[str] = Field(default_factory=list, max_length=50)
    projects: list[str] = Field(default_factory=list, max_length=30)
    certifications: list[str] = Field(default_factory=list, max_length=30)
