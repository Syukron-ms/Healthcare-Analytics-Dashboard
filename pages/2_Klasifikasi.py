# =====================================
# RANCANGAN 2: KLASIFIKASI
# Prediksi Hasil Tes Pasien
# Algoritma: Decision Tree Classifier
# =====================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (accuracy_score, classification_report,
                              confusion_matrix, ConfusionMatrixDisplay)

st.set_page_config(
    page_title="Klasifikasi - Healthcare Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0a0e1a 0%, #0d1224 50%, #0a0e1a 100%); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1224 0%, #111827 100%);
        border-right: 1px solid rgba(168,85,247,0.2);
    }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(168,85,247,0.1), rgba(99,102,241,0.05));
        border: 1px solid rgba(168,85,247,0.25);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: rgba(168,85,247,0.6);
        box-shadow: 0 0 20px rgba(168,85,247,0.2);
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] { font-weight: 600; color: #94a3b8 !important; font-size: 0.85rem !important; }
    [data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 1.8rem !important; font-weight: 700 !important; }
    h1 { color: #f1f5f9 !important; font-weight: 800 !important; }
    h2, h3 { color: #e2e8f0 !important; font-weight: 700 !important; }
    hr { border-color: rgba(168,85,247,0.2) !important; margin: 1.5rem 0 !important; }
    .stPlotlyChart { border-radius: 16px; overflow: hidden; border: 1px solid rgba(168,85,247,0.15); }
    .rancangan-box {
        background: linear-gradient(135deg, rgba(168,85,247,0.12), rgba(99,102,241,0.08));
        border: 1px solid rgba(168,85,247,0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        color: #cbd5e1;
        line-height: 1.7;
    }
    .rancangan-box h4 {
        color: #c084fc !important;
        margin: 0 0 0.75rem;
        font-size: 1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .page-header {
        background: linear-gradient(135deg, rgba(168,85,247,0.2), rgba(99,102,241,0.15), rgba(192,132,252,0.1));
        border: 1px solid rgba(168,85,247,0.35);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
    }
    .page-header h1 {
        margin: 0 !important; padding: 0 !important;
        background: linear-gradient(135deg, #c084fc, #818cf8, #e879f9);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; font-size: 2rem !important;
    }
    .page-header p { color: #94a3b8; margin-top: 0.5rem; font-size: 0.95rem; }
    .predict-result {
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 1rem;
    }
    .normal-result { background: rgba(74,222,128,0.15); border: 2px solid rgba(74,222,128,0.5); color: #4ade80; }
    .abnormal-result { background: rgba(248,113,113,0.15); border: 2px solid rgba(248,113,113,0.5); color: #f87171; }
    .inconclusive-result { background: rgba(251,146,60,0.15); border: 2px solid rgba(251,146,60,0.5); color: #fb923c; }
</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <span style='font-size: 3rem;'>🏥</span>
        <h2 style='color:#c084fc; margin:0.5rem 0 0; font-size:1.1rem;'>Healthcare Analytics</h2>
        <p style='color:#64748b; font-size:0.8rem; margin:0;'>Data Mining Dashboard</p>
    </div>
    <hr style='border-color:rgba(168,85,247,0.2); margin:1rem 0;'>
    """, unsafe_allow_html=True)
    st.page_link("app.py", label="🏠 Dashboard Utama")
    st.page_link("pages/1_Regresi.py", label="📈 Regresi - Prediksi Billing")
    st.page_link("pages/2_Klasifikasi.py", label="🔬 Klasifikasi - Hasil Tes")
    st.page_link("pages/3_Clustering.py", label="🔵 Clustering - Segmentasi Pasien")


# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_data():
    return pd.read_csv("healthcare_dataset.csv")

df = load_data()

# =====================================
# HEADER
# =====================================

st.markdown("""
<div class='page-header'>
    <h1>🔬 Rancangan 2: Klasifikasi</h1>
    <p>Memprediksi <strong>hasil tes pasien</strong> apakah Normal, Abnormal, atau Tidak Meyakinkan — menggunakan metode <strong>Decision Tree (Pohon Keputusan)</strong></p>
</div>
""", unsafe_allow_html=True)

# =====================================
# PENJELASAN RANCANGAN
# =====================================

st.subheader("📋 Penjelasan Rancangan Data Mining — Klasifikasi")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='rancangan-box'>
        <h4>🌳 Algoritma yang Diterapkan</h4>
        <p><strong style='color:#d8b4fe;'>Decision Tree (Pohon Keputusan)</strong> adalah metode yang cara kerjanya
        mirip seperti alur pertanyaan bercabang — seperti ketika dokter mendiagnosis penyakit dengan
        mengajukan pertanyaan satu per satu hingga sampai pada kesimpulan.</p>
        <p>Contohnya: <em>"Apakah pasien berumur di atas 60?" → Ya → "Apakah penyakitnya kanker?" → Ya → "Kemungkinan hasil tes: Abnormal"</em>.</p>
        <p style='margin:0;'>Komputer membuat ribuan pertanyaan seperti itu secara otomatis dari data pasien
        yang sudah ada, lalu menyusunnya menjadi sebuah <strong>pohon keputusan</strong> yang bisa dipakai untuk menebak pasien baru.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='rancangan-box'>
        <h4>📊 Data / Kolom yang Digunakan</h4>
        <p style='color:#64748b; font-size:0.82rem; margin-bottom:0.5rem;'>Data yang dipakai komputer untuk belajar memprediksi:</p>
        <ul style='margin:0; padding-left:1.2rem;'>
            <li><strong style='color:#d8b4fe;'>Data masukan (bahan prediksi):</strong>
                <ul>
                    <li><b>Age</b> — Umur pasien</li>
                    <li><b>Gender</b> — Jenis kelamin</li>
                    <li><b>Blood Type</b> — Golongan darah</li>
                    <li><b>Medical Condition</b> — Jenis penyakit yang diderita</li>
                    <li><b>Admission Type</b> — Jenis rawat inap (darurat/elektif/mendesak)</li>
                    <li><b>Medication</b> — Obat yang diberikan kepada pasien</li>
                    <li><b>Billing Amount</b> — Total tagihan biaya perawatan</li>
                </ul>
            </li>
            <li style='margin-top:0.5rem;'><strong style='color:#d8b4fe;'>Data yang diprediksi:</strong> Hasil Tes — Normal, Abnormal, atau Tidak Meyakinkan</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class='rancangan-box'>
        <h4>⚙️ Cara Kerja</h4>
        <ol style='margin:0; padding-left:1.2rem;'>
            <li><strong>Persiapan Data:</strong> Kolom yang berisi teks seperti nama penyakit dan nama obat diubah menjadi angka agar bisa diproses komputer</li>
            <li><strong>Bagi Data:</strong> Data dibagi dua — 80% untuk belajar, 20% untuk diuji. Pembagian dilakukan secara merata agar setiap jenis hasil tes terwakili</li>
            <li><strong>Proses Belajar:</strong> Komputer membuat pohon keputusan — ia mencari pertanyaan-pertanyaan terbaik dari data pasien yang bisa memisahkan hasil tes Normal, Abnormal, dan Tidak Meyakinkan</li>
            <li><strong>Prediksi:</strong> Ketika ada data pasien baru, komputer menelusurinya lewat pohon keputusan sampai menemukan jawaban (Normal/Abnormal/Tidak Meyakinkan)</li>
            <li><strong>Ukur Akurasi:</strong> Dihitung seberapa sering prediksi benar — menggunakan nilai Akurasi, Precision, Recall, dan Confusion Matrix</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='rancangan-box'>
        <h4>🎯 Fungsi dalam Pengambilan Keputusan</h4>
        <p>Dengan bisa memprediksi <em>hasil tes pasien lebih awal</em>, rumah sakit bisa:</p>
        <ul style='margin:0; padding-left:1.2rem;'>
            <li><strong style='color:#d8b4fe;'>Utamakan pasien yang paling butuh pertolongan:</strong> Pasien yang diprediksi hasilnya Abnormal bisa langsung ditangani lebih cepat, tanpa harus menunggu hasil lab selesai</li>
            <li><strong style='color:#d8b4fe;'>Atur jumlah dokter spesialis:</strong> Jika diprediksi banyak pasien dengan hasil Abnormal, rumah sakit bisa menyiapkan tenaga dokter yang cukup sejak awal</li>
            <li><strong style='color:#d8b4fe;'>Sistem peringatan dini:</strong> Pasien yang berisiko tinggi bisa segera dirujuk ke perawatan intensif sebelum kondisinya memburuk</li>
            <li><strong style='color:#d8b4fe;'>Kurangi waktu tunggu:</strong> Dengan tahu siapa yang lebih mendesak, antrian pasien bisa diatur lebih efisien dan tidak membuang waktu</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================
# PREPROCESSING & MODEL
# =====================================

st.subheader("🤖 Hasil Eksekusi Model — Decision Tree")

df_cls = df.copy()
le_dict = {}

cat_cols = ["Gender", "Blood Type", "Medical Condition", "Admission Type", "Medication"]
for col in cat_cols:
    le = LabelEncoder()
    df_cls[col] = le.fit_transform(df_cls[col])
    le_dict[col] = le

le_target = LabelEncoder()
df_cls["Test Results"] = le_target.fit_transform(df_cls["Test Results"])

features = ["Age", "Gender", "Blood Type", "Medical Condition", "Admission Type", "Medication", "Billing Amount"]
target = "Test Results"

X = df_cls[features]
y = df_cls[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model_dt = DecisionTreeClassifier(max_depth=8, random_state=42, min_samples_split=20)
model_dt.fit(X_train, y_train)
y_pred = model_dt.predict(X_test)

acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=le_target.classes_, output_dict=True)
cm = confusion_matrix(y_test, y_pred)

# =====================================
# METRICS
# =====================================

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("✅ Accuracy", f"{acc:.2%}")
with col2:
    macro_f1 = report["macro avg"]["f1-score"]
    st.metric("📊 Macro F1-Score", f"{macro_f1:.4f}")
with col3:
    st.metric("🏋️ Data Training", f"{len(X_train):,} baris")
with col4:
    st.metric("🧪 Data Testing", f"{len(X_test):,} baris")

st.divider()

# =====================================
# VISUALISASI
# =====================================

col1, col2 = st.columns(2)

with col1:
    # Confusion Matrix
    labels = le_target.classes_
    fig_cm = go.Figure(data=go.Heatmap(
        z=cm,
        x=labels,
        y=labels,
        colorscale=[[0, "#0d1224"], [0.5, "#4c1d95"], [1, "#c084fc"]],
        text=cm,
        texttemplate="%{text}",
        textfont=dict(color="white", size=16),
        showscale=True
    ))
    fig_cm.update_layout(
        title="Confusion Matrix",
        xaxis_title="Prediksi",
        yaxis_title="Aktual",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=14),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_cm, use_container_width=True)

with col2:
    # Classification Report Bar
    classes = [c for c in le_target.classes_]
    precision = [report[c]["precision"] for c in classes]
    recall = [report[c]["recall"] for c in classes]
    f1 = [report[c]["f1-score"] for c in classes]

    fig_report = go.Figure()
    x = classes
    fig_report.add_trace(go.Bar(name='Precision', x=x, y=precision, marker_color='#818cf8'))
    fig_report.add_trace(go.Bar(name='Recall', x=x, y=recall, marker_color='#c084fc'))
    fig_report.add_trace(go.Bar(name='F1-Score', x=x, y=f1, marker_color='#e879f9'))
    fig_report.update_layout(
        barmode='group',
        title="Precision, Recall, dan F1-Score per Kelas",
        yaxis_title="Score",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=14),
        legend=dict(font=dict(color="#94a3b8")),
        xaxis=dict(gridcolor="rgba(168,85,247,0.1)"),
        yaxis=dict(gridcolor="rgba(168,85,247,0.1)", range=[0, 1]),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_report, use_container_width=True)


# =====================================
# FEATURE IMPORTANCE
# =====================================

importance_df = pd.DataFrame({
    "Fitur": features,
    "Importance": model_dt.feature_importances_
}).sort_values("Importance", ascending=True)

fig_imp = go.Figure(go.Bar(
    x=importance_df["Importance"],
    y=importance_df["Fitur"],
    orientation='h',
    marker=dict(
        color=importance_df["Importance"],
        colorscale=[[0, "#4c1d95"], [0.5, "#818cf8"], [1, "#c084fc"]],
        showscale=False
    ),
    text=[f"{v:.4f}" for v in importance_df["Importance"]],
    textposition='outside',
    textfont=dict(color="#94a3b8")
))
fig_imp.update_layout(
    title="Feature Importance — Pengaruh Fitur terhadap Prediksi Hasil Tes",
    xaxis_title="Importance Score",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8"),
    title_font=dict(color="#e2e8f0", size=14),
    xaxis=dict(gridcolor="rgba(168,85,247,0.1)"),
    yaxis=dict(gridcolor="rgba(168,85,247,0.1)"),
    margin=dict(t=45, b=10, l=120, r=80),
    height=350
)
st.plotly_chart(fig_imp, use_container_width=True)

st.divider()


# =====================================
# PREDIKSI INTERAKTIF
# =====================================

st.subheader("🔮 Coba Prediksi Hasil Tes Pasien")
st.markdown("<p style='color:#64748b; font-size:0.85rem;'>Masukkan data pasien untuk memprediksi hasil tes laboratorium</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    inp_age = st.slider("Umur Pasien", 1, 90, 50, key="cls_age")
    inp_gender = st.selectbox("Gender", df["Gender"].unique(), key="cls_gender")
    inp_blood = st.selectbox("Golongan Darah", df["Blood Type"].unique(), key="cls_blood")
with col2:
    inp_condition = st.selectbox("Kondisi Medis", df["Medical Condition"].unique(), key="cls_cond")
    inp_admission = st.selectbox("Tipe Rawat Inap", df["Admission Type"].unique(), key="cls_adm")
with col3:
    inp_medication = st.selectbox("Obat / Medication", df["Medication"].unique(), key="cls_med")
    inp_billing = st.number_input("Billing Amount ($)", min_value=1000.0, max_value=100000.0, value=25000.0, step=500.0)

if st.button("🔬 Prediksi Hasil Tes", type="primary", use_container_width=True):
    # Encode input
    input_row = {
        "Age": inp_age,
        "Gender": le_dict["Gender"].transform([inp_gender])[0],
        "Blood Type": le_dict["Blood Type"].transform([inp_blood])[0],
        "Medical Condition": le_dict["Medical Condition"].transform([inp_condition])[0],
        "Admission Type": le_dict["Admission Type"].transform([inp_admission])[0],
        "Medication": le_dict["Medication"].transform([inp_medication])[0],
        "Billing Amount": inp_billing
    }
    inp_df = pd.DataFrame([input_row])
    pred_class_idx = model_dt.predict(inp_df)[0]
    pred_class = le_target.inverse_transform([pred_class_idx])[0]
    pred_proba = model_dt.predict_proba(inp_df)[0]

    result_class = "normal-result" if pred_class == "Normal" else ("abnormal-result" if pred_class == "Abnormal" else "inconclusive-result")
    icon = "✅" if pred_class == "Normal" else ("🚨" if pred_class == "Abnormal" else "⚠️")

    st.markdown(f"""
    <div class='predict-result {result_class}'>
        {icon} Prediksi Hasil Tes: <strong>{pred_class}</strong>
    </div>
    """, unsafe_allow_html=True)

    # Probability bar
    proba_df = pd.DataFrame({
        "Kelas": le_target.classes_,
        "Probabilitas": pred_proba
    })
    fig_proba = px.bar(
        proba_df, x="Kelas", y="Probabilitas",
        color="Kelas",
        color_discrete_map={"Normal": "#4ade80", "Abnormal": "#f87171", "Inconclusive": "#fb923c"},
        title="Probabilitas Prediksi per Kelas",
        text=[f"{p:.2%}" for p in pred_proba]
    )
    fig_proba.update_traces(textposition='outside')
    fig_proba.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0"),
        showlegend=False,
        yaxis=dict(gridcolor="rgba(168,85,247,0.1)", range=[0, 1]),
        xaxis=dict(gridcolor="rgba(168,85,247,0.1)"),
        margin=dict(t=45, b=10, l=10, r=10),
        height=300
    )
    st.plotly_chart(fig_proba, use_container_width=True)
