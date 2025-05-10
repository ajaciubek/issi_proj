import polars as pl

df = pl.scan_parquet("data/raw_data.parquet")

df = df.drop(
    [
        "Company Name",
        "Exp Years",
        "English Level",
        "Published",
        "id",
        "Long Description_lang",
        "__index_level_0__",
    ]
)

json = pl.read_json("data/programming_skills.json")
print(json["Skills"])
