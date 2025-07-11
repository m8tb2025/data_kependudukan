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
    try:
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            df.columns = df.columns.str.strip()
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
            expected = ['Nama', 'NIK', 'No KK', 'Jenis Kelamin', 'Tempat Lahir', 'Tanggal Lahir',
                        'Status Perkawinan', 'Agama', 'Pendidikan', 'Pekerjaan', 'Golongan Darah',
                        'Nama Ayah', 'Nama Ibu', 'RT', 'RW', 'Alamat', 'No HP']
            for col in expected:
                if col not in df.columns:
                    df[col] = ""
            df = df.fillna("")
            return df
        else:
            return pd.DataFrame(columns=[
                'Nama', 'NIK', 'No KK', 'Jenis Kelamin', 'Tempat Lahir',
                'Tanggal Lahir', 'Status Perkawinan', 'Agama', 'Pendidikan',
                'Pekerjaan', 'Golongan Darah', 'Nama Ayah', 'Nama Ibu',
                'RT', 'RW', 'Alamat', 'No HP'
            ])
    except Exception as e:
        st.error(f"❌ Gagal load data: {e}")
        return pd.DataFrame()

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
# Halaman HOME
# ------------------------
if st.session_state.page == "home":
    st.markdown(f"""
        <div style="text-align:center; background-color:#e7f0fa; padding: 20px; border-radius: 12px;">
            <h1 style="color:#0b5394; font-weight:bold;">📊 DATA KEPENDUDUKAN</h1>
            <h3 style="margin-top:-10px; color:#000;">Dusun Klotok, Desa Simogirang</h3>
            <p style="font-size:16px; color:#444;">{waktu_sekarang()}</p>
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
        if st.button("📥 Upload File CSV", use_container_width=True):
            st.session_state.page = "upload"

    st.markdown("---")
    st.markdown("<p style='text-align:center; font-size:15px; color:#777;'>RT. 1 / RW. 2</p>", unsafe_allow_html=True)

# ------------------------
# Halaman Lihat
# ------------------------
elif st.session_state.page == "lihat":
    st.header("📄 Data Penduduk")
    df = load_data()
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Unduh CSV", csv, "data_penduduk.csv", "text/csv")

    st.button("⬅️ Kembali", on_click=lambda: st.session_state.update({"page": "home"}))

# ------------------------
# Halaman Upload
# ------------------------
elif st.session_state.page == "upload":
    st.header("📥 Upload File CSV")
    uploaded = st.file_uploader("Unggah file CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Data berhasil diunggah dan disimpan!")
    st.button("⬅️ Kembali", on_click=lambda: st.session_state.update({"page": "home"}))

# ------------------------
# Halaman Edit / Hapus
# ------------------------
elif st.session_state.page == "edit":
    st.header("✏️ Edit / Hapus Data")
    df = load_data()

    if df.empty:
        st.info("Belum ada data.")
    else:
        nama_list = df['Nama'].dropna().unique().tolist()
        selected_nama = st.selectbox("🔍 Pilih Nama", nama_list)

        selected_data = df[df['Nama'] == selected_nama]
        if not selected_data.empty:
            selected_row = selected_data.iloc[0]

            with st.form("form_edit"):
                nama = st.text_input("Nama", selected_row['Nama'])
                nik = st.text_input("NIK", selected_row['NIK'])
                kk = st.text_input("No KK", selected_row['No KK'])
                jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"],
                                  index=["Laki-laki", "Perempuan"].index(selected_row['Jenis Kelamin']))
                tempat = st.text_input("Tempat Lahir", selected_row['Tempat Lahir'])
                try:
                    tgl = datetime.strptime(selected_row['Tanggal Lahir'], "%d/%m/%Y")
                except:
                    tgl = datetime(1990, 1, 1)
                tgl = st.date_input("Tanggal Lahir", tgl)
                status = st.selectbox("Status Perkawinan", ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"],
                                      index=0 if selected_row['Status Perkawinan'] not in ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"]
                                      else ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"].index(selected_row['Status Perkawinan']))
                agama = st.selectbox("Agama", ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"],
                                     index=0 if selected_row['Agama'] not in ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"]
                                     else ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"].index(selected_row['Agama']))
                pendidikan = st.selectbox("Pendidikan", ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"],
                                          index=0 if selected_row['Pendidikan'] not in ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"]
                                          else ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"].index(selected_row['Pendidikan']))
                pekerjaan = st.text_input("Pekerjaan", selected_row['Pekerjaan'])
                goldar = st.selectbox("Golongan Darah", ["A", "B", "AB", "O", "-", "Tidak Tahu"],
                                      index=0 if selected_row['Golongan Darah'] not in ["A", "B", "AB", "O", "-", "Tidak Tahu"]
                                      else ["A", "B", "AB", "O", "-", "Tidak Tahu"].index(selected_row['Golongan Darah']))
                ayah = st.text_input("Nama Ayah", selected_row['Nama Ayah'])
                ibu = st.text_input("Nama Ibu", selected_row['Nama Ibu'])
                rt = st.text_input("RT", selected_row['RT'])
                rw = st.text_input("RW", selected_row['RW'])
                alamat = st.text_area("Alamat", selected_row['Alamat'])
                hp = st.text_input("No HP", selected_row['No HP'])

                update = st.form_submit_button("✅ Update")
                delete = st.form_submit_button("🗑️ Hapus")

                if update:
                    df.loc[df['Nama'] == selected_nama] = [
                        nama, nik, kk, jk, tempat, tgl.strftime("%d/%m/%Y"),
                        status, agama, pendidikan, pekerjaan, goldar,
                        ayah, ibu, rt, rw, alamat, hp
                    ]
                    save_data(df)
                    st.success("✅ Data berhasil diperbarui!")

                if delete:
                    df = df[df['Nama'] != selected_nama]
                    save_data(df)
                    st.warning("🗑️ Data berhasil dihapus!")

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
        tgl = st.date_input("Tanggal Lahir", datetime(1990, 1, 1))
        status = st.selectbox("Status Perkawinan", ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"])
        agama = st.selectbox("Agama", ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"])
        pendidikan = st.selectbox("Pendidikan", ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"])
        pekerjaan = st.text_input("Pekerjaan")
        goldar = st.selectbox("Golongan Darah", ["A", "B", "AB", "O", "-", "Tidak Tahu"])
        ayah = st.text_input("Nama Ayah")
        ibu = st.text_input("Nama Ibu")
        rt = st.text_input("RT")
        rw = st.text_input("RW")
        alamat = st.text_area("Alamat")
        hp = st.text_input("No HP")

        simpan = st.form_submit_button("✅ Simpan")
        if simpan:
            new_data = pd.DataFrame([{
                'Nama': nama, 'NIK': nik, 'No KK': kk, 'Jenis Kelamin': jk,
                'Tempat Lahir': tempat, 'Tanggal Lahir': tgl.strftime("%d/%m/%Y"),
                'Status Perkawinan': status, 'Agama': agama, 'Pendidikan': pendidikan,
                'Pekerjaan': pekerjaan, 'Golongan Darah': goldar, 'Nama Ayah': ayah,
                'Nama Ibu': ibu, 'RT': rt, 'RW': rw, 'Alamat': alamat, 'No HP': hp
            }])
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)
            st.success("✅ Data berhasil disimpan!")

    st.button("⬅️ Kembali", on_click=lambda: st.session_state.update({"page": "home"}))
