import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# 1. KONFIGURASI Halaman & TEMA STATLAB
# ==========================================
st.set_page_config(
    page_title="StatLab Pro - Solusi Analisis Data",
    page_icon="🔬",
    layout="wide"
)

# Gaya CSS Kustom Profesional (Gaya Lab Statistik Modern)
st.markdown("""
    <style>
    .main-header {
        font-size: 28px !important;
        font-weight: 700;
        color: #0F172A; /* Slate Dark */
        margin-bottom: 2px;
    }
    .tagline {
        font-size: 14px !important;
        color: #64748B; /* Muted text */
        margin-bottom: 20px;
    }
    .card {
        background-color: #F8FAFC;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 15px;
    }
    .metric-box {
        background-color: #EFF6FF;
        padding: 10px;
        border-radius: 6px;
        text-align: center;
        border: 1px solid #BFDBFE;
    }
    </style>
    """, unsafe_allow_html=True)

# Header Aplikasi
st.markdown('<div class="main-header">🔬 StatLab Pro v2.0</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Sistem Komputasi & Pengolahan Data Statistika Deskriptif Terpadu</div>', unsafe_allow_html=True)

# Menyimpan Data Menggunakan Session State
if 'data_makro' not in st.session_state:
    st.session_state['data_makro'] = None

# ==========================================
# 2. TOMBOL NAVIGASI UTAMA (TABS TAMPILAN ATAS)
# ==========================================
tab_dashboard, tab_analisis, tab_visualisasi, tab_dokumen = st.tabs([
    "📂 Repositori Data", 
    "📊 Modul Analisis", 
    "📈 Visualisasi Distribusi", 
    "📋 Lembar Kerja UTS"
])

