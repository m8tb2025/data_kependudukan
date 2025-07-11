import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import pytz

DATA_FILE = 'data_penduduk.csv'

# Fungsi Data Handling
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

def waktu_sekarang():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz)
    return now.strftime('%A, %-d %B %Y • %H:%M WIB')

# Konfigurasi Streamlit
st.set_page_config(page_title="Data Kependudukan", layout="centered")
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------------- HALAMAN UTAMA -----------------------
if st.session_state.page == "home":
    st.markdown(f"""
        <div style="text-align:center; background-color:#e7f0fa; padding: 14px; border-radius: 12px;">
            <h1 style="color:#0b5394; font-weight:bold;">📱 DATA KEPENDUDUKAN</h1>
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
        if st.button("📤 Import Excel", use_container_width=True):
            st.session_state.page = "import"

    st.download_button("⬇️ Unduh Data CSV", load_data().to_csv(index=False), file_name='data_penduduk.csv')

# ---------------------- LIHAT DATA -----------------------
elif st.session_state.page == "lihat":
    st.header("📄 Lihat Data Penduduk")
    df = load_data()
    if df.empty:
        st.warning("Belum ada data.")
    else:
        st.dataframe(df, use_container_width=True)
    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))

# ---------------------- INPUT DATA -----------------------
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
                'RW': "RW 01",
                'Alamat': alamat,
                'No HP': hp
            }
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            save_data(df)
            st.success("✅ Data berhasil disimpan!")

    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))

# ---------------------- EDIT / HAPUS -----------------------
elif st.session_state.page == "edit":
    st.header("✏️ Edit / Hapus Data")
    df = load_data()

    if df.empty:
        st.info("Belum ada data.")
    else:
        keyword = st.text_input("🔍 Cari Nama", "")
        nama_list = df['Nama'].dropna().unique().tolist()
        filtered_nama = [n for n in nama_list if keyword.lower() in n.lower()]

        if not filtered_nama:
            st.warning("Tidak ada nama yang cocok.")
        else:
            selected_nama = st.selectbox("Pilih Nama", filtered_nama)
            selected_data = df[df['Nama'] == selected_nama]
            selected_row = selected_data.iloc[0]

            try:
                tgl_lahir = datetime.strptime(selected_row['Tanggal Lahir'], "%d/%m/%Y").date()
            except:
                try:
                    tgl_lahir = datetime.strptime(selected_row['Tanggal Lahir'], "%Y-%m-%d").date()
                except:
                    tgl_lahir = date(1990, 1, 1)

            with st.form("form_edit"):
                nama = st.text_input("Nama", selected_row['Nama'])
                nik = st.text_input("NIK", selected_row['NIK'])
                kk = st.text_input("No KK", selected_row['No KK'])
                jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"], index=0 if selected_row['Jenis Kelamin'] == "Laki-laki" else 1)
                tempat = st.text_input("Tempat Lahir", selected_row['Tempat Lahir'])
                tgl = st.date_input("Tanggal Lahir", tgl_lahir, format="DD/MM/YYYY")
                status = st.selectbox("Status Perkawinan", ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"], index=0)
                agama = st.selectbox("Agama", ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Khonghucu", "Lainnya"], index=0)
                pendidikan = st.selectbox("Pendidikan", ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D3", "S1", "S2", "S3"], index=0)
                pekerjaan = st.text_input("Pekerjaan", selected_row['Pekerjaan'])
                goldar = st.selectbox("Golongan Darah", ["A", "B", "AB", "O", "-", "Tidak Tahu"], index=0)
                ayah = st.text_input("Nama Ayah", selected_row['Nama Ayah'])
                ibu = st.text_input("Nama Ibu", selected_row['Nama Ibu'])
                rt = st.selectbox("RT", [f"RT 0{i+1}" for i in range(7)], index=0)
                alamat = st.text_area("Alamat", selected_row['Alamat'])
                hp = st.text_input("No HP", selected_row['No HP'])

                col1, col2 = st.columns(2)
                update = col1.form_submit_button("✏️ Update")
                delete = col2.form_submit_button("🗑️ Hapus")

                if update:
                    df.loc[df['Nama'] == selected_nama] = [
                        nama, nik, kk, jk, tempat, tgl.strftime("%d/%m/%Y"), status,
                        agama, pendidikan, pekerjaan, goldar, ayah, ibu, rt, "RW 01", alamat, hp
                    ]
                    save_data(df)
                    st.success("✅ Data berhasil diperbarui!")

                if delete:
                    df = df[df['Nama'] != selected_nama]
                    save_data(df)
                    st.warning("🗑️ Data berhasil dihapus!")

    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))

# ---------------------- IMPORT EXCEL -----------------------
elif st.session_state.page == "import":
    st.header("📤 Import Data dari Excel (.xlsx)")
    st.info("Pastikan file memiliki header yang sesuai.")

    uploaded_file = st.file_uploader("Unggah File Excel", type=["xlsx"])
    if uploaded_file:
        try:
            new_df = pd.read_excel(uploaded_file)
            expected_columns = [
                'Nama', 'NIK', 'No KK', 'Jenis Kelamin', 'Tempat Lahir', 'Tanggal Lahir',
                'Status Perkawinan', 'Agama', 'Pendidikan', 'Pekerjaan', 'Golongan Darah',
                'Nama Ayah', 'Nama Ibu', 'RT', 'RW', 'Alamat', 'No HP'
            ]

            if all(col in new_df.columns for col in expected_columns):
                df = load_data()
                df = pd.concat([df, new_df], ignore_index=True)
                save_data(df)
                st.success(f"✅ {len(new_df)} data berhasil ditambahkan.")
            else:
                st.error("❌ Kolom tidak sesuai. Gunakan format template yang benar.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

    st.button("⬅️ Kembali ke Menu", on_click=lambda: st.session_state.update({"page": "home"}))
