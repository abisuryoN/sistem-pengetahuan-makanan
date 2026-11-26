"""Data Makanan — add, edit, and delete food entries."""

import streamlit as st

from components.sidebar import render_sidebar
from components.styles import apply_custom_styles
from components.ui import compact, empty_state, esc, fmt_decimal, page_head, section_head
from database.connection import SessionLocal
from database.models import Makanan
from services.makanan_service import VALID_KATEGORI, create_makanan, delete_makanan, get_all_makanan, update_makanan

st.set_page_config(page_title="Data Makanan", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()
render_sidebar("Data Makanan")

page_head("Data Makanan", "Kelola daftar makanan, kategori, kalori, dan manfaat.")

with st.expander("Tambah makanan baru", icon=":material/add:"):
    with st.form("add_makanan", clear_on_submit=True):
        c1, c2 = st.columns(2, gap="small")
        with c1:
            nama = st.text_input("Nama makanan*", placeholder="Contoh: Pisang")
            kategori = st.selectbox("Kategori*", VALID_KATEGORI, index=0)
        with c2:
            kalori = st.number_input("Kalori per 100 g", min_value=0.0, value=0.0, format="%.1f", step=1.0)
        manfaat = st.text_area("Manfaat", placeholder="Deskripsi singkat manfaat gizi...", height=80)
        if st.form_submit_button("Simpan", type="primary", use_container_width=True):
            if not nama.strip():
                st.error("Nama makanan wajib diisi.")
            else:
                try:
                    create_makanan(nama.strip(), kategori, kalori, manfaat.strip())
                    st.success("Makanan ditambahkan.")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

data = get_all_makanan()
section_head("Daftar makanan", f"{len(data)} entri")

if not data:
    empty_state(
        "Belum ada data makanan",
        "Tambahkan makanan pertama dengan tombol di atas.",
        "Setiap makanan akan bisa dikaitkan dengan penyakit di Data Relasi.",
    )
    st.stop()

for m in data:
    with st.expander(f"{m.nama} ({m.kategori})", expanded=False):
        with st.form(f"edit_{m.id}"):
            c1, c2 = st.columns(2, gap="small")
            with c1:
                new_nama = st.text_input("Nama", value=m.nama)
                new_kategori = st.selectbox("Kategori", VALID_KATEGORI, index=VALID_KATEGORI.index(m.kategori))
            with c2:
                new_kalori = st.number_input("Kalori per 100 g", min_value=0.0, value=float(m.kalori or 0), format="%.1f", step=1.0)
            new_manfaat = st.text_area("Manfaat", value=m.manfaat or "", height=80)
            col = st.columns([1, 1, 1], gap="small")
            with col[0]:
                if st.form_submit_button("Simpan", use_container_width=True):
                    try:
                        update_makanan(m.id, new_nama.strip(), new_kategori, new_kalori, new_manfaat.strip())
                        st.success("Diperbarui.")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
            with col[2]:
                if st.form_submit_button("Hapus", type="primary", use_container_width=True):
                    try:
                        delete_makanan(m.id)
                        st.success("Dihapus.")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
        st.markdown(
            compact(
                f"""
                <div class="hr" style="margin:8px 0"></div>
                <div class="small faint">
                  Kalori: <span class="num">{fmt_decimal(m.kalori)} kkal/100 g</span> ·
                  ID: {m.id}
                </div>
                """
            ),
            unsafe_allow_html=True,
        )