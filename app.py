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
        return df.rename(columns={
            'NAMA LENGKAP': 'Nama',
            'N I K': 'NIK',
            'NOMOR KK': 'No KK',
            'JENIS KELAMIN': 'Jenis Kelamin',
            'TEMPAT LAHIR': 'Tempat Lahir',
            'TANGGAL LAHIR': 'Tanggal Lahir',
            'STATUS PERKAWINAN': 'Status Perkawinan',
            'AGAMA': 'Agama',
            'PENDIDIKAN': 'Pendidikan',
            'JENIS PEKERJAAN': 'Pekerjaan',
            'GOLONGAN DARAH': 'Golongan Darah',
            'Nama AYAH': 'Nama Ayah',
            'Nama IBU': 'Nama Ibu',
            'RT': 'RT',
            'RW': 'RW',
            'Alamat': 'Alamat',
            'No HP': 'No HP'
        }, errors='ignore')
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
    st.session_state.page = "edit"

# ------------------------
# Halaman Edit / Hapus
# ------------------------
if st.session_state.page == "edit":
    st.header("✏️ Edit / Hapus Data")
    df = load_data()

    if df.empty:
        st.info("Belum ada data.")
    else:
        st.markdown("### 🔍 Cari dan Pilih Nama untuk Diedit atau Dihapus")
        nama_list = df['Nama'].dropna().unique().tolist()

        nama_input = st.text_input("🔍 Cari Nama")
        filtered_nama = [n for n in nama_list if nama_input.lower() in n.lower()]
        selected_nama = st.selectbox("Pilih Nama", filtered_nama if filtered_nama else ["(Tidak ditemukan)"])

        selected_data = df[df['Nama'] == selected_nama]

        if not selected_data.empty:
            selected_row = selected_data.iloc[0]

            with st.form("form_edit"):
                nama = st.text_input("Nama", selected_row.get('Nama', ''))
                nik = st.text_input("NIK", selected_row.get('NIK', ''))
                kk = st.text_input("No KK", selected_row.get('No KK', ''))
                jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"],
                                  index=["Laki-laki", "Perempuan"].index(selected_row.get('Jenis Kelamin', 'Laki-laki')))
                tempat = st.text_input("Tempat Lahir", selected_row.get('Tempat Lahir', ''))

                # Aman dari format error tanggal
                tgl_str = selected_row.get('Tanggal Lahir', '01/01/1990')
                try:
                    tgl_date = datetime.strptime(tgl_str, "%d/%m/%Y").date()
                except:
                    try:
                        tgl_date = pd.to_datetime(tgl_str).date()
                    except:
                        tgl_date = datetime(1990, 1, 1).date()

                tgl = st.date_input("Tanggal Lahir", value=tgl_date, format="%d/%m/%Y")

                status = st.selectbox("Status Perkawinan", ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"],
                                      index=["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"].index(selected_row.get('Status Perkawinan', 'Belum Kawin')))
                agama = st.selectbox("Agama", ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"],
                                     index=["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"].index(selected_row.get('Agama', 'Islam')))
                pendidikan = st.selectbox("Pendidikan", ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"],
                                          index=["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"].index(selected_row.get('Pendidikan', 'SD')))
                pekerjaan = st.text_input("Pekerjaan", selected_row.get('Pekerjaan', ''))
                goldar = st.selectbox("Golongan Darah", ["A", "B", "AB", "O", "-", "Tidak Tahu"],
                                      index=["A", "B", "AB", "O", "-", "Tidak Tahu"].index(selected_row.get('Golongan Darah', '-')))
                ayah = st.text_input("Nama Ayah", selected_row.get('Nama Ayah', ''))
                ibu = st.text_input("Nama Ibu", selected_row.get('Nama Ibu', ''))
                rt = st.selectbox("RT", [f"RT 0{i+1}" for i in range(7)],
                                  index=[f"RT 0{i+1}" for i in range(7)].index(selected_row.get('RT', 'RT 01')))
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

    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))
