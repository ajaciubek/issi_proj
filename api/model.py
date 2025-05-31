from pydantic import BaseModel, Field
from typing import List, Tuple, Optional


# class PredictRequest(BaseModel):
#     skills: List[str] = Field(..., min_items=4)
#     limit: int = Field(..., gt=0)


# class PredictResponse(BaseModel):
#     prediction: List[Tuple[str, float]]

class RecommendationRequest(BaseModel):
    skills: List[str] = Field(..., min_items=4)
    category: str = None

class RecommendationSkill(BaseModel):
    skill: str
    status: bool
    skillGapPercent: Optional[int]

class RecommendationRole(BaseModel):
    role: str
    matchPercent: int
    skills: List[RecommendationSkill]

class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationRole]

class SkillsResponse(BaseModel):
    skills: List[str]

class CategoryRequest(BaseModel):
    skills: List[str] = Field(..., min_items=4)

class CategoryResponse(BaseModel):
    categories: List[str]