import streamlit as st
import pandas as pd
import os

DATA_FILE = 'data_penduduk.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except Exception as e:
            st.error(f"Gagal memuat data: {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame(columns=[
            'Nama', 'NIK', 'No KK', 'Jenis Kelamin', 'Tempat Lahir', 'Tanggal Lahir',
            'Status Perkawinan', 'Agama', 'Pendidikan', 'Pekerjaan', 'Golongan Darah',
            'Nama Ayah', 'Nama Ibu', 'RT', 'RW', 'Alamat', 'No HP'
        ])

# Judul halaman
st.header("📄 Lihat Data Penduduk")

# Load dan tampilkan data
df = load_data()

if df.empty:
    st.warning("⚠️ Belum ada data tersedia.")
else:
    st.dataframe(df, use_container_width=True)

# Tombol unduh CSV
st.download_button(
    label="⬇️ Unduh Data CSV",
    data=df.to_csv(index=False),
    file_name="data_penduduk.csv",
    mime="text/csv"
)
