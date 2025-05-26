import json
import spacy
import polars as pl
from google import genai
from dotenv import load_dotenv
from settings import Settings
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder
import joblib

load_dotenv(dotenv_path="./config/.ml-env")
settings = Settings()
nlp = spacy.load("en_core_web_sm")
gemini_client = genai.Client(api_key=settings.GEMINI_KEY)


def load_data_from_json(data_type: str) -> List[str]:
    with open("./data/metadata.json", "r", encoding="utf-8") as file:
        metadata = json.load(file)

    data = set()
    for _, roles in metadata["Job Segments"].items():
        data.update(roles[data_type])

    return list(data)


def get_skills(text: str) -> Optional[str]:
    if not text:
        return []
    doc = nlp(text)
    skills = {ent.text.lower() for ent in doc.ents if ent.label_ == "TECH_STACK"}
    if len(skills) <= 3:
        return None
    return ",".join(sorted(skills))


def generate_prompt(position: str, description: str, skills: str, roles: str) -> str:
    return (
        f"You are a job role generator.\n"
        f"Given the position name, description, and skills, classify it into one of the predefined roles.\n"
        f"Choose exactly one role from the Roles list that best fits the job.\n"
        f"Respond with only the name of the selected role — no explanation, no punctuation.\n"
        f"Position: {position}\n"
        f"Description: {description}\n"
        f"Skills: {skills}\n"
        f"Roles: {roles}"
    )


def generate_response(prompt: str) -> Optional[str]:
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            # generation_config={
            #     "temperature": 0.5,
            #     "max_output_tokens": 10,
            # },
        )
        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] Gemini generation failed: {e}")
        return None


def get_label(
    position: str, description: str, skills: str, roles: str
) -> Optional[str]:
    return generate_response(generate_prompt(position, description, skills, roles))


def pre_process_df(df: pl.DataFrame, encoder: LabelEncoder) -> pl.DataFrame:
    tech_terms = load_data_from_json("Skills")
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [
        {"label": "TECH_STACK", "pattern": [{"lower": term.lower()}]}
        for term in tech_terms
    ]
    ruler.add_patterns(patterns)
    roles_list = load_data_from_json("Roles")
    roles = str(roles_list)

    df = (
        df.with_columns(
            pl.col("Long Description")
            .str.replace_all(r"\r\n|\r|\n", " ")
            .str.strip_chars()
            .alias("Description")
        )
        .with_columns(
            pl.col("Description")
            .map_elements(get_skills, return_dtype=pl.Utf8)
            .alias("Skills")
        )
        .filter(pl.col("Skills").is_not_null())
        .select(["Position", "Description", "Skills"])
        .with_columns(pl.lit(None).cast(pl.Utf8).alias("Label"))
        .with_columns(
            pl.struct(["Position", "Description", "Skills"])
            .map_elements(
                lambda row: get_label(
                    row["Position"], row["Description"], row["Skills"], roles
                ),
                return_dtype=pl.Utf8,
            )
            .alias("Label")
        )
        .drop(["Position", "Description"])
        .filter(pl.col("Label").is_in(roles_list))
        .collect()
    )
    labels_encoded = encoder.transform(df["Label"].to_list())
    model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)
    embeddings = model.encode(df["Skills"].to_list(), show_progress_bar=True)

    embedding_df = pl.DataFrame(
        embeddings, schema=[f"emb_{i}" for i in range(len(embeddings[0]))]
    )

    df = (
        df.drop(["Skills", "Label"])
        .with_columns([pl.Series("Role_encoded", labels_encoded)])
        .hstack(embedding_df)
    )

    return df


label_encoder = joblib.load(settings.LABEL_MODEL_PATH)
df = pl.scan_parquet("./data/raw_data.parquet").head(10)
df = pre_process_df(df, label_encoder)
# df.write_csv("./data/pre_processed_data.parquet", compression="zstd")
