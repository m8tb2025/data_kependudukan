import streamlit as st
import pandas as pd
import datetime
import os
import pytz
from datetime import datetime

DATA_FILE = 'data_penduduk.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = df.rename(columns=lambda x: x.strip())  # Bersihkan header
        df.columns = [c.strip() for c in df.columns]
        df = df.rename(columns={
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
            'No HP': 'No HP'
        }, errors='ignore')
        
        df['Jenis Kelamin'] = df['Jenis Kelamin'].str.strip().str.capitalize()
        df['Tanggal Lahir'] = df['Tanggal Lahir'].fillna("01/01/1990")
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

# ---------------- HALAMAN HOME ----------------
if st.session_state.page == "home":
    st.title("📱 Data Kependudukan")
    st.caption("Dusun Klotok, Desa Simogirang")
    st.write(waktu_sekarang())

    st.markdown("## 📋 Pilih Menu")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Lihat Data"):
            st.session_state.page = "lihat"
    with col2:
        if st.button("➕ Input Data"):
            st.session_state.page = "input"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("✏️ Edit / Hapus"):
            st.session_state.page = "edit"
    with col4:
        st.download_button("⬇️ Unduh CSV", data=open(DATA_FILE, "rb"), file_name="data_penduduk.csv")

# ---------------- HALAMAN LIHAT ----------------
elif st.session_state.page == "lihat":
    st.header("📄 Data Penduduk")
    df = load_data()
    st.dataframe(df, use_container_width=True)
    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))

# ---------------- HALAMAN INPUT ----------------
elif st.session_state.page == "input":
    st.header("➕ Tambah Data Baru")
    df = load_data()

    with st.form("form_input"):
        nama = st.text_input("Nama")
        nik = st.text_input("NIK")
        kk = st.text_input("No KK")
        jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        tempat = st.text_input("Tempat Lahir")
        tgl_str = selected_row.get('Tanggal Lahir', '01/01/1990')
        try:
            tgl_date = datetime.strptime(tgl_str, "%d/%m/%Y").date()
        except:
            tgl_date = datetime(1990, 1, 1).date()
        tgl = st.date_input("Tanggal Lahir", value=tgl_date, format="DD/MM/YYYY")
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
            new_data = {
                'Nama': nama, 'NIK': nik, 'No KK': kk, 'Jenis Kelamin': jk,
                'Tempat Lahir': tempat, 'Tanggal Lahir': tgl.strftime("%d/%m/%Y"),
                'Status Perkawinan': status, 'Agama': agama, 'Pendidikan': pendidikan,
                'Pekerjaan': pekerjaan, 'Golongan Darah': goldar, 'Nama Ayah': ayah,
                'Nama Ibu': ibu, 'RT': rt, 'RW': rw, 'Alamat': alamat, 'No HP': hp
            }
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            save_data(df)
            st.success("✅ Data berhasil disimpan!")

    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))

# ---------------- HALAMAN EDIT ----------------
elif st.session_state.page == "edit":
    st.header("✏️ Edit / Hapus Data")
    df = load_data()

    if df.empty:
        st.info("Belum ada data.")
    else:
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

                jk_list = ["Laki-laki", "Perempuan"]
                jk_val = selected_row.get('Jenis Kelamin', 'Laki-laki')
                jk = st.selectbox("Jenis Kelamin", jk_list, index=jk_list.index(jk_val) if jk_val in jk_list else 0)

                tempat = st.text_input("Tempat Lahir", selected_row.get('Tempat Lahir', ''))
                tgl_str = selected_row.get('Tanggal Lahir', '01/01/1990')
                tgl = st.date_input("Tanggal Lahir", datetime.strptime(tgl_str, "%d/%m/%Y"), format="DD/MM/YYYY")

                status_list = ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"]
                status_val = selected_row.get('Status Perkawinan', 'Belum Kawin')
                status = st.selectbox("Status Perkawinan", status_list, index=status_list.index(status_val) if status_val in status_list else 0)

                agama_list = ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"]
                agama_val = selected_row.get('Agama', 'Islam')
                agama = st.selectbox("Agama", agama_list, index=agama_list.index(agama_val) if agama_val in agama_list else 0)

                pend_list = ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"]
                pend_val = selected_row.get('Pendidikan', 'SD')
                pendidikan = st.selectbox("Pendidikan", pend_list, index=pend_list.index(pend_val) if pend_val in pend_list else 0)

                pekerjaan = st.text_input("Pekerjaan", selected_row.get('Pekerjaan', ''))

                goldar_list = ["A", "B", "AB", "O", "-", "Tidak Tahu"]
                goldar_val = selected_row.get('Golongan Darah', '-')
                goldar = st.selectbox("Golongan Darah", goldar_list, index=goldar_list.index(goldar_val) if goldar_val in goldar_list else 0)

                ayah = st.text_input("Nama Ayah", selected_row.get('Nama Ayah', ''))
                ibu = st.text_input("Nama Ibu", selected_row.get('Nama Ibu', ''))
                rt_list = [f"RT 0{i+1}" for i in range(7)]
                rt_val = selected_row.get('RT', 'RT 01')
                rt = st.selectbox("RT", rt_list, index=rt_list.index(rt_val) if rt_val in rt_list else 0)
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
