from sentence_transformers import SentenceTransformer
from tensorflow.keras.models import load_model
import numpy as np
import joblib
from dotenv import load_dotenv
from settings import Settings

load_dotenv(dotenv_path="./config/.env.prod")
settings = Settings()

job_model = load_model(settings.JOB_PREDICT_MODEL_PATH)
label_encoder = joblib.load(settings.LABEL_MODEL_PATH)
encoder = SentenceTransformer("all-MiniLM-L6-v2")


def predict_job_role(job_description: str) -> str:
    input = encoder.encode(job_description)
    input = np.expand_dims(input, axis=0)

    predictions = job_model.predict(input)
    predicted_class = predictions.argmax(axis=1)[0]

    role = label_encoder.inverse_transform([predicted_class])[0]

    return role


print(predict_job_role("Java script"))
print(predict_job_role("SQL"))
