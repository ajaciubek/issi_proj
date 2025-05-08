from pydantic import BaseModel, Field
from typing import List, Tuple


class PredictRequest(BaseModel):
    skills: List[str] = Field(..., min_items=1)
    limit: int = Field(..., gt=0)


class PredictResponse(BaseModel):
    prediction: List[Tuple[str, float]]
