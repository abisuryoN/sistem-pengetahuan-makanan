"""Beranda — the state of the knowledge base in one screen.

Question: is the base complete, and which food–disease pairs are still empty?
The matrix is the largest block because it answers exactly that.
"""

from datetime import date

import streamlit as st

from components.sidebar import render_sidebar
from components.styles import apply_custom_styles
from components.ui import (
    compact,
    fmt_int,
    kpi_strip,
    page_head,
    relation_line,
    relation_matrix,
    status_share,
)
from database.connection import SessionLocal
from database.models import Makanan, Penyakit, Relasi

st.set_page_config(page_title="Beranda", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()
render_sidebar("Beranda")

BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

db = SessionLocal()
try:
    makanan = db.query(Makanan).order_by(Makanan.nama.asc()).all()
    penyakit = db.query(Penyakit).order_by(Penyakit.nama.asc()).all()
    relasi_rows = (
        db.query(Relasi.status, Makanan.nama, Penyakit.nama, Relasi.alasan)
        .join(Makanan, Relasi.makanan_id == Makanan.id)
        .join(Penyakit, Relasi.penyakit_id == Penyakit.id)
        .order_by(Penyakit.nama.asc(), Makanan.nama.asc())
        .all()
    )
finally:
    db.close()

foods = [m.nama for m in makanan]
diseases = [p.nama for p in penyakit]
statuses = {(food, disease): status for status, food, disease, _ in relasi_rows}

counts = {"Dianjurkan": 0, "Batasi": 0, "Hindari": 0}
for status, _, _, _ in relasi_rows:
    if status in counts:
        counts[status] += 1

total_cells = len(foods) * len(diseases)
filled = len(statuses)
coverage = round(filled / total_cells * 100) if total_cells else 0

food_diseases = {food for _, food, _, _ in relasi_rows}
disease_foods = {disease for _, _, disease, _ in relasi_rows}
foods_without = [food for food in foods if food not in food_diseases]
diseases_without = [disease for disease in diseases if disease not in disease_foods]

empty_parts = []
if foods_without:
    empty_parts.append(f"{len(foods_without)} makanan belum punya relasi")
if diseases_without:
    empty_parts.append(f"{len(diseases_without)} penyakit belum punya relasi")
if not empty_parts:
    empty_parts.append("semua makanan dan penyakit sudah terhubung")

today = date.today()
page_head(
    "Ikhtisar",
    f"Basis pengetahuan berisi {fmt_int(len(foods))} makanan dan {fmt_int(len(diseases))} penyakit. "
    f"{filled} dari {fmt_int(total_cells)} kemungkinan relasi sudah diisi; {' dan '.join(empty_parts)}.",
    f"{today.day} {BULAN[today.month - 1]} {today.year}",
)

kpi_strip(
    [
        {"label": "Makanan", "value": fmt_int(len(foods)), "note": "dengan profil kalori"},
        {"label": "Penyakit", "value": fmt_int(len(diseases)), "note": "dengan gejala & pencegahan"},
        {"label": "Relasi", "value": fmt_int(len(relasi_rows)), "note": "alasan ilmiah tersimpan"},
        {
            "label": "Cakupan matriks",
            "value": f"{coverage}",
            "unit": "%",
            "note": f"{filled} dari {fmt_int(total_cells)} sel",
            "accent": True,
        },
    ]
)

matrix_panel = compact(
    f"""
    <div class="panel">
      <div class="panel-head">
        <h2>Peta hubungan makanan–penyakit</h2>
        <span class="panel-meta">{filled} sel terisi · {total_cells - filled} kosong</span>
      </div>
      {relation_matrix(diseases, foods, statuses)}
      <div class="panel-note">
        D = Dianjurkan · B = Batasi · H = Hindari · – = belum ada relasi.
        Setiap sel adalah satu alasan ilmiah yang bisa dibuka di halaman Data Relasi.
      </div>
    </div>
    """
)
st.markdown(matrix_panel, unsafe_allow_html=True)

left, right = st.columns([0.56, 0.44], gap="medium")

with left:
    share_panel = compact(
        f"""
        <div class="panel" style="min-height:236px">
          <div class="panel-head">
            <h2>Status hubungan</h2>
            <span class="panel-meta">{len(relasi_rows)} relasi</span>
          </div>
          {status_share(counts)}
          <div class="panel-note">
            Hijau boleh diteruskan, kuning dibatasi, merah dihindari.
          </div>
        </div>
        """
    )
    st.markdown(share_panel, unsafe_allow_html=True)

with right:
    with st.container(border=True):
        st.markdown(
            compact(
                """
                <div class="panel-head">
                  <h2>Perlu perhatian</h2>
                  <span class="panel-meta">status Hindari</span>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )
        db = SessionLocal()
        try:
            hindari = (
                db.query(Makanan.nama, Penyakit.nama, Relasi.alasan)
                .join(Relasi, Relasi.makanan_id == Makanan.id)
                .join(Penyakit, Relasi.penyakit_id == Penyakit.id)
                .filter(Relasi.status == "Hindari")
                .order_by(Penyakit.nama.asc())
                .all()
            )
        finally:
            db.close()

        if hindari:
            rows_html = "".join(
                relation_line(f"{food} — {disease}", "Hindari", alasan)
                for food, disease, alasan in hindari[:3]
            )
            st.markdown(rows_html, unsafe_allow_html=True)
            if len(hindari) > 3:
                st.markdown(
                    f'<div class="panel-note">{len(hindari) - 3} relasi Hindari lainnya ada di Data Relasi.</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown('<div class="panel-note">Belum ada relasi berstatus Hindari.</div>', unsafe_allow_html=True)

        st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
        if st.button("Kelola relasi", icon=":material/device_hub:", type="primary", use_container_width=True):
            st.switch_page("pages/6_Data_Relasi.py")
        if st.button("Cari makanan", icon=":material/search:", use_container_width=True):
            st.switch_page("pages/2_Cari_Makanan.py")

