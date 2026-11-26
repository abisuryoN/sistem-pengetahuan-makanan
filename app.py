"""Sistem Pengetahuan Makanan & Kesehatan — login screen.

One card, one form. The brand panel carries the product's own numbers, read
from the database, so the screen belongs to this app and not to a template.
"""

import streamlit as st

from components.styles import apply_custom_styles
from components.ui import fmt_int
from database.connection import SessionLocal
from database.models import Makanan, Penyakit, Relasi
from services.auth_service import authenticate_user, init_admin

st.set_page_config(
    page_title="Masuk · Sistem Pengetahuan Makanan & Kesehatan",
    page_icon=":material/eco:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_custom_styles(login=True)

BRAND_MARK = """
<svg width="30" height="30" viewBox="0 0 30 30" fill="none" aria-hidden="true">
  <path d="M15 23c0-5 1.7-8.4 6.2-10.2-3.7-.7-6.2.4-7.7 2.6" stroke="#8fb9a2" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M15 23c0-4.3-1.8-7.3-6-8.7 3.3-.6 5.8.5 7.3 2.6" stroke="#8fb9a2" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M15 23v-6.4" stroke="#8fb9a2" stroke-width="1.8" stroke-linecap="round"/>
</svg>
"""

if st.session_state.get("admin"):
    st.switch_page("pages/1_Beranda.py")

try:
    init_admin()
except Exception:
    pass


def _counts() -> tuple[int, int, int]:
    db = SessionLocal()
    try:
        return (
            db.query(Makanan).count(),
            db.query(Penyakit).count(),
            db.query(Relasi).count(),
        )
    finally:
        db.close()


try:
    total_makanan, total_penyakit, total_relasi = _counts()
except Exception:
    total_makanan = total_penyakit = total_relasi = 0

left, right = st.columns([1.02, 0.98], gap="large", vertical_alignment="center")

with left:
    st.markdown(
        f"""
        <section class="login-brand">
          <div>
            <div class="brand-mark">{BRAND_MARK}<span class="brand-name">Sistem Pengetahuan Makanan &amp; Kesehatan</span></div>
            <h2>Keputusan gizi yang bisa ditelusuri.</h2>
            <p>Hubungan antara makanan dan penyakit, disusun dari alasan ilmiah — bukan dari daftar yang dihafal.</p>
            <ul class="brand-facts">
              <li><span class="fact-n">{fmt_int(total_makanan)}</span> makanan dengan profil kalori dan manfaat</li>
              <li><span class="fact-n">{fmt_int(total_penyakit)}</span> penyakit dengan gejala dan pencegahan</li>
              <li><span class="fact-n">{fmt_int(total_relasi)}</span> relasi berstatus D, B, atau H</li>
            </ul>
          </div>
          <div class="brand-foot">Ruang kerja administrator · data lokal</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

with right:
    with st.container(border=True):
        st.markdown('<h1 class="login-form-title">Masuk</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p class="login-form-sub">Gunakan akun administrator untuk mengelola basis pengetahuan.</p>',
            unsafe_allow_html=True,
        )

        error_slot = st.empty()

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Nama pengguna", placeholder="admin", autocomplete="username")
            password = st.text_input(
                "Kata sandi", type="password", placeholder="••••••••", autocomplete="current-password"
            )
            submitted = st.form_submit_button("Masuk", type="primary", use_container_width=True)

        if submitted:
            if not username.strip() or not password:
                error_slot.error("Nama pengguna dan kata sandi wajib diisi.")
            else:
                admin = authenticate_user(username.strip(), password)
                if admin is None:
                    error_slot.error("Nama pengguna atau kata sandi tidak sesuai.")
                else:
                    st.session_state.admin = {"id": admin.id, "username": admin.username}
                    st.switch_page("pages/1_Beranda.py")

        st.markdown(
            '<div class="login-note">Akun bawaan: <b>admin</b> / <b>admin123</b>. '
            "Ganti kata sandi setelah instalasi bila aplikasi dipakai bersama.</div>",
            unsafe_allow_html=True,
        )

st.markdown(
    '<div class="login-foot">Ruang kerja lokal · basis data tersimpan di mesin Anda</div>',
    unsafe_allow_html=True,
)