# ==========================================
# TAB 1: REPOSITORI DATA
# ==========================================
with tab_dashboard:
    st.subheader("1. Unggah Dataset Riset")
    file_masuk = st.file_uploader("Pilih berkas format Microsoft Excel (.xlsx, .xls) atau CSV [wajib]", type=["xlsx", "xls", "csv"])
    
    if file_masuk is not None:
        try:
            if file_masuk.name.endswith('.csv'):
                st.session_state['data_makro'] = pd.read_csv(file_masuk)
            else:
                st.session_state['data_makro'] = pd.read_excel(file_masuk)
            st.toast("Data sukses diunggah ke server StatLab!", icon="✅")
        except Exception as kegagalan:
            st.error(f"Gagal memproses berkas: {kegagalan}")
            
    # Tampilan jika data sudah terunggah
    if st.session_state['data_makro'] is not None:
        df = st.session_state['data_makro']
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### Ringkasan Struktur Data Berhasil Dimuat:")
        
        # Grid Metriks Indikator Data
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-box"><b>Total Sampel (Baris):</b><br><span style="font-size:20px; color:#1E3A8A;">{df.shape[0]}</span></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-box"><b>Total Variabel (Kolom):</b><br><span style="font-size:20px; color:#1E3A8A;">{df.shape[1]}</span></div>', unsafe_allow_html=True)
        with m3:
            total_missing = df.isnull().sum().sum()
            warna_missing = "#10B981" if total_missing == 0 else "#EF4444"
            st.markdown(f'<div class="metric-box"><b>Data Kosong (Missing):</b><br><span style="font-size:20px; color:{warna_missing};">{total_missing}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Penanganan Data Kosong Eksploratif (Poin Kreativitas Nilai Tambah)
        if total_missing > 0:
            st.warning("⚠️ Perhatian: Sistem mendeteksi adanya data kosong pada dataset Anda.")
            if st.button("Lakukan Pembersihan Otomatis (Imputasi Mean)"):
                st.session_state['data_makro'] = df.fillna(df.mean(numeric_only=True))
                st.rerun()
                
        st.markdown("##### Tabel Data Pratinjau (5 Baris Teratas):")
        st.dataframe(df.head(), use_container_width=True)
    else:
        st.info("💡 **Petunjuk Awal:** Silakan unggah berkas data Anda di atas terlebih dahulu untuk membuka kunci fitur modul analisis dan grafik.")

# ==========================================
# TAB 2: MODUL ANALISIS STATISTIKA
# ==========================================
with tab_analisis:
    if st.session_state['data_makro'] is not None:
        df = st.session_state['data_makro']
        kolom_angka = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(kolom_angka) == 0:
            st.error("Kesalahan validasi data: Tidak ditemukan variabel numerik untuk dihitung.")
        else:
            st.write("### ⚙️ Konfigurasi Parameter Analisis")
            
            # Layout Seleksi Parameter
            s1, s2 = st.columns([1, 1])
            with s1:
                variabel_terpilih = st.multiselect("Pilih Variabel yang akan Dihitung:", kolom_angka, default=kolom_angka[:1])
            with s2:
                parameter_wajib = ["N", "Minimum", "Maksimum", "Mean", "Median", "Modus", "Varians", "Standar Deviasi", "Kuartil (Q1, Q2, Q3)"]
                parameter_terpilih = st.multiselect("Pilih Metrik Indikator Statistika:", parameter_wajib, default=parameter_wajib)
                
            if len(variabel_terpilih) > 0 and len(parameter_terpilih) > 0:
                st.write("### 📋 Hasil Ringkasan Deskriptif Eksklusif")
                
                matriks_hasil = {}
                for var in variabel_terpilih:
                    sub_hasil = {}
                    data_clean = df[var].dropna()
                    
                    if "N" in parameter_terpilih: sub_hasil["N (Jumlah Data)"] = int(len(data_clean))
                    if "Minimum" in parameter_terpilih: sub_hasil["Minimum"] = data_clean.min()
                    if "Maksimum" in parameter_terpilih: sub_hasil["Maksimum"] = data_clean.max()
                    if "Mean" in parameter_terpilih: sub_hasil["Mean (Rata-rata)"] = round(data_clean.mean(), 4)
                    if "Median" in parameter_terpilih: sub_hasil["Median"] = data_clean.median()
                    if "Modus" in parameter_terpilih: 
                        md = data_clean.mode()
                        sub_hasil["Modus"] = md.iloc[0] if not md.empty else np.nan
                    if "Varians" in parameter_terpilih: sub_hasil["Varians"] = round(data_clean.var(), 4)
                    if "Standar Deviasi" in parameter_terpilih: sub_hasil["Standar Deviasi"] = round(data_clean.std(), 4)
                    if "Kuartil (Q1, Q2, Q3)" in parameter_terpilih:
                        sub_hasil["Kuartil 1 (Q1)"] = data_clean.quantile(0.25)
                        sub_hasil["Kuartil 2 (Q2/Med)"] = data_clean.quantile(0.50)
                        sub_hasil["Kuartil 3 (Q3)"] = data_clean.quantile(0.75)
                        
                    matriks_hasil[var] = sub_hasil
                
                df_akhir = pd.DataFrame(matriks_hasil)
                st.dataframe(df_akhir.style.highlight_max(axis=1, color='#D1FAE5').highlight_min(axis=1, color='#FEE2E2'), use_container_width=True)
                
                # Fitur Unduh Ekspor Data Ringkasan Hasil
                csv_siap = df_akhir.to_csv().encode('utf-8')
                st.download_button(
                    label="📥 Ekspor Tabel Hasil ke CSV",
                    data=csv_siap,
                    file_name="Laporan_StatLab_Pro.csv",
                    mime="text/csv"
                )
            else:
                st.warning("Silakan tentukan minimal 1 variabel dan 1 metrik parameter statistik di atas.")
    else:
        st.warning("Akses Ditolak: Anda belum memasukkan berkas data pada Tab 'Repositori Data'.")

# ==========================================
# TAB 3: VISUALISASI DISTRIBUSI
# ==========================================
with tab_visualisasi:
    if st.session_state['data_makro'] is not None:
        df = st.session_state['data_makro']
        kolom_angka = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(kolom_angka) > 0:
            st.write("### 📊 Pembuat Grafik Interaktif")
            v_col1, v_col2 = st.columns([1, 2])
            
            with v_col1:
                pilih_var_grafik = st.selectbox("Pilih Variabel Analisis:", kolom_angka)
                tipe_grafik = st.radio("Metode Visualisasi Grafis:", ["Histogram Distribusi", "Line Chart (Tren Runtun Waktu)"])
                
            with v_col2:
                st.info(f"Menampilkan {tipe_grafik} untuk Variabel: **{pilih_var_grafik}**")
                if tipe_grafik == "Histogram Distribusi":
                    frekuensi = df[pilih_var_grafik].value_counts().sort_index()
                    st.bar_chart(frekuensi, color="#0284C7")
                elif tipe_grafik == "Line Chart (Tren Runtun Waktu)":
                    st.line_chart(df[pilih_var_grafik], color="#10B981")
        else:
            st.error("Tidak ditemukan data angka untuk pembuatan grafik.")
    else:
        st.warning("Akses Ditolak: Anda belum memasukkan berkas data pada Tab 'Repositori Data'.")

# ==========================================
# TAB 4: LEMBAR KERJA UTS (INFORMASI AKADEMIK)
# ==========================================
with tab_dokumen:
    st.write("### 📝 Lembar Kendali Mutu Ujian")
    st.markdown("""
    <div style="background-color: #F8FAFC; padding: 20px; border-radius: 8px; border: 1px solid #CBD5E1;">
        <h4 style="color:#0F172A; margin-top:0;">INFORMASI UJIAN TENGAH SEMESTER (UTS)</h4>
        <hr style="margin: 10px 0;">
        <table style="width:100%; font-size:14px; border-collapse:collapse;">
