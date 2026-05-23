from pathlib import Path
import pandas as pd

OUTPUT_FOLDER = Path("output")
MASTER_OUTPUT = Path("master_cleaned.csv")

all_dataframes = []

# =========================
# LOOP THROUGH CSV FILES
# =========================

for csv_file in OUTPUT_FOLDER.glob("*.csv"):

    print(f"\nLoading: {csv_file.name}")

    try:

        # READ CSV
        df = pd.read_csv(csv_file, on_bad_lines="skip")

        print("Original shape:", df.shape)

        # CLEAN COLUMN NAMES
        df.columns = [
            str(col)
            .replace("\n", " ")
            .replace("\r", " ")
            .strip()
            for col in df.columns
        ]

        print("Detected columns:")
        print(df.columns.tolist())

        # =========================
        # CREATE CLEAN DATAFRAME
        # =========================

        cleaned_df = pd.DataFrame()

        # SOURCE FILE
        cleaned_df["source_file"] = [csv_file.name] * len(df)

        # YEAR
        cleaned_df["year"] = 2025

        # ROUND
        filename = csv_file.name.lower()

        if "r2" in filename:
            cleaned_df["round"] = "R2"
        elif "stray" in filename:
            cleaned_df["round"] = "STRAY"
        else:
            cleaned_df["round"] = "R1"

        # =========================
        # AUTO COLUMN DETECTION
        # =========================

        rank_col = None
        course_col = None
        category_col = None
        college_col = None
        fees_col = None

        for col in df.columns:

            lower = col.lower()

            if "rank" in lower:
                rank_col = col

            elif "course name" in lower:
                course_col = col

            elif "category" in lower:
                category_col = col

            elif "college" in lower:
                college_col = col

            elif "fees" in lower:
                fees_col = col

        # FALLBACKS
        columns_list = list(df.columns)

        if rank_col is None and len(columns_list) > 1:
            rank_col = columns_list[1]

        if course_col is None and len(columns_list) > 4:
            course_col = columns_list[4]

        if category_col is None and len(columns_list) > 5:
            category_col = columns_list[5]

        if college_col is None and len(columns_list) > 3:
            college_col = columns_list[3]

        if fees_col is None and len(columns_list) > 6:
            fees_col = columns_list[6]

        # =========================
        # EXTRACT VALUES
        # =========================

        cleaned_df["rank"] = (
            df[rank_col].astype(str)
            if rank_col in df.columns
            else ""
        )

        cleaned_df["course"] = (
            df[course_col].astype(str)
            if course_col in df.columns
            else ""
        )

        cleaned_df["category"] = (
            df[category_col].astype(str)
            if category_col in df.columns
            else ""
        )

        cleaned_df["college"] = (
            df[college_col].astype(str)
            if college_col in df.columns
            else ""
        )

        cleaned_df["fees"] = (
            df[fees_col].astype(str)
            if fees_col in df.columns
            else ""
        )

        # =========================
        # BASIC CLEANING
        # =========================

        cleaned_df = cleaned_df.dropna(how="all")

        cleaned_df = cleaned_df[
            cleaned_df["rank"].str.contains(r"\d", na=False)
        ]

        print("Rows cleaned:", len(cleaned_df))

        print(cleaned_df.head())

        # APPEND
        if len(cleaned_df) > 0:
            all_dataframes.append(cleaned_df)

    except Exception as e:

        print(f"FAILED: {csv_file.name}")
        print(e)

# =========================
# MERGE EVERYTHING
# =========================

if len(all_dataframes) == 0:

    print("\nNO DATAFRAMES CREATED")
    print("Cleaning logic failed.")
    exit()

master_df = pd.concat(all_dataframes, ignore_index=True)

# =========================
# SAVE
# =========================

print("\n========================")
print("MASTER DATAFRAME")
print("========================")

print(master_df.head())

print("\nTotal rows:", len(master_df))

master_df.to_csv(MASTER_OUTPUT, index=False)

print("\nmaster_cleaned.csv created")