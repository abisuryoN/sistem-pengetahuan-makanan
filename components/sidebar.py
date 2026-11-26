"""The product's sidebar: brand, grouped navigation, account and sign-out.

Navigation is built from buttons plus ``st.switch_page`` so the current screen
can be marked by a real disabled state instead of a colour that lies. The whole
set is rendered in the sidebar; pages only call ``render_sidebar("<name>")``.
"""

import streamlit as st

from components.styles import apply_custom_styles
from components.ui import compact

BRAND_MARK = """
<svg width="26" height="26" viewBox="0 0 26 26" fill="none" aria-hidden="true">
  <rect x="0.5" y="0.5" width="25" height="25" rx="7" fill="#e8f1f3" stroke="#cfe0e4"/>
  <path d="M13 19.5c0-4.2 1.4-7.1 5.2-8.6-3.1-.6-5.2.3-6.5 2.1" stroke="#1b6c80" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M13 19.5c0-3.6-1.5-6.2-5-7.4 2.8-.5 4.9.4 6.2 2.2" stroke="#1b6c80" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M13 19.5v-5.4" stroke="#1b6c80" stroke-width="1.6" stroke-linecap="round"/>
</svg>
"""

NAV = [
    (
        "Sistem Pengetahuan",
        [
            ("Beranda", "pages/1_Beranda.py", ":material/space_dashboard:"),
            ("Cari Makanan", "pages/2_Cari_Makanan.py", ":material/search:"),
            ("Cari Penyakit", "pages/3_Cari_Penyakit.py", ":material/medical_information:"),
        ],
    ),
    (
        "Manajemen Data",
        [
            ("Data Makanan", "pages/4_Data_Makanan.py", ":material/grocery:"),
            ("Data Penyakit", "pages/5_Data_Penyakit.py", ":material/health_and_safety:"),
            ("Data Relasi", "pages/6_Data_Relasi.py", ":material/device_hub:"),
        ],
    ),
]


def _brand() -> None:
    st.sidebar.markdown(
        compact(
            f"""
            <div class="side-brand">{BRAND_MARK}
              <div><div class="side-name">Sistem Pengetahuan</div>
              <div class="side-scope">Makanan &amp; Kesehatan</div></div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def _account(username: str) -> None:
    initial = (username or "A")[0].upper()
    st.sidebar.markdown(
        compact(
            f"""
            <div class="side-account">
              <div class="avatar">{initial}</div>
              <div><div class="acc-name">{username}</div>
              <div class="acc-role">Administrator</div></div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def render_sidebar(current: str = "") -> None:
    """Draw the sidebar. Redirects to the login screen when there is no session."""
    apply_custom_styles()

    admin = st.session_state.get("admin")
    if not admin:
        st.switch_page("app.py")

    with st.sidebar:
        _brand()

        for group, items in NAV:
            st.markdown(f'<div class="side-group">{group}</div>', unsafe_allow_html=True)
            for label, path, icon in items:
                if label == current:
                    st.button(
                        label,
                        icon=icon,
                        key=f"nav_{label}",
                        disabled=True,
                        use_container_width=True,
                    )
                elif st.button(
                    label,
                    icon=icon,
                    key=f"nav_{label}",
                    use_container_width=True,
                ):
                    st.switch_page(path)

        _account(admin.get("username", "admin"))

        if st.button("Keluar", icon=":material/logout:", key="nav_logout", use_container_width=True):
            st.session_state.pop("admin", None)
            st.switch_page("app.py")

        st.markdown('<div class="side-foot">Basis pengetahuan gizi · v1.0</div>', unsafe_allow_html=True)
