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

PREDICTIONS_PER_REQUEST = 5
METADATA_PATH = "data/metadata.json"

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



@app.get("/")
async def main():
    return {"message": "Welcome to the Job Role Recommendation API"}


@app.get("/available_skills", response_model=SkillsResponse)
async def get_available_skills():
    with open(METADATA_PATH, "r") as file:
        data = json.load(file)
        skills = set()
        for segment in data["Job Segments"].values():
            skills.update(segment["Skills"])

        # Convert to a sorted list
        distinct_skills = sorted(skills)

        return SkillsResponse(skills=distinct_skills)



@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendation(request: RecommendationRequest):
    prediction = predict_job_role(request.skills, PREDICTIONS_PER_REQUEST)
    recommendations = [
        RecommendationRole(
            role=role,
            matchPercent = int(probability * 100),
            skills = build_recomendation_skill_for_role(role, request.skills)
        )
        for role, probability in prediction
    ]
    return RecommendationResponse(recommendations=recommendations)


def build_recomendation_skill_for_role(role, user_skills):
    with open(METADATA_PATH, "r") as file:
        data = json.load(file)

    resommendation_skills = []

    for segment in data["Job Segments"].values():
        if role in segment.get("Roles", []):
            for skill_name in segment.get("Skills", []):
                status = skill_name in user_skills
                resommendation_skill = RecommendationSkill(skill=skill_name, status=status, skillGapPercent=None)
                resommendation_skills.append(resommendation_skill)
                
    return sorted(resommendation_skills, key=lambda skill: not skill.status)[:10]


