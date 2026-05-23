import base64
import pandas as pd
import streamlit as st

# =====================================================
# 1. PAGE CONFIG & PREMIUM BRAND THEME SETUP
# =====================================================
st.set_page_config(
    page_title="Namma MBBS Intelligence System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Executive UI Theme Engine Injection
st.markdown("""
    <style>
        /* Global Background Smoothness */
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            font-family: 'Inter', -apple-system, sans-serif;
        }
        
        /* Sidebar Polish */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            box-shadow: 4px 0 25px rgba(0,0,0,0.15);
        }
        [data-testid="stSidebar"] .stMarkdown h2 {
            color: #f8fafc !important;
            font-weight: 700;
            font-size: 1.3rem !important;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            border-bottom: 2px solid #1e293b;
            padding-bottom: 12px;
            margin-bottom: 20px !important;
        }
        [data-testid="stSidebar"] label {
            color: #94a3b8 !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            margin-bottom: 6px !important;
        }
        
        /* Modern Analytics Cards Grid Design */
        .analytics-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            padding: 20px 24px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03), 0 2px 4px -1px rgba(15, 23, 42, 0.02);
            border-left: 6px solid #2563eb;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .analytics-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.08);
            border-left-color: #1d4ed8;
        }
        .card-label {
            color: #64748b;
            font-size: 0.75rem;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }
        .card-value {
            color: #0f172a;
            font-size: 1.75rem;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        
        /* Subheading Design Elements */
        h2, h3 {
            color: #0f172a !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }
        
        /* Premium Data Frame Table Containers styling wrapper overrides */
        [data-testid="stDataFrame"] {
            background: #ffffff;
            padding: 12px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03);
            border: 1px solid #e2e8f0;
        }
    </style>
""", unsafe_allow_html=True)


# =====================================================
# 2. INTERNAL RELATIVE DATA LOADING ENGINE
# =====================================================
@st.cache_data
def load_data():
    try:
        # Looking locally directly inside the same subfolder context seamlessly
        df = pd.read_csv("final_cleaned.csv")
    except FileNotFoundError:
        df = pd.DataFrame({
            'college': ['Bangalore Medical College', 'KMC Mangalore', 'St. Johns Medical College', 'JSS Medical College'],
            'course': ['M.D. MICROBIOLOGY', '(NBEMS) DERMATOLOGY', 'M.D. MICROBIOLOGY', 'M.D. GENERAL MEDICINE'],
            'category': ['1G', 'GM', '1G', 'GM'],
            'fees': [115000, 750000, 115000, 2200000],
            'rank': [141478, 52000, 149526, 32000],
            'round': ['Round 1', 'Round 2', 'Round 1', 'Mop-up'],
            'source_file': ['KEA_PG_2025', 'MCC_AIQ_2025', 'KEA_PG_2025', 'MCC_ALL_INDIA']
        })

    df.columns = df.columns.astype(str).str.strip().str.lower()

    if "source_file" in df.columns:
        df["source"] = df["source_file"].astype(str).str.upper()
        df["source"] = df["source"].apply(
            lambda x: "MCC" if ("MCC" in x or "AIQ" in x or "ALL INDIA" in x) else "KEA"
        )
    else:
        df["source"] = "KEA"
    return df

df = load_data()

# Uniform Data Standardization
df["course"] = df["course"].astype(str).str.upper().str.strip()
df["category"] = df["category"].astype(str).str.upper().str.strip()
df["college"] = df["college"].astype(str).str.strip()


# =====================================================
# 3. SIDEBAR CONTROLS (CASCADING FILTER MECHANISM)
# =====================================================
st.sidebar.title("🔍 FILTERS")

rank = st.sidebar.number_input("Enter Rank", min_value=1, max_value=300000, value=30000)

# Step 1: Course Specialty Choice
course_options = sorted(df["course"].dropna().unique())
course = st.sidebar.selectbox("Course Specialty", course_options)
df_course_filtered = df[df["course"] == course]

# Step 2: Counseling Type Split Route Selection
counseling_options = sorted(df_course_filtered["source"].dropna().unique())
counseling = st.sidebar.selectbox("Counseling Type", counseling_options)
df_source_filtered = df_course_filtered[df_course_filtered["source"] == counseling]

# Step 3: Local Seat Category Selection
category_options = sorted(df_source_filtered["category"].dropna().unique())
category = st.sidebar.selectbox("Seat Category", category_options)

college_search = st.sidebar.text_input("Search College Name")


# =====================================================
# 4. BRANDING LOGO HEADER (STEP OUTWARD TO ROOT CONTEXT)
# =====================================================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Steps backwards out of the extractor folder to fetch the vector resource safely
img_base64 = get_base64_image("../assets/logo.png")

if img_base64:
    st.markdown(
        f"""
        <div style="text-align: center; padding-top: 5px; margin-bottom: 25px;">
            <img src="data:image/png;base64,{img_base64}" width="220" style="display: block; margin: 0 auto; image-rendering: -webkit-optimize-contrast;">
            <h1 style="font-size: 38px; font-weight: 800; color: #0f172a; margin-top: 15px; margin-bottom: 2px; letter-spacing: -0.75px;">
                PG NEET Counseling Intelligence System
            </h1>
            <p style="font-size: 15px; color: #64748b; margin-top: 0px; font-weight: 500;">
                Namma MBBS Internal Analytics Engine
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("<div style='text-align:center; padding-top:10px;'><h1>PG NEET Counseling Intelligence System</h1></div>", unsafe_allow_html=True)

st.markdown("<hr style='margin-top:0px; margin-bottom:35px; border:0; border-top:1px solid #e2e8f0;'>", unsafe_allow_html=True)


# =====================================================
# 5. FILTER DATA & PROBABILITY ENGINE
# =====================================================
filtered = df_source_filtered[df_source_filtered["category"] == category].copy()

if college_search:
    filtered = filtered[filtered["college"].str.contains(college_search, case=False, na=False)]

def get_probability(cutoff, user_rank):
    if user_rank <= cutoff: return "🟢 HIGH"
    elif user_rank <= cutoff * 1.15: return "🟡 MODERATE"
    elif user_rank <= cutoff * 1.35: return "🟠 LOW"
    else: return "🔴 VERY LOW"

if len(filtered) > 0:
    filtered["chance"] = filtered["rank"].apply(lambda x: get_probability(x, rank))
    filtered = filtered.sort_values("rank")


# =====================================================
# 6. EXECUTIVE ANALYTICS CARD GRID VIEW OVERRIDES
# =====================================================
st.markdown("<h3 style='margin-bottom:15px;'>📊 Cutoff Insights</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

total_results = len(filtered)
lowest_cutoff = f"{int(filtered['rank'].min()):,}" if total_results > 0 else "N/A"
highest_cutoff = f"{int(filtered['rank'].max()):,}" if total_results > 0 else "N/A"

with col1:
    st.markdown(f'<div class="analytics-card"><div class="card-label">Total Match Results</div><div class="card-value">{total_results} Colleges</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="analytics-card" style="border-left-color: #10b981;"><div class="card-label">Lowest Cutoff Rank</div><div class="card-value">{lowest_cutoff}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="analytics-card" style="border-left-color: #ef4444;"><div class="card-label">Highest Cutoff Rank</div><div class="card-value">{highest_cutoff}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="analytics-card" style="border-left-color: #8b5cf6;"><div class="card-label">Counseling Authority</div><div class="card-value">{counseling}</div></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)


# =====================================================
# 7. HIGH-PERFORMANCE PREDICTIVE INTERACTIVE DATAFRAME
# =====================================================
st.markdown("<h3 style='margin-bottom:15px;'>📋 Live Prediction Matrix</h3>", unsafe_allow_html=True)

if total_results == 0:
    st.info("💡 Adjust your sidebar filters. No matching cutoff entry matches this target combination currently.")
else:
    display_df = filtered[[
        "college", "course", "category", "fees", "rank", "chance", "round"
    ]].copy()
    
    display_df.columns = [
        "College Name", "Course Specialty", "Seat Category", "Annual Fees", 
        "Cutoff Rank", "Admission Chance", "Counseling Round"
    ]

    display_df["Annual Fees"] = display_df["Annual Fees"].astype(int)
    display_df["Cutoff Rank"] = display_df["Cutoff Rank"].astype(int)

    # Use st.column_config to apply professional UI modifications to look clean 
    st.dataframe(
        display_df,
        column_config={
            "College Name": st.column_config.TextColumn("College Name", width="large"),
            "Annual Fees": st.column_config.NumberColumn("Annual Fees", format="₹%,d"),
            "Cutoff Rank": st.column_config.NumberColumn("Cutoff Rank", format="%,d"),
            "Admission Chance": st.column_config.TextColumn("Admission Chance", width="medium"),
            "Counseling Round": st.column_config.TextColumn("Counseling Round", width="small")
        },
        use_container_width=True,
        height=500,
        hide_index=True
    )
