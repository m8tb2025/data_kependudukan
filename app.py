import streamlit as st
import pandas as pd
import datetime

# Load atau buat data dummy
DATA_FILE = 'data_penduduk.csv'

@st.cache_data
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except:
        # Jika file belum ada, buat data dummy
        data_dummy = pd.DataFrame({
            'Nama': ['Andi', 'Siti'],
            'NIK': ['3512345678900001', '3512345678900002'],
            'No KK': ['3512345678000001', '3512345678000002'],
            'Jenis Kelamin': ['Laki-laki', 'Perempuan'],
            'Tempat Lahir': ['Sidoarjo', 'Prambon'],
            'Tanggal Lahir': ['1990-01-01', '1992-02-02'],
            'Status Perkawinan': ['Kawin', 'Belum Kawin'],
            'Agama': ['Islam', 'Islam'],
            'Pendidikan': ['SMA', 'S1'],
            'Pekerjaan': ['Petani', 'Guru'],
            'RT': ['RT 01', 'RT 02'],
            'RW': ['RW 01', 'RW 01'],
            'Alamat': ['Dusun Klotok', 'Dusun Klotok']
        })
        data_dummy.to_csv(DATA_FILE, index=False)
        return data_dummy

def save_data(new_entry):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# -----------------------
# Streamlit Layout
# -----------------------
st.set_page_config(page_title="Data Kependudukan RT/RW", layout="wide")

st.title("📋 Data Kependudukan Dusun Klotok")
st.subheader("Desa Simogirang, Kecamatan Prambon")

menu = st.sidebar.selectbox("Pilih Menu", ["Lihat Data", "Input Data", "Visualisasi"])

# -----------------------
# Halaman Lihat Data
# -----------------------
if menu == "Lihat Data":
    df = load_data()
    st.dataframe(df, use_container_width=True)

# -----------------------
# Halaman Input Data
# -----------------------
elif menu == "Input Data":
    with st.form("form_input"):
        st.markdown("### 📝 Input Data Penduduk")

        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap")
            nik = st.text_input("NIK")
            kk = st.text_input("Nomor KK")
            jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
            tempat = st.text_input("Tempat Lahir")
            tgl = st.date_input("Tanggal Lahir", datetime.date(1990, 1, 1))
        with col2:
            status = st.selectbox("Status Perkawinan", ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"])
            agama = st.selectbox("Agama", ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"])
            pendidikan = st.selectbox("Pendidikan Terakhir", ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"])
            pekerjaan = st.text_input("Pekerjaan")
            rt = st.selectbox("RT", [f"RT 0{i+1}" for i in range(7)])
            rw = "RW 01"
        
        alamat = st.text_area("Alamat Lengkap", "Dusun Klotok")

        submitted = st.form_submit_button("Simpan Data")
        if submitted:
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
            save_data(new_data)
            st.success("✅ Data berhasil disimpan!")

# -----------------------
# Halaman Visualisasi
# -----------------------
elif menu == "Visualisasi":
    df = load_data()
    st.markdown("### 📊 Visualisasi Kependudukan")

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(df['RT'].value_counts())
    with col2:
        st.bar_chart(df['Jenis Kelamin'].value_counts())

    st.markdown("Distribusi Pendidikan")
    st.bar_chart(df['Pendidikan'].value_counts())

    st.markdown("Distribusi Agama")
    st.bar_chart(df['Agama'].value_counts())
