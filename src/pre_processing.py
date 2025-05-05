from sentence_transformers import SentenceTransformer
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow as tf
import joblib

tf.config.set_visible_devices([], "GPU")

job_model = load_model("./data/job_model.keras")
label_encoder = joblib.load("./data/role_label_encoder.pkl")
encoder = SentenceTransformer("all-MiniLM-L6-v2")


input = encoder.encode("Java script")
input = np.expand_dims(input, axis=0)


predictions = job_model.predict(input)
predicted_class = predictions.argmax(axis=1)[0]

role = label_encoder.inverse_transform([predicted_class])[0]
print("Predicted Role:", role)
