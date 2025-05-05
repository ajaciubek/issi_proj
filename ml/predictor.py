from sentence_transformers import SentenceTransformer
from tensorflow.keras.models import load_model
import numpy as np
import joblib
from dotenv import load_dotenv
from ml.settings import Settings
from typing import List

load_dotenv(dotenv_path="./config/.ml-env")
settings = Settings()

job_model = load_model(settings.JOB_PREDICT_MODEL_PATH)
label_encoder = joblib.load(settings.LABEL_MODEL_PATH)
encoder = SentenceTransformer("all-MiniLM-L6-v2")


def predict_job_role(skills: List[str]) -> str:
    input = encoder.encode(" ".join(skills))
    input = np.expand_dims(input, axis=0)

    predictions = job_model.predict(input)
    predicted_class = predictions.argmax(axis=1)[0]

    role = label_encoder.inverse_transform([predicted_class])[0]

    return role
