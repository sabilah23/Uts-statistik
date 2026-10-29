import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman Utama ala Lab Profesional
st.set_page_config(
    page_title="StatLab - Interactive Desktop", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kustomisasi CSS untuk mempercantik tampilan di HP & Browser
st.markdown("""
    <style>
    .main-title { font-size:2.5rem; font-weight:800; color:#1E3A8A; text-align:center; margin-bottom:0.5rem; }
    .subtitle { text-align:center; color:#6B7280; font-size:1.1rem; margin-bottom:2rem; }
    .stat-card { background-color:#F3F4F6; padding:20px; border-radius:10px; border-left:5px solid #3B82F6; margin-bottom:10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧪 StatLab: Virtual Statistical Laboratory</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Platform Pengolahan Data & Visualisasi Statistika Deskriptif Otomatis</div>', unsafe_allow_html=True)

# Inisialisasi awal variabel data
df = pd.DataFrame()
numeric_cols = []

# =========================================================================
# PANEL NAVIGASI UTAMA (Menggunakan Sidebar & Ekspander agar Rapi di HP)
# =========================================================================
with st.sidebar:
    st.image("https://icons8.com", width=80)
    st.header("⚙️ Kontrol Laboratorium")
    
    # Pilihan Metode Input Data
    input_method = st.radio(
        "Pilih Sumber Data:",
        ["📁 Unggah File (Excel/CSV)", "✍️ Ketik Data Manual"]
    )
    
    st.markdown("---")
    st.subheader("🎨 Pengaturan Grafis")
    # Fitur Ekstra: Pilihan palet warna visualisasi ala StatLab
    theme_color = st.selectbox("Palet Warna Grafik:", ["Deep Ocean (Blue)", "Emerald Nature (Green)", "Magma Sunset", "Cyberpunk"])
    
    st.info("💡 Semua perubahan parameter di panel ini akan langsung memperbarui kalkulasi lab secara otomatis.")

# =========================================================================
# STRUKTUR KOTAK INPUT (Halaman Utama Bagian Atas)
# =========================================================================
st.subheader("📥 Struktur & Pemasukan Data")

if "📁 Unggah File" in input_method:
    uploaded_file = st.file_uploader("Pilih dokumen data (.xlsx, .xls, .csv)", type=["xlsx", "xls", "csv"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.toast("Sukses: Dokumen berhasil diunggah ke laboratorium!", icon="✅")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        except Exception as e:
            st.error(f"Gagal membaca file dokumen: {e}")
else:
    # Mode Mengetik Data Manual langsung di Layar
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        var1_name = st.text_input("Nama Variabel A:", "Nilai_Statistika")
        var1_data = st.text_area("Input Nilai (Pisahkan dengan koma):", "75, 80, 85, 90, 65, 70, 85, 95, 80, 88")
    with col_in2:
        var2_name = st.text_input("Nama Variabel B:", "Jam_Belajar")
        var2_data = st.text_area("Input Nilai (Pisahkan dengan koma):", "4, 5, 6, 7, 3, 4, 6, 8, 5, 6")
        
    try:
        data_dict = {}
        if var1_data:
            data_dict[var1_name] = [float(x.strip()) for x in var1_data.split(",") if x.strip() != ""]
        if var2_data:
            data_dict[var2_name] = [float(x.strip()) for x in var2_data.split(",") if x.strip() != ""]
        if data_dict:
            # Cari panjang maksimum agar tidak error jika jumlah data tidak sama
            max_len = max(len(v) for v in data_dict.values())
            for k in data_dict:
                while len(data_dict[k]) < max_len:
                    data_dict[k].append(np.nan) # Berikan nilai kosong jika tidak seimbang
            df = pd.DataFrame(data_dict)
            numeric_cols = df.columns.tolist()
    except ValueError:
        st.error("⚠️ Kesalahan Ketik: Pastikan hanya memasukkan angka yang dipisahkan tanda koma.")

# Memastikan data tersedia sebelum merender Lab Workspace
if not df.empty and len(numeric_cols) > 0:
    
    # Tampilkan Pratinjau Data dengan Expandable Tab yang interaktif
    with st.expander("🔍 Lihat Matriks Data Laboratorium", expanded=False):
        st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    
    # =========================================================================
    # LAB WORKSPACE (Menggunakan Pemisah Tab Eksklusif ala StatLab)
    # =========================================================================
    tab1, tab2, tab3 = st.tabs(["🔢 Ringkasan Statistika", "📊 Ruang Visualisasi", "📝 Interpretasi Lab"])
    
    # Penentuan Warna Berdasarkan Pilihan Tema
    color_map = {"Deep Ocean (Blue)": "skyblue", "Emerald Nature (Green)": "seagreen", "Magma Sunset": "magma", "Cyberpunk": "coolwarm"}
    sns_palette = color_map[theme_color]
    single_color = "skyblue" if theme_color=="Deep Ocean (Blue)" else "mediumseagreen" if theme_color=="Emerald Nature (Green)" else "#ff7f0e" if theme_color=="Magma Sunset" else "#e377c2"

    # --- TAB 1: KALKULASI PARAMETER STATISTIKA ---
    with tab1:
        st.subheader("📐 Pengukuran Parameter Deskriptif")
        
        col_select1, col_select2 = st.columns([1, 2])
        with col_select1:
            selected_vars = st.multiselect("Variabel Target:", numeric_cols, default=numeric_cols)
        with col_select2:
            options = ["N", "Min", "Max", "Mean", "Median", "Modus", "Varians", "Standar Deviasi", "Q1", "Q2", "Q3"]
            selected_metrics = st.multiselect("Parameter Ukuran:", options, default=options[:5])
            
        if selected_vars and selected_metrics:
            summary_dict = {}
            for var in selected_vars:
                c_data = df[var].dropna()
                res = {}
                if "N" in selected_metrics: res["Jumlah Data (N)"] = len(c_data)
                if "Min" in selected_metrics: res["Minimum"] = c_data.min() if not c_data.empty else np.nan
                if "Max" in selected_metrics: res["Maksimum"] = c_data.max() if not c_data.empty else np.nan
                if "Mean" in selected_metrics: res["Mean (Rata-rata)"] = round(c_data.mean(), 3) if not c_data.empty else np.nan
                if "Median" in selected_metrics: res["Median"] = c_data.median() if not c_data.empty else np.nan
                if "Modus" in selected_metrics: 
                    res["Modus"] = c_data.mode().iloc[0] if not c_data.empty and not c_data.mode().empty else np.nan
                if "Varians" in selected_metrics: res["Varians"] = round(c_data.var(), 3) if not c_data.empty else np.nan
                if "Standar Deviasi" in selected_metrics: res["Standar Deviasi"] = round(c_data.std(), 3) if not c_data.empty else np.nan
                if "Q1" in selected_metrics: res["Kuartil 1 (Q1)"] = c_data.quantile(0.25) if not c_data.empty else np.nan
                if "Q2" in selected_metrics: res["Kuartil 2 (Q2)"] = c_data.quantile(0.50) if not c_data.empty else np.nan
                if "Q3" in selected_metrics: res["Kuartil 3 (Q3)"] = c_data.quantile(0.75) if not c_data.empty else np.nan
                summary_dict[var] = res
            
            summary_df = pd.DataFrame(summary_dict).T
            
            # Tampilan Tabel Dashboard Utama
            st.dataframe(summary_df, use_container_width=True)
            
            # Tombol Ekspor Hasil Lab
            csv = summary_df.to_csv().encode('utf-8')
            st.download_button("📥 Ekspor Tabel ke CSV", csv, "statlab_report.csv", "text/csv")
            
            # Cetak Kartu Metrik Singkat (KPI Cards) untuk Variabel Pertama sebagai visual interaktif
            st.write("### 📌 Sorotan Utama (Variabel Pertama):")
            v1 = selected_vars[0]
            v1_data = df[v1].dropna()
            if not v1_data.empty:
                kpi1, kpi2, kpi3 = st.columns(3)
                kpi1.metric(label=f"Rata-rata {v1}", value=f"{round(v1_data.mean(), 2)}")
                kpi2.metric(label=f"Total Data {v1}", value=f"{len(v1_data)} subjek")
                kpi3.metric(label=f"Nilai Tertinggi", value=f"{v1_data.max()}")
        else:
            st.warning("Silakan tentukan variabel dan ukuran statistik pada opsi di atas.")

    # --- TAB 2: RUANG VISUALISASI DATA INTERAKTIF ---
    with tab2:
        st.subheader("📈 Pembuat Grafik Lab Otomatis")
        c_col1, c_col2 = st.columns([1, 3])
        
        with c_col1:
            chart_type = st.radio("Pilih Tipe Grafik:", ["Histogram Densitas", "Box & Whisker Plot", "Diagram Batang"])
            var_plot = st.selectbox("Pilih Variabel Analisis Grafik:", selected_vars if 'selected_vars' in locals() and selected_vars else numeric_cols)
            
        with c_col2:
            plot_data = df[var_plot].dropna()
            if not plot_data.empty:
                fig, ax = plt.subplots(figsize=(7, 4))
                
                if chart_type == "Histogram Densitas":
                    sns.histplot(plot_data, kde=True, ax=ax, color=single_color)
                    ax.set_ylabel("Kerapatan (Frekuensi)")
                elif chart_type == "Box & Whisker Plot":
                    sns.boxplot(x=plot_data, ax=ax, color=single_color)
                    ax.set_xlabel("Distribusi Nilai")
                elif chart_type == "Diagram Batang":
                    v_counts = plot_data.value_counts().sort_index()
                    if theme_color in ["Magma Sunset", "Cyberpunk"]:
                        sns.barplot(x=v_counts.index, y=v_counts.values, ax=ax, palette=sns_palette)
else:
    
