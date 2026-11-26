"""Data Penyakit — add, edit, and delete condition entries."""

import streamlit as st

from components.sidebar import render_sidebar
from components.styles import apply_custom_styles
from components.ui import empty_state, page_head, section_head
from services.penyakit_service import create_penyakit, delete_penyakit, get_all_penyakit, update_penyakit

st.set_page_config(page_title="Data Penyakit", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()
render_sidebar("Data Penyakit")

page_head("Data Penyakit", "Kelola penyakit beserta gejala dan pencegahan.")

with st.expander("Tambah penyakit baru", icon=":material/add:"):
    with st.form("add_penyakit", clear_on_submit=True):
        nama = st.text_input("Nama penyakit*", placeholder="Contoh: Gastritis/GERD")
        c1, c2 = st.columns(2, gap="small")
        with c1:
            deskripsi = st.text_area("Deskripsi", height=80)
            gejala = st.text_area("Gejala umum", height=80)
        with c2:
            pencegahan = st.text_area("Pencegahan", height=80)
        if st.form_submit_button("Simpan", type="primary", use_container_width=True):
            if not nama.strip():
                st.error("Nama penyakit wajib diisi.")
            else:
                try:
                    create_penyakit(nama.strip(), deskripsi.strip(), gejala.strip(), pencegahan.strip())
                    st.success("Penyakit ditambahkan.")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

data = get_all_penyakit()
section_head("Daftar penyakit", f"{len(data)} entri")

if not data:
    empty_state(
        "Belum ada data penyakit",
        "Tambahkan penyakit pertama dengan tombol di atas.",
        "Penyakit yang sudah ada dapat ditautkan ke makanan di Data Relasi.",
    )
    st.stop()

for p in data:
    with st.expander(f"{p.nama}", expanded=False):
        with st.form(f"edit_{p.id}"):
            new_nama = st.text_input("Nama", value=p.nama)
            new_desk = st.text_area("Deskripsi", value=p.deskripsi or "", height=70)
            new_gejala = st.text_area("Gejala", value=p.gejala or "", height=70)
            new_cegah = st.text_area("Pencegahan", value=p.pencegahan or "", height=70)
            col = st.columns([1, 1, 1], gap="small")
            with col[0]:
                if st.form_submit_button("Simpan", use_container_width=True):
                    try:
                        update_penyakit(p.id, new_nama.strip(), new_desk.strip(), new_gejala.strip(), new_cegah.strip())
                        st.success("Diperbarui.")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
            with col[2]:
                if st.form_submit_button("Hapus", type="primary", use_container_width=True):
                    try:
                        delete_penyakit(p.id)
                        st.success("Dihapus.")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))