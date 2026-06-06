import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import time

# --- Page Configuration ---
st.set_page_config(page_title="DataMedic AI", page_icon="🧪", layout="wide")

# --- Native CSS Engine (Total Button Text Visibility Fix) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Base UI Background Canvas */
.stApp {
    background: radial-gradient(circle at 20% 20%, #111827 0%, #030712 100%);
    color: #f9fafb;
}

/* Sidebar Custom Restyling */
section[data-testid="stSidebar"] {
    background-color: #0b0f19 !important;
    border-right: 1px solid #1f2937;
    min-width: 340px !important;
}

/* Sidebar Navigation Header */
.nav-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #4b5563;
    letter-spacing: 2px;
    margin-bottom: 15px;
    margin-top: 10px;
    text-transform: uppercase;
}

/* ==============================================================================
   BULLETPROOF BUTTON CSS RESTYLE
   ============================================================================== */

/* 1. Global Reset: Stop Streamlit's internal <p> tags from turning text white/invisible */
.stApp button p, 
.stApp button span, 
.stApp button div {
    color: inherit !important; 
}

/* 2. Sidebar Navigation Buttons */
div[data-testid="stSidebarContent"] div.stButton > button {
    width: 100% !important;
    height: 56px !important;
    border-radius: 14px !important;
    background-color: #111827 !important; /* Dark base */
    color: #9ca3af !important; /* Visible grey text */
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 1.05rem !important;
    text-align: left !important;
    padding-left: 20px !important;
    margin-bottom: 4px !important;
    transition: all 0.2s ease-in-out !important;
}

div[data-testid="stSidebarContent"] div.stButton > button:hover {
    background-color: #1f2937 !important;
    color: #ffffff !important;
    border-color: rgba(56, 189, 248, 0.4) !important;
}

/* Active Selected Sidebar Button */
div[data-testid="stSidebarContent"] div.stButton > button[disabled] {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.2), rgba(6, 182, 212, 0.2)) !important;
    color: #38bdf8 !important; /* Cyan text */
    border: 2px solid #38bdf8 !important;
    opacity: 1 !important;
    font-weight: 700 !important;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.15) !important;
}

/* 3. Execute Deep Cleanse (Primary Button) */
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #2563eb, #06b6d4) !important;
    color: #ffffff !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    height: 56px !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.4) !important;
}

div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(6, 182, 212, 0.5) !important;
}

/* 4. Download Export Buttons */
div[data-testid="stDownloadButton"] > button {
    background-color: #1f2937 !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(56, 189, 248, 0.4) !important;
    border-radius: 12px !important;
    height: 50px !important;
    width: 100% !important;
    font-weight: 600 !important;
    transition: all 0.2s ease-in-out !important;
}

div[data-testid="stDownloadButton"] > button:hover {
    background-color: #38bdf8 !important;
    color: #030712 !important; /* Dark text on hover */
    box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3) !important;
}

/* Emergency Purge System Action Switch (Targeting parent div wrapper class) */
.reset-btn button {
    background: linear-gradient(90deg, #dc2626, #991b1b) !important;
    color: #ffffff !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    height: 50px !important;
    border: none !important;
}

/* ============================================================================== */

/* Content Hero Display Card */
.hero {
    text-align: center;
    padding: 50px 30px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(17, 24, 39, 0.8), rgba(31, 41, 55, 0.5));
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 35px;
}

