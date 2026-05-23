from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# =========================================
# LOAD DATA
# =========================================

df = pd.read_csv("final_cleaned.csv")

df["rank"] = pd.to_numeric(df["rank"], errors="coerce")
df["fees"] = pd.to_numeric(df["fees"], errors="coerce")

df = df.dropna(subset=["rank"])

# =========================================
# DROPDOWNS
# =========================================

courses = sorted(df["course"].dropna().unique())
categories = sorted(df["category"].dropna().unique())

# =========================================
# CHANCE LOGIC
# =========================================

def classify(student_rank, cutoff_rank):

    if student_rank <= cutoff_rank:
        return "SAFE"

    elif student_rank <= cutoff_rank * 1.3:
        return "MODERATE"

    else:
        return "DREAM"

# =========================================
# HOME
# =========================================

@app.route("/", methods=["GET", "POST"])
def home():

    results = None

    if request.method == "POST":

        student_rank = int(request.form["rank"])

        category = request.form["category"]

        selected_course = request.form["course"]

        # =====================================
        # FILTER
        # =====================================

        filtered = df[
            (df["category"] == category)
            &
            (df["course"] == selected_course)
        ].copy()

        # =====================================
        # CHANCE
        # =====================================

        filtered["chance"] = filtered["rank"].apply(
            lambda cutoff: classify(student_rank, cutoff)
        )

        # =====================================
        # SORT
        # =====================================

        filtered = filtered.sort_values("rank")

        # =====================================
        # RESULTS
        # =====================================

        results = filtered[
            [
                "college",
                "course",
                "category",
                "fees",
                "rank",
                "chance",
                "round"
            ]
        ].head(100).to_dict(orient="records")

    return render_template(
        "index.html",
        results=results,
        courses=courses,
        categories=categories
    )

# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    app.run(debug=True)