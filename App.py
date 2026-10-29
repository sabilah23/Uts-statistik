import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(
    page_title="Statistika Deskriptif",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.card {
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #dddddd;
    text-align: center;
}

.card-title {
    font-size: 14px;
}

.card-value {
    font-size: 25px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


st.title("📊 Statistika Deskriptif")

st.divider()


# =========================
# UPLOAD DATA
# =========================

file = st.file_uploader(
    "📂 Upload Dataset",
    type=["xlsx", "xls", "csv"]
)

if file is None:
    st.info("Silakan upload dataset.")
    st.stop()


# =========================
# MEMBACA DATA
# =========================

try:

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)

    else:
        df = pd.read_excel(file)

except:

    st.error("File tidak dapat dibaca.")
    st.stop()


# =========================
# INFORMASI DATA
# =========================

jumlah_data = len(df)
jumlah_variabel = len(df.columns)
jumlah_missing = int(df.isna().sum().sum())

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">Jumlah Data</div>
            <div class="card-value">{jumlah_data}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">Jumlah Variabel</div>
            <div class="card-value">{jumlah_variabel}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">Missing Value</div>
            <div class="card-value">{jumlah_missing}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# =========================
# MENU
# =========================

menu = st.radio(
    "",
    [
        "📋 Data",
        "📊 Statistik",
        "📈 Grafik"
    ],
    horizontal=True
)


# =========================================================
# DATA
# =========================================================

if menu == "📋 Data":

    st.subheader("Data")

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )


# =========================================================
# STATISTIK
# =========================================================

elif menu == "📊 Statistik":

    st.subheader("Statistika Deskriptif")

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if not numeric_columns:
        st.warning("Tidak terdapat variabel numerik.")
        st.stop()

    variables = st.multiselect(
        "Pilih Variabel",
        numeric_columns,
        default=numeric_columns[:1]
    )

    statistics = st.multiselect(
        "Pilih Ukuran Statistik",
        [
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
        ],
        default=[
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
    )

    if variables and statistics:

        hasil = []

        for variable in variables:

            data = pd.to_numeric(
                df[variable],
                errors="coerce"
            ).dropna()

            if len(data) == 0:
                continue

            modus = data.mode()

            if len(modus) > 1:
                modus_hasil = ", ".join(
                    str(x) for x in modus.tolist()
                )
            elif len(modus) == 1:
                modus_hasil = modus.iloc[0]
            else:
                modus_hasil = "-"

            row = {
                "Variabel": variable
            }

            if "N" in statistics:
                row["N"] = len(data)

            if "Minimum" in statistics:
                row["Minimum"] = data.min()

            if "Maksimum" in statistics:
                row["Maksimum"] = data.max()

            if "Mean" in statistics:
                row["Mean"] = data.mean()

            if "Median" in statistics:
                row["Median"] = data.median()

            if "Modus" in statistics:
                row["Modus"] = modus_hasil

            if "Varians" in statistics:
                row["Varians"] = (
                    data.var()
                    if len(data) > 1
                    else np.nan
                )

            if "Standar Deviasi" in statistics:
                row["Standar Deviasi"] = (
                    data.std()
                    if len(data) > 1
                    else np.nan
                )

            if "Q1" in statistics:
                row["Q1"] = data.quantile(0.25)

            if "Q2" in statistics:
                row["Q2"] = data.quantile(0.50)

            if "Q3" in statistics:
                row["Q3"] = data.quantile(0.75)

            hasil.append(row)

        hasil_df = pd.DataFrame(hasil)

        st.dataframe(
            hasil_df,
            use_container_width=True
        )

        # CSV

        csv = hasil_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            csv,
            "hasil_statistika.csv",
            "text/csv"
        )

        # EXCEL

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
            "⬇️ Download Excel",
            buffer.getvalue(),
            "hasil_statistika.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


# =========================================================
# GRAFIK
# =========================================================

elif menu == "📈 Grafik":

    st.subheader("Grafik")

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if not numeric_columns:
        st.warning("Tidak terdapat variabel numerik.")
        st.stop()

    variable = st.selectbox(
        "Pilih Variabel",
        numeric_columns
    )

    jenis_grafik = st.selectbox(
        "Pilih Grafik",
        [
            "Histogram",
            "Boxplot",
            "Diagram Batang",
            "Diagram Garis",
            "Diagram Lingkaran"
        ]
    )

    data = pd.to_numeric(
        df[variable],
        errors="coerce"
    ).dropna()


    # HISTOGRAM

    if jenis_grafik == "Histogram":

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        ax.hist(
            data,
            bins="auto"
        )

        ax.set_xlabel(variable)
        ax.set_ylabel("Frekuensi")
        ax.set_title(f"Histogram {variable}")

        ax.grid(alpha=0.2)

        st.pyplot(fig)

        plt.close(fig)


    # BOXPLOT

    elif jenis_grafik == "Boxplot":

        fig, ax = plt.subplots(
            figsize=(10, 4)
        )

        ax.boxplot(
            data,
            vert=False
        )

        ax.set_xlabel(variable)
        ax.set_title(f"Boxplot {variable}")

        ax.grid(alpha=0.2)

        st.pyplot(fig)

        plt.close(fig)


    # DIAGRAM BATANG

    elif jenis_grafik == "Diagram Batang":

        frekuensi = data.value_counts().sort_index()

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        ax.bar(
            frekuensi.index.astype(str),
            frekuensi.values
        )

        ax.set_xlabel(variable)
        ax.set_ylabel("Frekuensi")
        ax.set_title(f"Diagram Batang {variable}")

        plt.xticks(rotation=45)

        st.pyplot(fig)

        plt.close(fig)


    # DIAGRAM GARIS

    elif jenis_grafik == "Diagram Garis":

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        ax.plot(
            data.reset_index(drop=True)
        )

        ax.set_xlabel("Observasi")
        ax.set_ylabel(variable)
        ax.set_title(f"Diagram Garis {variable}")

        ax.grid(alpha=0.2)

        st.pyplot(fig)

        plt.close(fig)


    # DIAGRAM LINGKARAN

    elif jenis_grafik == "Diagram Lingkaran":

        frekuensi = data.value_counts()

        fig, ax = plt.subplots(
            figsize=(7, 7)
        )

        ax.pie(
            frekuensi.values,
            labels=frekuensi.index.astype(str),
            autopct="%1.1f%%"
        )

        ax.set_title(
            f"Diagram Lingkaran {variable}"
        )

        st.pyplot(fig)

        plt.close(fig)


st.divider()

st.markdown(
    "<center>📊 Statistika Deskriptif</center>",
    unsafe_allow_html=True
    )
