from pydantic import BaseModel
from typing import List


class PredictRequest(BaseModel):
    skills: List[str]


class PredictResponse(BaseModel):
    prediction: str
