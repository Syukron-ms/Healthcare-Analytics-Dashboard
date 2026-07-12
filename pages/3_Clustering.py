# =====================================
# RANCANGAN 3: CLUSTERING
# Segmentasi Pasien
# Algoritma: K-Means Clustering
# =====================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

st.set_page_config(
    page_title="Clustering - Healthcare Dashboard",
    page_icon="🔵",
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
        border-right: 1px solid rgba(74,222,128,0.2);
    }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(74,222,128,0.1), rgba(16,185,129,0.05));
        border: 1px solid rgba(74,222,128,0.25);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: rgba(74,222,128,0.6);
        box-shadow: 0 0 20px rgba(74,222,128,0.2);
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] { font-weight: 600; color: #94a3b8 !important; font-size: 0.85rem !important; }
    [data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 1.8rem !important; font-weight: 700 !important; }
    h1 { color: #f1f5f9 !important; font-weight: 800 !important; }
    h2, h3 { color: #e2e8f0 !important; font-weight: 700 !important; }
    hr { border-color: rgba(74,222,128,0.2) !important; margin: 1.5rem 0 !important; }
    .stPlotlyChart { border-radius: 16px; overflow: hidden; border: 1px solid rgba(74,222,128,0.15); }
    .rancangan-box {
        background: linear-gradient(135deg, rgba(74,222,128,0.1), rgba(16,185,129,0.05));
        border: 1px solid rgba(74,222,128,0.25);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        color: #cbd5e1;
        line-height: 1.7;
    }
    .rancangan-box h4 {
        color: #4ade80 !important;
        margin: 0 0 0.75rem;
        font-size: 1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .page-header {
        background: linear-gradient(135deg, rgba(74,222,128,0.15), rgba(16,185,129,0.1), rgba(52,211,153,0.08));
        border: 1px solid rgba(74,222,128,0.3);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
    }
    .page-header h1 {
        margin: 0 !important; padding: 0 !important;
        background: linear-gradient(135deg, #4ade80, #34d399, #6ee7b7);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; font-size: 2rem !important;
    }
    .page-header p { color: #94a3b8; margin-top: 0.5rem; font-size: 0.95rem; }
    .cluster-card {
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    .cluster-card:hover { transform: translateY(-3px); }
</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <span style='font-size: 3rem;'>🏥</span>
        <h2 style='color:#4ade80; margin:0.5rem 0 0; font-size:1.1rem;'>Healthcare Analytics</h2>
        <p style='color:#64748b; font-size:0.8rem; margin:0;'>Data Mining Dashboard</p>
    </div>
    <hr style='border-color:rgba(74,222,128,0.2); margin:1rem 0;'>
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
    <h1>🔵 Rancangan 3: Clustering</h1>
    <p>Mengelompokkan pasien ke dalam beberapa <strong>kelompok berdasarkan kemiripan profil</strong> mereka — menggunakan metode <strong>K-Means Clustering</strong></p>
</div>
""", unsafe_allow_html=True)

# =====================================
# PENJELASAN RANCANGAN
# =====================================

st.subheader("📋 Penjelasan Rancangan Data Mining — Clustering")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='rancangan-box'>
        <h4>🔵 Algoritma yang Diterapkan</h4>
        <p><strong style='color:#6ee7b7;'>K-Means Clustering</strong> adalah metode yang digunakan untuk
        <strong>mengelompokkan data secara otomatis</strong> tanpa perlu memberi label terlebih dahulu.
        Algoritma ini bekerja seperti ketika kita memisahkan sekumpulan bola berdasarkan warna
        tanpa tahu ada berapa warna — komputer yang menentukan sendiri kelompok-kelompoknya.</p>
        <p>Cara kerjanya: komputer memilih beberapa titik pusat (disebut <em>centroid</em>), lalu
        mengelompokkan setiap pasien ke titik pusat yang paling mirip dengannya.
        Proses ini diulang terus sampai kelompok-kelompok itu tidak berubah lagi.</p>
        <p style='margin:0;'>Jumlah kelompok terbaik dicari menggunakan
        <code style='background:rgba(74,222,128,0.2); padding:2px 6px; border-radius:4px; color:#6ee7b7;'>Elbow Method</code> dan
        <code style='background:rgba(74,222,128,0.2); padding:2px 6px; border-radius:4px; color:#6ee7b7;'>Silhouette Score</code>.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='rancangan-box'>
        <h4>📊 Data / Kolom yang Digunakan</h4>
        <p style='color:#64748b; font-size:0.82rem; margin-bottom:0.5rem;'>Data yang dipakai untuk mengelompokkan pasien:</p>
        <ul style='margin:0; padding-left:1.2rem;'>
            <li><strong style='color:#6ee7b7;'>Data yang digunakan:</strong>
                <ul>
                    <li><b>Age</b> — Umur pasien</li>
                    <li><b>Billing Amount</b> — Total tagihan biaya perawatan</li>
                    <li><b>Room Number</b> — Nomor kamar yang ditempati</li>
                    <li><b>Length of Stay</b> — Berapa hari pasien dirawat (dihitung dari tanggal masuk hingga keluar)</li>
                </ul>
            </li>
            <li style='margin-top:0.5rem;'><strong style='color:#6ee7b7;'>Pra-pemrosesan:</strong> Semua data disamakan skalanya agar tidak ada fitur yang "mendominasi" pengelompokan</li>
            <li style='margin-top:0.3rem;'><strong style='color:#6ee7b7;'>Hasil:</strong> Setiap pasien mendapat label kelompok (Cluster 0, Cluster 1, dst.)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class='rancangan-box'>
        <h4>⚙️ Cara Kerja</h4>
        <ol style='margin:0; padding-left:1.2rem;'>
            <li><strong>Hitung Lama Rawat:</strong> Dari data tanggal masuk dan tanggal keluar, kita hitung berapa hari setiap pasien dirawat</li>
            <li><strong>Samakan Skala:</strong> Karena umur, tagihan, dan nomor kamar punya satuan berbeda, semua diubah ke skala yang sama agar tidak ada yang terlalu mendominasi</li>
            <li><strong>Cari Jumlah Kelompok Terbaik:</strong> Dicoba dengan berbagai jumlah kelompok (2 sampai 10), lalu dipilih yang paling baik pemisahannya</li>
            <li><strong>Kelompokkan Pasien:</strong> Komputer secara otomatis mengelompokkan setiap pasien ke kelompok yang paling mirip profilnya</li>
            <li><strong>Beri Nama Kelompok:</strong> Setelah dikelompokkan, kita analisis ciri-ciri tiap kelompok (misalnya: pasien muda tagihan rendah, pasien tua tagihan tinggi, dll)</li>
            <li><strong>Tampilkan secara Visual:</strong> Kelompok divisualisasikan dalam grafik 2D agar mudah dipahami</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='rancangan-box'>
        <h4>🎯 Fungsi dalam Pengambilan Keputusan</h4>
        <p>Dengan mengelompokkan pasien berdasarkan profil mereka, rumah sakit bisa:</p>
        <ul style='margin:0; padding-left:1.2rem;'>
            <li><strong style='color:#6ee7b7;'>Layanan yang lebih personal:</strong> Setiap kelompok pasien mendapatkan pelayanan yang sesuai dengan kebutuhan dan kondisi mereka, bukan layanan yang sama untuk semua</li>
            <li><strong style='color:#6ee7b7;'>Program kesehatan yang tepat sasaran:</strong> Misal, kelompok pasien lansia bisa ditawarkan paket perawatan khusus atau program pencegahan penyakit yang sesuai</li>
            <li><strong style='color:#6ee7b7;'>Atur ketersediaan kamar dan tenaga medis:</strong> Jika satu kelompok pasien biasanya butuh rawat inap lama, rumah sakit bisa menyiapkan lebih banyak kamar untuk mereka</li>
            <li><strong style='color:#6ee7b7;'>Temukan pasien yang tidak biasa:</strong> Pasien yang profilnya sangat berbeda dari kelompok mana pun bisa langsung mendapat perhatian khusus</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================
# PREPROCESSING
# =====================================

st.subheader("🤖 Hasil Eksekusi Model — K-Means Clustering")

df_clust = df.copy()
df_clust["Date of Admission"] = pd.to_datetime(df_clust["Date of Admission"])
df_clust["Discharge Date"] = pd.to_datetime(df_clust["Discharge Date"])
df_clust["Length of Stay"] = (df_clust["Discharge Date"] - df_clust["Date of Admission"]).dt.days

features_clust = ["Age", "Billing Amount", "Room Number", "Length of Stay"]
X_clust = df_clust[features_clust].dropna()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_clust)


# =====================================
# ELBOW METHOD + SILHOUETTE
# =====================================

@st.cache_data
def compute_elbow(X_scaled):
    inertias = []
    sil_scores = []
    k_range = range(2, 11)
    for k in k_range:
        km = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)
        sil_scores.append(silhouette_score(X_scaled, km.labels_, sample_size=5000, random_state=42))
    return list(k_range), inertias, sil_scores

k_range, inertias, sil_scores = compute_elbow(X_scaled)

col1, col2 = st.columns(2)

with col1:
    fig_elbow = go.Figure()
    fig_elbow.add_trace(go.Scatter(
        x=k_range, y=inertias,
        mode='lines+markers',
        line=dict(color='#4ade80', width=2),
        marker=dict(color='#4ade80', size=8),
        name='Inertia'
    ))
    fig_elbow.update_layout(
        title="Elbow Method — Menentukan Jumlah Cluster Optimal",
        xaxis_title="Jumlah Cluster (K)",
        yaxis_title="Inertia (WCSS)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=14),
        xaxis=dict(gridcolor="rgba(74,222,128,0.1)", tickvals=k_range),
        yaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_elbow, use_container_width=True)

with col2:
    fig_sil = go.Figure()
    fig_sil.add_trace(go.Bar(
        x=k_range, y=sil_scores,
        marker=dict(
            color=sil_scores,
            colorscale=[[0, "#064e3b"], [0.5, "#059669"], [1, "#4ade80"]],
            showscale=False
        ),
        text=[f"{s:.3f}" for s in sil_scores],
        textposition='outside',
        textfont=dict(color="#94a3b8")
    ))
    best_k = k_range[sil_scores.index(max(sil_scores))]
    fig_sil.add_vline(x=best_k, line_dash="dash", line_color="#f87171",
                      annotation_text=f"K={best_k} (terbaik)", annotation_font_color="#f87171")
    fig_sil.update_layout(
        title="Silhouette Score per Jumlah Cluster",
        xaxis_title="Jumlah Cluster (K)",
        yaxis_title="Silhouette Score",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=14),
        xaxis=dict(gridcolor="rgba(74,222,128,0.1)", tickvals=k_range),
        yaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_sil, use_container_width=True)


# =====================================
# INTERACTIVE K SELECTOR
# =====================================

st.markdown(f"<p style='color:#6ee7b7; font-size:0.9rem;'>💡 K optimal berdasarkan Silhouette Score: <strong>K = {best_k}</strong></p>", unsafe_allow_html=True)

k_selected = st.slider("Pilih jumlah cluster (K)", min_value=2, max_value=8, value=best_k, step=1)


# =====================================
# FIT FINAL K-MEANS
# =====================================

@st.cache_data
def fit_kmeans(X_scaled, k):
    km = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    sil = silhouette_score(X_scaled, labels, sample_size=5000, random_state=42)
    return labels, sil

labels, sil = fit_kmeans(X_scaled, k_selected)
df_result = X_clust.copy()
df_result["Cluster"] = [f"Cluster {l}" for l in labels]

# Add original categorical info
for col in ["Gender", "Medical Condition", "Admission Type", "Test Results"]:
    df_result[col] = df_clust.loc[X_clust.index, col].values


# =====================================
# METRICS POST-CLUSTERING
# =====================================

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Silhouette Score", f"{sil:.4f}")
with col2:
    st.metric("🔵 Jumlah Cluster", k_selected)
with col3:
    st.metric("📋 Total Pasien", f"{len(df_result):,}")
with col4:
    largest = df_result["Cluster"].value_counts().max()
    st.metric("📦 Cluster Terbesar", f"{largest:,} pasien")

st.divider()


# =====================================
# PCA SCATTER PLOT
# =====================================

@st.cache_data
def compute_pca(X_scaled):
    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(X_scaled)
    return components, pca.explained_variance_ratio_

pca_result, evr = compute_pca(X_scaled)

pca_df = pd.DataFrame({
    "PC1": pca_result[:, 0],
    "PC2": pca_result[:, 1],
    "Cluster": df_result["Cluster"].values,
    "Age": df_result["Age"].values,
    "Billing Amount": df_result["Billing Amount"].values,
    "Length of Stay": df_result["Length of Stay"].values
})

cluster_colors = ["#4ade80", "#60a5fa", "#f87171", "#fb923c", "#c084fc", "#34d399", "#fbbf24", "#a78bfa"]

col1, col2 = st.columns(2)

with col1:
    fig_pca = px.scatter(
        pca_df.sample(min(5000, len(pca_df)), random_state=42),
        x="PC1", y="PC2",
        color="Cluster",
        color_discrete_sequence=cluster_colors[:k_selected],
        title=f"Visualisasi Cluster (PCA 2D) — Var. Explained: {(evr[0]+evr[1])*100:.1f}%",
        hover_data=["Age", "Billing Amount", "Length of Stay"],
        opacity=0.65
    )
    fig_pca.update_traces(marker=dict(size=4))
    fig_pca.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=13),
        legend=dict(font=dict(color="#94a3b8")),
        xaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
        yaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_pca, use_container_width=True)

with col2:
    # Cluster distribution
    dist = df_result["Cluster"].value_counts().reset_index()
    dist.columns = ["Cluster", "Jumlah"]
    fig_dist = px.bar(
        dist, x="Cluster", y="Jumlah",
        color="Cluster",
        color_discrete_sequence=cluster_colors[:k_selected],
        title="Distribusi Jumlah Pasien per Cluster",
        text="Jumlah"
    )
    fig_dist.update_traces(textposition='outside')
    fig_dist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=14),
        showlegend=False,
        xaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
        yaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_dist, use_container_width=True)


# =====================================
# CLUSTER PROFILE
# =====================================

col1, col2 = st.columns(2)

with col1:
    fig_age = px.box(
        df_result, x="Cluster", y="Age",
        color="Cluster",
        color_discrete_sequence=cluster_colors[:k_selected],
        title="Distribusi Umur per Cluster"
    )
    fig_age.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=14),
        showlegend=False,
        xaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
        yaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    fig_bill = px.box(
        df_result, x="Cluster", y="Billing Amount",
        color="Cluster",
        color_discrete_sequence=cluster_colors[:k_selected],
        title="Distribusi Billing Amount per Cluster"
    )
    fig_bill.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=14),
        showlegend=False,
        xaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
        yaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
        margin=dict(t=45, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_bill, use_container_width=True)


# =====================================
# STATISTIK PER CLUSTER
# =====================================

st.subheader("📊 Statistik Deskriptif per Cluster")
st.markdown("<p style='color:#64748b; font-size:0.85rem;'>Rata-rata karakteristik setiap cluster pasien</p>", unsafe_allow_html=True)

cluster_stats = df_result.groupby("Cluster")[features_clust].mean().round(2)
cluster_stats["Jumlah Pasien"] = df_result.groupby("Cluster").size()
cluster_stats = cluster_stats.reset_index()

# Display cards per cluster
cols = st.columns(min(k_selected, 4))
for i, row in cluster_stats.iterrows():
    col_idx = i % len(cols)
    color = cluster_colors[i % len(cluster_colors)]
    with cols[col_idx]:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg, {color}18, {color}08);
                    border:1px solid {color}40; border-radius:14px; padding:1.2rem;
                    margin-bottom:0.75rem;'>
            <h4 style='color:{color}; margin:0 0 0.75rem; font-size:0.95rem; font-weight:700;'>
                🔵 {row["Cluster"]}
            </h4>
            <table style='width:100%; font-size:0.82rem; color:#94a3b8; border-collapse:collapse;'>
                <tr><td>👥 Pasien</td><td style='color:#e2e8f0; text-align:right; font-weight:600;'>{int(row["Jumlah Pasien"]):,}</td></tr>
                <tr><td>🎂 Rata Umur</td><td style='color:#e2e8f0; text-align:right; font-weight:600;'>{row["Age"]:.1f} th</td></tr>
                <tr><td>💰 Avg Billing</td><td style='color:#e2e8f0; text-align:right; font-weight:600;'>${row["Billing Amount"]:,.0f}</td></tr>
                <tr><td>🏠 Avg Kamar</td><td style='color:#e2e8f0; text-align:right; font-weight:600;'>{row["Room Number"]:.0f}</td></tr>
                <tr><td>📅 Avg LoS</td><td style='color:#e2e8f0; text-align:right; font-weight:600;'>{row["Length of Stay"]:.1f} hari</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

if k_selected > 4:
    cols2 = st.columns(k_selected - 4)
    for i, row in cluster_stats.iloc[4:].iterrows():
        col_idx = i - 4
        color = cluster_colors[i % len(cluster_colors)]
        with cols2[col_idx]:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg, {color}18, {color}08);
                        border:1px solid {color}40; border-radius:14px; padding:1.2rem;'>
                <h4 style='color:{color}; margin:0 0 0.75rem; font-size:0.95rem; font-weight:700;'>
                    🔵 {row["Cluster"]}
                </h4>
                <table style='width:100%; font-size:0.82rem; color:#94a3b8; border-collapse:collapse;'>
                    <tr><td>👥 Pasien</td><td style='color:#e2e8f0; text-align:right; font-weight:600;'>{int(row["Jumlah Pasien"]):,}</td></tr>
                    <tr><td>🎂 Rata Umur</td><td style='color:#e2e8f0; text-align:right; font-weight:600;'>{row["Age"]:.1f} th</td></tr>
                    <tr><td>💰 Avg Billing</td><td style='color:#e2e8f0; text-align:right; font-weight:600;'>${row["Billing Amount"]:,.0f}</td></tr>
                    <tr><td>🏠 Avg Kamar</td><td style='color:#e2e8f0; text-align:right; font-weight:600;'>{row["Room Number"]:.0f}</td></tr>
                    <tr><td>📅 Avg LoS</td><td style='color:#e2e8f0; text-align:right; font-weight:600;'>{row["Length of Stay"]:.1f} hari</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

st.divider()


# =====================================
# TEST RESULTS PER CLUSTER
# =====================================

test_cluster = df_result.groupby(["Cluster", "Test Results"]).size().reset_index(name="Jumlah")
fig_test_clust = px.bar(
    test_cluster,
    x="Cluster", y="Jumlah",
    color="Test Results",
    color_discrete_map={"Normal": "#4ade80", "Abnormal": "#f87171", "Inconclusive": "#fb923c"},
    title="Distribusi Hasil Tes per Cluster",
    barmode="group",
    text="Jumlah"
)
fig_test_clust.update_traces(textposition='outside')
fig_test_clust.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8"),
    title_font=dict(color="#e2e8f0", size=14),
    legend=dict(font=dict(color="#94a3b8")),
    xaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
    yaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
    margin=dict(t=45, b=10, l=10, r=10)
)
st.plotly_chart(fig_test_clust, use_container_width=True)


# =====================================
# MEDICAL CONDITION PER CLUSTER
# =====================================

cond_cluster = df_result.groupby(["Cluster", "Medical Condition"]).size().reset_index(name="Jumlah")
fig_cond_clust = px.bar(
    cond_cluster,
    x="Medical Condition", y="Jumlah",
    color="Cluster",
    color_discrete_sequence=cluster_colors[:k_selected],
    title="Kondisi Medis per Cluster",
    barmode="group"
)
fig_cond_clust.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8"),
    title_font=dict(color="#e2e8f0", size=14),
    legend=dict(font=dict(color="#94a3b8")),
    xaxis=dict(gridcolor="rgba(74,222,128,0.1)", tickangle=-20),
    yaxis=dict(gridcolor="rgba(74,222,128,0.1)"),
    margin=dict(t=45, b=60, l=10, r=10)
)
st.plotly_chart(fig_cond_clust, use_container_width=True)
