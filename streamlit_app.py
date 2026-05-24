import pandas as pd
import streamlit as st

# ======================================================
# PAGE CONFIG  –  must be first Streamlit call
# ======================================================
st.set_page_config(
    page_title="Namma MBBS – PG NEET Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CSS INJECTION
# ======================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark sidebar */
[data-testid="stSidebar"] {
    background: #0c1445 !important;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] label {
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    color: #94a3b8 !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stNumberInput > div > div > input {
    background: #1e2a5e !important;
    border: 1px solid #334155 !important;
    color: #f1f5f9 !important;
    border-radius: 8px !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.1rem 1.4rem !important;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
[data-testid="stMetric"] label { color: #64748b !important; font-size: 0.75rem !important; text-transform: uppercase !important; letter-spacing: 0.6px; }
[data-testid="stMetricValue"] { color: #0f172a !important; font-size: 2rem !important; font-weight: 700 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 6px; background: #f1f5f9; padding: 4px; border-radius: 10px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px !important; padding: 6px 18px !important; font-weight: 600 !important; color: #64748b !important; }
.stTabs [aria-selected="true"] { background: #1e3a8a !important; color: white !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* Alert/info box */
.stAlert { border-radius: 10px; }

/* Header */
.app-header { background: linear-gradient(135deg, #0c1445 0%, #1e3a8a 60%, #1d4ed8 100%); padding: 2rem 2.5rem; border-radius: 16px; margin-bottom: 1.5rem; }
.app-header h1 { color: white !important; font-size: 1.9rem !important; font-weight: 800 !important; margin: 0 !important; letter-spacing: -0.3px; }
.app-header p { color: #93c5fd !important; margin: 0.3rem 0 0 0 !important; font-size: 0.95rem; }

/* Chance badge */
.badge-safe      { background:#dcfce7; color:#166534; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:700; }
.badge-likely    { background:#fef9c3; color:#854d0e; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:700; }
.badge-border    { background:#ffedd5; color:#9a3412; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:700; }
.badge-nearmiss  { background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:700; }
</style>
""", unsafe_allow_html=True)


# ======================================================
# HELPER FUNCTIONS  –  defined at module level (CRITICAL)
# ======================================================

def get_chance(student_rank: int, cutoff_rank) -> str:
    """Return admission chance label for a student rank vs a cutoff rank."""
    if pd.isna(cutoff_rank) or cutoff_rank == 0:
        return "—"
    c = float(cutoff_rank)
    r = float(student_rank)
    if r <= c:
        return "✅ Safe"
    elif r <= c * 1.15:
        return "🟡 Likely"
    elif r <= c * 1.35:
        return "⚠️ Borderline"
    else:
        return "🔴 Near Miss"


def color_chance(val: str) -> str:
    """Pandas Styler function: returns CSS color string for Admission Chance column."""
    if "Safe" in str(val):
        return "background-color:#dcfce7; color:#166534; font-weight:700"
    elif "Likely" in str(val):
        return "background-color:#fef9c3; color:#854d0e; font-weight:700"
    elif "Borderline" in str(val):
        return "background-color:#ffedd5; color:#9a3412; font-weight:700"
    elif "Near Miss" in str(val):
        return "background-color:#fee2e2; color:#991b1b; font-weight:700"
    return ""


def color_cutoff(val) -> str:
    """Pandas Styler function: colors numeric cutoff cells by value."""
    try:
        v = float(val)
        if v <= 10000:
            return "background-color:#dbeafe; color:#1e40af; font-weight:600"
        elif v <= 30000:
            return "background-color:#dcfce7; color:#166534; font-weight:600"
        elif v <= 60000:
            return "background-color:#fef9c3; color:#854d0e; font-weight:600"
        elif v <= 100000:
            return "background-color:#ffedd5; color:#9a3412; font-weight:600"
        else:
            return "background-color:#fee2e2; color:#991b1b; font-weight:600"
    except (ValueError, TypeError):
        return ""


def best_cutoff(row: pd.Series) -> float:
    """Returns the most recent available cutoff rank for a row."""
    for col in ["Stray Vacancy", "Round 3", "Round 2", "Round 1"]:
        if col in row and pd.notna(row[col]):
            return float(row[col])
    return float("nan")


def fmt_rank(val) -> str:
    """Format a rank value as comma-separated integer, or blank if NaN."""
    if pd.isna(val):
        return "—"
    return f"{int(val):,}"


# ======================================================
# DATA LOADING
# ======================================================
@st.cache_data(show_spinner="Loading cutoff data…")
def load_data() -> pd.DataFrame:
    try:
        df = pd.read_csv("mcc_pg_cutoffs_2025.csv")
    except FileNotFoundError:
        st.error("❌ Data file `mcc_pg_cutoffs_2025.csv` not found. Please add it to the repo root.")
        st.stop()

    # Ensure column dtypes
    df["college"]  = df["college"].astype(str).str.strip()
    df["course"]   = df["course"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    for col in ["Round 1", "Round 2", "Round 3", "Stray Vacancy"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            df[col] = float("nan")
    return df


df = load_data()


# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:
    st.markdown("## 🎯 Filter Options")
    st.markdown("---")

    rank = st.number_input(
        "Enter AIR Rank",
        min_value=1, max_value=300_000,
        value=14_000, step=100,
        help="Your NEET PG 2025 All India Rank"
    )

    # Cascading filters
    course_options = sorted(df["course"].dropna().unique().tolist())
    course = st.selectbox("Course Specialty", course_options)

    df_course = df[df["course"] == course]
    category_options = sorted(df_course["category"].dropna().unique().tolist())
    category = st.selectbox("Seat Category", category_options)

    df_filtered = df_course[df_course["category"] == category].copy()

    college_search = st.text_input("🔍 Search College Name", placeholder="e.g. AIIMS, Maulana…")
    if college_search:
        df_filtered = df_filtered[
            df_filtered["college"].str.contains(college_search, case=False, na=False)
        ]

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem; color:#94a3b8; line-height:1.6;'>"
        "<b style='color:#e2e8f0;'>Data Source</b><br>"
        "MCC NEET PG 2025<br>"
        "Round 1 · Round 2 · Round 3 · Stray<br><br>"
        "<b style='color:#e2e8f0;'>Powered by</b><br>"
        "Namma MBBS 🩺"
        "</div>",
        unsafe_allow_html=True
    )


# ======================================================
# HEADER
# ======================================================
st.markdown("""
<div class="app-header">
    <h1>🩺 Namma MBBS – PG NEET Predictor</h1>
    <p>MCC All India Quota · Round-by-Round Cutoff Intelligence · 2025</p>
</div>
""", unsafe_allow_html=True)


# ======================================================
# COMPUTE ADMISSION CHANCES
# ======================================================
ROUNDS = ["Round 1", "Round 2", "Round 3", "Stray Vacancy"]

if len(df_filtered) > 0:
    df_filtered = df_filtered.copy()
    df_filtered["_best_cutoff"] = df_filtered.apply(best_cutoff, axis=1)
    df_filtered["Admission Chance"] = df_filtered["_best_cutoff"].apply(
        lambda c: get_chance(rank, c)
    )
    df_filtered = df_filtered.sort_values("_best_cutoff", ascending=True, na_position="last")


# ======================================================
# ANALYTICS CARDS
# ======================================================
total  = len(df_filtered)
safe   = int((df_filtered["Admission Chance"] == "✅ Safe").sum())    if total else 0
likely = int((df_filtered["Admission Chance"] == "🟡 Likely").sum())  if total else 0
border = int((df_filtered["Admission Chance"] == "⚠️ Borderline").sum()) if total else 0
near   = int((df_filtered["Admission Chance"] == "🔴 Near Miss").sum())  if total else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🏥 Total Options",   total)
c2.metric("✅ Safe",            safe)
c3.metric("🟡 Likely",          likely)
c4.metric("⚠️ Borderline",      border)
c5.metric("🔴 Near Miss",       near)

st.markdown("<br>", unsafe_allow_html=True)


# ======================================================
# TABS
# ======================================================
tab1, tab2 = st.tabs(["📊 Round-by-Round Cutoff Matrix", "📋 College List"])


# -----------------------------------------------
# TAB 1: ROUND-BY-ROUND CUTOFF MATRIX
# -----------------------------------------------
with tab1:
    if total == 0:
        st.info("💡 No colleges found for this combination. Try adjusting your filters.")
    else:
        # Build display dataframe
        matrix_cols = ["college"] + ROUNDS + ["Admission Chance"]
        matrix_df = df_filtered[
            ["college"] + [c for c in ROUNDS if c in df_filtered.columns] + ["Admission Chance"]
        ].copy()

        # Sort by Round 1 cutoff if available
        if "Round 1" in matrix_df.columns:
            matrix_df = matrix_df.sort_values("Round 1", ascending=True, na_position="last")

        matrix_df = matrix_df.rename(columns={"college": "College"})

        # Format rank columns for display
        rank_display_cols = [c for c in ROUNDS if c in matrix_df.columns]
        for col in rank_display_cols:
            matrix_df[col] = matrix_df[col].apply(fmt_rank)

        st.markdown(
            f"**Showing {len(matrix_df)} colleges** · "
            f"Your Rank: **{rank:,}** · "
            f"Course: **{course}** · "
            f"Category: **{category}**"
        )
        st.markdown(
            "<small style='color:#64748b;'>Cutoff = highest (worst) rank admitted in that round. "
            "If your rank ≤ cutoff → you are competitive.</small>",
            unsafe_allow_html=True
        )
        st.markdown("")

        # Apply styling only to Admission Chance column
        styled_df = matrix_df.style.map(color_chance, subset=["Admission Chance"])

        st.dataframe(
            styled_df,
            use_container_width=True,
            height=560,
            hide_index=True
        )

        # Legend
        st.markdown(
            "<div style='display:flex;gap:10px;margin-top:10px;flex-wrap:wrap;'>"
            "<span class='badge-safe'>✅ Safe – rank ≤ cutoff</span>"
            "<span class='badge-likely'>🟡 Likely – within 15% of cutoff</span>"
            "<span class='badge-border'>⚠️ Borderline – within 35% of cutoff</span>"
            "<span class='badge-nearmiss'>🔴 Near Miss – beyond 35%</span>"
            "</div>",
            unsafe_allow_html=True
        )


# -----------------------------------------------
# TAB 2: FULL COLLEGE LIST WITH ALL DETAILS
# -----------------------------------------------
with tab2:
    if total == 0:
        st.info("💡 No colleges found. Adjust your filters.")
    else:
        detail_df = df_filtered[["college", "category"] + ROUNDS + ["Admission Chance"]].copy()
        detail_df = detail_df.rename(columns={"college": "College", "category": "Category"})
        for col in ROUNDS:
            if col in detail_df.columns:
                detail_df[col] = detail_df[col].apply(fmt_rank)

        styled_detail = detail_df.style.map(color_chance, subset=["Admission Chance"])

        st.dataframe(
            styled_detail,
            use_container_width=True,
            height=560,
            hide_index=True
        )

        # Download button
        csv_export = df_filtered[["college","category"] + ROUNDS + ["Admission Chance"]].copy()
        for col in ROUNDS:
            if col in csv_export.columns:
                csv_export[col] = csv_export[col].apply(lambda x: int(x) if pd.notna(x) else "")
        st.download_button(
            label="⬇️ Download Results as CSV",
            data=csv_export.to_csv(index=False),
            file_name=f"nammambbs_{course.replace(' ','_')}_{category}.csv",
            mime="text/csv"
        )


# ======================================================
# FOOTER
# ======================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<hr style='border:none;border-top:1px solid #e2e8f0;margin:0;'>"
    "<p style='text-align:center;color:#94a3b8;font-size:0.78rem;margin-top:10px;'>"
    "Data: MCC NEET PG 2025 Allotment Lists (R1/R2/R3/Stray) · "
    "For guidance purposes only · Verify with official MCC/NMC records · "
    "© 2025 Namma MBBS Private Limited"
    "</p>",
    unsafe_allow_html=True
)
