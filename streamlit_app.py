import base64
import pandas as pd
import numpy as np
import streamlit as st

# =====================================================
# 1. PAGE CONFIG & UNIFIED DEEP METALLIC THEME
# =====================================================
st.set_page_config(
    page_title="Namma MBBS – PG NEET Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide default white headers and background decoration elements
st.markdown("""
    <style>
    header[data-testid="stHeader"] { background: #0D1B2E !important; }
    [data-testid="stDecoration"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# Injecting Global CSS Architecture
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* Background Canvas styling */
.stApp { background: linear-gradient(160deg, #0D1B2E 0%, #1A2F4A 40%, #0F2240 100%); min-height: 100vh; }

/* Left Hand Side Menu Control Track Panel */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1628 0%, #152238 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 { color: white !important; margin-top: 15px !important;}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important; color: white !important;
}

/* Fixes the whited-out text inside text and number input boxes */
input[type="text"], input[type="number"], [data-baseweb="input"] input {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    background-color: #0F2240 !important;
    caret-color: #F15A24 !important;
}

/* Forces the container background to remain dark deep blue */
[data-baseweb="input"] {
    background-color: #0F2240 !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 10px !important;
}

/* Adjusts the inner spin buttons so they don't cause rendering quirks */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

/* Glassmorphism Dashboard Metric Cards */
.glass-card {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}
.glass-card:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 16px 48px rgba(0,0,0,0.5) !important;
}

/* Interactive Output Matrix Wrapper */
[data-testid="stDataFrame"] {
    border-radius: 16px !important; 
    overflow: hidden !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* Custom Typography Colors overrides */
h1,h2,h3,h4 { color: white !important; }
p, span, label { color: rgba(255,255,255,0.8) !important; }
</style>
""", unsafe_allow_html=True)


# =====================================================
# 2. INTERNAL RELATIVE DATA LOADING ENGINE
# =====================================================
@st.cache_data
def load_data():
    try:
        # Pulls data securely from your nested folder position
        df = pd.read_csv("extractor/final_cleaned.csv")
    except FileNotFoundError:
        # Temporary internal backup fallback layout
        df = pd.DataFrame({
            'college': ['Bangalore Medical College', 'KMC Mangalore'],
            'course': ['M.D. GENERAL MEDICINE', 'M.D. GENERAL MEDICINE'],
            'category': ['GM', 'GM'],
            'fees': [115000, 750000],
            'rank': [12000, 28000],
            'round': ['ROUND 1', 'ROUND 2'],
            'source': ['KEA', 'MCC']
        })

    # Standardize column headers for reliable parsing
    df.columns = df.columns.astype(str).str.strip().str.lower()
    
    # Keyword translation engine to map your CSV keys perfectly
    rename_dict = {}
    for col in df.columns:
        if 'college' in col: rename_dict[col] = 'college'
        elif 'course' in col or 'specialty' in col: rename_dict[col] = 'course'
        elif 'category' in col or 'quota' in col: rename_dict[col] = 'category'
        elif 'fee' in col: rename_dict[col] = 'fees'
        elif 'rank' in col or 'cutoff' in col: rename_dict[col] = 'rank'
        elif 'round' in col: rename_dict[col] = 'round'
        elif 'type' in col or 'source' in col or 'file' in col: rename_dict[col] = 'source'
        
    df = df.rename(columns=rename_dict)
    
    # Strip lingering double-quotes out of dataset rows
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.replace('"', '', regex=False).str.strip()

    # Apply global string transformations
    if "course" in df.columns:
        df["course"] = df["course"].astype(str).str.upper().str.replace('(', '', regex=False).str.replace(')', '', regex=False)
    if "category" in df.columns:
        df["category"] = df["category"].astype(str).str.upper()
    if "college" in df.columns:
        df["college"] = df["college"].astype(str)
    if "round" in df.columns:
        df["round"] = df["round"].astype(str).str.upper()
        
    if "source" in df.columns:
        df["source"] = df["source"].astype(str).str.upper()
        df["source"] = df["source"].apply(lambda x: "MCC" if "MCC" in x or "AIQ" in x else "KEA")
    else:
        df["source"] = "MCC"
        
    return df

df = load_data()


# =====================================================
# 3. SIDEBAR CONTROLS (GROUPED CONTEXT ARCHITECTURE)
# =====================================================
with st.sidebar:
    st.markdown("## 🎯 Student Details")
    rank = st.number_input("Enter AIR Rank", min_value=1, max_value=300000, value=14000, step=100, key="pg_user_rank")

    course_options = sorted(df["course"].dropna().unique()) if "course" in df.columns else []
    course = st.selectbox("Course Specialty", course_options, key="pg_user_course")
    df_course = df[df["course"] == course] if "course" in df.columns else df

    st.divider()
    st.markdown("## 🏛️ Counseling Details")
    counseling_options = sorted(df_course["source"].dropna().unique()) if "source" in df_course.columns else ["MCC"]
    counseling = st.selectbox("Counseling Type", counseling_options, key="pg_user_source")
    df_source = df_course[df_course["source"] == counseling] if "source" in df_course.columns else df_course

    st.divider()
    st.markdown("## 👥 Seat Category")
    category_options = sorted(df_source["category"].dropna().unique()) if "category" in df_source.columns else []
    category = st.selectbox("Category Quota", category_options, key="pg_user_cat")

    st.divider()
    st.markdown("## 🔍 Advanced Filters")
    college_search = st.text_input("Search College Name", placeholder="e.g., Bangalore Medical...", key="pg_user_search")
    near_miss = st.checkbox("Include Near Miss colleges", value=True, key="pg_user_near_miss")


# =====================================================
# 4. BRANDING HERO CONTAINER HEADER BLOCK
# =====================================================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

img_base64 = get_base64_image("logo.png") or get_base64_image("assets/logo.png")

if img_base64:
    logo_img = f'<img src="data:image/png;base64,{img_base64}" style="height:120px;width:120px;object-fit:cover;border-radius:50%;border:3px solid rgba(241,90,36,0.6);box-shadow:0 8px 32px rgba(0,0,0,0.5);background:white;padding:8px;">'
else:
    logo_img = '<div style="font-size:3rem;">🏥</div>'

st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(241,90,36,0.15) 0%,rgba(27,42,74,0.4) 50%,rgba(241,90,36,0.1) 100%);
    backdrop-filter:blur(20px); border:1px solid rgba(255,255,255,0.12);
    border-radius:24px; padding:40px 30px; text-align:center; margin-bottom:28px;
    box-shadow:0 20px 60px rgba(0,0,0,0.4);">
  {logo_img}
  <h1 style="color:white !important; font-size:2.8rem; font-weight:900; margin:14px 0 0; letter-spacing:-1px;">
    NEET PG College Predictor
  </h1>
  <p style="color:rgba(255,255,255,0.6) !important; font-size:1.05rem; margin:8px 0 20px;">
    Specialty Tracking Module &nbsp;•&nbsp; Custom Round Matrix Analytics Engine
  </p>
  <div style="display:inline-block;background:linear-gradient(90deg,#F15A24,#D04010);
      color:white;padding:8px 20px;border-radius:100px;font-weight:700;font-size:0.85rem;
      box-shadow:0 4px 20px rgba(241,90,36,0.5);">
    ✦ Powered by Namma MBBS · Trusted Medical Admissions Partner
  </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# 5. PREDICTIVE PROCESSING MATCH ENGINE LOGIC
