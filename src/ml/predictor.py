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
encoder = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)


def predict_job_role(skills: List[str], limit: int) -> List[str]:
    input = encoder.encode(" ".join(skills))
    input = np.expand_dims(input, axis=0)

    predictions = job_model.predict(input)
    indices = predictions[0].argsort()[-limit:][::-1]
    propabilities = predictions[0][indices]
    roles = label_encoder.inverse_transform(indices)

    return list(zip(roles, propabilities))