.hero h1 {
    font-size: 4rem;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(90deg, #38bdf8, #3b82f6, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #9ca3af;
    font-size: 1.2rem;
    margin-top: 10px;
}

/* Analytical KPI Cards */
[data-testid="metric-container"] {
    background: rgba(17, 24, 39, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 20px !important;
    padding: 22px !important;
}

[data-testid="stMetricLabel"] {
    color: #9ca3af !important;
    font-size: 0.95rem !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
}

/* Audit Logs Layout Component */
.timeline {
    background: rgba(31, 41, 55, 0.4);
    border-left: 4px solid #06b6d4;
    padding: 18px;
    margin: 14px 0;
    border-radius: 0 16px 16px 0;
    color: #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# --- Memory Engine Initialization (Session Core Preservation Loop) ---
if "active_page" not in st.session_state: st.session_state.active_page = "workspace"
if "logs" not in st.session_state: st.session_state.logs = []
if "raw_df" not in st.session_state: st.session_state.raw_df = None
if "cleaned_df" not in st.session_state: st.session_state.cleaned_df = None
if "stats" not in st.session_state: st.session_state.stats = {}
if "filename" not in st.session_state: st.session_state.filename = ""

def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.logs.insert(0, f"[{timestamp}] {msg}")

def clean_data(df):
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())
    df_cleaned = df.drop_duplicates().copy()
    outliers = 0
    for c in df_cleaned.select_dtypes(include=np.number).columns:
        q1 = df_cleaned[c].quantile(.25)
        q3 = df_cleaned[c].quantile(.75)
        iqr = q3 - q1
        mask = (df_cleaned[c] < (q1 - 1.5 * iqr)) | (df_cleaned[c] > (q3 + 1.5 * iqr))
        outliers += int(mask.sum())
        df_cleaned.loc[mask, c] = df_cleaned[c].median()
        df_cleaned[c] = df_cleaned[c].fillna(df_cleaned[c].mean())
    for c in df_cleaned.select_dtypes(exclude=np.number).columns:
        df_cleaned[c] = df_cleaned[c].fillna("Fixed")
    score = max(0, 100 - (missing + duplicates + outliers))
    return df_cleaned, missing, duplicates, outliers, score

# --- Sidebar UI Dashboard Components Layout ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 2.3rem; font-weight:800; color:#fff; margin-bottom:0;'>🧪 DataMedic</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #4b5563; font-size:0.9rem; margin-top:0;'>AI Dataset Diagnostics Suite</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<div class='nav-header'>Navigation Dashboard</div>", unsafe_allow_html=True)
    
    # Navigation Buttons
    if st.button("📊 DATASET WORKSPACE", key="btn_ws", disabled=(st.session_state.active_page == "workspace")):
        st.session_state.active_page = "workspace"
        st.rerun()
        
    if st.button("📈 ANALYTICAL INSIGHTS", key="btn_an", disabled=(st.session_state.active_page == "analytics")):
        st.session_state.active_page = "analytics"
        st.rerun()
        
    if st.button("📜 PIPELINE LOGS", key="btn_lg", disabled=(st.session_state.active_page == "logs")):
        st.session_state.active_page = "logs"
        st.rerun()

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Global System Flash Reset Switch
    st.markdown("<div class='reset-btn'>", unsafe_allow_html=True)
    if st.button("🗑️ RESET SYSTEM FIELDS", key="system_wipe"):
        st.session_state.raw_df = None
        st.session_state.cleaned_df = None
        st.session_state.stats = {}
        st.session_state.filename = ""
        st.session_state.logs = []
        st.session_state.active_page = "workspace"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# --- Routing Layout Execution Logic Hub ---

# TAB 1: WORKSPACE
if st.session_state.active_page == "workspace":
    st.markdown("""
    <div class="hero">
        <h1>DataMedic AI Workspace</h1>
        <p>Drop multi-format dirty operational data structures to auto-heal systemic errors instantly.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.raw_df is None:
        uploaded = st.file_uploader("Upload targeted data table config file (CSV, XLSX, JSON)", type=["csv","xlsx","xls","json"])
        if uploaded:
            ext = uploaded.name.split(".")[-1].lower()
            if ext == "csv": st.session_state.raw_df = pd.read_csv(uploaded)
            elif ext == "json": st.session_state.raw_df = pd.read_json(uploaded)
            else: st.session_state.raw_df = pd.read_excel(uploaded)
            
            st.session_state.filename = uploaded.name
            log(f"Injected raw matrix tracking data structure: {uploaded.name}")
            st.rerun()

    if st.session_state.raw_df is not None:
        st.markdown(f"#### 📁 Active Asset Tracking Ledger: `{st.session_state.filename}`")
        df = st.session_state.raw_df

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Structural Rows", len(df))
        c2.metric("Matrix Features/Cols", len(df.columns))
        c3.metric("Raw Missing Cells", int(df.isna().sum().sum()))
        c4.metric("Identified Duplicates", int(df.duplicated().sum()))

        st.markdown("<br>", unsafe_allow_html=True)
        
        # NOTE: Added type="primary" so our CSS targets it perfectly
        if st.button("🚀 EXECUTE AI DEEP CLEANSE", key="run_cleanse", type="primary"):
            p = st.progress(0)
            for i in range(100):
                p.progress(i + 1)
                time.sleep(0.003)
                
            cleaned, missing, duplicates, outliers, score = clean_data(df)
            st.session_state.cleaned_df = cleaned
            st.session_state.stats = {
                "missing": missing, "outliers": outliers, 
                "duplicates": duplicates, "score": score
            }
            log(f"Successfully processed and cleansed matrix mapping logic for {st.session_state.filename}")
            st.rerun()

        if st.session_state.cleaned_df is not None:
            st.markdown("---")
            st.subheader("📋 Clean Data Table Preview (First 20 Entries)")
            st.dataframe(st.session_state.cleaned_df.head(20), use_container_width=True)

            st.markdown("### 📥 Dispatch Export Control Hub")
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                st.session_state.cleaned_df.to_excel(writer, index=False)
            
            d1, d2 = st.columns(2)
            with d1:
                st.download_button("Download Cleaned Excel Structure", excel_buffer.getvalue(), "cleaned_dataset.xlsx")
            with d2:
                st.download_button("Download Cleaned CSV Structure", st.session_state.cleaned_df.to_csv(index=False).encode(), "cleaned_dataset.csv")

# TAB 2: ANALYTICAL INSIGHTS
elif st.session_state.active_page == "analytics":
    st.markdown("## 📈 Analytics & Health Interface")
    
    if st.session_state.cleaned_df is not None:
        stats = st.session_state.stats
        cleaned_df = st.session_state.cleaned_df

        a, b, c, d = st.columns(4)
        a.metric("Fixed Missing Values", stats["missing"])
        b.metric("Adjusted Outliers", stats["outliers"])
        c.metric("Dropped Duplicates", stats["duplicates"])
        d.metric("Final Integrity Score", f"{stats['score']}%")

        g1, g2 = st.columns([1, 1])
        with g1:
            fig = go.Figure(data=[go.Pie(
                labels=['Healthy Data', 'Anomalies Patched'],
                values=[stats["score"], max(0, 100 - stats["score"])],
                hole=.75,
                marker=dict(colors=['#06b6d4', '#2563eb'])
            )])
            fig.update_layout(
                title="Overall Table Quality Score",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff', family='Poppins'),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

        with g2:
            metrics_df = pd.DataFrame({
                "Anomalies Solved": ["Missing Cells", "Outlier Triggers", "Duplicate Clusters"],
                "Count": [stats["missing"], stats["outliers"], stats["duplicates"]]
            })
            bar = px.bar(metrics_df, x="Anomalies Solved", y="Count", color="Anomalies Solved",
                         color_discrete_sequence=["#38bdf8", "#3b82f6", "#a855f7"])
            bar.update_layout(
                title="Repaired Data Anomalies",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff', family='Poppins'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(bar, use_container_width=True)

        num = cleaned_df.select_dtypes(include=np.number)
        if len(num.columns) > 1:
            st.markdown("### 📊 Clean Structural Feature Matrix Correlation Map")
            heat = px.imshow(num.corr(), text_auto=".2f", color_continuous_scale="Blugrn")
            heat.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff', family='Poppins')
            )
            st.plotly_chart(heat, use_container_width=True)
    else:
        st.warning("⚠️ No operational dataset metadata currently residing in engine memory. Head to Workspace to upload a file first.")

# TAB 3: OPERATION PIPELINE RECORDS LOG
elif st.session_state.active_page == "logs":
    st.markdown("## 📜 Active Internal Pipeline Execution Ledger")
    st.write("Auditable transactional logs detailing system interactions within your active deployment session.")
    
    if st.session_state.logs:
        for item in st.session_state.logs[:40]:
            st.markdown(f"<div class='timeline'>{item}</div>", unsafe_allow_html=True)
    else:
        st.info("System Engine logs are completely empty. Initialize procedures to view automated activity records.")