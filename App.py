import streamlit as st
import pandas as pd
import numpy as np

# Pengaturan halaman
st.set_page_config(page_title="Kalkulator Statistika Deskriptif", layout="wide")

st.title("📊 Aplikasi Analisis Statistika Deskriptif")
st.write("Dibuat untuk memenuhi Tugas UTS Statistika.")

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
        
        st.success("Data berhasil diunggah!")
        st.dataframe(df.head()) # Menampilkan 5 data teratas dalam bentuk tabel
        
        # Penanganan data kosong (Fitur Tambahan)
        if df.isnull().sum().sum() > 0:
            st.warning("Peringatan: Terdapat data kosong (missing values) pada dataset Anda.")
            if st.checkbox("Isi data kosong dengan nilai rata-rata (mean)?"):
                df = df.fillna(df.mean(numeric_only=True))
                st.info("Data kosong berhasil diisi.")
        
        # Filter hanya kolom numerik
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            st.error("Tidak ada variabel numerik di dalam dataset ini!")
        else:
            # 2. Fitur Pilih Variabel
            st.header("2. Pilih Variabel")
            selected_vars = st.multiselect("Pilih satu atau beberapa variabel untuk dianalisis:", numeric_cols)
            
            if len(selected_vars) > 0:
                # 3. Fitur Pilih Ukuran Statistik
                st.header("3. Pilih Ukuran Statistik")
                all_metrics = ["N (Jumlah Data)", "Minimum", "Maksimum", "Mean", "Median", "Modus", "Varians", "Standar Deviasi", "Kuartil (Q1, Q2, Q3)"]
                selected_metrics = st.multiselect("Pilih ukuran statistik yang ingin dihitung:", all_metrics, default=all_metrics)
                
                if len(selected_metrics) > 0:
                    st.header("4. Hasil Analisis")
                    
                    # Wadah untuk menampung hasil perhitungan
                    summary_dict = {}
                    
                    for col in selected_vars:
                        col_summary = {}
                        data_col = df[col].dropna() # Mengabaikan NaN saat berhitung
                        
                        # Hitung otomatis sesuai pilihan pengguna
                        if "N (Jumlah Data)" in selected_metrics:
                            col_summary["N"] = len(data_col)
                        if "Minimum" in selected_metrics:
                            col_summary["Minimum"] = data_col.min()
                        if "Maksimum" in selected_metrics:
                            col_summary["Maksimum"] = data_col.max()
                        if "Mean" in selected_metrics:
                            col_summary["Mean"] = data_col.mean()
                        if "Median" in selected_metrics:
                            col_summary["Median"] = data_col.median()
                        if "Modus" in selected_metrics:
                            # Mengambil modus pertama jika ada beberapa modus
                            col_summary["Modus"] = data_col.mode()[0] if not data_col.mode().empty else np.nan
                        if "Varians" in selected_metrics:
                            col_summary["Varians"] = data_col.var()
                        if "Standar Deviasi" in selected_metrics:
                            col_summary["Standar Deviasi"] = data_col.std()
                        if "Kuartil (Q1, Q2, Q3)" in selected_metrics:
                            col_summary["Q1 (Kuartil 1)"] = data_col.quantile(0.25)
                        if "Kuartil (Q1, Q2, Q3)" in selected_metrics:
                            col_summary["Q2 (Kuartil 2/Median)"] = data_col.quantile(0.50)
                        if "Kuartil (Q1, Q2, Q3)" in selected_metrics:
                            col_summary["Q3 (Kuartil 3)"] = data_col.quantile(0.75)
                            
                        summary_dict[col] = col_summary
                    
                    # Membuat Dataframe Hasil Akhir
                    summary_df = pd.DataFrame(summary_dict)
                    st.table(summary_df) # Menampilkan tabel ringkasan rapi
                    
                    # Fitur Unduh Hasil (Fitur Tambahan)
                    csv_data = summary_df.to_csv().encode('utf-8')
                    st.download_button(
                        label="📥 Unduh Ringkasan Hasil (CSV)",
                        data=csv_data,
                        file_name="ringkasan_statistika.csv",
                        mime="text/csv"
                    )
                    
                    # Visualisasi Data (Fitur Tambahan Opsional)
                    st.header("📈 Visualisasi Data (Opsional)")
                    viz_type = st.selectbox("Pilih jenis grafik:", ["Tidak Ada", "Histogram", "Boxplot"])
                    
                    if viz_type == "Histogram":
                        for col in selected_vars:
                            st.write(f"**Histogram untuk {col}**")
                            st.bar_chart(df[col].value_counts())
                    elif viz_type == "Boxplot":
                        for col in selected_vars:
                            st.write(f"**Boxplot Data untuk {col}**")
                            st.line_chart(df[col]) # Pendekatan grafik bawaan sederhana di mobile
                            
            else:
                st.info("Silakan pilih minimal satu variabel untuk memulai analisis.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Menunggu file diunggah... Silakan unggah file Excel atau CSV Anda.")
