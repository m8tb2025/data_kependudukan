# app.py (dashboard utama)
import streamlit as st
import pytz
from datetime import datetime

def waktu_sekarang():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz)
    return now.strftime('%A, %-d %B %Y • %H:%M WIB')

st.set_page_config(page_title="Data Kependudukan", layout="centered")

# Header
st.markdown("""
    <div style="text-align:center; background-color:#e7f0fa; padding: 20px; border-radius: 12px;">
        <h1 style="color:#0b5394; font-weight:bold;">📊 APLIKASI DATA KEPENDUDUKAN</h1>
        <h3 style="margin-top:-10px;">Dusun Klotok, Desa Simogirang</h3>
        <p style="font-size:12px; color:#444;">""" + waktu_sekarang() + """</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("## 📁 Menu Aplikasi")
st.info("👈 Silakan pilih menu di sidebar untuk melihat, input, edit, unggah, atau cetak data.")
