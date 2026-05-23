import pandas as pd

INPUT_FILE = "final_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded.")
print("Rows:", len(df))

# ======================================
# USER INPUT
# ======================================

student_rank = int(input("\nEnter student rank: "))

student_category = input(
    "Enter category: "
).upper()

# ======================================
# FILTER CATEGORY
# ======================================

filtered = df.copy()

if student_category != "ALL":

    filtered = filtered[
        filtered["category"] == student_category
    ]

# ======================================
# CALCULATE PROBABILITY
# ======================================

results = []

for _, row in filtered.iterrows():

    cutoff = row["rank"]

    difference = student_rank - cutoff

    if difference <= -10000:
        probability = "HIGHLY SAFE"

    elif difference <= -3000:
        probability = "SAFE"

    elif difference <= 3000:
        probability = "MODERATE"

    elif difference <= 10000:
        probability = "RISKY"

    else:
        probability = "VERY RISKY"

    results.append({

        "college": row["college"],
        "course": row["course"],
        "category": row["category"],
        "cutoff_rank": cutoff,
        "student_rank": student_rank,
        "fees": row["fees"],
        "round": row["round"],
        "probability": probability

    })

# ======================================
# FINAL RESULTS
# ======================================

results_df = pd.DataFrame(results)

priority_order = {
    "HIGHLY SAFE": 1,
    "SAFE": 2,
    "MODERATE": 3,
    "RISKY": 4,
    "VERY RISKY": 5
}

results_df["priority"] = results_df[
    "probability"
].map(priority_order)

results_df = results_df.sort_values(
    by=["priority", "cutoff_rank"]
)

print("\n======================")
print("COLLEGE PREDICTIONS")
print("======================")

print(
    results_df[
        [
            "college",
            "course",
            "category",
            "cutoff_rank",
            "student_rank",
            "probability",
            "fees",
            "round"
        ]
    ]
    .head(50)
)

print("\nTotal predictions:", len(results_df))

# SAVE
results_df.to_csv(
    "predictions.csv",
    index=False
)

print("\npredictions.csv created")