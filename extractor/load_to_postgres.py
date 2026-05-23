from sqlalchemy import create_engine
import pandas as pd

# =========================
# DATABASE CONNECTION
# =========================

DATABASE_URL = "postgresql+psycopg2://user@localhost/neet_db"

engine = create_engine(DATABASE_URL)

# =========================
# LOAD CSV
# =========================

print("Loading CSV...")

df = pd.read_csv("final_cleaned.csv")

print(df.head())

print(f"\nRows found: {len(df)}")

# =========================
# PUSH TO POSTGRES
# =========================

print("\nUploading to PostgreSQL...")

df.to_sql(
    "pgneet_2025",
    engine,
    if_exists="replace",
    index=False
)

print("\nSUCCESS")
print("Table created: pgneet_2025")