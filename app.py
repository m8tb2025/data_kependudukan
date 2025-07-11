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
        return pd.read_csv(DATA_FILE)
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
    return now.strftime('%A, %-d %B %Y • %H:%M WIB') \
        .replace("Monday", "Senin").replace("Tuesday", "Selasa") \
        .replace("Wednesday", "Rabu").replace("Thursday", "Kamis") \
        .replace("Friday", "Jumat").replace("Saturday", "Sabtu") \
        .replace("Sunday", "Minggu") \
        .replace("January", "Januari").replace("February", "Februari") \
        .replace("March", "Maret").replace("April", "April") \
        .replace("May", "Mei").replace("June", "Juni") \
        .replace("July", "Juli").replace("August", "Agustus") \
        .replace("September", "September").replace("October", "Oktober") \
        .replace("November", "November").replace("December", "Desember")

st.set_page_config(page_title="Data Kependudukan", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "home"

# ------------------------
# Halaman Home
# ------------------------
if st.session_state.page == "home":
    st.markdown("""
        <div style="text-align:center; background-color:#e7f0fa; padding: 20px; border-radius: 12px;">
            <h1 style="color:#0b5394; font-weight:bold; text-transform:uppercase;">📱 DATA KEPENDUDUKAN</h1>
            <h3 style="margin-top:-10px; color:#000000; font-weight:bold;">Dusun Klotok, Desa Simogirang</h3>
            <p style="font-size:16px; color:#444;">""" + waktu_sekarang() + """</p>
        </div>
    """, unsafe_allow_html=True)

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
        if st.button("🔄 Upload CSV", use_container_width=True):
            st.session_state.page = "upload"

    st.markdown("---")
    st.markdown("<p style='text-align:center; font-size:15px; color:#777;'>RT. 1 / RW. 2</p>", unsafe_allow_html=True)

# ------------------------
# Halaman Lihat Data
# ------------------------
elif st.session_state.page == "lihat":
    st.header("📄 Data Penduduk")
    df = load_data()
    st.dataframe(df, use_container_width=True)
    st.download_button("🔧 Unduh CSV", df.to_csv(index=False), "data_penduduk.csv")
    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))

# ------------------------
# Halaman Input
# ------------------------
elif st.session_state.page == "input":
    st.header("➕ Input Data Baru")
    df = load_data()

    with st.form("form_input"):
        nama = st.text_input("Nama Lengkap")
        nik = st.text_input("NIK")
        kk = st.text_input("Nomor KK")
        jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        tempat = st.text_input("Tempat Lahir")
        tgl = st.date_input("Tanggal Lahir", datetime.date(1990, 1, 1), max_value=datetime.date.today())
        status = st.selectbox("Status Perkawinan", ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"])
        agama = st.selectbox("Agama", ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"])
        pendidikan = st.selectbox("Pendidikan", ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"])
        pekerjaan = st.text_input("Pekerjaan")
        goldar = st.selectbox("Golongan Darah", ["A", "B", "AB", "O", "-", "Tidak Tahu"])
        ayah = st.text_input("Nama Ayah")
        ibu = st.text_input("Nama Ibu")
        rt = st.selectbox("RT", [f"RT 0{i+1}" for i in range(7)])
        rw = "RW 01"
        alamat = st.text_area("Alamat", "Dusun Klotok")
        hp = st.text_input("Nomor HP")

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
                'RW': rw,
                'Alamat': alamat,
                'No HP': hp
            }
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            save_data(df)
            st.success("✅ Data berhasil disimpan!")

    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))

# ------------------------
# Halaman Upload CSV
# ------------------------
elif st.session_state.page == "upload":
    st.header("🔄 Upload Data dari File")
    uploaded = st.file_uploader("Unggah file CSV dengan format kolom yang sesuai:", type="csv")

    if uploaded is not None:
        uploaded_df = pd.read_csv(uploaded)
        st.write("Pratinjau Data:")
        st.dataframe(uploaded_df.head())

        if st.button("📅 Ganti Data Lama dengan File Ini"):
            save_data(uploaded_df)
            st.success("Data berhasil diganti!")

    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))
