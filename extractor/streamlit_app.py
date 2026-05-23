import base64
import pandas as pd
import streamlit as st

# =====================================================
# 1. EMULATE UG CONFIG & DEEP BLUE THEME ENGINE
# =====================================================
st.set_page_config(
    page_title="Namma MBBS - PG NEET Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Premium Theme CSS (Emulating your uploaded UI screenshots)
st.markdown("""
    <style>
        /* Deep Dashboard Metallic Navy Background */
        .stApp {
            background-color: #0b132b !important;
            color: #ffffff !important;
            font-family: 'Inter', -apple-system, sans-serif;
        }
        
        /* Sidebar Restyling matching premium interface */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #1e293b;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {
            color: #cbd5e1 !important;
        }
        
        /* Main App Header Banner Container */
        .hero-container {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        /* Metric Badges Grid System (Safe, Likely, Borderline) */
        .metric-row {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }
        .metric-box {
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.05);
        }
        .m-total { background-color: #1e293b; border-top: 4px solid #94a3b8; }
        .m-safe { background-color: #064e3b; border-top: 4px solid #10b981; color: #a7f3d0; }
        .m-likely { background-color: #14532d; border-top: 4px solid #22c55e; color: #bbf7d0; }
        .m-border { background-color: #78350f; border-top: 4px solid #f59e0b; color: #fef3c7; }
        .m-miss { background-color: #7f1d1d; border-top: 4px solid #ef4444; color: #fee2e2; }
        
        .metric-val { font-size: 24px; font-weight: 800; margin-top: 5px; }
        .metric-lbl { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.8; }

        /* Container styling for our interactive tables */
        [data-testid="stDataFrame"] {
            background-color: #1e293b !important;
            padding: 10px;
            border-radius: 16px;
            border: 1px solid #334155;
        }
        
        h2, h3 {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }
    </style>
""", unsafe_allow_html=True)


# =====================================================
# 2. INTERNAL RELATIVE DATA LOADING ENGINE
# =====================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("final_cleaned.csv")
    except FileNotFoundError:
        # Emergency backup fallback block if file path snaps
        df = pd.DataFrame({
            'college': ['Bangalore Medical College', 'Bangalore Medical College', 'KMC Mangalore', 'St. Johns Medical College'],
            'course': ['M.D. GENERAL MEDICINE', 'M.D. GENERAL MEDICINE', 'M.D. GENERAL MEDICINE', 'M.D. GENERAL MEDICINE'],
            'category': ['GM', 'GM', 'GM', 'GM'],
            'fees': [115000, 115000, 750000, 115000],
            'rank': [12000, 15500, 28000, 14000],
            'round': ['Round 1', 'Round 2', 'Round 1', 'Mop-up'],
            'source_file': ['KEA_PG_2025', 'KEA_PG_2025', 'MCC_AIQ_2025', 'KEA_PG_2025']
        })

    df.columns = df.columns.astype(str).str.strip().str.lower()
    
    if "source_file" in df.columns:
        df["source"] = df["source_file"].astype(str).str.upper()
        df["source"] = df["source"].apply(
            lambda x: "MCC" if ("MCC" in x or "AIQ" in x or "ALL INDIA" in x) else "KEA"
        )
    else:
        df["source"] = "KEA"
        
    # Formatting cleaning steps
    df["course"] = df["course"].astype(str).str.upper().str.strip()
    df["category"] = df["category"].astype(str).str.upper().str.strip()
    df["college"] = df["college"].astype(str).str.strip()
    df["round"] = df["round"].astype(str).str.strip().str.upper()
    return df

df = load_data()


# =====================================================
# 3. SIDEBAR CONTROLS (STUDENT DETAILS)
# =====================================================
st.sidebar.markdown("### 🎯 Student Details")
rank = st.sidebar.number_input("Enter AIR Rank", min_value=1, max_value=300000, value=30000)

course_options = sorted(df["course"].dropna().unique())
course = st.sidebar.selectbox("Course Specialty", course_options)

# Isolate dataset base targets
df_course = df[df["course"] == course]

counseling_options = sorted(df_course["source"].dropna().unique())
counseling = st.sidebar.selectbox("Counseling Type", counseling_options)
df_source = df_course[df_course["source"] == counseling]

category_options = sorted(df_source["category"].dropna().unique())
category = st.sidebar.selectbox("Seat Category", category_options)

college_search = st.sidebar.text_input("Search College Name")


# =====================================================
# 4. BRANDING HERO CONTAINER BLOCK
# =====================================================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

img_base64 = get_base64_image("../assets/logo.png")

if img_base64:
    st.markdown(f"""
        <div class="hero-container">
            <img src="data:image/png;base64,{img_base64}" width="180" style="margin-bottom: 15px;">
            <h1 style="font-size: 32px; font-weight: 800; margin: 0; color: #ffffff;">NEET PG College Predictor</h1>
            <p style="font-size: 14px; color: #94a3b8; margin: 5px 0 0 0;">Powered by Namma MBBS • Trusted Medical Admissions Partner</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="hero-container">
            <h1 style="font-size: 32px; font-weight: 800; margin: 0;">NEET PG College Predictor</h1>
        </div>
    """, unsafe_allow_html=True)


# =====================================================
# 5. PREDICTIVE PROCESSING ENGINE
# =====================================================
# Filter base core logic matches
filtered = df_source[df_source["category"] == category].copy()
if college_search:
    filtered = filtered[filtered["college"].str.contains(college_search, case=False, na=False)]

# Create Predictive Classification Metrics based on your premium look
def classify_chance(cutoff, user_rank):
    if user_rank <= cutoff * 0.85: return "🟢 SAFE"
    elif user_rank <= cutoff: return "🟢 LIKELY"
    elif user_rank <= cutoff * 1.15: return "🟡 BORDERLINE"
    else: return "🔴 NEAR MISS"

if len(filtered) > 0:
    filtered["chance_status"] = filtered["rank"].apply(lambda x: classify_chance(x, rank))
    
    # Segment totals out for analytical summary row
    c_total = filtered["college"].nunique()
    c_safe = filtered[filtered["chance_status"] == "🟢 SAFE"]["college"].nunique()
    c_likely = filtered[filtered["chance_status"] == "🟢 LIKELY"]["college"].nunique()
    c_border = filtered[filtered["chance_status"] == "🟡 BORDERLINE"]["college"].nunique()
    c_miss = filtered[filtered["chance_status"] == "🔴 NEAR MISS"]["college"].nunique()
else:
    c_total = c_safe = c_likely = c_border = c_miss = 0


# =====================================================
# 6. RENDER TOP-LEVEL METRIC BOXES
# =====================================================
st.markdown(f"""
    <div class="metric-row">
        <div class="metric-box m-total"><div class="metric-lbl">Total Options</div><div class="metric-val">{c_total}</div></div>
        <div class="metric-box m-safe"><div class="metric-lbl">✔ Safe</div><div class="metric-val">{c_safe}</div></div>
        <div class="metric-box m-likely"><div class="metric-lbl">👍 Likely</div><div class="metric-val">{c_likely}</div></div>
        <div class="metric-box m-border"><div class="metric-lbl">⚠ Borderline</div><div class="metric-val">{c_border}</div></div>
        <div class="metric-box m-miss"><div class="metric-lbl">🚨 Near Miss</div><div class="metric-val">{c_miss}</div></div>
    </div>
""", unsafe_allow_html=True)


# =====================================================
# 7. GENERATE MULTI-ROUND CUTOFF COMPARISON MATRIX
# =====================================================
st.markdown("### 📊 Round-by-Round Cutoff Comparison Matrix")

if len(filtered) == 0:
    st.info("💡 Adjust your filters in the sidebar. No matching combination found in our historical database entries.")
else:
    # We aggregate data to construct the requested horizontal Round grid matrix dynamically
    matrix_data = []
    
    for college_name, group in filtered.groupby("college"):
        # Default empty slots
        r1_val = r2_val = r3_val = stray_val = None
        fees_val = group["fees"].iloc[0] if "fees" in group.columns else 0
        
        # Pull cutoffs for separate rounds mapped to standard rows
        for _, row in group.iterrows():
            rnd = str(row["round"])
            if "1" in rnd: r1_val = int(row["rank"])
            elif "2" in rnd: r2_val = int(row["rank"])
            elif "3" in rnd or "MOP" in rnd: r3_val = int(row["rank"])
            elif "STRAY" in rnd: stray_val = int(row["rank"])
            
        # Determine consolidated display logic chance tag based on final active cutoff
        final_cutoff = group["rank"].max()
        overall_chance = classify_chance(final_cutoff, rank)
        
        matrix_data.append({
            "Chance": overall_chance,
            "College Name": college_name,
            "Round 1 Cutoff": r1_val,
            "Round 2 Cutoff": r2_val,
            "Mop-Up Cutoff": r3_val,
            "Stray Cutoff": stray_val,
            "Annual Fees": int(fees_val)
        })
        
    matrix_df = pd.DataFrame(matrix_data)
    
    # Sort colleges alphabetically or by minimum cutoff rank
    matrix_df = matrix_df.sort_values(by="Round 1 Cutoff", na_position="last")
    
    # Implement Streamlit's DataFrame configuration layer to output a beautiful grid structure
    st.dataframe(
        matrix_df,
        column_config={
            "Chance": st.column_config.TextColumn("Chance", width="small"),
            "College Name": st.column_config.TextColumn("College Name", width="large"),
            "Round 1 Cutoff": st.column_config.NumberColumn("Round 1", format="%,d"),
            "Round 2 Cutoff": st.column_config.NumberColumn("Round 2", format="%,d"),
            "Mop-Up Cutoff": st.column_config.NumberColumn("Mop-Up", format="%,d"),
            "Stray Cutoff": st.column_config.NumberColumn("Stray", format="%,d"),
            "Annual Fees": st.column_config.NumberColumn("Annual Fees", format="₹%,d")
        },
        use_container_width=True,
        height=550,
        hide_index=True
    )
