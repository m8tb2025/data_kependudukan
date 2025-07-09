import streamlit as st
import pandas as pd
import datetime
import os

DATA_FILE = 'data_penduduk.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=[
            'Nama', 'NIK', 'No KK', 'Jenis Kelamin', 'Tempat Lahir',
            'Tanggal Lahir', 'Status Perkawinan', 'Agama', 'Pendidikan',
            'Pekerjaan', 'RT', 'RW', 'Alamat'
        ])
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Tampilan mobile
st.set_page_config(page_title="Data Kependudukan", layout="centered")

st.title("📱 Data Kependudukan Mobile")
st.markdown("Dusun Klotok, Desa Simogirang, Kec. Prambon")

menu = st.selectbox("Menu", ["Lihat Data", "Input Data Baru", "Edit/Hapus Data"])

df = load_data()

# -------------------------------
# Input Data
# -------------------------------
if menu == "Input Data Baru":
    with st.form("form_input"):
        nama = st.text_input("Nama Lengkap")
        nik = st.text_input("NIK")
        kk = st.text_input("Nomor KK")
        jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        tempat = st.text_input("Tempat Lahir")
        tgl = st.date_input("Tanggal Lahir", datetime.date(1990, 1, 1))
        status = st.selectbox("Status Perkawinan", ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"])
        agama = st.selectbox("Agama", ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"])
        pendidikan = st.selectbox("Pendidikan Terakhir", ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"])
        pekerjaan = st.text_input("Pekerjaan")
        rt = st.selectbox("RT", [f"RT 0{i+1}" for i in range(7)])
        rw = "RW 01"
        alamat = st.text_area("Alamat Lengkap", "Dusun Klotok")

        simpan = st.form_submit_button("✅ Simpan")
        if simpan:
            new_data = {
                'Nama': nama,
                'NIK': nik,
                'No KK': kk,
                'Jenis Kelamin': jk,
                'Tempat Lahir': tempat,
                'Tanggal Lahir': tgl.strftime("%Y-%m-%d"),
                'Status Perkawinan': status,
                'Agama': agama,
                'Pendidikan': pendidikan,
                'Pekerjaan': pekerjaan,
                'RT': rt,
                'RW': rw,
                'Alamat': alamat
            }
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            save_data(df)
            st.success("✅ Data berhasil disimpan!")

# -------------------------------
# Lihat Data
# -------------------------------
elif menu == "Lihat Data":
    st.subheader("📋 Data Penduduk")
    st.dataframe(df, use_container_width=True)

# -------------------------------
# Edit/Hapus Data
# -------------------------------
elif menu == "Edit/Hapus Data":
    st.subheader("✏️ Edit atau 🗑️ Hapus Data")
    if df.empty:
        st.info("Belum ada data.")
    else:
        selected_index = st.selectbox("Pilih Data Berdasarkan NIK", df['NIK'].tolist())
        selected_row = df[df['NIK'] == selected_index].iloc[0]

        with st.form("form_edit"):
            nama = st.text_input("Nama Lengkap", selected_row['Nama'])
            nik = st.text_input("NIK", selected_row['NIK'])
            kk = st.text_input("Nomor KK", selected_row['No KK'])
            jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"], index=["Laki-laki", "Perempuan"].index(selected_row['Jenis Kelamin']))
            tempat = st.text_input("Tempat Lahir", selected_row['Tempat Lahir'])
            tgl = st.date_input("Tanggal Lahir", pd.to_datetime(selected_row['Tanggal Lahir']))
            status = st.selectbox("Status Perkawinan", ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"], index=["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"].index(selected_row['Status Perkawinan']))
            agama = st.selectbox("Agama", ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"], index=["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"].index(selected_row['Agama']))
            pendidikan = st.selectbox("Pendidikan Terakhir", ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"], index=["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"].index(selected_row['Pendidikan']))
            pekerjaan = st.text_input("Pekerjaan", selected_row['Pekerjaan'])
            rt = st.selectbox("RT", [f"RT 0{i+1}" for i in range(7)], index=[f"RT 0{i+1}" for i in range(7)].index(selected_row['RT']))
            alamat = st.text_area("Alamat Lengkap", selected_row['Alamat'])

            col1, col2 = st.columns(2)
            update = col1.form_submit_button("✏️ Update")
            delete = col2.form_submit_button("🗑️ Hapus")

            if update:
                df.loc[df['NIK'] == selected_index] = [
                    nama, nik, kk, jk, tempat, tgl.strftime("%Y-%m-%d"),
                    status, agama, pendidikan, pekerjaan, rt, "RW 01", alamat
                ]
                save_data(df)
                st.success("✅ Data berhasil diperbarui!")

            if delete:
                df = df[df['NIK'] != selected_index]
                save_data(df)
                st.warning("🗑️ Data berhasil dihapus!")
