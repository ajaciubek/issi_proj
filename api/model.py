from pydantic import BaseModel
from typing import List, Tuple


class PredictRequest(BaseModel):
    skills: List[str]


class PredictResponse(BaseModel):
    prediction: List[Tuple[str, float]]