# =====================================================
filtered = df_source[df_source["category"] == category].copy() if "category" in df_source.columns else df_source.copy()
if college_search:
    filtered = filtered[filtered["college"].str.contains(college_search, case=False, na=False)]

def chance_label(user_rank, cutoff):
    try:
        cutoff_val = float(cutoff)
    except:
        return "❌ Out of Range"
    if user_rank <= cutoff_val:
        m = (cutoff_val - user_rank) / user_rank * 100
        if m >= 20: return "✅ Safe"
        if m >= 5:  return "🟡 Likely"
        return "⚠️ Borderline"
    if (user_rank - cutoff_val) / user_rank * 100 <= 15: return "🔴 Near Miss"
    return "❌ Out of Range"

def color_chance(val):
    if "Safe" in str(val): return "background-color:#0a3d1f;color:#4ade80;font-weight:700;border-radius:6px;"
    if "Likely" in str(val): return "background-color:#3d2e00;color:#fbbf24;font-weight:700;border-radius:6px;"
    if "Borderline" in str(val): return "background-color:#3d1500;color:#fb923c;font-weight:700;border-radius:6px;"
    if "Near Miss" in str(val): return "background-color:#3d0a0a;color:#f87171;font-weight:700;border-radius:6px;"
    return "color:rgba(255,255,255,0.4);"


