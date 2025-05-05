from fastapi import FastAPI
from ml.predictor import predict_job_role
from api.model import PredictRequest, PredictResponse

app = FastAPI()


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    return PredictResponse(prediction=predict_job_role(request.skills))
