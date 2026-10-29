import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Pengaturan judul halaman
st.set_page_config(page_title="Aplikasi Statistika Deskriptif", layout="wide")

st.title("📊 Aplikasi Interaktif Statistika Deskriptif & Visualisasi")
st.write("Dibuat untuk memenuhi Tugas UTS Statistika")

# 1. Fitur Unggah Data
st.header("1. Unggah Dataset")
uploaded_file = st.file_uploader("Pilih file Excel (.xlsx, .xls) atau CSV", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        # Membaca file berdasarkan formatnya
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("File berhasil diunggah!")
        st.write("### Tampilan Data (Maksimal 10 baris pertama):")
        st.dataframe(df.head(10))
        
        # Ambil kolom numerik saja
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            st.warning("Dataset tidak memiliki variabel numerik untuk dianalisis.")
        else:
            # 2. Pilih Variabel yang Dianalisis
            st.header("2. Pilih Variabel")
            selected_vars = st.multiselect("Pilih satu atau beberapa variabel numerik:", numeric_cols, default=numeric_cols[:1])
            
            if len(selected_vars) > 0:
                # Pembuatan Kolom Layout (Kiri untuk Statistik, Kanan untuk Grafik)
                col1, col2 = st.columns(2)
                
                with col1:
                    # 3. Pilih Ukuran Statistika Deskriptif
                    st.header("3. Ukuran Statistik")
                    options = [
                        "Jumlah Data (N)", "Minimum", "Maksimum", "Mean", 
                        "Median", "Modus", "Varians", "Standar Deviasi", 
                        "Kuartil 1 (Q1)", "Kuartil 2 (Q2)", "Kuartil 3 (Q3)"
                    ]
                    selected_metrics = st.multiselect("Pilih ukuran statistik:", options, default=options[:5])
                    
                    if len(selected_metrics) > 0:
                        summary_dict = {}
                        for var in selected_vars:
                            col_data = df[var].dropna() # Mengabaikan missing values
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
                        st.write("### Hasil Analisis Deskriptif")
                        st.dataframe(summary_df.T)
                        
                        # Fitur Unduh Hasil
                        csv_data = summary_df.T.to_csv().encode('utf-8')
                        st.download_button(
                            label="📥 Unduh Hasil (CSV)",
                            data=csv_data,
                            file_name='ringkasan_statistika.csv',
                            mime='text/csv',
                        )
                    else:
                        st.info("Silakan pilih minimal satu ukuran statistik.")
                
                with col2:
                    # B. Fitur Tambahan: Pilihan Visualisasi Data
                    st.header("📊 Visualisasi Data")
                    chart_options = ["Tidak Ada", "Histogram", "Boxplot", "Diagram Batang (Bar Chart)"]
                    selected_chart = st.selectbox("Pilih jenis grafik yang ingin digunakan:", chart_options)
                    
                    if selected_chart != "Tidak Ada":
                        # Memilih satu variabel spesifik untuk dijadikan grafik
                        var_to_plot = st.selectbox("Pilih variabel untuk dibuatkan grafik:", selected_vars)
                        plot_data = df[var_to_plot].dropna()
                        
                        if not plot_data.empty:
                            fig, ax = plt.subplots(figsize=(6, 4))
                            
                            if selected_chart == "Histogram":
                                sns.histplot(plot_data, kde=True, ax=ax, color="skyblue")
                                ax.set_title(f"Histogram - {var_to_plot}")
                                ax.set_ylabel("Frekuensi")
                                
                            elif selected_chart == "Boxplot":
                                sns.boxplot(y=plot_data, ax=ax, color="lightgreen")
                                ax.set_title(f"Boxplot - {var_to_plot}")
                                
                            elif selected_chart == "Diagram Batang (Bar Chart)":
                                # Berguna jika variabel berupa data diskrit/skala nilai tertentu
                                value_counts = plot_data.value_counts().sort_index()
                                sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax, palette="plasma")
                                ax.set_title(f"Diagram Batang - {var_to_plot}")
                                ax.set_ylabel("Jumlah")
                                ax.set_xlabel(var_to_plot)
                            
                            st.pyplot(fig)
                        else:
                            st.warning("Data kosong, tidak dapat membuat grafik.")
            else:
                st.info("Silakan pilih minimal satu variabel untuk dianalisis.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Menunggu unggahan file...")
                            
