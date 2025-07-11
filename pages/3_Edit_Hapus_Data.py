import streamlit as st
import pandas as pd
import datetime
import os

DATA_FILE = 'data_penduduk.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame()

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

st.header("✏️ Edit / Hapus Data")

df = load_data()

if df.empty:
    st.info("Belum ada data.")
else:
    keyword = st.text_input("🔍 Cari Nama")
    nama_list = df['Nama'].dropna().unique().tolist()
    filtered_nama = [n for n in nama_list if keyword.lower() in n.lower()]

    if not filtered_nama:
        st.warning("Tidak ada nama yang cocok.")
    else:
        selected_nama = st.selectbox("Pilih Nama", filtered_nama)
        selected_rows = df[df['Nama'] == selected_nama]

        if selected_rows.empty:
            st.error("Data tidak ditemukan.")
        else:
            index = selected_rows.index[0]
            selected_row = selected_rows.iloc[0]

            try:
                tgl_lahir = datetime.datetime.strptime(selected_row['Tanggal Lahir'], "%d/%m/%Y").date()
            except:
                tgl_lahir = datetime.date(1990, 1, 1)

            with st.form("form_edit"):
                nama = st.text_input("Nama", selected_row['Nama'])
                nik = st.text_input("NIK", selected_row['NIK'])
                kk = st.text_input("No KK", selected_row['No KK'])

                jk_options = ["Laki-laki", "Perempuan"]
                jk = st.selectbox("Jenis Kelamin", jk_options, index=jk_options.index(selected_row.get('Jenis Kelamin', 'Laki-laki')) if selected_row.get('Jenis Kelamin', 'Laki-laki') in jk_options else 0)

                tempat = st.text_input("Tempat Lahir", selected_row['Tempat Lahir'])
                tgl = st.date_input("Tanggal Lahir", tgl_lahir, format="DD/MM/YYYY")

                status_opts = ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"]
                status = st.selectbox("Status Perkawinan", status_opts, index=status_opts.index(selected_row['Status Perkawinan']) if selected_row['Status Perkawinan'] in status_opts else 0)

                agama_opts = ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"]
                agama = st.selectbox("Agama", agama_opts, index=agama_opts.index(selected_row['Agama']) if selected_row['Agama'] in agama_opts else 0)

                pendidikan_opts = ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"]
                pendidikan = st.selectbox("Pendidikan", pendidikan_opts, index=pendidikan_opts.index(selected_row['Pendidikan']) if selected_row['Pendidikan'] in pendidikan_opts else 0)

                pekerjaan = st.text_input("Pekerjaan", selected_row['Pekerjaan'])

                goldar_opts = ["A", "B", "AB", "O", "-", "Tidak Tahu"]
                goldar = st.selectbox("Golongan Darah", goldar_opts, index=goldar_opts.index(selected_row['Golongan Darah']) if selected_row['Golongan Darah'] in goldar_opts else 0)

                ayah = st.text_input("Nama Ayah", selected_row['Nama Ayah'])
                ibu = st.text_input("Nama Ibu", selected_row['Nama Ibu'])

                rt_opts = [f"RT 0{i+1}" for i in range(7)]
                rt = st.selectbox("RT", rt_opts, index=rt_opts.index(selected_row['RT']) if selected_row['RT'] in rt_opts else 0)

                alamat = st.text_area("Alamat", selected_row['Alamat'])
                hp = st.text_input("No HP", selected_row['No HP'])

                col1, col2 = st.columns(2)
                update = col1.form_submit_button("✏️ Update")
                delete = col2.form_submit_button("🗑️ Hapus")

                if update:
                    df.loc[index] = [
                        nama, nik, kk, jk, tempat, tgl.strftime("%d/%m/%Y"), status,
                        agama, pendidikan, pekerjaan, goldar, ayah, ibu, rt, "RW 01", alamat, hp
                    ]
                    save_data(df)
                    st.success("✅ Data berhasil diperbarui!")

                if delete:
                    df.drop(index, inplace=True)
                    save_data(df)
                    st.warning("🗑️ Data berhasil dihapus!")
