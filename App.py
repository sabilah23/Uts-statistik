import streamlit as st
import pandas as pd
import numpy as np

# 1. KONFIGURASI UTAMA HALAMAN STATLAB
st.set_page_config(
    page_title="StatLab Pro - Analisis Data",
    page_icon="🔬",
    layout="wide"
)

# Kustomisasi Gaya Visual Antarmuka
st.markdown("""
    <style>
    .main-title { font-size:28px !important; font-weight: bold; color: #1E3A8A; margin-bottom: 2px; }
    .tagline { font-size:14px !important; color: #4B5563; margin-bottom: 20px; }
    .card-box { background-color: #F3F4F6; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🔬 StatLab Deskriptif Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Sistem Komputasi Data Interaktif - Bebas Input Tanpa Batasan File</p>', unsafe_allow_html=True)

# 2. PENGATURAN SUMBER DATA (FILE UPLOAD VS INPUT MANUAL)
st.subheader("📂 Sumber Masukan Data")
opsi_input = st.radio("Pilih Metode Pemasukan Data:", ["Gunakan Data Contoh (Bawaan)", "Ketik Data Manual (Tanpa File)", "Unggah File Excel/CSV"])

# Inisialisasi awal variabel data kosong
df_aktif = None

if opsi_input == "Gunakan Data Contoh (Bawaan)":
    # Data contoh instan agar aplikasi langsung bisa dicoba tanpa input apapun
    data_dummy = {
        'Usia':,
        'Tinggi_Badan':,
        'Nilai_Ujian': [85, 90, 78, 88, 92, 80, 85, 87, 95, 83]
    }
    df_aktif = pd.DataFrame(data_dummy)
    st.info("Menggunakan dataset contoh bawaan StatLab (Usia, Tinggi Badan, Nilai Ujian). Anda bisa langsung masuk ke modul analisis.")

elif opsi_input == "Ketik Data Manual (Tanpa File)":
    st.markdown('<div class="card-box"><b>Panduan Ketik Data Manual:</b> Masukkan nama variabel dan ketikkan angka data dipisahkan dengan tanda koma ( , ). Contoh: 80, 85, 90, 75</div>', unsafe_allow_html=True)
    
    nama_var1 = st.text_input("Nama Variabel 1:", "Variabel_A")
    input_var1 = st.text_area("Masukkan Data Angka Variabel 1 (pisahkan dengan koma):", "10, 20, 30, 40, 50")
    
    nama_var2 = st.text_input("Nama Variabel 2 (Opsional):", "Variabel_B")
    input_var2 = st.text_area("Masukkan Data Angka Variabel 2 (pisahkan dengan koma):", "15, 25, 35, 45, 55")
    
    try:
        list_var1 = [float(x.strip()) for x in input_var1.split(",") if x.strip() != ""]
        list_var2 = [float(x.strip()) for x in input_var2.split(",") if x.strip() != ""]
        
        # Penyelarasan panjang array data agar tidak error saat dikonversi ke tabel
        panjang_maks = max(len(list_var1), len(list_var2))
        while len(list_var1) < panjang_maks: list_var1.append(np.nan)
        while len(list_var2) < panjang_maks: list_var2.append(np.nan)
        
        df_aktif = pd.DataFrame({nama_var1: list_var1, nama_var2: list_var2})
        st.success("Data manual berhasil diproses ke dalam matriks sistem!")
    except ValueError:
        st.error("Format Error: Pastikan input Anda hanya berisi angka-angka yang dipisahkan oleh tanda koma.")

elif opsi_input == "Unggah File Excel/CSV":
    uploaded_file = st.file_uploader("Unggah dataset berkas Microsoft Excel (.xlsx, .xls) atau CSV", type=["xlsx", "xls", "csv"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_aktif = pd.read_csv(uploaded_file)
            else:
                df_aktif = pd.read_excel(uploaded_file)
            st.success("File sukses diunggah!")
        except Exception as err:
            st.error(f"Gagal membaca berkas: {err}")

# Tampilkan preview data jika data sudah siap
if df_aktif is not None:
    st.markdown("**Pratinjau Tabel Struktur Data Terkini:**")
    st.dataframe(df_aktif.head(5), use_container_width=True)

# 3. TOMBOL NAVIGASI UTAMA (TABS INTERAKTIF)
menu_tab1, menu_tab2, menu_tab3 = st.tabs([
    "📊 Modul Analisis Statistik", 
    "📈 Modul Grafik Visualisasi", 
    "📋 Lembar Spesifikasi Ujian"
])

# ==========================================
# TAB 1: MODUL ANALISIS STATISTIK
# ==========================================
with menu_tab1:
    st.subheader("Komputasi Parameter Statistika Deskriptif")
    if df_aktif is not None:
        numeric_columns = df_aktif.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_columns) == 0:
            st.error("Tidak ditemukan kolom numerik bertipe angka untuk dihitung.")
        else:
            col_left, col_right = st.columns(2)
            with col_left:
                pilih_variabel = st.multiselect("Centang Pilihan Variabel:", numeric_columns, default=numeric_columns[:1])
            with col_right:
                opsi_metrik = ["N", "Minimum", "Maksimum", "Mean", "Median", "Modus", "Varians", "Standar Deviasi", "Kuartil (Q1, Q2, Q3)"]
                pilih_metrik = st.multiselect("Centang Opsi Parameter Statistik:", opsi_metrik, default=opsi_metrik)
                
            if len(pilih_variabel) > 0 and len(pilih_metrik) > 0:
                hasil_kamus = {}
                for var in pilih_variabel:
                    data_clean = df_aktif[var].dropna()
                    metrics_result = {}
                    
                    if "N" in pilih_metrik: metrics_result["N (Jumlah Data)"] = float(len(data_clean))
                    if "Minimum" in pilih_metrik: metrics_result["Minimum"] = float(data_clean.min())
                    if "Maksimum" in pilih_metrik: metrics_result["Maksimum"] = float(data_clean.max())
                    if "Mean" in pilih_metrik: metrics_result["Mean (Rata-rata)"] = round(float(data_clean.mean()), 4)
                    if "Median" in pilih_metrik: metrics_result["Median"] = float(data_clean.median())
                    if "Modus" in pilih_metrik: 
                        mode_series = data_clean.mode()
                        metrics_result["Modus"] = float(mode_series.iloc[0]) if not mode_series.empty else np.nan
                    if "Varians" in pilih_metrik: metrics_result["Varians"] = round(float(data_clean.var()), 4)
                    if "Standar Deviasi" in pilih_metrik: metrics_result["Standar Deviasi"] = round(float(data_clean.std()), 4)
                    if "Kuartil (Q1, Q2, Q3)" in pilih_metrik:
                        metrics_result["Kuartil 1 (Q1)"] = float(data_clean.quantile(0.25))
                        metrics_result["Kuartil 2 (Q2)"] = float(data_clean.quantile(0.50))
                        metrics_result["Kuartil 3 (Q3)"] = float(data_clean.quantile(0.75))
                        
                    hasil_kamus[var] = metrics_result
                
                df_report = pd.DataFrame(hasil_kamus)
                st.dataframe(df_report, use_container_width=True)
                
                csv_bytes = df_report.to_csv().encode('utf-8')
                st.download_button(
                    label="📥 Unduh Ringkasan Hasil Analisis (.CSV)",
                    data=csv_bytes,
                    file_name="Laporan_StatLab.csv",
                    mime="text/csv"
                )
    else:
        st.warning("Silakan tentukan sumber masukan data terlebih dahulu di bagian atas.")

# ==========================================
# TAB 2: MODUL GRAFIK VISUALISASI MULTIPLE
# ==========================================
with menu_tab2:
    st.subheader("Pilihan Visualisasi Grafik Interaktif Multi-Variasi")
    if df_aktif is not None:
        numeric_columns = df_aktif.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_columns) > 0:
            v_left, v_right = st.columns(2)
            with v_left:
                var_grafik = st.selectbox("Pilih Variabel untuk Grafik:", numeric_columns, key="select_grafik")
                jenis_grafik = st.selectbox("Pilih Jenis Model Grafik:", [
                    "Bar Chart (Grafik Batang)", 
                    "Line Chart (Grafik Garis)", 
                    "Area Chart (Grafik Area Spasial)",
                    "Horizontal Bar Chart (Distribusi Nilai)"
                ])
            
            with v_right:
                st.markdown(f"**Visualisasi Grafik Variabel: {var_grafik}**")
                counts_data = df_aktif[var_grafik].value_counts().sort_index()
                
                if jenis_grafik == "Bar Chart (Grafik Batang)":
                    st.bar_chart(counts_data, color="#1E3A8A")
                elif jenis_grafik == "Line Chart (Grafik Garis)":
                    st.line_chart(df_aktif[var_grafik], color="#10B981")
                elif jenis_grafik == "Area Chart (Grafik Area Spasial)":
                    st.area_chart(df_aktif[var_grafik], color="#F59E0B")
                elif jenis_grafik == "Horizontal Bar Chart (Distribusi Nilai)":
                    st.bar_chart(counts_data, horizontal=True, color="#8B5CF6")
                    
            # Tabel Distribusi Frekuensi Pelengkap Otomatis
            st.markdown("**Tabel Distribusi Frekuensi:**")
            df_freq = pd.DataFrame({
                'Nilai Data': counts_data.index,
                'Frekuensi Muncul (F)': counts_data.values
            })
            st.dataframe(df_freq, use_container_width=True)
        else:
            st.error("Tidak ditemukan variabel bertipe angka untuk digambar.")
    else:
        st.warning("Silakan tentukan sumber masukan data terlebih dahulu di bagian atas.")

# ==========================================
# TAB 3: LEMBAR SPESIFIKASI UJIAN
# ==========================================
with menu_tab3:
    st.markdown("""
    <div style="background-color: #F9FAFB; padding: 15px; border-radius: 8px; border: 1px solid #D1D5DB;">
        <h4 style="margin-top:0; color:#1E3A8A;">LEMBAR SPESIFIKASI AKADEMIK UTS</h4>
        <p style="margin:4px 0; font-size:14px;"><b>Mata Kuliah:</b> Statistika</p>
