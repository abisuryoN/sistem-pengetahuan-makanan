"""Cari Makanan — find a food and see what it means for each condition."""

import streamlit as st

from components.sidebar import render_sidebar
from components.styles import apply_custom_styles
from components.ui import (
    compact,
    empty_state,
    esc,
    fmt_decimal,
    page_head,
    relation_line,
    section_head,
)
from database.connection import SessionLocal
from database.models import Makanan, Penyakit, Relasi
from services.makanan_service import VALID_KATEGORI

st.set_page_config(page_title="Cari Makanan", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()
render_sidebar("Cari Makanan")

KATEGORI = ["Semua"] + list(VALID_KATEGORI)

page_head(
    "Cari makanan",
    "Cari berdasarkan nama atau manfaat, lalu saring per kategori. Setiap makanan menampilkan status hubungannya dengan penyakit.",
)

filters = st.columns([2.4, 1.1, 0.9], gap="small", vertical_alignment="center")
with filters[0]:
    query = st.text_input(
        "Kata kunci",
        placeholder="Contoh: oatmeal, kalium, serat",
        label_visibility="collapsed",
    )
with filters[1]:
    kategori = st.selectbox("Kategori", KATEGORI, label_visibility="collapsed")
with filters[2]:
    st.markdown("**Hasil**")

db = SessionLocal()
try:
    rows = (
        db.query(Makanan, Relasi.status, Penyakit.nama)
        .outerjoin(Relasi, Relasi.makanan_id == Makanan.id)
        .outerjoin(Penyakit, Relasi.penyakit_id == Penyakit.id)
        .order_by(Makanan.nama.asc())
        .all()
    )
finally:
    db.close()

foods = {}
for makanan, status, disease in rows:
    entry = foods.setdefault(
        makanan.id,
        {"nama": makanan.nama, "kategori": makanan.kategori, "kalori": makanan.kalori, "manfaat": makanan.manfaat, "relasi": []},
    )
    if status and disease:
        entry["relasi"].append((status, disease))

needle = (query or "").strip().lower()
results = []
for entry in foods.values():
    if kategori != "Semua" and entry["kategori"] != kategori:
        continue
    if needle and needle not in entry["nama"].lower() and needle not in (entry["manfaat"] or "").lower():
        continue
    results.append(entry)

section_head("Hasil pencarian", f"{len(results)} makanan")

if not results:
    empty_state(
        "Tidak ada makanan yang cocok",
        f"Tidak ditemukan makanan untuk “{query.strip()}”" if needle else "Belum ada makanan pada kategori ini.",
        "Coba kata kunci lain, pilih kategori Semua, atau tambahkan data di Data Makanan.",
    )
    st.stop()

for entry in results:
    with st.container(border=True):
        head = st.columns([3.2, 1.1], gap="small", vertical_alignment="center")
        with head[0]:
            st.markdown(
                compact(
                    f"""
                    <div style="display:flex;align-items:baseline;gap:9px;flex-wrap:wrap">
                      <span style="font-size:15px;font-weight:600">{esc(entry['nama'])}</span>
                      <span class="small faint">{esc(entry['kategori'])}</span>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )
        with head[1]:
            kalori = entry["kalori"]
            st.markdown(
                compact(
                    f"""
                    <div class="num" style="font-size:13px">
                      <span style="font-variant-numeric:tabular-nums">{fmt_decimal(kalori)}</span>
                      <span class="small faint">kkal / 100 g</span>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

        if entry["manfaat"]:
            st.markdown(f'<div class="muted" style="font-size:13.5px;margin-top:2px">{esc(entry["manfaat"])}</div>', unsafe_allow_html=True)

        if entry["relasi"]:
            st.markdown('<div class="hr" style="margin:10px 0 4px"></div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="small faint" style="margin-bottom:6px">Hubungan dengan penyakit</div>',
                unsafe_allow_html=True,
            )
            for status, disease in sorted(entry["relasi"], key=lambda item: item[1]):
                st.markdown(relation_line(disease, status), unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="panel-note">Belum ada relasi dengan penyakit mana pun.</div>',
                unsafe_allow_html=True,
            )