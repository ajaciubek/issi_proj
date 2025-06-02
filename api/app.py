from fastapi import FastAPI
from api.model import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationSkill,
    RecommendationRole,
    SkillsResponse,
)
from fastapi.middleware.cors import CORSMiddleware


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

FAKE_SKILLS = [
    "python",
    "api",
    "pandas",
    "pyTorch",
    "postgreSQL",
    "polars",
    "TensorFlow",
    "PyGame",
]


# @app.get("/")
# def root():
#     return "Welcome to the Job Role Prediction API!"


# @app.post("/predict", response_model=PredictResponse)
# def predict(request: PredictRequest):
#     return PredictResponse(prediction=predict_job_role(request.skills, request.limit))


@app.get("/available_skills", response_model=SkillsResponse)
async def get_available_skills():
    return SkillsResponse(skills=FAKE_SKILLS)


@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendation(data: RecommendationRequest):
    # Tu można podpiąć prawdziwy model ML lub logikę
    return RecommendationResponse(recommendations=FAKE_RECOMMENDATIONS)
