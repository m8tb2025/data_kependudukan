import streamlit as st
import pandas as pd
from datetime import datetime

DATA_FILE = 'data_penduduk.csv'

def load_data():
    return pd.read_csv(DATA_FILE) if DATA_FILE else pd.DataFrame()

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

st.header("✏️ Edit / Hapus Data")

df = load_data()

if df.empty:
    st.info("Belum ada data.")
else:
    keyword = st.text_input("🔍 Cari Nama", "")
    nama_list = df['Nama'].dropna().unique().tolist()
    filtered_nama = [n for n in nama_list if keyword.lower() in n.lower()]

    if not filtered_nama:
        st.warning("Tidak ada nama yang cocok.")
    else:
        selected_nama = st.selectbox("Pilih Nama", filtered_nama)
        selected_data = df[df['Nama'] == selected_nama]

        if not selected_data.empty:
            selected_row = selected_data.iloc[0]
            tgl_str = selected_row.get("Tanggal Lahir", "01/01/1990")
            try:
                tgl_lahir = datetime.strptime(tgl_str, "%d/%m/%Y")
            except:
                try:
                    tgl_lahir = datetime.strptime(tgl_str, "%Y-%m-%d")
                except:
                    tgl_lahir = datetime(1990, 1, 1)

            with st.form("form_edit"):
                nama = st.text_input("Nama", selected_row.get('Nama', ''))
                nik = st.text_input("NIK", selected_row.get('NIK', ''))
                kk = st.text_input("No KK", selected_row.get('No KK', ''))

                jk_opts = ["Laki-laki", "Perempuan"]
                jk_val = selected_row.get('Jenis Kelamin', 'Laki-laki').capitalize().strip()
                jk = st.selectbox("Jenis Kelamin", jk_opts, index=jk_opts.index(jk_val) if jk_val in jk_opts else 0)

                tempat = st.text_input("Tempat Lahir", selected_row.get('Tempat Lahir', ''))
                tgl = st.date_input("Tanggal Lahir", tgl_lahir, format="DD/MM/YYYY")

                status_opts = ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"]
                status_val = selected_row.get('Status Perkawinan', 'Belum Kawin')
                status = st.selectbox("Status Perkawinan", status_opts, index=status_opts.index(status_val) if status_val in status_opts else 0)

                agama_opts = ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"]
                agama_val = selected_row.get('Agama', 'Islam')
                agama = st.selectbox("Agama", agama_opts, index=agama_opts.index(agama_val) if agama_val in agama_opts else 0)

                pendidikan_opts = ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"]
                pendidikan_val = selected_row.get('Pendidikan', 'SD')
                pendidikan = st.selectbox("Pendidikan", pendidikan_opts, index=pendidikan_opts.index(pendidikan_val) if pendidikan_val in pendidikan_opts else 0)

                pekerjaan = st.text_input("Pekerjaan", selected_row.get('Pekerjaan', ''))

                goldar_opts = ["A", "B", "AB", "O", "-", "Tidak Tahu"]
                goldar_val = selected_row.get('Golongan Darah', '-')
                goldar = st.selectbox("Golongan Darah", goldar_opts, index=goldar_opts.index(goldar_val) if goldar_val in goldar_opts else 0)

                ayah = st.text_input("Nama Ayah", selected_row.get('Nama Ayah', ''))
                ibu = st.text_input("Nama Ibu", selected_row.get('Nama Ibu', ''))

                rt_opts = [f"RT 0{i+1}" for i in range(7)]
                rt_val = selected_row.get('RT', 'RT 01')
                rt = st.selectbox("RT", rt_opts, index=rt_opts.index(rt_val) if rt_val in rt_opts else 0)

                alamat = st.text_area("Alamat", selected_row.get('Alamat', ''))
                hp = st.text_input("No HP", selected_row.get('No HP', ''))

                col1, col2 = st.columns(2)
                update = col1.form_submit_button("✏️ Update")
                delete = col2.form_submit_button("🗑️ Hapus")

                if update:
                    df.loc[df['Nama'] == selected_nama] = [
                        nama, nik, kk, jk, tempat, tgl.strftime("%d/%m/%Y"), status,
                        agama, pendidikan, pekerjaan, goldar, ayah, ibu, rt, "RW 01", alamat, hp
                    ]
                    save_data(df)
                    st.success("✅ Data berhasil diperbarui!")

                if delete:
                    df = df[df['Nama'] != selected_nama]
                    save_data(df)
                    st.warning("🗑️ Data berhasil dihapus!")
