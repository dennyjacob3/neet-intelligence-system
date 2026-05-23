import pandas as pd
from pathlib import Path

INPUT_FOLDER = Path("extractor/output")

all_dataframes = []

for csv_file in INPUT_FOLDER.glob("*.csv"):

    print(f"Loading: {csv_file.name}")

    try:

        df = pd.read_csv(csv_file)

        # Add source tracking
        df["source_file"] = csv_file.name

        # Remove completely empty rows
        df = df.dropna(how="all")

        # Convert columns to string
        df.columns = [str(col).strip() for col in df.columns]

        all_dataframes.append(df)

    except Exception as e:

        print(f"Failed: {csv_file.name}")
        print(e)

# =========================
# MERGE EVERYTHING
# =========================

master_df = pd.concat(all_dataframes, ignore_index=True)

print("\nMASTER DATAFRAME")
print(master_df.head())

print("\nTotal rows:", len(master_df))

# =========================
# SAVE MASTER FILE
# =========================

master_df.to_csv("extractor/master_output.csv", index=False)

print("\nmaster_output.csv created")