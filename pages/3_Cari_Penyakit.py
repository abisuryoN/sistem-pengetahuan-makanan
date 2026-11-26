"""Cari Penyakit — one condition, its symptoms, and the foods that help or hurt."""

import streamlit as st

from components.sidebar import render_sidebar
from components.styles import apply_custom_styles
from components.ui import (
    compact,
    empty_state,
    esc,
    page_head,
    relation_line,
    section_head,
)
from database.connection import SessionLocal
from database.models import Makanan, Penyakit, Relasi

st.set_page_config(page_title="Cari Penyakit", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()
render_sidebar("Cari Penyakit")

page_head(
    "Cari penyakit",
    "Pilih satu penyakit untuk melihat gejala, pencegahan, dan daftar makanan yang dianjurkan, dibatasi, atau dihindari.",
)

db = SessionLocal()
try:
    penyakit_list = db.query(Penyakit).order_by(Penyakit.nama.asc()).all()
    names = [p.nama for p in penyakit_list]
finally:
    db.close()

if not names:
    empty_state(
        "Belum ada data penyakit",
        "Tambahkan penyakit terlebih dahulu agar halaman ini bisa menampilkan anjuran makanan.",
        "Buka Data Penyakit untuk menambahkan entri pertama.",
    )
    st.stop()

top = st.columns([2.2, 1], gap="small", vertical_alignment="bottom")
with top[0]:
    pilihan = st.selectbox("Penyakit", names, index=0)
with top[1]:
    st.markdown(
        compact(
            f"""
            <div class="small faint" style="padding-bottom:9px">
              {len(names)} penyakit tersedia
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

db = SessionLocal()
try:
    penyakit = db.query(Penyakit).filter(Penyakit.nama == pilihan).first()
    relasi = (
        db.query(Relasi, Makanan)
        .join(Makanan, Relasi.makanan_id == Makanan.id)
        .filter(Relasi.penyakit_id == penyakit.id)
        .order_by(Makanan.nama.asc())
        .all()
    )
finally:
    db.close()

if penyakit is None:
    st.stop()

st.markdown(
    compact(
        f"""
        <div class="panel" style="margin-top:14px">
          <div class="panel-head">
            <h2>{esc(penyakit.nama)}</h2>
            <span class="panel-meta">{len(relasi)} makanan ditinjau</span>
          </div>
          <div class="muted" style="font-size:14px">{esc(penyakit.deskripsi or 'Belum ada deskripsi.')}</div>
        </div>
        """
    ),
    unsafe_allow_html=True,
)

detail = st.columns(2, gap="medium")
with detail[0]:
    st.markdown(
        compact(
            f"""
            <div class="panel" style="min-height:150px">
              <div class="panel-head"><h2>Gejala umum</h2></div>
              <div style="font-size:13.5px;color:#3d4348;white-space:pre-line">{esc(penyakit.gejala or 'Belum dicatat.')}</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )
with detail[1]:
    st.markdown(
        compact(
            f"""
            <div class="panel" style="min-height:150px">
              <div class="panel-head"><h2>Pencegahan</h2></div>
              <div style="font-size:13.5px;color:#3d4348;white-space:pre-line">{esc(penyakit.pencegahan or 'Belum dicatat.')}</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

section_head("Anjuran pola makan", "Dikelompokkan menurut status relasi")

if not relasi:
    empty_state(
        "Belum ada makanan yang ditinjau",
        f"Belum ada relasi antara makanan dan {penyakit.nama}.",
        "Tambahkan relasi di Data Relasi agar anjuran muncul di sini.",
    )
    st.stop()

kolom = st.columns(3, gap="medium")
kelompok = [("Dianjurkan", "boleh diteruskan"), ("Batasi", "porsi & frekuensi"), ("Hindari", "sebaiknya tidak")]
for kolom_col, (status, keterangan) in zip(kolom, kelompok):
    with kolom_col:
        items = [rel for rel, makanan in relasi if rel.status == status]
        st.markdown(
            compact(
                f"""
                <div class="panel" style="min-height:186px">
                  <div class="panel-head">
                    <h2>{esc(status)}</h2>
                    <span class="panel-meta">{len(items)} · {esc(keterangan)}</span>
                  </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )
        if not items:
            st.markdown('<div class="panel-note">Tidak ada makanan pada status ini.</div>', unsafe_allow_html=True)
            continue
        for rel, makanan in relasi:
            if rel.status != status:
                continue
            st.markdown(relation_line(makanan.nama, rel.status, rel.alasan), unsafe_allow_html=True)