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
import numpy as np

BATCH_SIZE = 50
NO_OF_SKILLS = 7
SETTINGS = None
MODEL = None
NLP = None


def load_data_from_json(data_type: str) -> List[str]:
    with open("./data/metadata.json", "r", encoding="utf-8") as file:
        metadata = json.load(file)

    data = set()
    for _, roles in metadata["Job Segments"].items():
        data.update(roles[data_type])

    return list(data)


def get_skills(text: str) -> Optional[str]:
    global NLP

    if not text:
        return None
    doc = NLP(text)
    skills = {ent.text.lower() for ent in doc.ents if ent.label_ == "TECH_STACK"}
    if len(skills) <= NO_OF_SKILLS:
        return None
    return ",".join(sorted(skills))


def get_label(
    position: str, description: str, skills: str, roles: List[str]
) -> Optional[str]:
    response = generate_llm_response(position, description, skills, roles)
    return response.role if response else None


def pre_process_common(
    df: pl.DataFrame, roles: List[str], role_encoder: LabelEncoder
) -> pl.DataFrame:
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
        labels_encoded = role_encoder.transform(df["Label"].to_list())
        df = df.with_columns([pl.Series("Role_encoded", labels_encoded)])

    return df


def pre_process_roles(df_original: pl.DataFrame) -> pl.DataFrame:
    global MODEL

    df = df_original.clone()
    if not df.is_empty():
        embeddings = MODEL.encode(df["Skills"].to_list(), show_progress_bar=True)
        print(f"{embeddings.shape=}")
        embedding_df = pl.DataFrame(
            embeddings, schema=[f"emb_{i}" for i in range(len(embeddings[0]))]
        )

        df = df.drop(["Skills", "Label"]).hstack(embedding_df)

    return df


def pre_process_skill(
    df_original: pl.DataFrame, skills_encoder: LabelEncoder
) -> pl.DataFrame:
    df = df_original.clone()
    no_of_skills = len(skills_encoder.classes_)
    if not df.is_empty():
        all_skills_vec = np.empty((0, no_of_skills))
        for skill in df["Skills"].to_list():
            skills_vec = np.zeros(no_of_skills).reshape(1, -1)
            encoded = skills_encoder.transform(skill.split(","))
            for i in encoded:
                skills_vec[0][i] = 1
            all_skills_vec = np.append(all_skills_vec, skills_vec, axis=0)
        skills_df = pl.DataFrame(
            all_skills_vec, schema=[f"skill_{i}" for i in range(len(all_skills_vec[0]))]
        )
        df = df.drop(["Label", "Skills"]).hstack(skills_df)
    return df


def combine_df(
    batch: pl.DataFrame,
    combined_df: pl.DataFrame,
    offset: int,
    file_name_prev: str,
    file_name: str,
    label: str,
):
    if not batch.is_empty():
        combined_df = pl.concat([combined_df, batch])
        file_name = f"./data/pre_processed_{label}_data_{offset}"

        if file_name_prev:
            os.rename(f"{file_name_prev}.parquet", f"{file_name}.parquet")

        combined_df.write_parquet(f"{file_name}.parquet", compression="zstd")
        file_name_prev = file_name
    return (combined_df, file_name, file_name_prev)


def main():
    global SETTINGS, MODEL, NLP

    load_dotenv(dotenv_path="./config/.ml-env")
    SETTINGS = Settings()
    MODEL = SentenceTransformer(SETTINGS.SENTENCE_TRANSFORMER_MODEL)

    roles = load_data_from_json("Roles")

    NLP = spacy.load(SETTINGS.SPACY_MODEL)
    skills = [skill.lower() for skill in load_data_from_json("Skills")]
    ruler = NLP.add_pipe("entity_ruler", before="ner")
    patterns = [
        {"label": "TECH_STACK", "pattern": [{"lower": skill}]} for skill in skills
    ]
    ruler.add_patterns(patterns)

    offset = 0

    skills_encoder = LabelEncoder()
    skills_encoder.fit(skills)
    joblib.dump(skills_encoder, Path("./data/skill_label_encoder.pkl"))

    label_encoder = LabelEncoder()
    label_encoder.fit(roles)
    joblib.dump(label_encoder, Path(SETTINGS.LABEL_MODEL_PATH))

    df = pl.scan_parquet("./data/raw_data.parquet")
    # length = df.select(pl.len()).collect().item()
    length = 50

    role_file_name = None
    role_file_name_prev = None
    combined_role_df = pl.DataFrame()

    skills_file_name = None
    skills_file_name_prev = None
    combined_skills_df = pl.DataFrame()

    while offset < length:
        batch = df.slice(offset, BATCH_SIZE)
        batch = pre_process_common(batch, roles, label_encoder)
        batch_role = pre_process_roles(batch)
        batch_skills = pre_process_skill(batch, skills_encoder)

        combined_role_df, role_file_name, role_file_name_prev = combine_df(
            batch_role,
            combined_role_df,
            offset,
            role_file_name_prev,
            role_file_name,
            "role",
        )
        combined_skills_df, skills_file_name, skills_file_name_prev = combine_df(
            batch_skills,
            combined_skills_df,
            offset,
            skills_file_name_prev,
            skills_file_name,
            "skills",
        )

        offset += BATCH_SIZE

        print(f"Processed {offset} / {length}")

    os.rename(f"{role_file_name}.parquet", "./data/pre_processed_data.parquet")
    os.rename(f"{skills_file_name}.parquet", "./data/pre_processed_skills_data.parquet")


if __name__ == "__main__":
    main()
