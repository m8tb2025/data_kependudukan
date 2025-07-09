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

# -------------------------
# Setup Layout dan Page
# -------------------------
st.set_page_config(page_title="Data Kependudukan", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "home"

# -------------------------
# Tampilan HOME MENU
# -------------------------
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align:center;'>📱 Data Kependudukan</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Dusun Klotok, Desa Simogirang</h3>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 📋 Pilih Menu", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Lihat Data", use_container_width=True):
            st.session_state.page = "lihat"
    with col2:
        if st.button("➕ Input Data", use_container_width=True):
            st.session_state.page = "input"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("✏️ Edit / Hapus", use_container_width=True):
            st.session_state.page = "edit"
    with col4:
        if st.button("🔁 Kembali ke Awal", use_container_width=True):
            st.session_state.page = "home"

    st.markdown("---")
    st.markdown("<p style='text-align:center;'>M8TB • 2025</p>", unsafe_allow_html=True)

# -------------------------
# LIHAT DATA
# -------------------------
elif st.session_state.page == "lihat":
    st.header("📄 Lihat Data Penduduk")
    df = load_data()
    st.dataframe(df, use_container_width=True)
    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))

# -------------------------
# INPUT DATA
# -------------------------
elif st.session_state.page == "input":
    st.header("➕ Input Data Baru")
    df = load_data()

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

    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))

# -------------------------
# EDIT DATA
# -------------------------
elif st.session_state.page == "edit":
    st.header("✏️ Edit / Hapus Data")
    df = load_data()

    if df.empty:
        st.info("Belum ada data.")
    else:
        selected_nama = st.selectbox("Cari Nama Penduduk", df['Nama'].tolist())
        selected_row = df[df['Nama'] == selected_nama].iloc[0]

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
                df.loc[df['Nama'] == selected_nama] = [
                    nama, nik, kk, jk, tempat, tgl.strftime("%Y-%m-%d"),
                    status, agama, pendidikan, pekerjaan, rt, "RW 01", alamat
                ]
                save_data(df)
                st.success("✅ Data berhasil diperbarui!")

            if delete:
                df = df[df['Nama'] != selected_nama]
                save_data(df)
                st.warning("🗑️ Data berhasil dihapus!")

    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))
