# =====================================
# HEALTHCARE ANALYTICS DASHBOARD
# Main Page - Overview & KPI
# =====================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =====================================
# KONFIGURASI HALAMAN
# =====================================

st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CUSTOM CSS - PREMIUM DARK DESIGN
# =====================================

st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1224 50%, #0a0e1a 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1224 0%, #111827 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: #94a3b8;
    }

    /* Main content */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(99,102,241,0.1) 0%, rgba(168,85,247,0.05) 100%);
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: rgba(99,102,241,0.6);
        box-shadow: 0 0 20px rgba(99,102,241,0.2);
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    /* Headers */
    h1 {
        color: #f1f5f9 !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
    }
    h2, h3 {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }

    /* Divider */
    hr {
        border-color: rgba(99,102,241,0.2) !important;
        margin: 1.5rem 0 !important;
    }

    /* Plotly chart container */
    .stPlotlyChart {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(99,102,241,0.15);
        transition: box-shadow 0.3s ease;
    }
    .stPlotlyChart:hover {
        box-shadow: 0 0 25px rgba(99,102,241,0.15);
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Badge / info box */
    .info-badge {
        background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.1));
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        color: #c4b5fd;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* Page header card */
    .page-header {
        background: linear-gradient(135deg, rgba(99,102,241,0.2) 0%, rgba(168,85,247,0.15) 50%, rgba(59,130,246,0.1) 100%);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
    }
    .page-header h1 {
        margin: 0 !important;
        padding: 0 !important;
        background: linear-gradient(135deg, #818cf8, #c084fc, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem !important;
    }
    .page-header p {
        color: #94a3b8;
        margin-top: 0.5rem;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_data():
    df = pd.read_csv("healthcare_dataset.csv")
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
    df["Discharge Date"] = pd.to_datetime(df["Discharge Date"])
    df["Length of Stay"] = (df["Discharge Date"] - df["Date of Admission"]).dt.days
    return df

df = load_data()


# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <span style='font-size: 3rem;'>🏥</span>
        <h2 style='color:#818cf8; margin:0.5rem 0 0; font-size:1.1rem;'>Healthcare Analytics</h2>
        <p style='color:#64748b; font-size:0.8rem; margin:0;'>Data Mining Dashboard</p>
    </div>
    <hr style='border-color:rgba(99,102,241,0.2); margin:1rem 0;'>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='color:#64748b; font-size:0.75rem; font-weight:600; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.5rem;'>Navigasi</p>
    """, unsafe_allow_html=True)

    st.page_link("app.py", label="🏠 Dashboard Utama", )
    st.page_link("pages/1_Regresi.py", label="📈 Regresi - Prediksi Billing")
    st.page_link("pages/2_Klasifikasi.py", label="🔬 Klasifikasi - Hasil Tes")
    st.page_link("pages/3_Clustering.py", label="🔵 Clustering - Segmentasi Pasien")

    st.markdown("<hr style='border-color:rgba(99,102,241,0.2);'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='color:#475569; font-size:0.75rem; text-align:center;'>
        <p>Total Record: <strong style='color:#818cf8;'>{len(df):,}</strong></p>
        <p>Fitur: <strong style='color:#818cf8;'>15 Kolom</strong></p>
    </div>
    """, unsafe_allow_html=True)


# =====================================
# HEADER
# =====================================

st.markdown("""
<div class='page-header'>
    <h1>🏥 Healthcare Analytics Dashboard</h1>
    <p>Sistem analitik data pasien rumah sakit berbasis <strong>Data Mining</strong> untuk mendukung pengambilan keputusan</p>
</div>
""", unsafe_allow_html=True)


# =====================================
# KPI METRICS
# =====================================

total_pasien = len(df)
rata_umur = round(df["Age"].mean(), 1)
total_dokter = df["Doctor"].nunique()
total_rs = df["Hospital"].nunique()
rata_billing = f"${df['Billing Amount'].mean():,.0f}"
avg_los = round(df["Length of Stay"].mean(), 1)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("👨‍⚕️ Total Pasien", f"{total_pasien:,}")
with col2:
    st.metric("🎂 Rata-rata Umur", f"{rata_umur} th")
with col3:
    st.metric("🩺 Jumlah Dokter", f"{total_dokter:,}")
with col4:
    st.metric("🏥 Jumlah RS", f"{total_rs:,}")
with col5:
    st.metric("💰 Avg Billing", rata_billing)
with col6:
    st.metric("📅 Avg LoS", f"{avg_los} hari")

st.divider()


# =====================================
# CHART ROW 1
# =====================================

col1, col2, col3 = st.columns(3)

with col1:
    gender = df["Gender"].value_counts().reset_index()
    gender.columns = ["Gender", "Jumlah"]
    fig_gender = px.pie(
        gender, names="Gender", values="Jumlah",
        title="Distribusi Gender",
        color_discrete_sequence=["#818cf8", "#c084fc"],
        hole=0.45
    )
    fig_gender.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=15),
        legend=dict(font=dict(color="#94a3b8")),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_gender, use_container_width=True)

