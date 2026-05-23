import base64
import pandas as pd
import streamlit as st

# =====================================================
# 1. PAGE CONFIG & THEME SETUP
# =====================================================
st.set_page_config(
    page_title="Namma MBBS Intelligence System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium UI CSS Injection
st.markdown("""
    <style>
        .stApp {
            background-color: #f8fafc;
        }
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            padding-top: 2rem;
        }
        [data-testid="stSidebar"] .stMarkdown h2 {
            color: #f8fafc !important;
            font-size: 1.5rem;
            letter-spacing: 1px;
            border-bottom: 2px solid #334155;
            padding-bottom: 10px;
        }
        [data-testid="stSidebar"] label {
            color: #cbd5e1 !important;
            font-weight: 600 !important;
        }
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            padding: 1.25rem 1.5rem !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border-left: 5px solid #1e40af;
            transition: transform 0.2s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        }
        div[data-testid="stMetric"] label {
            color: #64748b !important;
            font-size: 0.85rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #0f172a !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }
        h2, h3 {
            color: #1e3a8a !important;
            font-weight: 700 !important;
            margin-top: 1.5rem !important;
        }
    </style>
""", unsafe_allow_html=True)


# =====================================================
# 2. DATA LOADING ENGINE
# =====================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("extractor/final_cleaned.csv")
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

    # Standardize column headers to clean lowercase
    df.columns = df.columns.astype(str).str.strip().str.lower()

    # Dynamic Parsing for Counseling Body
    if "source_file" in df.columns:
        df["source"] = df["source_file"].astype(str).str.upper()
        df["source"] = df["source"].apply(
            lambda x: "MCC" if ("MCC" in x or "AIQ" in x or "ALL INDIA" in x) else "KEA"
        )
    else:
        df["source"] = "KEA"
    return df

df = load_data()

# Data Normalization
df["course"] = df["course"].astype(str).str.upper().str.strip()
df["category"] = df["category"].astype(str).str.upper().str.strip()
df["college"] = df["college"].astype(str).str.strip()


# =====================================================
# 3. SIDEBAR CONTROLS (STRICTLY CASCADING PIPELINE)
# =====================================================
st.sidebar.title("🔍 FILTERS")

rank = st.sidebar.number_input("Enter Rank", min_value=1, max_value=300000, value=30000)

# Step 1: Filter by Course Specialty
course_options = sorted(df["course"].dropna().unique())
course = st.sidebar.selectbox("Course Specialty", course_options)
df_course_filtered = df[df["course"] == course]

# Step 2: Filter by Counseling Type (Isolates KEA / MCC cleanly)
counseling_options = sorted(df_course_filtered["source"].dropna().unique())
counseling = st.sidebar.selectbox("Counseling Type", counseling_options)
df_source_filtered = df_course_filtered[df_course_filtered["source"] == counseling]

# Step 3: Filter by Seat Category (Populates categories ONLY belonging to selected counseling type)
category_options = sorted(df_source_filtered["category"].dropna().unique())
category = st.sidebar.selectbox("Seat Category", category_options)

college_search = st.sidebar.text_input("Search College Name")


# =====================================================
# 4. BRANDING LOGO HEADER
# =====================================================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

img_base64 = get_base64_image("assets/logo.png")

if img_base64:
    st.markdown(
        f"""
        <div style="text-align: center; padding-top: 15px; margin-bottom: 25px;">
            <img src="data:image/png;base64,{img_base64}" width="250" style="display: block; margin: 0 auto; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;">
            <h1 style="font-size: 42px; font-weight: 800; color: #0f172a; margin-top: 20px; margin-bottom: 4px; letter-spacing: -0.5px;">
                PG NEET Counseling Intelligence System
            </h1>
            <p style="font-size: 16px; color: #64748b; margin-top: 0px; font-weight: 500;">
                Namma MBBS Internal Intelligence Platform
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("<div style='text-align:center; padding-top:20px;'><h1>PG NEET Counseling Intelligence System</h1></div>", unsafe_allow_html=True)

st.markdown("<hr style='margin-top:0px; margin-bottom:30px; border:0; border-top:1px solid #e2e8f0;'>", unsafe_allow_html=True)


# =====================================================
# 5. FILTER DATA & PROBABILITY ENGINE
# =====================================================
# Safely capture the final localized subset matrix layer
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
# 6. ANALYTICS CARDS
# =====================================================
st.subheader("📊 Prediction Analytics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Results", f"{len(filtered)} Colleges")

with col2:
    lowest = int(filtered["rank"].min()) if len(filtered) > 0 else 0
    st.metric("Lowest Cutoff", f"{lowest:,}" if lowest else "N/A")

with col3:
    highest = int(filtered["rank"].max()) if len(filtered) > 0 else 0
    st.metric("Highest Cutoff", f"{highest:,}" if highest else "N/A")

with col4:
    st.metric("Counseling Body", counseling)

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# 7. RESULTS TABLE
# =====================================================
st.subheader("📋 Prediction Results")

if len(filtered) == 0:
    st.info("💡 Adjust your sidebar filters. No matching cutoff entry matches this target combination currently.")
else:
    display_df = filtered[[
        "college", "course", "category", "fees", "rank", "chance", "round"
    ]].copy()
    
    display_df.columns = [
        "College Name", "Course Specialty", "Seat Category", "Annual Fees", 
        "Cutoff Rank", "Admission Chance", "Counseling Round"
    ]

    # Convert values cleanly to flat integers to prevent decimal trail issues
    display_df["Annual Fees"] = display_df["Annual Fees"].astype(int)
    display_df["Cutoff Rank"] = display_df["Cutoff Rank"].astype(int)

    st.dataframe(
        display_df.style.format({
            "Annual Fees": "₹{:,}", 
            "Cutoff Rank": "{:,}"
        }),
        use_container_width=True,
        height=550,
        hide_index=True
    )
