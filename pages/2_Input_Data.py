import streamlit as st
import pandas as pd
import os
from datetime import datetime

DATA_FILE = 'data_penduduk.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            'Nama', 'NIK', 'No KK', 'Jenis Kelamin', 'Tempat Lahir', 'Tanggal Lahir',
            'Status Perkawinan', 'Agama', 'Pendidikan', 'Pekerjaan', 'Golongan Darah',
            'Nama Ayah', 'Nama Ibu', 'RT', 'RW', 'Alamat', 'No HP'
        ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

st.header("➕ Input Data Baru")

df = load_data()

with st.form("form_input"):
    nama = st.text_input("Nama")
    nik = st.text_input("NIK")
    kk = st.text_input("No KK")
    jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    tempat = st.text_input("Tempat Lahir")
    tgl = st.date_input("Tanggal Lahir", datetime(1990, 1, 1), format="DD/MM/YYYY")
    status = st.selectbox("Status Perkawinan", ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"])
    agama = st.selectbox("Agama", ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"])
    pendidikan = st.selectbox("Pendidikan", ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"])
    pekerjaan = st.text_input("Pekerjaan")
    goldar = st.selectbox("Golongan Darah", ["A", "B", "AB", "O", "-", "Tidak Tahu"])
    ayah = st.text_input("Nama Ayah")
    ibu = st.text_input("Nama Ibu")
    rt = st.selectbox("RT", [f"RT 0{i+1}" for i in range(7)])
    alamat = st.text_area("Alamat")
    hp = st.text_input("No HP")

    simpan = st.form_submit_button("✅ Simpan")

    if simpan:
        new_data = {
            'Nama': nama,
            'NIK': nik,
            'No KK': kk,
            'Jenis Kelamin': jk,
            'Tempat Lahir': tempat,
            'Tanggal Lahir': tgl.strftime("%d/%m/%Y"),
            'Status Perkawinan': status,
            'Agama': agama,
            'Pendidikan': pendidikan,
            'Pekerjaan': pekerjaan,
            'Golongan Darah': goldar,
            'Nama Ayah': ayah,
            'Nama Ibu': ibu,
            'RT': rt,
            'RW': "RW 01",
            'Alamat': alamat,
            'No HP': hp
        }

        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        save_data(df)
        st.success("✅ Data berhasil disimpan!")