with col2:
    blood = df["Blood Type"].value_counts().reset_index()
    blood.columns = ["Blood Type", "Jumlah"]
    fig_blood = px.bar(
        blood, x="Blood Type", y="Jumlah",
        title="Distribusi Golongan Darah",
        color="Jumlah",
        color_continuous_scale=["#312e81", "#818cf8", "#c084fc"]
    )
    fig_blood.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=15),
        coloraxis_showscale=False,
        margin=dict(t=45, b=10, l=10, r=10),
        xaxis=dict(gridcolor="rgba(99,102,241,0.1)"),
        yaxis=dict(gridcolor="rgba(99,102,241,0.1)")
    )
    st.plotly_chart(fig_blood, use_container_width=True)

with col3:
    test = df["Test Results"].value_counts().reset_index()
    test.columns = ["Test Results", "Jumlah"]
    color_map = {"Normal": "#4ade80", "Abnormal": "#f87171", "Inconclusive": "#fb923c"}
    fig_test = px.pie(
        test, names="Test Results", values="Jumlah",
        title="Distribusi Hasil Tes",
        color="Test Results",
        color_discrete_map=color_map,
        hole=0.45
    )
    fig_test.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=15),
        legend=dict(font=dict(color="#94a3b8")),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_test, use_container_width=True)

st.divider()


# =====================================
# CHART ROW 2
# =====================================

col1, col2 = st.columns(2)

with col1:
    condition = df["Medical Condition"].value_counts().reset_index()
    condition.columns = ["Medical Condition", "Jumlah"]
    fig_cond = px.bar(
        condition, x="Jumlah", y="Medical Condition",
        orientation='h',
        title="Distribusi Kondisi Medis",
        color="Jumlah",
        color_continuous_scale=["#312e81", "#818cf8", "#c084fc"]
    )
    fig_cond.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=15),
        coloraxis_showscale=False,
        margin=dict(t=45, b=10, l=10, r=10),
        xaxis=dict(gridcolor="rgba(99,102,241,0.1)"),
        yaxis=dict(gridcolor="rgba(99,102,241,0.1)")
    )
    st.plotly_chart(fig_cond, use_container_width=True)

with col2:
    admission = df["Admission Type"].value_counts().reset_index()
    admission.columns = ["Admission Type", "Jumlah"]
    fig_adm = px.pie(
        admission, names="Admission Type", values="Jumlah",
        title="Tipe Rawat Inap",
        color_discrete_sequence=["#818cf8", "#c084fc", "#60a5fa"],
        hole=0.45
    )
    fig_adm.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=15),
        legend=dict(font=dict(color="#94a3b8")),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_adm, use_container_width=True)

st.divider()


# =====================================
# BILLING DISTRIBUTION
# =====================================

