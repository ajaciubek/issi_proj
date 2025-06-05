from pydantic import BaseModel, Field
from typing import List, Optional


class RecommendationRequest(BaseModel):
    skills: List[str] = Field(..., min_items=1)


class RecommendationSkill(BaseModel):
    skill: str
    status: bool
    skillGapPercent: Optional[int]


class RecommendationRole(BaseModel):
    role: str
    matchPercent: float
    skills: List[RecommendationSkill]


class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationRole]


class SkillsResponse(BaseModel):
    skills: List[str]
