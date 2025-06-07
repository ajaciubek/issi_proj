from sklearn.preprocessing import LabelEncoder
import joblib
from pathlib import Path
import json
from typing import List
from settings import Settings
from dotenv import load_dotenv

load_dotenv(dotenv_path="./config/.ml-env")
settings = Settings()


def load_data_from_json(data_type: str) -> List[str]:
    with open("./data/metadata.json", "r", encoding="utf-8") as file:
        metadata = json.load(file)

    data = set()
    for _, roles in metadata["Job Segments"].items():
        data.update(roles[data_type])

    return list(data)


encoder = LabelEncoder()
encoder.fit(load_data_from_json("Roles"))
joblib.dump(encoder, Path(settings.LABEL_MODEL_PATH))
