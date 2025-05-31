from fastapi import FastAPI
from ml.predictor import predict_job_role
from api.model import CategoryRequest, CategoryResponse, RecommendationRequest, RecommendationResponse,RecommendationSkill,  RecommendationRole, SkillsResponse


app = FastAPI()

FAKE_RECOMMENDATIONS = [
    RecommendationRole(
        role="Machine Learning Engineer",
        matchPercent=98,
        skills=[
            RecommendationSkill(skill="Python", status=True, skillGapPercent=None),
            RecommendationSkill(skill="Pandas", status=True, skillGapPercent=None),
            RecommendationSkill(skill="PyTorch", status=True, skillGapPercent=None),
            RecommendationSkill(skill="TensorFlow", status=True, skillGapPercent=None),
            RecommendationSkill(skill="Polars", status=False, skillGapPercent=40)
        ]
    ),
    RecommendationRole(
        role="Python Developer",
        matchPercent=69,
        skills=[
            RecommendationSkill(skill="Python", status=True, skillGapPercent=None),
            RecommendationSkill(skill="Pandas", status=True, skillGapPercent=None),
            RecommendationSkill(skill="Flask", status=True, skillGapPercent=None),
            RecommendationSkill(skill="FastAPI", status=False, skillGapPercent=90),
            RecommendationSkill(skill="SQL ALchemy", status=False, skillGapPercent=11)
        ]
    )
]

FAKE_SKILLS = [
    "python",
    "api",
    "pandas",
    "pyTorch",
    "postgreSQL",
    "polars",
    "TensorFlow",
    "PyGame"
]

FAKE_CATEGORIES = [
    "Backend",
    "Data Science",
    "Databases"
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

@app.post("/suggest_category", response_model=CategoryResponse)
async def suggest_category(data: CategoryRequest):
    # Mock logic: return top 3 matching categories
    return CategoryResponse(categories=FAKE_CATEGORIES[:3])