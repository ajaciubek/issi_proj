from fastapi import FastAPI
from .predictor import predict_job_role
from .rest_model import PredictRequest, PredictResponse

app = FastAPI()


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    prediction = predict_job_role(request.skills)
    return PredictResponse(prediction=prediction)
