import json
from fastapi import FastAPI
from api.model import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationSkill,
    RecommendationRole,
    SkillsResponse,
)
from fastapi.middleware.cors import CORSMiddleware
from ml.predictor import predict_job_role

PREDICTIONS_PER_REQUEST = 3

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FAKE_RECOMMENDATIONS = [
    RecommendationRole(
        role="Machine Learning Engineer",
        matchPercent=98,
        skills=[
            RecommendationSkill(skill="Python", status=True, skillGapPercent=None),
            RecommendationSkill(skill="Pandas", status=True, skillGapPercent=None),
            RecommendationSkill(skill="PyTorch", status=True, skillGapPercent=None),
            RecommendationSkill(skill="TensorFlow", status=True, skillGapPercent=None),
            RecommendationSkill(skill="Polars", status=False, skillGapPercent=40),
        ],
    ),
    RecommendationRole(
        role="Python Developer",
        matchPercent=69,
        skills=[
            RecommendationSkill(skill="Python", status=True, skillGapPercent=None),
            RecommendationSkill(skill="Pandas", status=True, skillGapPercent=None),
            RecommendationSkill(skill="Flask", status=True, skillGapPercent=None),
            RecommendationSkill(skill="FastAPI", status=False, skillGapPercent=90),
            RecommendationSkill(skill="SQL ALchemy", status=False, skillGapPercent=11),
        ],
    ),
]


@app.get("/")
async def main():
    return {"message": "Welcome to the Job Role Recommendation API"}


@app.get("/available_skills", response_model=SkillsResponse)
async def get_available_skills():
    with open("data/programming_skills.json", "r") as file:
        data = json.load(file)
        return SkillsResponse(skills=data["Skills"])


@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendation(request: RecommendationRequest):
    prediction = predict_job_role(request.skills, PREDICTIONS_PER_REQUEST)
    recommendations = [
        RecommendationRole(
            role=role,
            matchPercent=int(probability),
            skills=[RecommendationSkill(skill="", status=True, skillGapPercent=None)],
        )
        for role, probability in prediction
    ]
    return RecommendationResponse(recommendations=recommendations)
