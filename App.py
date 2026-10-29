import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io

# 1. Konfigurasi Halaman (Desain Profesional & Responsif HP)
st.set_page_config(
    page_title="StatLab - Deskriptif",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# KUSTOMISASI CSS AMAN
st.markdown(
    """
    <style>
    .main-header { font-size:28px !important; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-header { font-size:16px !important; color: #4B5563; margin-bottom: 20px; }
    .card { background-color: #F3F4F6; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
    </style>
    """, 
    unsafe_allow_html=True
)

st.markdown('<div class="main-header">📊 StatLab: Analisis Statistika Deskriptif</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Aplikasi Interaktif Pengolahan Data Praktis & Profesional</div>', unsafe_allow_html=True)

# 2. Inisialisasi State Data agar Pilihan Fitur Tetap Muncul di Layar
if 'df' not in st.session_state:
    st.session_state.df = None

# 3. PANEL INPUT (Selalu tampil di layar utama)
st.markdown("### 📥 Langkah 1: Input Data")
input_method = st.radio(
    "Pilih Metode Input Data:",
    ("Ketik Variabel & Data Manual", "Unggah File (Excel/.xlsx/.xls atau .csv)"),
    horizontal=True
)

if input_method == "Ketik Variabel & Data Manual":
    col1, col2 = st.columns(2)
    with col1:
        var_name = st.text_input("Nama Variabel Numerik:", value="Nilai_Ujian")
    with col2:
        raw_data = st.text_area("Masukkan Data (pisahkan dengan koma atau spasi):", value="85, 90, 78, 92, 88, 65, 80, 95, 70, missing, 88")
    
    # Tombol Proses Data Manual
    if st.button("Proses Data Manual", type="primary"):
        try:
            tokens = raw_data.replace('\n', ',').replace(' ', ',').split(',')
            parsed_data = []
            for t in tokens:
                t = t.strip()
                if t == '': continue
                if t.lower() in ['missing', 'nan', 'null', '-', '']:
                    parsed_data.append(np.nan)
                else:
                    parsed_data.append(float(t))
            
            st.session_state.df = pd.DataFrame({var_name: parsed_data})
            st.success("Data manual berhasil diproses!")
        except Exception as e:
            st.error(f"Gagal memproses data. Pastikan format benar (hanya angka). Error: {e}")

else:
    uploaded_file = st.file_uploader("Pilih file Excel atau CSV", type=["xlsx", "xls", "csv"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                st.session_state.df = pd.read_csv(uploaded_file)
            else:
                st.session_state.df = pd.read_excel(uploaded_file)
            st.success("File berhasil diunggah!")
        except Exception as e:
            st.error(f"Gagal membaca file. Error: {e}")

# Tampilkan Tabel Data jika ada
if st.session_state.df is not None:
    with st.expander("🔍 Lihat Tabel Data Aktif", expanded=False):
        st.dataframe(st.session_state.df, use_container_width=True)

# 4. PANEL FITUR UTAMA (Tetap Render Meskipun Data Belum Ada)
st.markdown("---")
st.markdown("### ⚙️ Langkah 2: Konfigurasi Fitur & Parameter Analisis")

# Cek kolom numerik jika data ada, jika tidak sediakan dummy/kosong
if st.session_state.df is not None:
    numeric_cols = st.session_state.df.select_dtypes(include=[np.number]).columns.tolist()
    all_cols = st.session_state.df.columns.tolist()
else:
    numeric_cols = ["Belum ada data numerik"]
    all_cols = ["Belum ada data"]

# Fitur Pilih Variabel
selected_vars = st.multiselect(
    "➡️ Pilih Variabel Numerik untuk Dianalisis:",
    options=numeric_cols,
    default=numeric_cols[:1] if st.session_state.df is not None and numeric_cols else numeric_cols
)

# Fitur Pilih Ukuran Statistika Deskriptif
stat_options = {
    "Jumlah Data (N)": "count",
    "Minimum": "min",
    "Maksimum": "max",
    "Mean (Rata-rata)": "mean",
    "Median": "median",
    "Modus": "mode",
    "Varians": "var",
    "Standar Deviasi": "std",
    "Kuartil 1 (Q1)": "q1",
    "Kuartil 2 (Q2)": "q2",
    "Kuartil 3 (Q3)": "q3"
}

selected_stats = st.multiselect(
    "🧮 Pilih Ukuran Statistika yang Ingin Dihitung:",
    options=list(stat_options.keys()),
    default=list(stat_options.keys())
)

# Fitur Tambahan UI: Pengaturan Warna & Visualisasi
st.markdown("#### 🎨 Pengaturan Eksplorasi Visual")
col_c1, col_c2 = st.columns(2)
with col_c1:
    chart_color = st.color_picker("Pilih Warna Utama Grafik:", "#1E3A8A")
with col_c2:
    chart_types = st.multiselect(
        "📊 Pilih Jenis Grafik yang Ingin Ditampilkan:",
        options=["Histogram", "Boxplot", "Diagram Batang (Bar)", "Diagram Lingkaran (Pie)", "Tabel Distribusi Frekuensi"],
        default=["Histogram", "Boxplot"]
    )

# 5. EKSEKUSI DAN OUTPUT
st.markdown("---")
st.markdown("### 📊 Langkah 3: Hasil Analisis Ringkasan")

# Proteksi pemicu jika tombol ditekan namun data belum siap
if st.session_state.df is None:
    st.info("💡 Menunggu input data... Silakan isi data di Langkah 1 untuk melihat kalkulasi otomatis.")
elif not selected_vars or "Belum ada data numerik" in selected_vars:
    st.warning("⚠️ Silakan pilih minimal satu variabel numerik pada Langkah 2.")
elif not selected_stats:
    st.warning("⚠️ Silakan pilih minimal satu ukuran statistika.")
else:
    df_working = st.session_state.df[selected_vars].copy()
    
    # Penanganan Data Kosong
    missing_info = df_working.isnull().sum()
    if missing_info.sum() > 0:
        st.warning(f"ℹ️ Terdeteksi data kosong (Missing Values). Sistem otomatis mengecualikannya dalam perhitungan statistik dasar.")
        with st.expander("Detail Data Kosong Per Variabel"):
            st.write(missing_info)

    # Kalkulasi Statistika Deskriptif Kustom
    summary_results = {}
    for var in selected_vars:
        col_data = df_working[var].dropna()
        var_metrics = {}
        
        if "Jumlah Data (N)" in selected_stats: var_metrics["Jumlah Data (N)"] = len(col_data)
        if "Minimum" in selected_stats: var_metrics["Minimum"] = col_data.min() if not col_data.empty else np.nan
        if "Maksimum" in selected_stats: var_metrics["Maksimum"] = col_data.max() if not col_data.empty else np.nan
        if "Mean (Rata-rata)" in selected_stats: var_metrics["Mean (Rata-rata)"] = col_data.mean() if not col_data.empty else np.nan
        if "Median" in selected_stats: var_metrics["Median"] = col_data.median() if not col_data.empty else np.nan
        if "Modus" in selected_stats: 
            mode_val = col_data.mode()
            var_metrics["Modus"] = mode_val.iloc[0] if not mode_val.empty else np.nan
        if "Varians" in selected_stats: var_metrics["Varians"] = col_data.var() if not col_data.empty else np.nan
        if "Standar Deviasi" in selected_stats: var_metrics["Standar Deviasi"] = col_data.std() if not col_data.empty else np.nan
        if "Kuartil 1 (Q1)" in selected_stats: var_metrics["Kuartil 1 (Q1)"] = col_data.quantile(0.25) if not col_data.empty else np.nan
        if "Kuartil 2 (Q2)" in selected_stats: var_metrics["Kuartil 2 (Q2)"] = col_data.quantile(0.50) if not col_data.empty else np.nan
        if "Kuartil 3 (Q3)" in selected_stats: var_metrics["Kuartil 3 (Q3)"] = col_data.quantile(0.75) if not col_data.empty else np.nan
        
        summary_results[var] = var_metrics
    
    res_df = pd.DataFrame(summary_results)
    
    st.success("Perhitungan Berhasil!")
    st.dataframe(res_df.style.format(precision=3), use_container_width=True)
    
    # Ekspor ke CSV
    csv_data = res_df.to_csv().encode('utf-8')
    st.download_button(
        label="📥 Unduh Ringkasan Hasil (.CSV)",
        data=csv_data,
        file_name='ringkasan_statlab.csv',
        mime='text/csv',
    )
    
    st.markdown("#### 📝 Interpretasi Hasil Otomatis")
    for var in selected_vars:
        col_data = df_working[var].dropna()
        if not col_data.empty:
            st.write(f"Variabel **{var}** memiliki rata-rata sebesar **{col_data.mean():.2f}** dengan rentang nilai dari **{col_data.min()}** hingga **{col_data.max()}**. Nilai tengah (median) data ini berada pada **{col_data.median()}**.")

    st.markdown("### 📉 Eksplorasi Visual (Diagram Interaktif)")
    
    for var in selected_vars:
        st.markdown(f"#### Analisis Grafik untuk Variabel: **{var}**")
        data_clean = df_working[[var]].dropna()
        
        g_col1, g_col2 = st.columns(2)
        
        if "Histogram" in chart_types:
            fig_hist = px.histogram(data_clean, x=var, title=f"Histogram Distribusi {var}", color_discrete_sequence=[chart_color])
            g_col1.plotly_chart(fig_hist, use_container_width=True)
            
        if "Boxplot" in chart_types:
            fig_box = px.box(data_clean, y=var, title=f"Boxplot Pencilan {var}", color_discrete_sequence=[chart_color])
            g_col2.plotly_chart(fig_box, use_container_width=True)
            
        if "Diagram Batang (Bar)" in chart_types:
            fig_bar = px.bar(data_clean, y=var, title=f"Diagram Urutan Data {var}", color_discrete_sequence=[chart_color])
            g_col1.plotly_chart(fig_bar, use_container_width=True)
            
        if "Diagram Lingkaran (Pie)" in chart_types:
            counts, bins = np.histogram(data_clean[var], bins=5)
            labels = [f"{bins[i]:.1f} - {bins[i+1]:.1f}" for i in range(len(counts))]
            pie_df = pd.DataFrame({'Interval': labels, 'Frekuensi': counts})
            fig_pie = px.pie(pie_df, values='Frekuensi', names='Interval', title=f"Proporsi Interval {var}")
            g_col2.plotly_chart(fig_pie, use_container_width=True)
            
        if "Tabel Distribusi Frekuensi" in chart_types:
            counts, bins = np.histogram(data_clean[var], bins='sturges')
            intervals = [f"[{bins[i]:.2f} : {bins[i+1]:.2f}]" for i in range(len(counts))]
    
