import pandas as pd

INPUT_FILE = "final_cleaned.csv"

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

# =========================
# USER INPUT
# =========================

student_rank = int(input("Enter rank: "))
student_category = input("Enter category: ").upper()
max_budget = float(input("Enter max budget: "))
preferred_course = input("Preferred course keyword: ").lower()

# =========================
# CLEAN
# =========================

df["rank"] = pd.to_numeric(df["rank"], errors="coerce")
df["fees"] = pd.to_numeric(df["fees"], errors="coerce")

# =========================
# FILTER
# =========================

filtered = df[
    (df["category"].str.upper() == student_category)
    &
    (df["fees"] <= max_budget)
    &
    (df["course"].str.lower().str.contains(preferred_course))
]

# =========================
# SAFETY LOGIC
# =========================

def classify(college_rank):

    if student_rank < college_rank * 0.7:
        return "DREAM"

    elif student_rank < college_rank:
        return "MODERATE"

    else:
        return "SAFE"

filtered["chance"] = filtered["rank"].apply(classify)

# =========================
# SORT
# =========================

filtered = filtered.sort_values("rank")

# =========================
# OUTPUT
# =========================

print("\n========================")
print("RECOMMENDED COLLEGES")
print("========================")

print(
    filtered[
        [
            "college",
            "course",
            "category",
            "fees",
            "rank",
            "chance",
            "round"
        ]
    ].head(50)
)

print(f"\nTotal recommendations: {len(filtered)}")

# =========================
# SAVE
# =========================

filtered.to_csv("recommendations.csv", index=False)

print("\nrecommendations.csv created")