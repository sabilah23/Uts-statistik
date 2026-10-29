import io
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Statistika Deskriptif - UTS 1B",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CSS / TAMPILAN
# =========================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

.title {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 0;
}

.subtitle {
    font-size: 17px;
    opacity: 0.75;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(128,128,128,0.25);
    background-color: rgba(128,128,128,0.05);
    margin-bottom: 15px;
}

.card-title {
    font-size: 14px;
    opacity: 0.7;
}

.card-value {
    font-size: 25px;
    font-weight: 700;
}

.footer {
    text-align: center;
    opacity: 0.6;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# JUDUL
# =========================================================

st.markdown(
    '<div class="title">📊 Statistika Deskriptif</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Aplikasi Pengolahan Data Statistika Deskriptif '
    '• UTS S-1 Matematika Kelas 1B'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# FUNGSI
# =========================================================

def baca_data(file):
    """
    Membaca file Excel atau CSV.
    """

    nama_file = file.name.lower()

    if nama_file.endswith(".csv"):
        return pd.read_csv(file)

    elif nama_file.endswith(".xlsx"):
        return pd.read_excel(file)

    elif nama_file.endswith(".xls"):
        return pd.read_excel(file)

    else:
        raise ValueError("Format file tidak didukung.")


def hitung_modus(data):
    """
    Menghitung modus.
    """

    data = data.dropna()

    if len(data) == 0:
        return np.nan

    modus = data.mode()

    if len(modus) == 0:
        return np.nan

    if len(modus) == 1:
        return modus.iloc[0]

    return ", ".join(str(x) for x in modus.tolist())


def hitung_statistik(data):
    """
    Menghitung seluruh statistik deskriptif.
    """

    data = pd.to_numeric(
        data,
        errors="coerce"
    ).dropna()

    if len(data) == 0:

        return {
            "N": 0,
            "Minimum": np.nan,
            "Maksimum": np.nan,
            "Mean": np.nan,
            "Median": np.nan,
            "Modus": np.nan,
            "Varians": np.nan,
            "Standar Deviasi": np.nan,
            "Q1": np.nan,
            "Q2": np.nan,
            "Q3": np.nan
        }

    return {

        "N": len(data),

        "Minimum": data.min(),

        "Maksimum": data.max(),

        "Mean": data.mean(),

        "Median": data.median(),

        "Modus": hitung_modus(data),

        "Varians": data.var(ddof=1)
        if len(data) > 1
        else np.nan,

        "Standar Deviasi": data.std(ddof=1)
        if len(data) > 1
        else np.nan,

        "Q1": data.quantile(0.25),

        "Q2": data.quantile(0.50),

        "Q3": data.quantile(0.75)
    }


def format_angka(nilai):

    if pd.isna(nilai):
        return "-"

    if isinstance(nilai, (int, np.integer)):
        return f"{nilai:,}".replace(",", ".")

    if isinstance(nilai, (float, np.floating)):

        return f"{nilai:,.4f}".replace(
            ",", "X"
        ).replace(
            ".", ","
        ).replace(
            "X", "."
        )

    return str(nilai)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Pengaturan")

    st.write(
        "Upload dataset untuk memulai analisis."
    )

    file = st.file_uploader(
        "📂 Upload Dataset",
        type=[
            "xlsx",
            "xls",
            "csv"
        ]
    )

    st.divider()

    st.subheader("📐 Ukuran Statistik")

    semua_statistik = [

        "N",

        "Minimum",

        "Maksimum",

        "Mean",

        "Median",

        "Modus",

        "Varians",

        "Standar Deviasi",

        "Q1",

        "Q2",

        "Q3"
    ]

    statistik_dipilih = st.multiselect(

        "Pilih statistik yang ingin ditampilkan",

        semua_statistik,

        default=semua_statistik
    )


# =========================================================
# HALAMAN AWAL
# =========================================================

if file is None:

    st.info(
        "👈 Silakan upload file Excel atau CSV "
        "melalui menu di sebelah kiri."
    )

    st.markdown(
        """
        ### 🎯 Tujuan Aplikasi

        Aplikasi ini digunakan untuk melakukan
        analisis statistika deskriptif secara otomatis.

        ### 📌 Fitur

        - 📂 Upload data Excel / CSV
        - 📋 Menampilkan dataset
        - 🔢 Memilih variabel numerik
        - 🔢 Menghitung N
        - 📉 Minimum dan maksimum
        - 📊 Mean dan median
        - 🔁 Modus
        - 📐 Varians
        - 📏 Standar deviasi
        - 📦 Kuartil Q1, Q2, Q3
        - 📈 Histogram
        - 📦 Boxplot
        - ⚠️ Deteksi missing value
        - 💾 Download hasil analisis
        """
    )

    st.markdown(
        """
        ### 🛠️ Teknologi

        **Python + Streamlit + Pandas + NumPy + Matplotlib**
        """
    )

    st.stop()


# =========================================================
# MEMBACA DATA
# =========================================================

try:

    df = baca_data(file)

except Exception as error:

    st.error(
        f"❌ Terjadi kesalahan saat membaca file: {error}"
    )

    st.stop()


# =========================================================
# INFORMASI DATA
# =========================================================

st.success(
    f"✅ Dataset **{file.name}** berhasil dimuat."
)


# =========================================================
# KARTU INFORMASI
# =========================================================

jumlah_baris = df.shape[0]
jumlah_kolom = df.shape[1]

jumlah_missing = int(
    df.isna().sum().sum()
)

kolom_numerik = df.select_dtypes(
    include=np.number
).columns.tolist()


c1, c2, c3 = st.columns(3)


with c1:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">
                Jumlah Data
            </div>

            <div class="card-value">
                {jumlah_baris}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">
                Jumlah Variabel
            </div>

            <div class="card-value">
                {jumlah_kolom}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">
                Missing Value
            </div>

            <div class="card-value">
                {jumlah_missing}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# NAVIGASI TAB
# =========================================================

tab_data, tab_analisis, tab_visual = st.tabs(
    [
        "📋 Data",
        "📊 Analisis",
        "📈 Visualisasi"
    ]
)


# =========================================================
# TAB DATA
# =========================================================

with tab_data:

    st.header("📋 Dataset")

    st.write(
        f"Ukuran dataset: "
        f"**{df.shape[0]} baris × {df.shape[1]} kolom**"
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=450
    )

    st.subheader("🔎 Informasi Missing Value")

    missing = df.isna().sum()

    missing = missing[
        missing > 0
    ]

    if len(missing) == 0:

        st.success(
            "✅ Tidak terdapat missing value."
        )

    else:

        missing_table = missing.to_frame(
            name="Jumlah Missing"
        )

        st.dataframe(
            missing_table,
            use_container_width=True
        )


# =========================================================
# TAB ANALISIS
# =========================================================

with tab_analisis:

    st.header("📊 Analisis Statistika Deskriptif")

    if len(kolom_numerik) == 0:

        st.error(
            "❌ Tidak ditemukan variabel numerik."
        )

        st.stop()


    variabel = st.multiselect(

        "🔢 Pilih variabel yang akan dianalisis",

        kolom_numerik,

        default=kolom_numerik[:1]
    )


    if len(variabel) == 0:

        st.warning(
            "⚠️ Pilih minimal satu variabel."
        )

        st.stop()


    if len(statistik_dipilih) == 0:

        st.warning(
            "⚠️ Pilih minimal satu ukuran statistik."
        )

        st.stop()


    # -----------------------------------------------------
    # PERHITUNGAN
    # -----------------------------------------------------

    hasil = []

    for nama_variabel in variabel:

        statistik = hitung_statistik(
            df[nama_variabel]
        )

        baris = {
            "Variabel": nama_variabel
        }

        for nama_statistik in statistik_dipilih:

            baris[nama_statistik] = statistik[
                nama_statistik
            ]

        hasil.append(baris)


    hasil_df = pd.DataFrame(
        hasil
    )


    # -----------------------------------------------------
    # TAMPILAN HASIL
    # -----------------------------------------------------

    st.subheader(
        "📑 Hasil Statistika Deskriptif"
    )


    tabel_tampilan = hasil_df.copy()


    for kolom in statistik_dipilih:

        tabel_tampilan[kolom] = (
            tabel_tampilan[kolom]
            .apply(format_angka)
        )


    st.dataframe(
        tabel_tampilan,
        use_container_width=True
    )


    # -----------------------------------------------------
    # DOWNLOAD CSV
    # -----------------------------------------------------

    csv = hasil_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(

        label="⬇️ Download Hasil CSV",

        data=csv,

        file_name="hasil_statistika.csv",

        mime="text/csv"
    )


    # -----------------------------------------------------
    # DOWNLOAD EXCEL
    # -----------------------------------------------------

    buffer = io.BytesIO()


    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        hasil_df.to_excel(
            writer,
            index=False,
            sheet_name="Statistika"
        )


    st.download_button(

        label="⬇️ Download Hasil Excel",

        data=buffer.getvalue(),

        file_name="hasil_statistika.xlsx",

        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )


# =========================================================
# TAB VISUALISASI
# =========================================================

with tab_visual:

    st.header("📈 Visualisasi Data")

    if len(kolom_numerik) == 0:

        st.error(
            "Tidak ada variabel numerik."
        )

        st.stop()


    variabel_visual = st.selectbox(

        "🔢 Pilih variabel",

        kolom_numerik
    )


    data_visual = pd.to_numeric(

        df[variabel_visual],

        errors="coerce"

    ).dropna()


    if len(data_visual) == 0:

        st.warning(
            "Variabel tidak memiliki data numerik."
        )

        st.stop()


    # -----------------------------------------------------
    # HISTOGRAM
    # -----------------------------------------------------

    st.subheader(
        f"📊 Histogram — {variabel_visual}"
    )


    fig1, ax1 = plt.subplots(
        figsize=(9, 5)
    )


    ax1.hist(
        data_visual,
        bins="auto"
    )


    ax1.set_title(
        f"Histogram {variabel_visual}"
    )

    ax1.set_xlabel(
        variabel_visual
    )

    ax1.set_ylabel(
        "Frekuensi"
    )

    ax1.grid(
        alpha=0.2
    )


    st.pyplot(
        fig1,
        use_container_width=True
    )


    plt.close(fig1)


    # -----------------------------------------------------
    # BOXPLOT
    # -----------------------------------------------------

    st.subheader(
        f"📦 Boxplot — {variabel_visual}"
    )


    fig2, ax2 = plt.subplots(
        figsize=(9, 4)
    )


    ax2.boxplot(
        data_visual,
        vert=False
    )


    ax2.set_xlabel(
        variabel_visual
    )

    ax2.set_title(
        f"Boxplot {variabel_visual}"
    )


    ax2.grid(
        alpha=0.2
    )


    st.pyplot(
        fig2,
        use_container_width=True
    )


    plt.close(fig2)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        📊 Aplikasi Statistika Deskriptif<br>
        UTS Statistika • S-1 Matematika • Kelas 1B
    </div>
    """,
    unsafe_allow_html=True
)
