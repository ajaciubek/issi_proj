import polars as pl

df = pl.read_parquet("data/raw_data.parquet")
print(df.describe())
