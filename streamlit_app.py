import pandas as pd
import streamlit as st

# ══════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Namma MBBS – PG NEET Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

[data-testid="stSidebar"] { background: #0c1445 !important; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] label {
    font-weight: 600 !important; font-size: 0.78rem !important;
    text-transform: uppercase !important; letter-spacing: 0.8px !important;
    color: #94a3b8 !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stNumberInput > div > div > input {
    background: #1e2a5e !important; border: 1px solid #334155 !important;
    color: #f1f5f9 !important; border-radius: 8px !important;
}
[data-testid="stMetric"] {
    background: #fff; border-radius: 12px; padding: 1.1rem 1.4rem !important;
    border: 1px solid #e2e8f0; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
[data-testid="stMetric"] label { color: #64748b !important; font-size: 0.75rem !important;
    text-transform: uppercase !important; letter-spacing: 0.6px; }
[data-testid="stMetricValue"] { color: #0f172a !important; font-size: 2rem !important; font-weight: 700 !important; }
.stTabs [data-baseweb="tab-list"] { gap: 6px; background: #f1f5f9; padding: 4px; border-radius: 10px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px !important; padding: 6px 18px !important;
    font-weight: 600 !important; color: #64748b !important; }
.stTabs [aria-selected="true"] { background: #1e3a8a !important; color: white !important; }
.app-header { background: linear-gradient(135deg, #0c1445 0%, #1e3a8a 60%, #1d4ed8 100%);
    padding: 1.8rem 2.5rem; border-radius: 16px; margin-bottom: 1.5rem; }
.app-header h1 { color: white !important; font-size: 1.8rem !important;
    font-weight: 800 !important; margin: 0 !important; }
.app-header p { color: #93c5fd !important; margin: 0.3rem 0 0 0 !important; font-size: 0.9rem; }
.counsel-badge { display:inline-block; padding:4px 14px; border-radius:20px;
    font-size:0.8rem; font-weight:700; margin-bottom:8px; }
.badge-mcc  { background:#dbeafe; color:#1e40af; }
.badge-kea  { background:#fce7f3; color:#9d174d; }
.badge-ins  { background:#d1fae5; color:#065f46; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# HELPER FUNCTIONS  (all at module level — no scope bugs)
# ══════════════════════════════════════════════════════

def get_chance(student_rank: int, cutoff) -> str:
    if pd.isna(cutoff) or cutoff == 0:
        return "—"
    c, r = float(cutoff), float(student_rank)
    if r <= c:           return "✅ Safe"
    elif r <= c * 1.15:  return "🟡 Likely"
    elif r <= c * 1.35:  return "⚠️ Borderline"
    else:                return "🔴 Near Miss"

def color_chance(val: str) -> str:
    v = str(val)
    if "Safe"      in v: return "background-color:#dcfce7;color:#166534;font-weight:700"
    if "Likely"    in v: return "background-color:#fef9c3;color:#854d0e;font-weight:700"
    if "Borderline"in v: return "background-color:#ffedd5;color:#9a3412;font-weight:700"
    if "Near Miss" in v: return "background-color:#fee2e2;color:#991b1b;font-weight:700"
    return ""

def fmt_rank(val) -> str:
    if pd.isna(val): return "—"
    return f"{int(val):,}"

def fmt_fees(val) -> str:
    if pd.isna(val): return "—"
    return f"₹{int(val):,}"

def best_cutoff(row, round_cols):
    for c in reversed(round_cols):   # last round first (most recent)
        if c in row.index and pd.notna(row[c]):
            return float(row[c])
    return float("nan")


# ══════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════
@st.cache_data(show_spinner="Loading cutoff data…")
def load_all():
    try:
        mcc  = pd.read_csv("mcc_pg_cutoffs_2025.csv")
        kni  = pd.read_csv("kea_non_ins_cutoffs.csv")
        kins = pd.read_csv("kea_ins_cutoffs.csv")
    except FileNotFoundError as e:
        st.error(f"❌ Missing data file: {e}. Ensure all CSVs are in the repo root.")
        st.stop()
    for df in [mcc, kni, kins]:
        df["college"]  = df["college"].astype(str).str.strip()
        df["course"]   = df["course"].astype(str).str.strip()
        df["category"] = df["category"].astype(str).str.strip()
    return mcc, kni, kins

MCC_ROUNDS = ["Round 1", "Round 2", "Round 3", "Stray Vacancy"]
KNI_ROUNDS = ["Round 1", "Round 2", "Mop-up", "Stray", "Stray Extended"]
KIS_ROUNDS = ["Round 1", "Round 2", "Mop-up"]

mcc_df, kni_df, kins_df = load_all()

COUNSELING_OPTIONS = {
    "MCC – All India Quota":       (mcc_df,  MCC_ROUNDS, "mcc"),
    "KEA – Non-Inservice":         (kni_df,  KNI_ROUNDS, "kea"),
    "KEA – Inservice":             (kins_df, KIS_ROUNDS, "ins"),
}


# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎯 Counseling Filters")
    st.markdown("---")

    rank = st.number_input("Enter AIR Rank", min_value=1, max_value=300_000,
                           value=14_000, step=100, help="Your NEET PG 2025 All India Rank")

    counseling_label = st.selectbox("Counseling Body & Type", list(COUNSELING_OPTIONS.keys()))
    active_df, active_rounds, badge_cls = COUNSELING_OPTIONS[counseling_label]

    # Cascading dropdowns
    course_options = sorted(active_df["course"].dropna().unique().tolist())
    course = st.selectbox("Course Specialty", course_options)

    df_course = active_df[active_df["course"] == course]
    category_options = sorted(df_course["category"].dropna().unique().tolist())
    category = st.selectbox("Seat Category", category_options)

    df_filtered = df_course[df_course["category"] == category].copy()

    college_search = st.text_input("🔍 Search College", placeholder="e.g. KIMS, Ramaiah…")
    if college_search:
        df_filtered = df_filtered[
            df_filtered["college"].str.contains(college_search, case=False, na=False)
        ]

    st.markdown("---")
    # Category legend for KEA
    if "KEA" in counseling_label:
        st.markdown("""<div style='font-size:0.7rem;color:#94a3b8;line-height:1.8;'>
        <b style='color:#e2e8f0'>Category Guide</b><br>
        GM = Govt Merit &nbsp;|&nbsp; GMP = Pvt Merit<br>
        OPN = Open (Pvt) &nbsp;|&nbsp; MNG = Management<br>
        1G/2AG/2BG/3AG/3BG = OBC Govt<br>
        S1G/S2G/S3G = SC A/B/C Govt<br>
        STG = ST Govt &nbsp;|&nbsp; NRI = NRI seats
        </div>""", unsafe_allow_html=True)
    st.markdown("""<div style='font-size:0.72rem;color:#94a3b8;margin-top:12px;'>
    Powered by <b style='color:#e2e8f0'>Namma MBBS 🩺</b>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════
badge_map = {"mcc": ("MCC – All India Quota", "badge-mcc"),
             "kea": ("KEA – Non-Inservice", "badge-kea"),
             "ins": ("KEA – Inservice", "badge-ins")}
badge_text, badge_cls_name = badge_map[badge_cls]

st.markdown(f"""
<div class="app-header">
    <span class="counsel-badge {badge_cls_name}">{badge_text}</span>
    <h1>🩺 Namma MBBS – PG NEET Predictor</h1>
    <p>Karnataka & All India Quota · Round-by-Round Cutoff Intelligence · 2025</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# COMPUTE CHANCES
# ══════════════════════════════════════════════════════
has_fees = "fees" in df_filtered.columns

if len(df_filtered) > 0:
    df_filtered = df_filtered.copy()
    # Convert round cols to numeric
    for col in active_rounds:
        if col in df_filtered.columns:
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors="coerce")

    df_filtered["_best"] = df_filtered.apply(
        lambda r: best_cutoff(r, active_rounds), axis=1)
    df_filtered["Admission Chance"] = df_filtered["_best"].apply(
        lambda c: get_chance(rank, c))
    df_filtered = df_filtered.sort_values("_best", ascending=True, na_position="last")


# ══════════════════════════════════════════════════════
# METRIC CARDS
# ══════════════════════════════════════════════════════
total  = len(df_filtered)
safe   = int((df_filtered["Admission Chance"] == "✅ Safe").sum())    if total else 0
likely = int((df_filtered["Admission Chance"] == "🟡 Likely").sum())  if total else 0
border = int((df_filtered["Admission Chance"] == "⚠️ Borderline").sum()) if total else 0
near   = int((df_filtered["Admission Chance"] == "🔴 Near Miss").sum())  if total else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🏥 Total Options",  total)
c2.metric("✅ Safe",           safe)
c3.metric("🟡 Likely",         likely)
c4.metric("⚠️ Borderline",     border)
c5.metric("🔴 Near Miss",      near)

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
tab1, tab2 = st.tabs(["📊 Round-by-Round Cutoff Matrix", "📋 College List"])

def build_matrix(df_in, rounds, include_fees):
    if len(df_in) == 0:
        st.info("💡 No colleges found. Adjust your filters.")
        return

    disp_cols = ["college"] + [r for r in rounds if r in df_in.columns] + ["Admission Chance"]
    if include_fees and "fees" in df_in.columns:
        disp_cols = ["college"] + [r for r in rounds if r in df_in.columns] + ["fees", "Admission Chance"]

    matrix = df_in[disp_cols].copy()
    matrix = matrix.rename(columns={"college": "College", "fees": "Course Fees"})

    # Format rank columns
    for col in rounds:
        if col in matrix.columns:
            matrix[col] = matrix[col].apply(fmt_rank)
    if "Course Fees" in matrix.columns:
        matrix["Course Fees"] = df_in["fees"].apply(fmt_fees).values

    st.markdown(
        f"**{len(matrix)} colleges** · Rank: **{rank:,}** · "
        f"Course: **{course}** · Category: **{category}**"
    )
    st.caption("Cutoff = highest (worst) rank admitted in that round. Your rank ≤ cutoff → competitive.")
    st.markdown("")

    styled = matrix.style.map(color_chance, subset=["Admission Chance"])
    st.dataframe(styled, use_container_width=True, height=560, hide_index=True)

    st.markdown(
        "<div style='display:flex;gap:10px;margin-top:10px;flex-wrap:wrap;font-size:0.8rem;'>"
        "<span style='background:#dcfce7;color:#166534;padding:3px 10px;border-radius:20px;font-weight:700'>✅ Safe – rank ≤ cutoff</span>"
        "<span style='background:#fef9c3;color:#854d0e;padding:3px 10px;border-radius:20px;font-weight:700'>🟡 Likely – within 15%</span>"
        "<span style='background:#ffedd5;color:#9a3412;padding:3px 10px;border-radius:20px;font-weight:700'>⚠️ Borderline – within 35%</span>"
        "<span style='background:#fee2e2;color:#991b1b;padding:3px 10px;border-radius:20px;font-weight:700'>🔴 Near Miss – beyond 35%</span>"
        "</div>", unsafe_allow_html=True
    )

with tab1:
    build_matrix(df_filtered, active_rounds, include_fees=True)

with tab2:
    if total == 0:
        st.info("💡 No colleges found.")
    else:
        detail_cols = ["college", "category"] + [r for r in active_rounds if r in df_filtered.columns]
        if has_fees and "fees" in df_filtered.columns:
            detail_cols += ["fees"]
        detail_cols += ["Admission Chance"]

        det = df_filtered[detail_cols].copy()
        det = det.rename(columns={"college": "College", "category": "Category", "fees": "Course Fees"})
        for col in active_rounds:
            if col in det.columns:
                det[col] = det[col].apply(fmt_rank)
        if "Course Fees" in det.columns:
            det["Course Fees"] = df_filtered["fees"].apply(fmt_fees).values

        styled_det = det.style.map(color_chance, subset=["Admission Chance"])
        st.dataframe(styled_det, use_container_width=True, height=560, hide_index=True)

        # Export
        export = df_filtered[detail_cols].copy()
        for col in active_rounds:
            if col in export.columns:
                export[col] = export[col].apply(lambda x: int(x) if pd.notna(x) else "")
        st.download_button(
            "⬇️ Download as CSV",
            data=export.to_csv(index=False),
            file_name=f"nammambbs_{counseling_label.replace(' ','_')}_{course[:20]}_{category}.csv",
            mime="text/csv"
        )

# ══════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<hr style='border:none;border-top:1px solid #e2e8f0;'>"
    "<p style='text-align:center;color:#94a3b8;font-size:0.75rem;margin-top:8px;'>"
    "Data: KEA PG NEET 2025 (R1/R2/Mop-up/Stray) · MCC NEET PG 2025 (R1/R2/R3/Stray) · "
    "For guidance only · Verify with official KEA/MCC records · "
    "© 2025 Namma MBBS Private Limited"
    "</p>", unsafe_allow_html=True
)
