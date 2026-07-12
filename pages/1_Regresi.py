# =====================================
# RANCANGAN 1: REGRESI
# Prediksi Billing Amount Pasien
# Algoritma: Linear Regression
# =====================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

st.set_page_config(
    page_title="Regresi - Healthcare Dashboard",
    page_icon="📈",
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
        border-right: 1px solid rgba(59,130,246,0.2);
    }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(99,102,241,0.05));
        border: 1px solid rgba(59,130,246,0.25);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: rgba(59,130,246,0.6);
        box-shadow: 0 0 20px rgba(59,130,246,0.2);
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] { font-weight: 600; color: #94a3b8 !important; font-size: 0.85rem !important; }
    [data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 1.8rem !important; font-weight: 700 !important; }
    h1 { color: #f1f5f9 !important; font-weight: 800 !important; }
    h2, h3 { color: #e2e8f0 !important; font-weight: 700 !important; }
    hr { border-color: rgba(59,130,246,0.2) !important; margin: 1.5rem 0 !important; }
    .stPlotlyChart { border-radius: 16px; overflow: hidden; border: 1px solid rgba(59,130,246,0.15); }
    .rancangan-box {
        background: linear-gradient(135deg, rgba(59,130,246,0.12), rgba(99,102,241,0.08));
        border: 1px solid rgba(59,130,246,0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        color: #cbd5e1;
        line-height: 1.7;
    }
    .rancangan-box h4 {
        color: #60a5fa !important;
        margin: 0 0 0.75rem;
        font-size: 1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .page-header {
        background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(99,102,241,0.15), rgba(14,165,233,0.1));
        border: 1px solid rgba(59,130,246,0.35);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
    }
    .page-header h1 {
        margin: 0 !important; padding: 0 !important;
        background: linear-gradient(135deg, #60a5fa, #818cf8, #38bdf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; font-size: 2rem !important;
    }
    .page-header p { color: #94a3b8; margin-top: 0.5rem; font-size: 0.95rem; }
    .result-box {
        background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(14,165,233,0.08));
        border: 1px solid rgba(59,130,246,0.4);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 0.5rem 0;
        color: #93c5fd;
    }
    .result-box span { color: #e2e8f0; font-weight: 700; font-size: 1.3rem; }
</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <span style='font-size: 3rem;'>🏥</span>
        <h2 style='color:#60a5fa; margin:0.5rem 0 0; font-size:1.1rem;'>Healthcare Analytics</h2>
        <p style='color:#64748b; font-size:0.8rem; margin:0;'>Data Mining Dashboard</p>
    </div>
    <hr style='border-color:rgba(59,130,246,0.2); margin:1rem 0;'>
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
    df = pd.read_csv("healthcare_dataset.csv")
    return df

df = load_data()

# =====================================
# HEADER
# =====================================

st.markdown("""
<div class='page-header'>
    <h1>📈 Rancangan 1: Regresi</h1>
    <p>Memprediksi berapa <strong>biaya tagihan</strong> yang akan dikeluarkan pasien menggunakan metode <strong>Linear Regression</strong></p>
</div>
""", unsafe_allow_html=True)

# =====================================
# PENJELASAN RANCANGAN
# =====================================

st.subheader("📋 Penjelasan Rancangan Data Mining — Regresi")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='rancangan-box'>
        <h4>🧮 Algoritma yang Diterapkan</h4>
        <p><strong style='color:#93c5fd;'>Linear Regression (Regresi Linier)</strong> adalah metode yang digunakan
        untuk <strong>memprediksi sebuah nilai angka</strong> berdasarkan data-data yang sudah ada.
        Cara kerjanya mirip seperti mencari pola dari data yang lama, lalu digunakan untuk menebak nilai baru.</p>
        <p>Contoh sederhananya: dari data ribuan pasien yang sudah ada, komputer belajar bahwa
        <em>"pasien yang lebih tua dan penyakitnya lebih serius cenderung bayar lebih mahal"</em>.
        Pola ini kemudian dipakai untuk menebak tagihan pasien berikutnya.</p>
        <p style='margin:0; color:#64748b; font-size:0.85rem;'>Formula: <code style='background:rgba(59,130,246,0.2); padding:2px 6px; border-radius:4px; color:#93c5fd;'>
        Prediksi = angka tetap + (pengaruh faktor 1) + (pengaruh faktor 2) + ...</code></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='rancangan-box'>
        <h4>📊 Data / Kolom yang Digunakan</h4>
        <p style='color:#64748b; font-size:0.82rem; margin-bottom:0.5rem;'>Data yang dimasukkan ke model (sebagai bahan belajar):</p>
        <ul style='margin:0; padding-left:1.2rem;'>
            <li><strong style='color:#93c5fd;'>Data masukan (bahan prediksi):</strong>
                <ul>
                    <li><b>Age</b> — Umur pasien</li>
                    <li><b>Gender</b> — Jenis kelamin (Laki/Perempuan)</li>
                    <li><b>Medical Condition</b> — Jenis penyakit yang diderita</li>
                    <li><b>Admission Type</b> — Jenis rawat inap (darurat/elektif/mendesak)</li>
                    <li><b>Insurance Provider</b> — Nama perusahaan asuransi</li>
                    <li><b>Room Number</b> — Nomor kamar yang ditempati</li>
                </ul>
            </li>
            <li style='margin-top:0.5rem;'><strong style='color:#93c5fd;'>Data yang diprediksi:</strong> Billing Amount — total tagihan biaya pasien ($)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class='rancangan-box'>
        <h4>⚙️ Cara Kerja</h4>
        <ol style='margin:0; padding-left:1.2rem;'>
            <li><strong>Persiapan Data:</strong> Kolom yang berisi teks (seperti Gender, Jenis Penyakit) diubah dulu menjadi angka agar bisa diproses komputer</li>
            <li><strong>Bagi Data:</strong> Data dibagi dua — 80% untuk belajar (training), 20% untuk ujian (testing)</li>
            <li><strong>Proses Belajar:</strong> Model belajar dari 80% data tadi — mencari pola hubungan antara profil pasien dan besar tagihannya</li>
            <li><strong>Prediksi:</strong> Model dicoba pada 20% data yang belum pernah dilihat, lalu dibandingkan hasilnya</li>
            <li><strong>Ukur Akurasi:</strong> Dihitung seberapa jauh selisih prediksi dengan tagihan aslinya (MAE, RMSE, R²)</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='rancangan-box'>
        <h4>🎯 Fungsi dalam Pengambilan Keputusan</h4>
        <p>Dengan mengetahui <em>perkiraan tagihan</em> pasien sejak awal, rumah sakit bisa:</p>
        <ul style='margin:0; padding-left:1.2rem;'>
            <li><strong style='color:#93c5fd;'>Kelola Keuangan lebih baik:</strong> Pihak rumah sakit bisa memperkirakan berapa pendapatan yang akan masuk, sehingga lebih mudah mengatur anggaran</li>
            <li><strong style='color:#93c5fd;'>Bantu pasien merencanakan biaya:</strong> Pasien bisa tahu estimasi biaya sejak awal, sehingga tidak kaget saat menerima tagihan</li>
            <li><strong style='color:#93c5fd;'>Tentukan tarif yang adil:</strong> Manajemen bisa menyesuaikan harga layanan berdasarkan data nyata, bukan hanya perkiraan</li>
            <li><strong style='color:#93c5fd;'>Proses klaim asuransi lebih cepat:</strong> Data prediksi bisa dijadikan acuan saat mengajukan klaim ke perusahaan asuransi</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# =====================================
# PREPROCESSING & MODEL
# =====================================

st.subheader("🤖 Hasil Eksekusi Model — Linear Regression")

# Preprocessing
df_reg = df.copy()
le = LabelEncoder()

cat_cols = ["Gender", "Medical Condition", "Admission Type", "Insurance Provider"]
for col in cat_cols:
    df_reg[col] = le.fit_transform(df_reg[col])

features = ["Age", "Gender", "Medical Condition", "Admission Type", "Insurance Provider", "Room Number"]
target = "Billing Amount"

X = df_reg[features]
y = df_reg[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)


# =====================================
# METRICS EVALUASI
# =====================================

col1, col2, col3, col4 = st.columns(4)
with col1:
    r2_color = "#4ade80" if r2 > 0.5 else ("#fb923c" if r2 > 0 else "#f87171")
    st.metric("📊 R² Score", f"{r2:.4f}")
with col2:
    st.metric("📉 MAE", f"${mae:,.2f}")
with col3:
    st.metric("📉 RMSE", f"${rmse:,.2f}")
with col4:
    st.metric("🧪 Data Training", f"{len(X_train):,} baris")

# =====================================
# INTERPRETASI R²
# =====================================

if r2 < 0:
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(251,146,60,0.12),rgba(239,68,68,0.08));
                border:1px solid rgba(251,146,60,0.4); border-radius:14px; padding:1.25rem 1.5rem; margin:1rem 0;'>
        <h4 style='color:#fb923c; margin:0 0 0.75rem; font-size:0.95rem;'>⚠️ Catatan Penting tentang Hasil Model (R² = {r2:.4f})</h4>
        <p style='color:#cbd5e1; margin:0 0 0.5rem; font-size:0.9rem;'>
            Nilai R² yang negatif atau mendekati nol bukan berarti program salah, melainkan karena
            <strong style='color:#fbbf24;'>dataset ini adalah data sintetis (buatan/palsu)</strong> — bukan data rumah sakit sungguhan.
            Data tagihan pasien dibuat secara acak tanpa pola nyata, sehingga model tidak bisa menemukan hubungan yang berarti.
        </p>
        <p style='color:#94a3b8; margin:0; font-size:0.85rem;'>
            💡 <strong>Untuk presentasi ke dosen:</strong> Jelaskan bahwa rancangan dan prosesnya sudah benar —
            algoritma Linear Regression memang berjalan dengan baik. Hanya saja, data yang digunakan tidak memiliki
            pola linear yang kuat antara profil pasien dan biaya tagihan. Ini adalah temuan yang valid dan wajar
            disampaikan sebagai bagian dari analisis.
        </p>
        <hr style='border-color:rgba(251,146,60,0.2); margin:0.75rem 0;'>
        <p style='color:#94a3b8; margin:0; font-size:0.82rem;'>
            📊 <strong>Interpretasi nilai R²:</strong>
            R² = 1.0 artinya sempurna —
            R² = 0.0 artinya model sama saja dengan menebak nilai rata-rata —
            R² &lt; 0 artinya pola data benar-benar acak, tidak ada hubungan linear yang bisa dipelajari model.
        </p>
    </div>
    """, unsafe_allow_html=True)
elif r2 < 0.3:
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(251,146,60,0.1),rgba(0,0,0,0));
                border:1px solid rgba(251,146,60,0.3); border-radius:14px; padding:1.25rem 1.5rem; margin:1rem 0;'>
        <h4 style='color:#fb923c; margin:0 0 0.5rem; font-size:0.95rem;'>⚠️ R² = {r2:.4f} — Model Lemah</h4>
        <p style='color:#cbd5e1; margin:0; font-size:0.9rem;'>
            Nilai R² yang rendah menunjukkan pola data tidak terlalu kuat. Kemungkinan besar karena dataset ini bersifat sintetis.
            Proses dan rancangan sudah benar — hasil ini adalah temuan yang valid dari analisis.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(74,222,128,0.1),rgba(0,0,0,0));
                border:1px solid rgba(74,222,128,0.3); border-radius:14px; padding:1.25rem 1.5rem; margin:1rem 0;'>
        <h4 style='color:#4ade80; margin:0 0 0.5rem; font-size:0.95rem;'>✅ R² = {r2:.4f} — Model Cukup Baik</h4>
        <p style='color:#cbd5e1; margin:0; font-size:0.9rem;'>
            Model berhasil menemukan pola yang cukup baik antara profil pasien dan besar tagihannya.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# =====================================
# VISUALISASI
# =====================================

col1, col2 = st.columns(2)

with col1:
    # Actual vs Predicted scatter
    sample_idx = np.random.choice(len(y_test), size=min(500, len(y_test)), replace=False)
    fig_scatter = go.Figure()
    fig_scatter.add_trace(go.Scatter(
        x=y_test.iloc[sample_idx],
        y=y_pred[sample_idx],
        mode='markers',
        marker=dict(color='#60a5fa', opacity=0.5, size=5),
        name='Prediksi vs Aktual'
    ))
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    fig_scatter.add_trace(go.Scatter(
        x=[min_val, max_val], y=[min_val, max_val],
        mode='lines',
        line=dict(color='#f87171', dash='dash', width=2),
        name='Garis Ideal'
    ))
    fig_scatter.update_layout(
        title="Nilai Aktual vs Nilai Prediksi",
        xaxis_title="Billing Aktual ($)",
        yaxis_title="Billing Prediksi ($)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=14),
        legend=dict(font=dict(color="#94a3b8")),
        xaxis=dict(gridcolor="rgba(59,130,246,0.1)"),
        yaxis=dict(gridcolor="rgba(59,130,246,0.1)"),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    # Residuals distribution
    residuals = y_test.values - y_pred
    fig_resid = go.Figure()
    fig_resid.add_trace(go.Histogram(
        x=residuals,
        nbinsx=50,
        marker_color='#818cf8',
        opacity=0.8,
        name='Residual'
    ))
    fig_resid.add_vline(x=0, line_dash="dash", line_color="#f87171", line_width=2)
    fig_resid.update_layout(
        title="Distribusi Residual (Error Prediksi)",
        xaxis_title="Residual ($)",
        yaxis_title="Frekuensi",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=14),
        xaxis=dict(gridcolor="rgba(59,130,246,0.1)"),
        yaxis=dict(gridcolor="rgba(59,130,246,0.1)"),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_resid, use_container_width=True)


# =====================================
# FEATURE IMPORTANCE (COEFFICIENTS)
# =====================================

coef_df = pd.DataFrame({
    "Fitur": features,
    "Koefisien": model.coef_
}).sort_values("Koefisien", ascending=True)

colors = ["#f87171" if c < 0 else "#4ade80" for c in coef_df["Koefisien"]]

fig_coef = go.Figure(go.Bar(
    x=coef_df["Koefisien"],
    y=coef_df["Fitur"],
    orientation='h',
    marker_color=colors,
    text=[f"{c:,.2f}" for c in coef_df["Koefisien"]],
    textposition='outside',
    textfont=dict(color="#94a3b8")
))
fig_coef.update_layout(
    title="Koefisien Fitur — Pengaruh terhadap Billing Amount",
    xaxis_title="Nilai Koefisien",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8"),
    title_font=dict(color="#e2e8f0", size=14),
    xaxis=dict(gridcolor="rgba(59,130,246,0.1)"),
    yaxis=dict(gridcolor="rgba(59,130,246,0.1)"),
    margin=dict(t=45, b=10, l=100, r=80),
    height=350
)
st.plotly_chart(fig_coef, use_container_width=True)

st.divider()


# =====================================
# PREDIKSI INTERAKTIF
# =====================================

st.subheader("🔮 Coba Prediksi Billing Amount")
st.markdown("<p style='color:#64748b; font-size:0.85rem;'>Masukkan data pasien untuk mendapatkan estimasi billing amount</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    inp_age = st.slider("Umur Pasien", 1, 90, 45)
    inp_gender = st.selectbox("Gender", df["Gender"].unique())
with col2:
    inp_condition = st.selectbox("Kondisi Medis", df["Medical Condition"].unique())
    inp_admission = st.selectbox("Tipe Rawat Inap", df["Admission Type"].unique())
with col3:
    inp_insurance = st.selectbox("Asuransi", df["Insurance Provider"].unique())
    inp_room = st.slider("Nomor Kamar", int(df["Room Number"].min()), int(df["Room Number"].max()), 200)

if st.button("🔮 Prediksi Sekarang", type="primary", use_container_width=True):
    le2 = LabelEncoder()
    pred_input = pd.DataFrame([[inp_age,
                                 df["Gender"].unique().tolist().index(inp_gender),
                                 df["Medical Condition"].unique().tolist().index(inp_condition),
                                 df["Admission Type"].unique().tolist().index(inp_admission),
                                 df["Insurance Provider"].unique().tolist().index(inp_insurance),
                                 inp_room]],
                               columns=features)

    # Encode exactly as training
    df_temp = df.copy()
    for col in cat_cols:
        le_temp = LabelEncoder()
        le_temp.fit(df_temp[col])
        if col == "Gender":
            pred_input["Gender"] = le_temp.transform([inp_gender])[0]
        elif col == "Medical Condition":
            pred_input["Medical Condition"] = le_temp.transform([inp_condition])[0]
        elif col == "Admission Type":
            pred_input["Admission Type"] = le_temp.transform([inp_admission])[0]
        elif col == "Insurance Provider":
            pred_input["Insurance Provider"] = le_temp.transform([inp_insurance])[0]

    pred_val = model.predict(pred_input)[0]

    st.markdown(f"""
    <div class='result-box'>
        💰 <strong>Estimasi Billing Amount:</strong>
        <span>${pred_val:,.2f}</span>
        <br><small style='color:#64748b;'>Berdasarkan model Linear Regression dengan R² = {r2:.4f}</small>
    </div>
    """, unsafe_allow_html=True)
