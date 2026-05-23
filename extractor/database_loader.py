import pandas as pd
from sqlalchemy import create_engine

# ======================================
# DATABASE CONFIG
# ======================================

DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "neet_db"

# ======================================
# LOAD CSV
# ======================================

df = pd.read_csv("final_cleaned.csv")

print("Rows loaded:", len(df))

# ======================================
# CONNECT POSTGRES
# ======================================

engine = create_engine(

    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

)

# ======================================
# SAVE TO DATABASE
# ======================================

df.to_sql(

    "pgneet_cutoffs",

    engine,

    if_exists="replace",

    index=False

)

print("\nDATABASE LOAD COMPLETED")