# =====================================================
# 6. CARD VIEWS GENERATION AND DISPLAY ROW
# =====================================================
if len(filtered) > 0 and "rank" in filtered.columns:
    filtered["chance"] = filtered["rank"].apply(lambda x: chance_label(rank, x))
    
    allowed_chances = {"✅ Safe", "🟡 Likely", "⚠️ Borderline"}
    if near_miss:
        allowed_chances.add("🔴 Near Miss")
    filtered = filtered[filtered["chance"].isin(allowed_chances)]

if len(filtered) > 0:
    total_options = filtered["college"].nunique() if "college" in filtered.columns else 0
    safe_count = filtered[filtered["chance"] == "✅ Safe"]["college"].nunique() if "college" in filtered.columns else 0
    likely_count = filtered[filtered["chance"] == "🟡 Likely"]["college"].nunique() if "college" in filtered.columns else 0
    border_count = filtered[filtered["chance"] == "⚠️ Borderline"]["college"].nunique() if "college" in filtered.columns else 0
    near_count = filtered[filtered["chance"] == "🔴 Near Miss"]["college"].nunique() if "college" in filtered.columns else 0

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:16px 0 28px 0;">
      <div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);border-radius:14px;padding:16px;text-align:center;border-top:3px solid #4A90D9;">
        <div style="font-size:1.8rem;font-weight:900;color:white;">{total_options}</div>
        <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);font-weight:600;text-transform:uppercase;letter-spacing:1px;">Total Options</div>
      </div>
      <div style="background:rgba(0,200,81,0.1);border:1px solid rgba(0,200,81,0.25);border-radius:14px;padding:16px;text-align:center;border-top:3px solid #00C851;">
        <div style="font-size:1.8rem;font-weight:900;color:#4ade80;">{safe_count}</div>
        <div style="font-size:0.7rem;color:#4ade80;font-weight:600;text-transform:uppercase;letter-spacing:1px;">✅ Safe</div>
      </div>
      <div style="background:rgba(255,179,0,0.1);border:1px solid rgba(255,179,0,0.25);border-radius:14px;padding:16px;text-align:center;border-top:3px solid #FFB300;">
        <div style="font-size:1.8rem;font-weight:900;color:#fbbf24;">{likely_count}</div>
        <div style="font-size:0.7rem;color:#fbbf24;font-weight:600;text-transform:uppercase;letter-spacing:1px;">🟡 Likely</div>
      </div>
      <div style="background:rgba(251,146,60,0.1);border:1px solid rgba(251,146,60,0.25);border-radius:14px;padding:16px;text-align:center;border-top:3px solid #fb923c;">
        <div style="font-size:1.8rem;font-weight:900;color:#fb923c;">{border_count}</div>
        <div style="font-size:0.7rem;color:#fb923c;font-weight:600;text-transform:uppercase;letter-spacing:1px;">⚠️ Borderline</div>
      </div>
      <div style="background:rgba(248,113,113,0.1);border:1px solid rgba(248,113,113,0.25);border-radius:14px;padding:16px;text-align:center;border-top:3px solid #f87171;">
        <div style="font-size:1.8rem;font-weight:900;color:#f87171;">{near_count}</div>
        <div style="font-size:0.7rem;color:#f87171;font-weight:600;text-transform:uppercase;letter-spacing:1px;">🔴 Near Miss</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # 7. MULTI-ROUND PIVOT DATAFRAME MATRIX VIEW
    # =====================================================
    st.markdown("### 📊 Round-by-Round Cutoff Matrix")

    matrix_data = []
    for college_name, group in filtered.groupby("college"):
        r1_val = r2_val = r3_val = stray_val = None
        fees_val = group["fees"].iloc[0] if "fees" in group.columns else 0
        
        for _, row in group.iterrows():
            rnd = str(row["round"]).upper()
            try:
