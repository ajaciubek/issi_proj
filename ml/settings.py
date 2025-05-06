from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LABEL_MODEL_PATH: str
    JOB_PREDICT_MODEL_PATH: str
    SENTENCE_TRANSFORMER_MODEL: str
