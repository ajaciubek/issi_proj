from sentence_transformers import SentenceTransformer
from tensorflow.keras.models import load_model
import numpy as np
import joblib
from dotenv import load_dotenv
from .models import Settings
from typing import List, Tuple
from tensorflow import keras

load_dotenv(dotenv_path="./config/.ml-env")
settings = Settings()

job_model = load_model(settings.JOB_PREDICT_MODEL_PATH)
label_encoder = joblib.load(settings.LABEL_MODEL_PATH)
encoder = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)
skills_model = load_model(settings.SKILLS_PREDICT_MODEL_PATH)
skills_encoder = joblib.load(settings.SKILLS_MODEL_PATH)


def predict_job_role(skills: List[str], limit: int) -> List[Tuple[str, float]]:
    input_vector = encoder.encode(" ".join(skills))
    input_batch = input_vector[np.newaxis, :]

    predictions = job_model.predict(input_batch, verbose=0)
    pred_scores = predictions[0]

    top_indices = np.argpartition(pred_scores, -limit)[-limit:]
    top_indices = top_indices[np.argsort(pred_scores[top_indices])[::-1]]
    probabilities = pred_scores[top_indices]
    roles = label_encoder.inverse_transform(top_indices)

    return list(zip(roles, probabilities))


def predict_skills_for_role(role: str, number_of_skills: int) -> List[str]:
    role_encoded = label_encoder.transform([role])
    categorical = keras.utils.to_categorical(
        role_encoded, num_classes=len(label_encoder.classes_)
    )
    predictions = skills_model.predict(categorical, verbose=0)
    top_indices = np.argpartition(predictions[0], -number_of_skills)[-number_of_skills:]
    top_indices = top_indices[np.argsort(predictions[0][top_indices])[::-1]]

    return skills_encoder.inverse_transform(top_indices)
