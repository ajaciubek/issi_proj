from pydantic_settings import BaseSettings
from pydantic import BaseModel


class Settings(BaseSettings):
    LABEL_MODEL_PATH: str
    JOB_PREDICT_MODEL_PATH: str
    SKILLS_MODEL_PATH: str
    SENTENCE_TRANSFORMER_MODEL: str
    GEMINI_KEY: str
    SPACY_MODEL: str


class LlmOutput(BaseModel):
    role: str
