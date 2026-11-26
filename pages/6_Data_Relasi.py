"""Data Relasi — the food–disease pairs and the reason behind each."""

import streamlit as st

from components.sidebar import render_sidebar
from components.styles import apply_custom_styles
from components.ui import badge, compact, empty_state, esc, page_head, section_head
from services.makanan_service import get_all_makanan
from services.penyakit_service import get_all_penyakit
from services.relasi_service import VALID_STATUS, create_relasi, delete_relasi, get_all_relasi, update_relasi

st.set_page_config(page_title="Data Relasi", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()
render_sidebar("Data Relasi")

page_head(
    "Data Relasi",
    "Setiap pasangan makanan–penyakit menyimpan status dan alasan ilmiah. Status yang sama dipakai di seluruh aplikasi.",
)

makanan_list = get_all_makanan()
penyakit_list = get_all_penyakit()

if not makanan_list or not penyakit_list:
    empty_state(
        "Belum bisa membuat relasi",
        "Tambahkan setidaknya satu makanan dan satu penyakit terlebih dahulu.",
        "Buka Data Makanan atau Data Penyakit untuk melengkapi data dasar.",
    )
    st.stop()

with st.expander("Tambah relasi baru", icon=":material/add:"):
    with st.form("add_relasi", clear_on_submit=True):
        c1, c2 = st.columns(2, gap="small")
        with c1:
            m_opt = st.selectbox("Makanan*", makanan_list, format_func=lambda x: x.nama)
            p_opt = st.selectbox("Penyakit*", penyakit_list, format_func=lambda x: x.nama)
        with c2:
            status = st.selectbox("Status*", VALID_STATUS, index=0)
        alasan = st.text_area("Alasan ilmiah*", height=80, placeholder="Mengapa makanan ini dianjurkan/dibatasi/dihindari?")
        if st.form_submit_button("Simpan", type="primary", use_container_width=True):
            try:
                create_relasi(m_opt.id, p_opt.id, status, alasan.strip())
                st.success("Relasi ditambahkan.")
                st.rerun()
            except Exception as e:
                st.error(str(e))

filters = st.columns([1.2, 1.6, 1], gap="small", vertical_alignment="bottom")
with filters[0]:
    f_status = st.selectbox("Status", ["Semua"] + VALID_STATUS, label_visibility="collapsed")
with filters[1]:
    f_penyakit = st.selectbox("Penyakit", ["Semua"] + [p.nama for p in penyakit_list], label_visibility="collapsed")
with filters[2]:
    st.markdown('<div class="small faint" style="padding-bottom:9px">Filter relasi</div>', unsafe_allow_html=True)

relasi_data = get_all_relasi()
filtered = []
for r, m, p in relasi_data:
    if f_status != "Semua" and r.status != f_status:
        continue
    if f_penyakit != "Semua" and p.nama != f_penyakit:
        continue
    filtered.append((r, m, p))

section_head("Daftar relasi", f"{len(filtered)} pasangan")

if not filtered:
    empty_state(
        "Tidak ada relasi yang cocok",
        "Ubah filter atau tambahkan relasi baru melalui formulir di atas.",
        "Status yang tersedia: Dianjurkan, Batasi, Hindari.",
    )
    st.stop()

for r, m, p in filtered:
    with st.expander(f"{m.nama}  ↔  {p.nama}", expanded=False):
        st.markdown(compact(f'<div style="margin-bottom:8px">{badge(r.status)}</div>'), unsafe_allow_html=True)
        st.markdown(
            compact(
                f"""
                <div class="small faint" style="margin-bottom:3px">Alasan ilmiah</div>
                <div style="font-size:13.5px;color:#3d4348">{esc(r.alasan)}</div>
                <div class="hr" style="margin:8px 0"></div>
                <div class="small faint">ID relasi: {r.id}</div>
                """
            ),
            unsafe_allow_html=True,
        )
        with st.form(f"edit_rel_{r.id}"):
            new_status = st.selectbox(
                "Status",
                VALID_STATUS,
                index=VALID_STATUS.index(r.status),
            )
            new_alasan = st.text_area("Alasan ilmiah", value=r.alasan, height=70)
            col = st.columns([1, 1, 1], gap="small")
            with col[0]:
                if st.form_submit_button("Simpan", use_container_width=True):
                    try:
                        update_relasi(r.id, new_status, new_alasan.strip())
                        st.success("Diperbarui.")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
            with col[2]:
                if st.form_submit_button("Hapus", type="primary", use_container_width=True):
                    try:
                        delete_relasi(r.id)
                        st.success("Dihapus.")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))