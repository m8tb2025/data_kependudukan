import streamlit as st
import pandas as pd
import os
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
            'Nama', 'NIK', 'No KK', 'Jenis Kelamin', 'Tempat Lahir', 'Tanggal Lahir',
            'Status Perkawinan', 'Agama', 'Pendidikan', 'Pekerjaan', 'Golongan Darah',
            'Nama Ayah', 'Nama Ibu', 'RT', 'RW', 'Alamat', 'No HP'
        ])
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ------------------------
# Halaman Edit / Hapus
# ------------------------
st.header("✏️ Edit / Hapus Data")
df = load_data()

if df.empty:
    st.info("Belum ada data.")
else:
    st.markdown("### 🔍 Cari dan Pilih Nama untuk Diedit atau Dihapus")

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

            # Tanggal lahir parsing aman
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

                jenis_kelamin_options = ["Laki-laki", "Perempuan"]
                jk = st.selectbox("Jenis Kelamin", jenis_kelamin_options,
                                  index=jenis_kelamin_options.index(selected_row.get('Jenis Kelamin', 'Laki-laki')))

                tempat = st.text_input("Tempat Lahir", selected_row.get('Tempat Lahir', ''))
                tgl = st.date_input("Tanggal Lahir", tgl_lahir, format="DD/MM/YYYY")

                status_options = ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"]
                status = st.selectbox("Status Perkawinan", status_options,
                                      index=status_options.index(selected_row.get('Status Perkawinan', 'Belum Kawin')))

                agama_options = ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"]
                agama = st.selectbox("Agama", agama_options,
                                     index=agama_options.index(selected_row.get('Agama', 'Islam')))

                pendidikan_options = ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"]
                pendidikan = st.selectbox("Pendidikan", pendidikan_options,
                                          index=pendidikan_options.index(selected_row.get('Pendidikan', 'SD')))

                pekerjaan = st.text_input("Pekerjaan", selected_row.get('Pekerjaan', ''))

                goldar_options = ["A", "B", "AB", "O", "-", "Tidak Tahu"]
                goldar = st.selectbox("Golongan Darah", goldar_options,
                                      index=goldar_options.index(selected_row.get('Golongan Darah', '-')))

                ayah = st.text_input("Nama Ayah", selected_row.get('Nama Ayah', ''))
                ibu = st.text_input("Nama Ibu", selected_row.get('Nama Ibu', ''))

                rt_options = [f"RT 0{i+1}" for i in range(7)]
                rt = st.selectbox("RT", rt_options,
                                  index=rt_options.index(selected_row.get('RT', 'RT 01')))

                rw = "RW 01"
                alamat = st.text_area("Alamat", selected_row.get('Alamat', ''))
                hp = st.text_input("No HP", selected_row.get('No HP', ''))

                col1, col2 = st.columns(2)
                update = col1.form_submit_button("✏️ Update")
                delete = col2.form_submit_button("🗑️ Hapus")

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
