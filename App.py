import streamlit as st
import pandas as pd
import numpy as np

# 1. KUSTOMISASI TAMPILAN PROFESIONAL (Tema Aplikasi StatLab)
st.set_page_config(
    page_title="StatLab - Aplikasi Statistika Deskriptif Interaktif",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gaya CSS untuk mempercantik UI (Font, Warna Header, dan Kotak Informasi)
st.markdown("""
    <style>
    .main-title {
        font-size:32px !important;
        font-weight: bold;
        color: #1E3A8A; /* Biru Gelap Laboratorium */
        margin-bottom: 5px;
    }
    .sub-title {
        font-size:16px !important;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .section-header {
        font-size:22px !important;
        font-weight: 600;
        color: #1F2937;
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 5px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. TOMBOL NAVIGASI DI SIDEBAR (Menu Navigasi Kiri)
st.sidebar.image("https://flaticon.com", width=80) # Icon StatLab
st.sidebar.markdown("<h2 style='color: #1E3A8A; margin-bottom:0;'>StatLab Utama</h2>", unsafe_allow_html=True)
st.sidebar.write("UTS Statistika - Proyek Aplikasi")

# Menu Navigasi Utama
menu = st.sidebar.radio(
    "Navigasi Modul:",
    ["Dashboard & Unggah Data", "Analisis Statistika", "Visualisasi Data", "Informasi Aplikasi"]
)

# Petunjuk singkat di bagian bawah sidebar
st.sidebar.info("💡 **Tips:** Pastikan Anda mengunggah file terlebih dahulu di menu 'Dashboard & Unggah Data' sebelum membuka modul analisis.")

# Inisialisasi Data Global menggunakan Session State agar data tidak hilang saat pindah menu
if 'dataset' not in st.session_state:
    st.session_state['dataset'] = None

# ==========================================
# MODUL 1: DASHBOARD & UNGGAH DATA
# ==========================================
if menu == "Dashboard & Unggah Data":
    st.markdown('<p class="main-title">📊 StatLab Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Selamat datang di Laboratorium Komputasi Statistika Deskriptif Interaktif.</p>', unsafe_allow_html=True)
    
    st.markdown('<p class="section-header">1. Unggah Dataset Anda</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Format file yang didukung: Microsoft Excel (.xlsx, .xls) atau CSV", type=["xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                st.session_state['dataset'] = pd.read_csv(uploaded_file)
            else:
                st.session_state['dataset'] = pd.read_excel(uploaded_file)
            st.success(f"Sukses: File '{uploaded_file.name}' berhasil dimuat ke sistem StatLab.")
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")
            
    # Menampilkan preview tabel data jika sudah ada data terunggah
    if st.session_state['dataset'] is not None:
        df = st.session_state['dataset']
        st.markdown('<p class="section-header">2. Pratinjau Dataset (5 Data Teratas)</p>', unsafe_allow_html=True)
        st.dataframe(df.head(), use_container_width=True)
        
        # Informasi Matriks Data
        col1, col2, col3 = st.columns(3)
        col1.metric("Jumlah Baris Data", df.shape[0])
        col2.metric("Jumlah Kolom Variabel", df.shape[1])
        col3.metric("Data Kosong (Missing)", df.isnull().sum().sum())
        
        # Penanganan data kosong otomatis (Fitur Tambahan)
        if df.isnull().sum().sum() > 0:
            st.warning("⚠️ Terdeteksi data kosong pada dataset.")
            if st.button("Lakukan Imputasi Data Kosong (Isi Otomatis dengan Rata-rata/Mean)"):
                st.session_state['dataset'] = df.fillna(df.mean(numeric_only=True))
                st.experimental_rerun()
    else:
        st.info("Silakan unggah dataset Excel atau CSV Anda untuk memulai simulasi pengolahan data.")

# ==========================================
# MODUL 2: ANALISIS STATISTIKA DESKRIPTIF
# ==========================================
elif menu == "Analisis Statistika":
    st.markdown('<p class="main-title">📋 Modul Analisis Statistik</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Komputasi otomatis ukuran pemusatan, penyebaran, dan letak data secara presisi.</p>', unsafe_allow_html=True)
    
    if st.session_state['dataset'] is not None:
        df = st.session_state['dataset']
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            st.error("Format Error: Tidak ditemukan variabel numerik/angka di dalam file yang Anda unggah.")
        else:
            col_pilih1, col_pilih2 = st.columns([1, 1])
            
            with col_pilih1:
                st.markdown('**Pilih Variabel Numerik:**')
                selected_vars = st.multiselect("Bisa memilih lebih dari satu:", numeric_cols, default=numeric_cols[:1])
            
            with col_pilih2:
                st.markdown('**Pilih Ukuran Statistik (Parameter):**')
                all_metrics = ["N (Jumlah Data)", "Minimum", "Maksimum", "Mean", "Median", "Modus", "Varians", "Standar Deviasi", "Kuartil (Q1, Q2, Q3)"]
                selected_metrics = st.multiselect("Centang yang ingin ditampilkan:", all_metrics, default=all_metrics)
            
            if len(selected_vars) > 0 and len(selected_metrics) > 0:
                st.markdown('<p class="section-header">Hasil Komputasi Tabel Ringkasan Statistika Deskriptif</p>', unsafe_allow_html=True)
                
                summary_dict = {}
                for col in selected_vars:
                    col_summary = {}
                    data_col = df[col].dropna()
                    
                    if "N (Jumlah Data)" in selected_metrics: col_summary["N"] = int(len(data_col))
                    if "Minimum" in selected_metrics: col_summary["Minimum"] = data_col.min()
                    if "Maksimum" in selected_metrics: col_summary["Maksimum"] = data_col.max()
                    if "Mean" in selected_metrics: col_summary["Mean"] = round(data_col.mean(), 4)
                    if "Median" in selected_metrics: col_summary["Median"] = data_col.median()
                    if "Modus" in selected_metrics: 
                        modus_val = data_col.mode()
                        col_summary["Modus"] = modus_val.iloc[0] if not modus_val.empty else np.nan
                    if "Varians" in selected_metrics: col_summary["Varians"] = round(data_col.var(), 4)
                    if "Standar Deviasi" in selected_metrics: col_summary["Standar Deviasi"] = round(data_col.std(), 4)
                    if "Kuartil (Q1, Q2, Q3)" in selected_metrics:
                        col_summary["Q1 (Kuartil 1)"] = data_col.quantile(0.25)
                        col_summary["Q2 (Kuartil 2)"] = data_col.quantile(0.50)
                        col_summary["Q3 (Kuartil 3)"] = data_col.quantile(0.75)
                        
                    summary_dict[col] = col_summary
                
                summary_df = pd.DataFrame(summary_dict)
                st.dataframe(summary_df, use_container_width=True)
                
                # Tombol Ekspor Data / Download Ringkasan
                st.markdown("---")
                csv_data = summary_df.to_csv().encode('utf-8')
                st.download_button(
                    label="📥 Ekspor Laporan Ringkasan ke CSV",
                    data=csv_data,
                    file_name="Laporan_StatLab_Deskriptif.csv",
                    mime="text/csv"
                )
            else:
                st.warning("Mohon pilih setidaknya satu variabel dan satu ukuran statistik pada kolom di atas.")
    else:
        st.warning("⚠️ Menu terkunci. Anda harus mengunggah file data terlebih dahulu di menu 'Dashboard & Unggah Data'.")

# ==========================================
# MODUL 3: VISUALISASI DATA (FITUR TAMBAHAN)
# ==========================================
elif menu == "Visualisasi Data":
    st.markdown('<p class="main-title">📈 Modul Grafik & Visualisasi</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Pembuatan visualisasi distribusi data secara interaktif.</p>', unsafe_allow_html=True)
    
    if st.session_state['dataset'] is not None:
        df = st.session_state['dataset']
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            st.error("Tidak ditemukan kolom numerik untuk dibuatkan grafik.")
        else:
            col_v1, col_v2 = st.columns([1, 2])
            with col_v1:
                target_var = st.selectbox("Pilih Variabel yang akan digambar:", numeric_cols)
                chart_type = st.radio("Pilih Jenis Visualisasi:", ["Histogram Distribusi", "Line Chart Tren Data"])
            
            with col_v2:
                st.write(f"**Visualisasi Grafik untuk Variabel: {target_var}**")
                if chart_type == "Histogram Distribusi":
                    # Histogram menggunakan frekuensi distribusi data pembulatan
                    counts = df[target_var].value_counts().sort_index()
                    st.bar_chart(counts, color="#1E3A8A")
                elif chart_type == "Line Chart Tren Data":
                    st.line_chart(df[target_var], color="#EF4444")
    else:
        st.warning("⚠️ Menu terkunci. Silakan unggah berkas data terlebih dahulu di menu 'Dashboard & Unggah Data'.")

# ==========================================
# MODUL 4: INFORMASI APLIKASI
# ==========================================
elif menu == "Informasi Aplikasi":
    st.markdown('<p class="main-title">ℹ️ Informasi Sistem & Lembar Ujian</p>', unsafe_allow_html=True)
    
    # Menampilkan metadata ujian sesuai berkas soal UTS
    st.markdown("""
      
