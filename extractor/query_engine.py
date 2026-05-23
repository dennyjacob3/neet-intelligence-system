import pandas as pd

INPUT_FILE = "final_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded.")
print("Rows:", len(df))

# ======================================
# USER INPUTS
# ======================================

rank_input = int(input("\nEnter student rank: "))

category_input = input(
    "Enter category (GM/SCG/STG/etc): "
).upper()

# ======================================
# FILTER
# ======================================

filtered = df[
    (df["rank"] >= rank_input - 5000) &
    (df["rank"] <= rank_input + 5000)
]

if category_input != "ALL":

    filtered = filtered[
        filtered["category"] == category_input
    ]

# ======================================
# SORT
# ======================================

filtered = filtered.sort_values(
    by="rank"
)

# ======================================
# RESULTS
# ======================================

print("\n======================")
print("POSSIBLE COLLEGES")
print("======================")

if len(filtered) == 0:

    print("No matching colleges found.")

else:

    print(
        filtered[
            [
                "rank",
                "college",
                "course",
                "category",
                "fees",
                "round"
            ]
        ]
        .head(50)
    )

print("\nTotal matches:", len(filtered))