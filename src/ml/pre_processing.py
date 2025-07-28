import json
import spacy
import polars as pl
from dotenv import load_dotenv
from models import Settings
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder
import joblib
from pathlib import Path
import os
from llm_wrapper import generate_llm_response

BATCH_SIZE = 200
NO_OF_SKILLS = 7


def load_data_from_json(data_type: str) -> List[str]:
    with open("./data/metadata.json", "r", encoding="utf-8") as file:
        metadata = json.load(file)

    data = set()
    for _, roles in metadata["Job Segments"].items():
        data.update(roles[data_type])

    return list(data)


load_dotenv(dotenv_path="./config/.ml-env")
settings = Settings()
nlp = spacy.load(settings.SPACY_MODEL)
model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)

tech_terms = load_data_from_json("Skills")
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "TECH_STACK", "pattern": [{"lower": term.lower()}]} for term in tech_terms
]
ruler.add_patterns(patterns)
roles = load_data_from_json("Roles")


def get_skills(text: str) -> Optional[str]:
    if not text:
        return None
    doc = nlp(text)
    skills = {ent.text.lower() for ent in doc.ents if ent.label_ == "TECH_STACK"}
    if len(skills) <= NO_OF_SKILLS:
        return None
    return ",".join(sorted(skills))


def get_label(
    position: str, description: str, skills: str, roles: List[str]
) -> Optional[str]:
    response = generate_llm_response(position, description, skills, roles)
    return response.role if response else None


def pre_process_df(df: pl.DataFrame, encoder: LabelEncoder) -> pl.DataFrame:
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
        .filter(pl.col("Label").is_in(roles))
        .collect()
    )

    if not df.is_empty():
        labels_encoded = encoder.transform(df["Label"].to_list())
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


offset = 0

label_encoder = LabelEncoder()
label_encoder.fit(roles)
joblib.dump(label_encoder, Path(settings.LABEL_MODEL_PATH))

df = pl.scan_parquet("./data/raw_data.parquet")
length = df.select(pl.len()).collect().item()
file_name = None
file_name_prev = None
combined_df = pl.DataFrame()

while offset < length:
    batch = df.slice(offset, BATCH_SIZE)

    batch = pre_process_df(batch, label_encoder)
    offset += BATCH_SIZE

    if not batch.is_empty():
        combined_df = pl.concat([combined_df, batch])
        file_name = f"./data/pre_processed_data_{offset}"

        if file_name_prev:
            os.rename(f"{file_name_prev}.parquet", f"{file_name}.parquet")

        combined_df.write_parquet(f"{file_name}.parquet", compression="zstd")
        file_name_prev = file_name

    print(f"Processed {offset} / {length}")

os.rename(f"{file_name}.parquet", "./data/pre_processed_data.parquet")
