import streamlit as st
import pandas as pd
import datetime
import os
import pytz
from datetime import datetime

DATA_FILE = 'data_penduduk.csv'

# ------------------------
# Fungsi Data Handling
# ------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        return df
    else:
        df = pd.DataFrame(columns=[
            'Nama', 'NIK', 'No KK', 'Jenis Kelamin', 'Tempat Lahir',
            'Tanggal Lahir', 'Status Perkawinan', 'Agama', 'Pendidikan',
            'Pekerjaan', 'Golongan Darah', 'Nama Ayah', 'Nama Ibu',
            'RT', 'RW', 'Alamat', 'No HP'
        ])
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def waktu_sekarang():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz)
    return now.strftime('%A, %-d %B %Y • %H:%M WIB')

st.set_page_config(page_title="Data Kependudukan", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "home"

# ------------------------
# Halaman Utama
# ------------------------
if st.session_state.page == "home":
    st.title("📊 Data Kependudukan Desa")
    st.write(waktu_sekarang())

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Input Data"):
            st.session_state.page = "input"
    with col2:
        if st.button("📄 Lihat Data"):
            st.session_state.page = "lihat"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("✏️ Edit / Hapus"):
            st.session_state.page = "edit"
    with col4:
        st.download_button("⬇️ Unduh Data CSV", data=open(DATA_FILE, 'rb'), file_name="data_penduduk.csv")

# ------------------------
# Halaman Lihat Data
# ------------------------
elif st.session_state.page == "lihat":
    df = load_data()
    st.header("📄 Lihat Data Penduduk")
    st.dataframe(df, use_container_width=True)
    if st.button("⬅️ Kembali"):
        st.session_state.page = "home"

# ------------------------
# Halaman Input Data
# ------------------------
elif st.session_state.page == "input":
    df = load_data()
    st.header("➕ Input Data Baru")

    with st.form("form_input"):
        nama = st.text_input("Nama")
        nik = st.text_input("NIK")
        kk = st.text_input("No KK")
        jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        tempat = st.text_input("Tempat Lahir")
        tgl = st.date_input("Tanggal Lahir", datetime(1990, 1, 1), format="%d/%m/%Y")
        status = st.selectbox("Status Perkawinan", ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"])
        agama = st.selectbox("Agama", ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"])
        pendidikan = st.selectbox("Pendidikan", ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"])
        pekerjaan = st.text_input("Pekerjaan")
        goldar = st.selectbox("Golongan Darah", ["A", "B", "AB", "O", "-", "Tidak Tahu"])
        ayah = st.text_input("Nama Ayah")
        ibu = st.text_input("Nama Ibu")
        rt = st.selectbox("RT", [f"RT 0{i+1}" for i in range(7)])
        rw = "RW 01"
        alamat = st.text_area("Alamat")
        hp = st.text_input("No HP")

        simpan = st.form_submit_button("✅ Simpan")
        if simpan:
            new_row = pd.DataFrame([{
                'Nama': nama, 'NIK': nik, 'No KK': kk, 'Jenis Kelamin': jk, 'Tempat Lahir': tempat,
                'Tanggal Lahir': tgl.strftime("%d/%m/%Y"), 'Status Perkawinan': status, 'Agama': agama,
                'Pendidikan': pendidikan, 'Pekerjaan': pekerjaan, 'Golongan Darah': goldar, 'Nama Ayah': ayah,
                'Nama Ibu': ibu, 'RT': rt, 'RW': rw, 'Alamat': alamat, 'No HP': hp
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("✅ Data berhasil disimpan!")

    if st.button("⬅️ Kembali"):
        st.session_state.page = "home"

# ------------------------
# Halaman Edit / Hapus
# ------------------------
elif st.session_state.page == "edit":
    df = load_data()
    st.header("✏️ Edit / Hapus Data")

    if df.empty:
        st.info("Belum ada data.")
    else:
        st.markdown("### 🔍 Cari dan Pilih Nama untuk Diedit atau Dihapus")
        nama_search = st.text_input("🔍 Cari Nama")
        filtered_names = [n for n in df['Nama'].dropna().unique().tolist() if nama_search.lower() in n.lower()]
        selected_nama = st.selectbox("Pilih Nama", filtered_names)
        selected_data = df[df['Nama'] == selected_nama]

        if not selected_data.empty:
            selected_row = selected_data.iloc[0]
            tgl_str = selected_row.get('Tanggal Lahir', '01/01/1990')
            try:
                tgl_value = datetime.strptime(tgl_str, "%d/%m/%Y")
            except:
                tgl_value = datetime(1990, 1, 1)

            with st.form("form_edit"):
                nama = st.text_input("Nama", selected_row.get('Nama', ''))
                nik = st.text_input("NIK", selected_row.get('NIK', ''))
                kk = st.text_input("No KK", selected_row.get('No KK', ''))
                jk_options = ["Laki-laki", "Perempuan"]
                jk = st.selectbox("Jenis Kelamin", jk_options, index=jk_options.index(selected_row.get('Jenis Kelamin', 'Laki-laki')))
                tempat = st.text_input("Tempat Lahir", selected_row.get('Tempat Lahir', ''))
                tgl = st.date_input("Tanggal Lahir", tgl_value, format="%d/%m/%Y")
                status_options = ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"]
                status = st.selectbox("Status Perkawinan", status_options, index=status_options.index(selected_row.get('Status Perkawinan', 'Belum Kawin')))
                agama_options = ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"]
                agama = st.selectbox("Agama", agama_options, index=agama_options.index(selected_row.get('Agama', 'Islam')))
                pendidikan_options = ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"]
                pendidikan = st.selectbox("Pendidikan", pendidikan_options, index=pendidikan_options.index(selected_row.get('Pendidikan', 'SD')))
                pekerjaan = st.text_input("Pekerjaan", selected_row.get('Pekerjaan', ''))
                goldar_options = ["A", "B", "AB", "O", "-", "Tidak Tahu"]
                goldar = st.selectbox("Golongan Darah", goldar_options, index=goldar_options.index(selected_row.get('Golongan Darah', '-')))
                ayah = st.text_input("Nama Ayah", selected_row.get('Nama Ayah', ''))
                ibu = st.text_input("Nama Ibu", selected_row.get('Nama Ibu', ''))
                rt_options = [f"RT 0{i+1}" for i in range(7)]
                rt = st.selectbox("RT", rt_options, index=rt_options.index(selected_row.get('RT', 'RT 01')))
                alamat = st.text_area("Alamat", selected_row.get('Alamat', ''))
                hp = st.text_input("No HP", selected_row.get('No HP', ''))

                col1, col2 = st.columns(2)
                update = col1.form_submit_button("✏️ Update")
                delete = col2.form_submit_button("🗑️ Hapus")

                if update:
                    df.loc[df['Nama'] == selected_nama] = [
                        nama, nik, kk, jk, tempat, tgl.strftime("%d/%m/%Y"),
                        status, agama, pendidikan, pekerjaan, goldar,
                        ayah, ibu, rt, "RW 01", alamat, hp
                    ]
                    save_data(df)
                    st.success("✅ Data berhasil diperbarui!")

                if delete:
                    df = df[df['Nama'] != selected_nama]
                    save_data(df)
                    st.warning("🗑️ Data berhasil dihapus!")

    if st.button("⬅️ Kembali"):
        st.session_state.page = "home"