fig_billing = px.histogram(
    df, x="Billing Amount",
    nbins=50,
    title="Distribusi Billing Amount Pasien",
    color_discrete_sequence=["#818cf8"]
)
fig_billing.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8"),
    title_font=dict(color="#e2e8f0", size=15),
    margin=dict(t=45, b=10, l=10, r=10),
    xaxis=dict(gridcolor="rgba(99,102,241,0.1)", title="Billing Amount ($)"),
    yaxis=dict(gridcolor="rgba(99,102,241,0.1)", title="Frekuensi")
)
st.plotly_chart(fig_billing, use_container_width=True)

st.divider()


# =====================================
# RINGKASAN DATA MINING
# =====================================

st.subheader("🤖 Rancangan Data Mining")
st.markdown("""
<div class='info-badge'>
    Dashboard ini menerapkan <strong>3 teknik data mining</strong> untuk mendukung pengambilan keputusan di bidang healthcare.
    Navigasi ke halaman berikut untuk melihat detail setiap rancangan:
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(59,130,246,0.15),rgba(99,102,241,0.1));
                border:1px solid rgba(59,130,246,0.3); border-radius:16px; padding:1.5rem; height:100%;'>
        <div style='font-size:2rem; margin-bottom:0.5rem;'>📈</div>
        <h3 style='color:#60a5fa; margin:0 0 0.5rem; font-size:1.1rem;'>Rancangan 1: Regresi</h3>
        <p style='color:#94a3b8; font-size:0.85rem; margin:0;'>
            <strong style='color:#e2e8f0;'>Algoritma:</strong> Linear Regression<br>
            <strong style='color:#e2e8f0;'>Target:</strong> Prediksi Billing Amount<br>
            <strong style='color:#e2e8f0;'>Fungsi:</strong> Estimasi biaya perawatan pasien untuk manajemen keuangan RS
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(168,85,247,0.15),rgba(99,102,241,0.1));
                border:1px solid rgba(168,85,247,0.3); border-radius:16px; padding:1.5rem; height:100%;'>
        <div style='font-size:2rem; margin-bottom:0.5rem;'>🔬</div>
        <h3 style='color:#c084fc; margin:0 0 0.5rem; font-size:1.1rem;'>Rancangan 2: Klasifikasi</h3>
        <p style='color:#94a3b8; font-size:0.85rem; margin:0;'>
            <strong style='color:#e2e8f0;'>Algoritma:</strong> Decision Tree<br>
            <strong style='color:#e2e8f0;'>Target:</strong> Prediksi Hasil Tes<br>
            <strong style='color:#e2e8f0;'>Fungsi:</strong> Identifikasi pasien berisiko hasil tes abnormal
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(74,222,128,0.1),rgba(99,102,241,0.1));
                border:1px solid rgba(74,222,128,0.25); border-radius:16px; padding:1.5rem; height:100%;'>
        <div style='font-size:2rem; margin-bottom:0.5rem;'>🔵</div>
        <h3 style='color:#4ade80; margin:0 0 0.5rem; font-size:1.1rem;'>Rancangan 3: Clustering</h3>
        <p style='color:#94a3b8; font-size:0.85rem; margin:0;'>
            <strong style='color:#e2e8f0;'>Algoritma:</strong> K-Means Clustering<br>
            <strong style='color:#e2e8f0;'>Target:</strong> Segmentasi Pasien<br>
            <strong style='color:#e2e8f0;'>Fungsi:</strong> Pengelompokan pasien untuk optimasi layanan
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.divider()


# =====================================
# DATASET TABLE
# =====================================

st.subheader("📄 Dataset Healthcare")
st.markdown(f"<p style='color:#64748b; font-size:0.85rem;'>Menampilkan {len(df):,} baris × 15 kolom</p>", unsafe_allow_html=True)

st.dataframe(
    df,
    use_container_width=True,
    height=400
)