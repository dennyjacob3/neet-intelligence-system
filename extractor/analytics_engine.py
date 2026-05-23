import pandas as pd

INPUT_FILE = "final_cleaned.csv"

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print("\nTotal rows:", len(df))

# ======================================
# BASIC ANALYTICS
# ======================================

print("\n======================")
print("TOP COLLEGES BY COUNT")
print("======================")

print(
    df["college"]
    .value_counts()
    .head(10)
)

print("\n======================")
print("TOP COURSES")
print("======================")

print(
    df["course"]
    .value_counts()
    .head(10)
)

print("\n======================")
print("CATEGORY DISTRIBUTION")
print("======================")

print(
    df["category"]
    .value_counts()
)

print("\n======================")
print("LOWEST RANKS")
print("======================")

print(
    df.sort_values("rank")
    [
        [
            "rank",
            "college",
            "course",
            "category",
            "fees"
        ]
    ]
    .head(20)
)

print("\n======================")
print("HIGHEST RANKS")
print("======================")

print(
    df.sort_values("rank", ascending=False)
    [
        [
            "rank",
            "college",
            "course",
            "category",
            "fees"
        ]
    ]
    .head(20)
)

# ======================================
# SAVE ANALYTICS
# ======================================

college_summary = (
    df.groupby("college")
    .agg({
        "rank": ["min", "max", "mean"],
        "fees": ["mean"]
    })
)

college_summary.to_csv("college_summary.csv")

print("\ncollege_summary.csv created")
print("\n======================")
print("SAFETY ANALYSIS")
print("======================")

def classify_rank(rank):
    if rank >= 200000:
        return "HIGHLY SAFE"
    elif rank >= 100000:
        return "SAFE"
    elif rank >= 50000:
        return "MODERATE"
    else:
        return "RISKY"

df["safety"] = df["rank"].apply(classify_rank)

print(df["safety"].value_counts())
print("\n======================")
print("CHEAPEST COLLEGES")
print("======================")

cheap = (
    df.groupby("college")["fees"]
    .min()
    .sort_values()
    .head(20)
)

print(cheap)
print("\n======================")
print("MOST EXPENSIVE COLLEGES")
print("======================")

expensive = (
    df.groupby("college")["fees"]
    .max()
    .sort_values(ascending=False)
    .head(20)
)

print(expensive)
print("\n======================")
print("COURSE DEMAND")
print("======================")

course_rank = (
    df.groupby("course")["rank"]
    .mean()
    .sort_values()
)

print(course_rank.head(20))
df.to_csv("analytics_output.csv", index=False)

print("\nanalytics_output.csv created")