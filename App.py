import streamlit as st
import pandas as pd
import numpy as np

# Konfigurasi Tema Halaman Utama StatLab
st.set_page_config(
    page_title="StatLab - Aplikasi Statistika Deskriptif",
    page_icon="📊",
    layout="wide"
)

# Pengaturan Desain Antarmuka Profesional via HTML/CSS
st.markdown("""
    <style>
    .main-title { font-size:28px !important; font-weight: bold; color: #1E3A8A; margin-bottom: 2px; }
    .tagline { font-size:14px !important; color: #4B5563; margin-bottom: 20px; }
    .card-box { background-color: #F3F4F6; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🔬 StatLab Deskriptif Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Laboratorium Komputasi Interaktif Ujian Tengah Semester</p>', unsafe_allow_html=True)

# Membuat Session State untuk Menyimpan Dataset agar Aman saat Berpindah Menu
if 'my_dataframe' not in st.session_state:
    st.session_state['my_dataframe'] = None

# ---- TOMBOL NAVIGASI UTAMA ----
menu_tab1, menu_tab2, menu_tab3, menu_tab4 = st.tabs([
    "📂 Unggah & Tampilkan Data", 
    "📊 Hitung Ukuran Statistik", 
    "📈 Modul Grafik Visualisasi", 
    "📋 Dokumen Lembar Ujian"
])

# ==========================================
# 1. MODUL UNGGAH & TAMPILKAN DATA
# ==========================================
with menu_tab1:
    st.subheader("Modul 1: Manajemen Dataset File")
    uploaded_file = st.file_uploader("Unggah dataset berkas Microsoft Excel (.xlsx, .xls) atau CSV", type=["xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                st.session_state['my_dataframe'] = pd.read_csv(uploaded_file)
            else:
                st.session_state['my_dataframe'] = pd.read_excel(uploaded_file)
            st.success("File sukses diunggah dan diverifikasi oleh sistem StatLab!")
        except Exception as err:
            st.error(f"Gagal membaca file berkas: {err}")
            
    if st.session_state['my_dataframe'] is not None:
        current_df = st.session_state['my_dataframe']
        
        # Penanganan Masalah Data Kosong (Missing Values)
        missing_count = int(current_df.isnull().sum().sum())
        
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown(f"**Struktur Matriks Data Saat Ini:**")
        st.write(f"- Total Sampel Baris: {current_df.shape[0]}")
        st.write(f"- Total Variabel Kolom: {current_df.shape[1]}")
        st.write(f"- Total Sel Data Kosong: {missing_count}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if missing_count > 0:
            st.warning("Peringatan: Dataset terdeteksi mengandung nilai kosong.")
            if st.button("Isi Semua Data Kosong dengan Rata-rata (Mean)"):
                st.session_state['my_dataframe'] = current_df.fillna(current_df.mean(numeric_only=True))
                st.write("Proses selesai! Data kosong telah diisi.")
                
        st.markdown("**Pratinjau Tabel Isi Dataset (5 Baris Pertama):**")
        st.dataframe(current_df.head(), use_container_width=True)
    else:
        st.info("Silakan unggah dataset Excel atau CSV Anda terlebih dahulu untuk membuka pengolahan menu lainnya.")

# ==========================================
# 2. MODUL HITUNG UKURAN STATISTIK
# ==========================================
with menu_tab2:
    st.subheader("Modul 2: Komputasi Parameter Statistika Deskriptif")
    if st.session_state['my_dataframe'] is not None:
        current_df = st.session_state['my_dataframe']
        # Menyaring hanya kolom bertipe angka saja
        numeric_columns = current_df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_columns) == 0:
            st.error("Gagal: Tidak ditemukan variabel numerik (angka) di dalam dataset Anda.")
        else:
            col_left, col_right = st.columns(2)
            with col_left:
                pilih_variabel = st.multiselect("Pilih Satu atau Beberapa Variabel:", numeric_columns, default=numeric_columns[:1])
            with col_right:
                opsi_metrik = ["N", "Minimum", "Maksimum", "Mean", "Median", "Modus", "Varians", "Standar Deviasi", "Kuartil (Q1, Q2, Q3)"]
                pilih_metrik = st.multiselect("Pilih Ukuran Statistik yang Dihitung:", opsi_metrik, default=opsi_metrik)
                
            if len(pilih_variabel) > 0 and len(pilih_metrik) > 0:
                st.markdown("**Tabel Hasil Ringkasan Statistika Deskriptif Otomatis:**")
                
                hasil_kamus = {}
                for var in pilih_variabel:
                    data_clean = current_df[var].dropna()
                    metrics_result = {}
                    
                    if "N" in pilih_metrik: 
                        metrics_result["N (Jumlah Data)"] = float(len(data_clean))
                    if "Minimum" in pilih_metrik: 
                        metrics_result["Minimum"] = float(data_clean.min())
                    if "Maksimum" in pilih_metrik: 
                        metrics_result["Maksimum"] = float(data_clean.max())
                    if "Mean" in pilih_metrik: 
                        metrics_result["Mean (Rata-rata)"] = round(float(data_clean.mean()), 4)
                    if "Median" in pilih_metrik: 
                        metrics_result["Median"] = float(data_clean.median())
                    if "Modus" in pilih_metrik: 
                        mode_series = data_clean.mode()
                        metrics_result["Modus"] = float(mode_series.iloc[0]) if not mode_series.empty else np.nan
                    if "Varians" in pilih_metrik: 
                        metrics_result["Varians"] = round(float(data_clean.var()), 4)
                    if "Standar Deviasi" in pilih_metrik: 
                        metrics_result["Standar Deviasi"] = round(float(data_clean.std()), 4)
                    if "Kuartil (Q1, Q2, Q3)" in pilih_metrik:
                        metrics_result["Kuartil 1 (Q1)"] = float(data_clean.quantile(0.25))
                        metrics_result["Kuartil 2 (Q2)"] = float(data_clean.quantile(0.50))
                        metrics_result["Kuartil 3 (Q3)"] = float(data_clean.quantile(0.75))
                        
                    hasil_kamus[var] = metrics_result
                
                df_report = pd.DataFrame(hasil_kamus)
                st.dataframe(df_report, use_container_width=True)
                
                # Fitur Ekspor Hasil ke Berkas File Luar CSV
                csv_bytes = df_report.to_csv().encode('utf-8')
                st.download_button(
                    label="📥 Unduh Ringkasan Hasil Analisis (.CSV)",
                    data=csv_bytes,
                    file_name="Laporan_Ringkasan_StatLab.csv",
                    mime="text/csv"
                )
            else:
                st.warning("Mohon pilih minimal 1 kolom variabel dan 1 item ukuran statistik di susunan atas.")
    else:
        st.warning("Akses Menu Terkunci: Silakan unggah file data Anda terlebih dahulu di Tab pertama.")

# ==========================================
# 3. MODUL GRAFIK VISUALISASI
# ==========================================
with menu_tab3:
    st.subheader("Modul 3: Visualisasi Grafik & Tabel Distribusi Frekuensi")
    if st.session_state['my_dataframe'] is not None:
        current_df = st.session_state['my_dataframe']
        numeric_columns = current_df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_columns) > 0:
            v_left, v_right = st.columns(2)
            with v_left:
                var_grafik = st.selectbox("Pilih Variabel untuk Grafik:", numeric_columns)
                jenis_grafik = st.radio("Pilih Model Visualisasi:", ["Histogram Distribusi", "Line Chart (Tren Garis)"])
            
            with v_right:
                st.markdown(f"**Tampilan Visualisasi Grafik Variabel: {var_grafik}**")
                counts_data = current_df[var_grafik].value_counts().sort_index()
                
                if jenis_grafik == "Histogram Distribusi":
                    st.bar_chart(counts_data, color="#1E3A8A")
                elif jenis_grafik == "Line Chart (Tren Garis)":
                    st.line_chart(current_df[var_grafik], color="#10B981")
                    
            # Tabel Distribusi Frekuensi Sederhana (Poin Tambahan)
            st.markdown("**Tabel Distribusi Frekuensi Variabel Terpilih:**")
            df_freq = pd.DataFrame({
                'Nilai Variabel': counts_data.index,
                'Frekuensi Absolut (F)': counts_data.values
            })
            st.dataframe(df_freq, use_container_width=True)
        else:
            st.error("Tidak ditemukan kolom bertipe numerik untuk pembuatan visualisasi.")
    else:
        st.warning("Akses Menu Terkunci: Silakan unggah file data Anda terlebih dahulu di Tab pertama.")

# ==========================================
# 4. DOKUMEN LEMBAR UJIAN
# ==========================================
with menu_tab4:
    st.subheader("Modul 4: Validasi Administrasi Lembar Ujian")
    st.markdown("""
    <div style="background-color: #F9FAFB; padding: 15px; border-radius: 8px; border: 1px solid #D1D5DB;">
        <h4 style="margin-top:0; color:#1E3A8A;">SPESIFIKASI DOKUMEN UTS STATISTIKA</h4>
        <p style="margin:4px 0; font-size:14px;"><b>Program Studi:</b> S-1 Matematika (Kelas 1B / Semester 1)</p>
        <p style="margin:4px 0; font-size:14px;"><b>Dosen Pengampu:</b> Prana Ugiana Gio</p>
        <p style="margin:4px 0; font-size:14px;"><b>Sifat Tugas:</b> Take Home (Proyek Aplikasi Interaktif)</p>
        <p style="margin:4px 0; font-size:14px;"><b>Hari / Tanggal Rilis:</b> Kamis, 15 Oktober 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
