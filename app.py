import streamlit as st
import pandas as pd
import os
import pytz
from datetime import datetime, date

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
    return now.strftime('%A, %-d %B %Y • %H:%M WIB')

# ------------------------
# Konfigurasi Halaman
# ------------------------
st.set_page_config(page_title="Data Kependudukan", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "home"

# ------------------------
# Halaman Utama
# ------------------------
if st.session_state.page == "home":
    st.markdown("""
        <div style="text-align:center; background-color:#e7f0fa; padding: 20px; border-radius: 12px;">
            <h1 style="color:#0b5394; font-weight:bold; text-transform:uppercase;">📱 DATA KEPENDUDUKAN</h1>
            <h3 style="margin-top:-10px; color:#000000; font-weight:bold;">Dusun Klotok, Desa Simogirang</h3>
            <p style="font-size:16px; color:#444;">""" + waktu_sekarang() + """</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📋 Pilih Menu")
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
        if st.download_button("⬇️ Unduh CSV", data=open(DATA_FILE, 'rb'), file_name="data_penduduk.csv"):
            pass

    st.markdown("---")
    st.markdown("<p style='text-align:center; font-size:15px; color:#777;'>RT. 1 / RW. 2</p>", unsafe_allow_html=True)

# ------------------------
# Halaman Lihat Data
# ------------------------
elif st.session_state.page == "lihat":
    st.header("📄 Data Penduduk")
    df = load_data()
    st.dataframe(df, use_container_width=True)
    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))

# ------------------------
# Halaman Input Data
# ------------------------
elif st.session_state.page == "input":
    st.header("➕ Input Data Baru")
    df = load_data()

    with st.form("form_input"):
        nama = st.text_input("Nama")
        nik = st.text_input("NIK")
        kk = st.text_input("No KK")
        jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        tempat = st.text_input("Tempat Lahir")
        tgl = st.date_input("Tanggal Lahir", date(1990, 1, 1), format="DD/MM/YYYY")
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
# Halaman Edit Data
# ------------------------
elif st.session_state.page == "edit":
    st.header("✏️ Edit / Hapus Data")
    df = load_data()

    if df.empty:
        st.info("Belum ada data.")
    else:
        st.markdown("### 🔍 Cari dan Pilih Nama untuk Diedit atau Dihapus")
        keyword = st.text_input("🔍 Cari Nama").strip().lower()
        filtered_names = [n for n in df['Nama'].dropna().unique().tolist() if keyword in n.lower()]

        selected_nama = st.selectbox("Pilih Nama", filtered_names if keyword else df['Nama'].dropna().unique().tolist())
        selected_data = df[df['Nama'] == selected_nama]

        if not selected_data.empty:
            selected_row = selected_data.iloc[0]
            tgl_str = selected_row.get('Tanggal Lahir', '01/01/1990')

            try:
                default_tgl = datetime.strptime(tgl_str, "%d/%m/%Y")
            except:
                default_tgl = date(1990, 1, 1)

            with st.form("form_edit"):
                nama = st.text_input("Nama", selected_row.get('Nama', ''))
                nik = st.text_input("NIK", selected_row.get('NIK', ''))
                kk = st.text_input("No KK", selected_row.get('No KK', ''))
                jk_options = ["Laki-laki", "Perempuan"]
                jk = st.selectbox("Jenis Kelamin", jk_options,
                                  index=jk_options.index(selected_row.get('Jenis Kelamin', 'Laki-laki')))
                tempat = st.text_input("Tempat Lahir", selected_row.get('Tempat Lahir', ''))
                tgl = st.date_input("Tanggal Lahir", default_tgl, format="DD/MM/YYYY")
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
