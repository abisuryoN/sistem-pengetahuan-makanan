"""Small HTML renderers shared by the pages.

Everything here is presentation only: no queries, no writes. Keeping the markup
in one module is what makes the pages read as one product instead of six.
"""

import html
import re
from typing import Iterable, Mapping, Sequence

import streamlit as st

from components.styles import STATUS_STYLE


def esc(value) -> str:
    return html.escape(str(value if value is not None else ""))


def compact(markup: str) -> str:
    """Collapse indentation so Markdown never mistakes the block for code."""
    return re.sub(r"\n\s*", "", markup.strip())


def page_head(title: str, sub: str = "", meta: str = "") -> None:
    meta_html = f'<div class="page-meta">{esc(meta)}</div>' if meta else ""
    sub_html = f'<p class="page-sub">{esc(sub)}</p>' if sub else ""
    st.markdown(
        compact(
            f"""
            <div class="page-head">
              <div><h1>{esc(title)}</h1>{sub_html}</div>
              {meta_html}
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def section_head(title: str, meta: str = "") -> None:
    meta_html = f'<div class="section-meta">{esc(meta)}</div>' if meta else ""
    st.markdown(
        compact(f'<div class="section-head"><h2>{esc(title)}</h2>{meta_html}</div>'),
        unsafe_allow_html=True,
    )


def badge(status: str) -> str:
    css, letter = STATUS_STYLE.get(status, ("b-neutral", "?"))
    return f'<span class="badge {css}">{letter} · {esc(status)}</span>'


def fmt_int(value) -> str:
    return f"{int(value):,}".replace(",", ".")


def fmt_decimal(value, digits: int = 1) -> str:
    text = f"{float(value):,.{digits}f}"
    return text.replace(",", "X").replace(".", ",").replace("X", ".")


def kpi_strip(items: Sequence[Mapping]) -> None:
    cells = []
    for item in items:
        unit = f'<span class="kpi-unit">{esc(item["unit"])}</span>' if item.get("unit") else ""
        note = f'<div class="kpi-note">{esc(item["note"])}</div>' if item.get("note") else ""
        classes = "kpi accent" if item.get("accent") else "kpi"
        lead = " lead" if item.get("lead") else ""
        cells.append(
            f'<div class="{classes}"><div class="kpi-label">{esc(item["label"])}</div>'
            f'<div class="kpi-value{lead}">{esc(item["value"])}{unit}</div>{note}</div>'
        )
    st.markdown(f'<div class="kpi-strip">{"".join(cells)}</div>', unsafe_allow_html=True)


def empty_state(title: str, body: str, hint: str = "") -> None:
    hint_html = f'<div class="empty-hint">{esc(hint)}</div>' if hint else ""
    st.markdown(
        compact(
            f"""
            <div class="empty">
              <h3>{esc(title)}</h3>
              <p>{esc(body)}</p>
              {hint_html}
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def note(text: str, klass: str = "panel-note") -> None:
    st.markdown(f'<div class="{klass}">{esc(text)}</div>', unsafe_allow_html=True)


def relation_matrix(
    penyakit_names: Sequence[str],
    makanan_names: Sequence[str],
    statuses: Mapping[tuple, str],
) -> str:
    """The food × disease grid, returned as markup so a page can frame it."""
    head = "".join(f"<th>{esc(name)}</th>" for name in makanan_names)
    body_rows = []
    for penyakit in penyakit_names:
        cells = []
        for makanan in makanan_names:
            status = statuses.get((makanan, penyakit))
            if status == "Dianjurkan":
                cells.append('<td><span class="mk mk-d" title="Dianjurkan">D</span></td>')
            elif status == "Batasi":
                cells.append('<td><span class="mk mk-b" title="Batasi">B</span></td>')
            elif status == "Hindari":
                cells.append('<td><span class="mk mk-h" title="Hindari">H</span></td>')
            else:
                cells.append('<td><span class="mk-none" title="Belum ada relasi">–</span></td>')
        body_rows.append(f'<tr><td class="rowhead">{esc(penyakit)}</td>{"".join(cells)}</tr>')
    return compact(
        f"""
        <div class="tbl-scroll">
          <table class="matrix">
            <thead><tr><th class="rowhead">Penyakit</th>{head}</tr></thead>
            <tbody>{"".join(body_rows)}</tbody>
          </table>
        </div>
        """
    )


def bar_list(rows: Iterable[tuple], caption_unit: str = "") -> str:
    rows = list(rows)
    top = max((value for _, value in rows), default=0) or 1
    parts = []
    for label, value in rows:
        width = round(value / top * 100, 2)
        parts.append(
            f'<div class="bar-row"><span class="bar-label">{esc(label)}</span>'
            f'<span class="bar-track"><span class="bar-fill" style="width:{width}%"></span></span>'
            f'<span class="bar-value">{esc(value)}{esc(caption_unit)}</span></div>'
        )
    return f'<div class="bar-rows">{"".join(parts)}</div>'


def status_share(counts: Mapping[str, int]) -> str:
    total = sum(counts.values())
    order = [("Dianjurkan", "s-pos", "pos"), ("Batasi", "s-warn", "warn"), ("Hindari", "s-neg", "neg")]
    if total == 0:
        return '<div class="stack"><span class="s-none" style="width:100%"></span></div>'
    segments = "".join(
        f'<span class="{css}" style="width:{counts[name] / total * 100:.2f}%"></span>'
        for name, css, _ in order
        if counts[name]
    )
    legend = "".join(
        f'<div class="lg-row"><span class="dot {dot}"></span>'
        f'<span class="lg-name">{esc(name)}</span>'
        f'<span class="lg-val">{counts[name]}</span></div>'
        for name, _, dot in order
    )
    return f'<div class="stack">{segments}</div><div class="legend">{legend}</div>'



def relation_line(name: str, status: str, note_text: str = "") -> str:
    css, letter = STATUS_STYLE.get(status, ("b-neutral", "?"))
    note_html = f'<div class="rel-note">{esc(note_text)}</div>' if note_text else ""
    return (
        f'<div class="rel"><span class="badge {css}">{letter}</span>'
        f'<div class="rel-body"><div class="rel-name">{esc(name)}</div>{note_html}</div></div>'
    )


def flash(message: str, kind: str = "success") -> None:
    st.session_state["_flash"] = (kind, message)


def show_flash() -> None:
    payload = st.session_state.pop("_flash", None)
    if not payload:
        return
    kind, message = payload
    {"success": st.success, "info": st.info, "warning": st.warning, "error": st.error}[
        kind
    ](message)

