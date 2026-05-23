from pathlib import Path
import pandas as pd
import re

INPUT_FILE = Path("master_cleaned.csv")
OUTPUT_FILE = Path("final_cleaned.csv")

print("Loading master dataset...")

df = pd.read_csv(INPUT_FILE)

print("Original rows:", len(df))

# ======================================
# CLEAN COLUMN NAMES
# ======================================

df.columns = [
    str(col).strip().lower()
    for col in df.columns
]

# ======================================
# CLEAN TEXT FIELDS
# ======================================

text_columns = [
    "college",
    "course",
    "category"
]

for col in text_columns:

    if col in df.columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"\n", " ", regex=True)
            .str.replace(r"\r", " ", regex=True)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

# ======================================
# CLEAN CATEGORY
# ======================================

def clean_category(x):

    if pd.isna(x):
        return None

    x = str(x).upper().strip()

    valid_categories = [
        "GM",
        "GMP",
        "1G",
        "2AG",
        "2BG",
        "3AG",
        "3BG",
        "SCG",
        "STG",
        "GMK",
        "SCK",
        "STK",
        "OPN",
        "MNG",
        "NRI"
    ]

    for cat in valid_categories:
        if cat in x:
            return cat

    return None

df["category"] = df["category"].apply(clean_category)

# ======================================
# CLEAN RANK
# ======================================

def clean_rank(x):

    if pd.isna(x):
        return None

    x = str(x)

    numbers = re.findall(r"\d+", x)

    if len(numbers) == 0:
        return None

    return int(numbers[0])

df["rank"] = df["rank"].apply(clean_rank)

# ======================================
# CLEAN FEES
# ======================================

def clean_fees(x):

    if pd.isna(x):
        return None

    x = str(x)

    numbers = re.findall(r"\d+", x)

    if len(numbers) == 0:
        return None

    return int("".join(numbers))

df["fees"] = df["fees"].apply(clean_fees)

# ======================================
# REMOVE BAD ROWS
# ======================================

df = df.dropna(subset=["rank"])

df = df[
    df["rank"] > 0
]

df = df[
    df["college"].str.len() > 5
]

df = df[
    df["course"].str.len() > 3
]

# ======================================
# REMOVE DUPLICATES
# ======================================

df = df.drop_duplicates()

# ======================================
# SORT
# ======================================

df = df.sort_values(
    by=["rank"],
    ascending=True
)

# ======================================
# FINAL OUTPUT
# ======================================

print("\nFINAL DATASET")
print(df.head())

print("\nFinal rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())

# SAVE
df.to_csv(OUTPUT_FILE, index=False)

print("\nfinal_cleaned.csv created")