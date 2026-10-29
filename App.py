import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Pengaturan judul halaman
st.set_page_config(page_title="Aplikasi Statistika Deskriptif", layout="wide")

st.title("📊 Aplikasi Interaktif Statistika Deskriptif")
st.write("Dibuat untuk memenuhi Tugas UTS Statistika")

# Inisialisasi DataFrame kosong di awal agar semua menu bisa langsung dirender
df = pd.DataFrame()
numeric_cols = []

# ==========================================
# 1. MENU METODE INPUT DATA (LANGSUNG TAMPIL)
# ==========================================
st.header("1. Metode Input Data")
input_method = st.radio(
    "Pilih cara memasukkan data:",
    ["Unggah File (Excel/CSV)", "Ketik Data Manual (Variabel & Nilai)"]
)

if input_method == "Unggah File (Excel/CSV)":
    uploaded_file = st.file_uploader("Pilih file Excel (.xlsx, .xls) atau CSV", type=["xlsx", "xls", "csv"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.success("File berhasil dimuat!")
            st.write("### Pratinjau Data:")
            st.dataframe(df.head(5))
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")

else:
    st.subheader("Input Variabel & Data Manual")
    st.write("Masukkan nama variabel dan nilai datanya (pisahkan angka dengan koma).")
    
    # Input Variabel Mandiri 1
    var1_name = st.text_input("Nama Variabel 1:", "Usia")
    var1_data = st.text_area(f"Nilai untuk {var1_name} (Contoh: 20, 21, 22, 25, 23):", "20, 22, 21, 23, 24, 22, 25")
    
    # Input Variabel Mandiri 2
    var2_name = st.text_input("Nama Variabel 2:", "Nilai_Ujian")
    var2_data = st.text_area(f"Nilai untuk {var2_name} (Contoh: 80, 85, 90, 75):", "85, 90, 78, 92, 88, 85, 80")
    
    # Proses konversi teks input manual menjadi DataFrame
    try:
        data_dict = {}
        if var1_data:
            list1 = [float(x.strip()) for x in var1_data.split(",") if x.strip() != ""]
            data_dict[var1_name] = pd.Series(list1)
        if var2_data:
            list2 = [float(x.strip()) for x in var2_data.split(",") if x.strip() != ""]
            data_dict[var2_name] = pd.Series(list2)
            
        if data_dict:
            df = pd.DataFrame(data_dict)
            st.success("Data manual berhasil dibuat!")
            st.write("### Pratinjau Data Manual:")
            st.dataframe(df)
            numeric_cols = df.columns.tolist()
    except ValueError:
        st.error("Format penulisan salah! Pastikan hanya memasukkan angka yang dipisahkan oleh tanda koma ( , ).")

# ==========================================
# 2. MENU PILIH VARIABEL (LANGSUNG TAMPIL)
# ==========================================
st.header("2. Pilih Variabel")
if len(numeric_cols) > 0:
    selected_vars = st.multiselect("Pilih satu atau beberapa variabel untuk dianalisis:", numeric_cols, default=numeric_cols[:1])
else:
    st.info("Silakan masukkan data terlebih dahulu agar variabel muncul di sini.")
    selected_vars = []

# Membuat Tata Letak Kolom untuk Menu 3 & Fitur Tambahan Grafik
col1, col2 = st.columns(2)

with col1:
    # ==========================================
    # 3. MENU UKURAN STATISTIK (LANGSUNG TAMPIL)
    # ==========================================
    st.header("3. Ukuran Statistik")
    options = [
        "Jumlah Data (N)", "Minimum", "Maksimum", "Mean", 
        "Median", "Modus", "Varians", "Standar Deviasi", 
        "Kuartil 1 (Q1)", "Kuartil 2 (Q2)", "Kuartil 3 (Q3)"
    ]
    selected_metrics = st.multiselect("Centang ukuran statistik yang ingin dihitung:", options, default=options[:5])

with col2:
    # ==========================================
    # 4. MENU VISUALISASI GRAFIK (LANGSUNG TAMPIL)
    # ==========================================
    st.header("📊 Visualisasi Data")
    chart_options = ["Tidak Ada", "Histogram", "Boxplot", "Diagram Batang (Bar Chart)"]
    selected_chart = st.selectbox("Pilih jenis grafik yang ingin digunakan:", chart_options)
    
    if selected_chart != "Tidak Ada" and len(selected_vars) > 0:
        var_to_plot = st.selectbox("Pilih variabel spesifik untuk grafik:", selected_vars)
    else:
        var_to_plot = None

# ==========================================
# 5. HALAMAN EKSEKUSI & HASIL AKHIR
# ==========================================
st.header("4. Hasil Analisis")

# Tombol Hitung Utama agar eksekusi rapi
if st.button("🚀 Jalankan Analisis & Kalkulasi"):
    if not df.empty and len(selected_vars) > 0 and len(selected_metrics) > 0:
        
        # --- Bagian 1: Kalkulasi Statistik Deskriptif ---
        summary_dict = {}
        for var in selected_vars:
            col_data = df[var].dropna()
            metrics_res = {}
            
            if "Jumlah Data (N)" in selected_metrics:
                metrics_res["Jumlah Data (N)"] = len(col_data)
            if "Minimum" in selected_metrics:
                metrics_res["Minimum"] = col_data.min() if not col_data.empty else np.nan
            if "Maksimum" in selected_metrics:
                metrics_res["Maksimum"] = col_data.max() if not col_data.empty else np.nan
            if "Mean" in selected_metrics:
                metrics_res["Mean"] = col_data.mean() if not col_data.empty else np.nan
            if "Median" in selected_metrics:
                metrics_res["Median"] = col_data.median() if not col_data.empty else np.nan
            if "Modus" in selected_metrics:
                if not col_data.empty:
                    mode_val = col_data.mode()
                    metrics_res["Modus"] = mode_val.iloc[0] if not mode_val.empty else np.nan
                else:
                    metrics_res["Modus"] = np.nan
            if "Varians" in selected_metrics:
                metrics_res["Varians"] = col_data.var() if not col_data.empty else np.nan
            if "Standar Deviasi" in selected_metrics:
                metrics_res["Standar Deviasi"] = col_data.std() if not col_data.empty else np.nan
            if "Kuartil 1 (Q1)" in selected_metrics:
                metrics_res["Kuartil 1 (Q1)"] = col_data.quantile(0.25) if not col_data.empty else np.nan
            if "Kuartil 2 (Q2)" in selected_metrics:
                metrics_res["Kuartil 2 (Q2)"] = col_data.quantile(0.50) if not col_data.empty else np.nan
            if "Kuartil 3 (Q3)" in selected_metrics:
                metrics_res["Kuartil 3 (Q3)"] = col_data.quantile(0.75) if not col_data.empty else np.nan
            
            summary_dict[var] = metrics_res
        
        summary_df = pd.DataFrame(summary_dict)
        st.success("Kalkulasi berhasil diselesaikan!")
        st.write("### Tabel Ringkasan Statistika Deskriptif:")
        st.dataframe(summary_df.T)
        
        # Fitur Unduh Hasil CSV
        csv_data = summary_df.T.to_csv().encode('utf-8')
        st.download_button(
            label="📥 Unduh Tabel Hasil (CSV)",
            data=csv_data,
            file_name='ringkasan_statistika.csv',
            mime='text/csv',
        )
        
        # --- Bagian 2: Penggambaran Grafik ---
        if selected_chart != "Tidak Ada" and var_to_plot:
            st.write(f"### Grafik Visualisasi: {selected_chart}")
            plot_data = df[var_to_plot].dropna()
            
            if not plot_data.empty:
                fig, ax = plt.subplots(figsize=(6, 3.5))
                
                if selected_chart == "Histogram":
                    sns.histplot(plot_data, kde=True, ax=ax, color="skyblue")
                    ax.set_ylabel("Frekuensi")
                elif selected_chart == "Boxplot":
                    sns.boxplot(y=plot_data, ax=ax, color="lightgreen")
                elif selected_chart == "Diagram Batang (Bar Chart)":
                    value_counts = plot_data.value_counts().sort_index()
                    sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax, palette="plasma")
                    ax.set_ylabel("Jumlah")
                    ax.set_xlabel(var_to_plot)
                
                ax.set_title(f"{selected_chart} - {var_to_plot}")
                st.pyplot(fig)
            else:
                st.warning("Data kosong, grafik tidak dapat dibuat.")
    else:
        st.error("⚠️ Mohon pastikan data sudah terisi, variabel sudah dipilih, dan minimal satu ukuran statistik telah dicentang.")
            
