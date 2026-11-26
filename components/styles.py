"""Design tokens and the single stylesheet for the whole app.

The sheet is the framed-sheet app style (teal accent, tinted frame, white page
inset) with the product's own status hues kept apart from the brand hue:
brand teal is chrome, green/amber/red only ever mean Dianjurkan/Batasi/Hindari.
"""

import streamlit as st

TOKENS = {
    "ground": "#f4f6f8",
    "sheet": "#ffffff",
    "raised": "#f7f8f9",
    "active": "#eceff1",
    "border": "#e8eaec",
    "rule": "#eff1f2",
    "control": "#d3d8dc",
    "ink": "#131416",
    "muted": "#5b6167",
    "faint": "#6a6f75",
    "accent": "#1b6c80",
    "accent_ink": "#145263",
    "accent_soft": "#e8f1f3",
    "pos": "#1e7b4f",
    "pos_soft": "#e4f4ea",
    "pos_ink": "#14563a",
    "warn": "#8a5a10",
    "warn_soft": "#fdf4e3",
    "warn_ink": "#6d470c",
    "neg": "#b3261e",
    "neg_soft": "#fdecea",
    "neg_ink": "#8a1c16",
}

# The three relation states, encoded by letter as well as by hue so the marks
# still read for a colour-blind visitor or in a printed screenshot.
STATUS_STYLE = {
    "Dianjurkan": ("b-pos", "D"),
    "Batasi": ("b-warn", "B"),
    "Hindari": ("b-neg", "H"),
}

_CSS = """
:root {
  --ground: #f4f6f8;
  --sheet: #ffffff;
  --raised: #f7f8f9;
  --active: #eceff1;
  --border: #e8eaec;
  --rule: #eff1f2;
  --control: #d3d8dc;
  --ink: #131416;
  --muted: #5b6167;
  --faint: #6a6f75;
  --accent: #1b6c80;
  --accent-ink: #145263;
  --accent-soft: #e8f1f3;
  --pos: #1e7b4f;
  --pos-soft: #e4f4ea;
  --pos-ink: #14563a;
  --warn: #8a5a10;
  --warn-soft: #fdf4e3;
  --warn-ink: #6d470c;
  --neg: #b3261e;
  --neg-soft: #fdecea;
  --neg-ink: #8a1c16;
  --r-sheet: 14px;
  --r-card: 8px;
  --r-ctrl: 6px;
  --font: "IBM Plex Sans", ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
  font-family: var(--font);
  color: var(--ink);
}

.stApp { background: var(--ground); }

[data-testid="stDecoration"], [data-testid="stStatusWidget"], #MainMenu, footer { display: none; }

header[data-testid="stHeader"] {
  background: transparent;
  height: 2.75rem;
  border-bottom: none;
}
[data-testid="stToolbar"] { right: 0.75rem; }
[data-testid="stToolbar"] button { color: var(--muted); }

/* The page is a white sheet inset in the tinted frame. */
[data-testid="stMainBlockContainer"] {
   width: 100%;
   max-width: none;
   min-width: 0;
   margin: 0.35rem 0;
   padding: 26px 34px 64px;
   background: var(--sheet);
   border: none;
   border-radius: 0;
   min-height: calc(100vh - 4rem);
}
[data-testid="stMain"] { background: var(--ground); }

/* ---------- typography ---------- */
h1, h2, h3, h4, h5, h6 { color: var(--ink); font-family: var(--font); }
h1 { font-size: 25px !important; line-height: 1.25; font-weight: 600 !important; letter-spacing: -0.015em; padding: 0 !important; }
h2 { font-size: 18px !important; line-height: 1.3; font-weight: 600 !important; letter-spacing: -0.01em; padding: 0 !important; }
h3 { font-size: 15px !important; line-height: 1.35; font-weight: 600 !important; padding: 0 !important; }
p, li, label, .stMarkdown { font-size: 14px; line-height: 1.55; }
.stMarkdown p { margin-bottom: 0.4rem; }
a { color: var(--accent); }
code, pre { font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 12.5px; }
hr { border: none; border-top: 1px solid var(--rule); margin: 16px 0; }

.page-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; margin: 0 0 20px; }
.page-head h1 { margin: 0; }
.page-sub { margin: 6px 0 0; font-size: 14px; line-height: 1.5; color: var(--muted); max-width: 64ch; }
.page-meta { flex: none; font-size: 12px; color: var(--faint); padding-top: 4px; white-space: nowrap; }
.page-head .page-actions { flex: none; display: flex; gap: 8px; }

.section-head { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; margin: 22px 0 10px; }
.section-head h2 { margin: 0; }
.section-head .section-meta { font-size: 12px; color: var(--faint); }

.muted { color: var(--muted); }
.faint { color: var(--faint); }
.small { font-size: 12px; }
.strong { font-weight: 600; }
.num { font-variant-numeric: tabular-nums; text-align: right; }
.hr { height: 1px; background: var(--rule); margin: 18px 0; }

/* ---------- KPI strip: one container split by hairlines ---------- */
.kpi-strip {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: 1fr;
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: var(--r-card);
  overflow: hidden;
  margin: 0 0 22px;
}
.kpi { background: var(--sheet); padding: 14px 18px 15px; min-width: 0; }
.kpi-label { font-size: 12.5px; color: var(--muted); margin: 0 0 4px; }
.kpi-value { font-size: 28px; font-weight: 400; letter-spacing: -0.02em; line-height: 1.15; font-variant-numeric: tabular-nums; }
.kpi-value.lead { font-size: 30px; }
.kpi-unit { font-size: 13px; color: var(--muted); margin-left: 5px; }
.kpi-note { font-size: 12px; color: var(--faint); margin-top: 3px; }
.kpi.accent .kpi-value { color: var(--accent-ink); }

/* ---------- panels ---------- */
.panel { border: 1px solid var(--border); border-radius: var(--r-card); background: var(--sheet); padding: 16px 18px; }
.panel.raised { background: var(--raised); }
.panel-head { display: flex; align-items: baseline; justify-content: space-between; gap: 14px; margin-bottom: 12px; }
.panel-head h2 { margin: 0; }
.panel-head .panel-meta { font-size: 12px; color: var(--faint); white-space: nowrap; }
.panel-note { font-size: 12px; color: var(--faint); margin-top: 10px; }

/* bordered containers are stVerticalBlock with the theme's 1px edge */
[data-testid="stVerticalBlock"]:has([data-testid="stForm"]) { background: var(--sheet); }


/* ---------- badges, dots, marks ---------- */
.badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 12px; font-weight: 500; line-height: 1;
  padding: 4px 7px; border-radius: 4px; border: 1px solid transparent;
  white-space: nowrap;
}
.b-pos { background: var(--pos-soft); color: var(--pos-ink); border-color: #c8e6d3; }
.b-warn { background: var(--warn-soft); color: var(--warn-ink); border-color: #efdfbd; }
.b-neg { background: var(--neg-soft); color: var(--neg-ink); border-color: #f3cdc9; }
.b-neutral { background: var(--raised); color: var(--muted); border-color: var(--border); }
.dot { width: 7px; height: 7px; border-radius: 2px; display: inline-block; flex: none; }
.dot.pos { background: var(--pos); }
.dot.warn { background: #c08a2e; }
.dot.neg { background: var(--neg); }

/* ---------- tables ---------- */
.tbl { width: 100%; border-collapse: collapse; font-size: 14px; }
.tbl th {
  font-size: 12px; font-weight: 500; color: var(--muted); text-align: left;
  padding: 0 12px 8px; border-bottom: 1px solid var(--border); white-space: nowrap;
}
.tbl td { padding: 11px 12px; border-bottom: 1px solid var(--rule); vertical-align: middle; }
.tbl tr:last-child td { border-bottom: none; }
.tbl th.num, .tbl td.num { text-align: right; }
.tbl .row-name { font-weight: 500; }
.tbl .row-sub { font-size: 12px; color: var(--faint); margin-top: 2px; }
.tbl-scroll { overflow-x: auto; max-width: 100%; }

/* ---------- relation matrix (this product's own element) ---------- */
.matrix { border-collapse: collapse; width: 100%; min-width: 540px; font-size: 13px; }
.matrix th { font-weight: 500; font-size: 11.5px; color: var(--muted); padding: 0 0 8px; text-align: center; white-space: nowrap; }
.matrix th.rowhead { text-align: left; padding-right: 12px; }
.matrix td { padding: 5px 0; text-align: center; border-top: 1px solid var(--rule); }
.matrix td.rowhead { text-align: left; padding: 8px 12px 8px 0; font-size: 13px; color: var(--ink); white-space: nowrap; }
.mk {
  display: inline-flex; align-items: center; justify-content: center;
  width: 23px; height: 23px; border-radius: 4px;
  font-size: 10.5px; font-weight: 600; letter-spacing: 0.02em;
}
.mk-d { background: var(--pos-soft); color: var(--pos-ink); }
.mk-b { background: var(--warn-soft); color: var(--warn-ink); }
.mk-h { background: var(--neg-soft); color: var(--neg-ink); }
.mk-none { color: #b9c0c6; font-size: 13px; font-weight: 400; }

/* ---------- bar list + stacked share ---------- */
.bar-rows { display: flex; flex-direction: column; gap: 9px; }
.bar-row { display: grid; grid-template-columns: minmax(92px, 150px) 1fr 34px; align-items: center; gap: 12px; font-size: 13px; }
.bar-row .bar-label { color: var(--ink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.bar-track { height: 6px; background: var(--active); border-radius: 3px; overflow: hidden; }
.bar-fill { height: 100%; background: var(--accent); border-radius: 3px; }
.bar-row .bar-value { text-align: right; font-variant-numeric: tabular-nums; color: var(--muted); font-size: 12.5px; }

.stack { display: flex; gap: 2px; height: 10px; margin: 2px 0 12px; }
.stack span { display: block; height: 100%; }
.stack .s-pos { background: var(--pos); }
.stack .s-warn { background: #c08a2e; }
.stack .s-neg { background: var(--neg); }
.stack .s-none { background: var(--active); }
.legend { display: flex; flex-direction: column; gap: 7px; font-size: 13px; }
.legend .lg-row { display: flex; align-items: center; gap: 8px; }
.legend .lg-name { flex: 1; color: var(--muted); }
.legend .lg-val { font-variant-numeric: tabular-nums; color: var(--ink); }

/* ---------- relation rows ---------- */
.rel { display: flex; align-items: flex-start; gap: 10px; padding: 9px 0; border-top: 1px solid var(--rule); }
.rel:first-child { border-top: none; padding-top: 0; }
.rel .rel-body { min-width: 0; }
.rel .rel-name { font-size: 13.5px; font-weight: 500; }
.rel .rel-note { font-size: 12.5px; color: var(--muted); margin-top: 1px; line-height: 1.5; }

/* ---------- empty state ---------- */
.empty {
  border: 1px dashed var(--control); border-radius: var(--r-card);
  background: var(--raised); padding: 26px 22px; text-align: center;
}
.empty h3 { margin: 0 0 6px; font-size: 15px !important; }
.empty p { margin: 0 auto; max-width: 52ch; color: var(--muted); font-size: 13px; }
.empty .empty-hint { margin-top: 8px; font-size: 12px; color: var(--faint); }

/* ---------- login ---------- */
html:has(#login-screen) section[data-testid="stSidebar"],
html:has(#login-screen) [data-testid="stSidebarCollapsedControl"],
html:has(#login-screen) header[data-testid="stHeader"] { display: none !important; }
html:has(#login-screen) [data-testid="stMainBlockContainer"] {
  background: transparent; border: none; padding: 7vh 24px 40px; max-width: 1040px; min-height: 0;
}
.login-brand {
  background: #10382c; color: #eef5f0; border-radius: 12px;
  padding: 34px 32px;
  display: flex; flex-direction: column; gap: 22px; justify-content: center;
}
.login-brand .brand-mark { display: flex; align-items: center; gap: 11px; }
.login-brand .brand-name { font-size: 14px; font-weight: 600; letter-spacing: 0.01em; color: #dbe9df; }
.login-brand h2 { color: #dbe9df; font-size: 27px !important; line-height: 1.28; letter-spacing: -0.015em; margin: 26px 0 10px; max-width: 16ch; }
.login-brand p { color: #c3d8cb; font-size: 14px; line-height: 1.6; max-width: 36ch; margin: 0; }
.login-brand .brand-facts { list-style: none; padding: 0; margin: 22px 0 0; display: flex; flex-direction: column; gap: 8px; }
.login-brand .brand-facts li { color: #dbe9df; font-size: 13px; display: flex; gap: 9px; align-items: baseline; }
.login-brand .brand-facts .fact-n { color: #8fb9a2; font-variant-numeric: tabular-nums; font-size: 12px; min-width: 14px; }
.login-brand .brand-foot { font-size: 12px; color: #8fb9a2; }
.login-form-title { font-size: 21px !important; margin: 0 0 4px; }
.login-form-sub { font-size: 13.5px; color: var(--muted); margin: 0 0 18px; }
.login-note { margin-top: 16px; font-size: 12px; color: var(--muted); line-height: 1.6; }
html:has(#login-screen) [data-testid="stVerticalBlock"]:has([data-testid="stForm"]) { padding: 28px 26px 22px; }
html:has(#login-screen) [data-testid="stTextInput"] div[data-baseweb="input"] { min-height: 42px; }
html:has(#login-screen) .stFormSubmitButton > button { min-height: 42px; }
.login-foot { text-align: center; font-size: 12px; color: var(--muted); padding: 34px 0 6px; }


/* ---------- Streamlit widgets ---------- */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button,
button[data-testid="stBaseButton-secondary"], button[data-testid="stBaseButton-primaryFormSubmit"],
button[data-testid="stBaseButton-secondaryFormSubmit"] {
  border-radius: var(--r-ctrl);
  border: 1px solid var(--control);
  background: var(--sheet);
  color: var(--ink);
  font-family: var(--font);
  font-size: 13.5px;
  font-weight: 500;
  min-height: 36px;
  padding: 0 12px;
  box-shadow: none;
  transition: background-color 120ms ease, border-color 120ms ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover,
button[data-testid="stBaseButton-secondary"]:hover,
button[data-testid="stBaseButton-secondaryFormSubmit"]:hover {
  border-color: #b9c1c7;
  background: var(--raised);
  color: var(--ink);
}
.stButton > button:focus-visible, .stFormSubmitButton > button:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 1px;
  box-shadow: none;
}
button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] {
  background: var(--accent);
  border-color: var(--accent);
  color: #dbe9df;
}
button[data-testid="stBaseButton-primary"]:hover, button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
  background: var(--accent-ink);
  border-color: var(--accent-ink);
  color: #dbe9df;
}
.stButton > button p, .stFormSubmitButton > button p { font-size: 13.5px; font-weight: 500; }
.stButton > button:disabled, .stButton > button:disabled:hover {
  border-color: var(--border); color: var(--faint); background: var(--raised); opacity: 1;
}

/* inputs */
[data-testid="stTextInput"] div[data-baseweb="input"],
[data-testid="stNumberInput"] div[data-baseweb="input"],
[data-testid="stTextArea"] div[data-baseweb="textarea"],
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  background: var(--sheet);
  border: 1px solid var(--control);
  border-radius: var(--r-ctrl);
  box-shadow: none;
  min-height: 38px;
  transition: border-color 120ms ease;
}
[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within,
[data-testid="stTextArea"] div[data-baseweb="textarea"]:focus-within,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
  border-color: var(--accent);
  box-shadow: inset 0 0 0 1px var(--accent);
}
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] div[data-baseweb="select"] {
  background: transparent;
  color: var(--ink);
  font-family: var(--font);
  font-size: 14px;
  -webkit-text-fill-color: var(--ink);
}
[data-testid="stTextInput"] input::placeholder, [data-testid="stTextArea"] textarea::placeholder {
  color: var(--faint); opacity: 1;
}
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label p {
  font-size: 12.5px !important; font-weight: 500; color: var(--muted);
}
[data-testid="stWidgetLabel"] { margin-bottom: 4px; }
[data-testid="stNumberInput"] button { background: transparent; border: none; color: var(--muted); }

div[data-baseweb="popover"] ul, div[data-baseweb="popover"] div[role="listbox"] { background: var(--sheet); }
div[data-baseweb="popover"] li { font-size: 14px; color: var(--ink); }
div[data-baseweb="popover"] li:hover { background: var(--accent-soft); }

/* form + expander + tabs + alerts */
[data-testid="stForm"] { border: none; padding: 0; }
[data-testid="stExpander"] details {
  border: 1px solid var(--border);
  border-radius: var(--r-card);
  background: var(--sheet);
  overflow: hidden;
}
[data-testid="stExpander"] summary { padding: 11px 14px; font-size: 13.5px; font-weight: 500; color: var(--ink); }
[data-testid="stExpander"] summary:hover { background: var(--raised); color: var(--ink); }
[data-testid="stExpander"] summary svg { color: var(--muted); }
[data-testid="stExpander"] [data-testid="stExpanderDetails"] { padding: 4px 14px 16px; border-top: 1px solid var(--rule); }
[data-testid="stExpander"] p { font-size: 13.5px; }

.stTabs [data-baseweb="tab-list"] { gap: 20px; border-bottom: 1px solid var(--border); }
.stTabs [data-baseweb="tab"] { padding: 8px 0; font-size: 13.5px; color: var(--muted); background: transparent; }
.stTabs [aria-selected="true"] { color: #dbe9df; font-weight: 600; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--accent); height: 2px; }

[data-testid="stAlert"] { border-radius: var(--r-ctrl); border: 1px solid var(--border); font-size: 13.5px; }
[data-testid="stAlert"] p { font-size: 13.5px; }
[data-testid="stAlertContentInfo"] { background: var(--accent-soft); }
[data-testid="stAlertContentSuccess"] { background: var(--pos-soft); }
[data-testid="stAlertContentWarning"] { background: var(--warn-soft); }
[data-testid="stAlertContentError"] { background: var(--neg-soft); }

div[data-baseweb="popover"] [data-testid="stPopoverBody"] {
  background: var(--sheet);
  border: 1px solid var(--border);
  border-radius: var(--r-card);
  box-shadow: 0 10px 28px rgba(19, 20, 22, 0.10);
  padding: 14px;
}
[data-testid="stPopover"] > div > button { min-height: 30px; font-size: 13px; }
[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: var(--r-card); }

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {
  width: 262px !important;
  min-width: 262px !important;
  background-color: #10382c;
  border-right: 1px solid rgba(255,255,255,0.3);
}
section[data-testid="stSidebar"] > div { width: 262px !important; }
[data-testid="stSidebarContent"] { padding: 16px 14px 14px; height: 100%; }
[data-testid="stSidebarUserContent"] { padding: 0; height: 100%; }
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebarHeader"] { padding: 0; height: 0; }
[data-testid="stSidebarCollapseButton"] { color: var(--ink); }
[data-testid="stSidebarCollapseButton"] button { color: var(--ink); }
/* Sidebar fills the whole height: nav up top, account / logout / version pinned to bottom */
[data-testid="stSidebarUserContent"] div[data-testid="stVerticalBlock"] {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 30px);
  gap: 0.7rem;
}
[data-testid="stSidebarUserContent"] div[data-testid="stElementContainer"]:has(.side-spacer) {
  flex: 1 1 auto;
  margin-top: 0;
}
.side-spacer { flex: 1 1 auto; min-height: 8px; }
[data-testid="stSidebarUserContent"] div[data-testid="stElementContainer"]:has(.side-account) {
  margin-top: 0;
  padding-top: 8px;
}
[data-testid="stSidebar"] .stButton > button {
  width: 100%;
  justify-content: flex-start;
  background: transparent;
  border-color: transparent;
  color: #dbe9df;
  min-height: 48px;
  padding: 0 14px;
  font-weight: 500;
}
[data-testid="stSidebar"] .stButton > button:hover { background: rgba(255,255,255,0.08); color: #dbe9df; border-color: transparent; }
[data-testid="stSidebar"] .stButton > button > div { gap: 8px; justify-content: flex-start; }
[data-testid="stSidebar"] .stButton > button:disabled {
  background: rgba(255,255,255,0.12); color: #dbe9df; border-color: rgba(255,255,255,0.2); font-weight: 600;
}
/* Icon fallback: dark for page glyphs (legible on white), white in sidebar */
[data-testid="stIconMaterial"] { color: #131416; }
[data-testid="stSidebar"] .stButton > button [data-testid="stIconMaterial"] { color: #ffffff; }

.side-brand { display: flex; align-items: center; gap: 9px; padding: 2px 2px 14px; }
.side-brand .side-name { font-size: 13px; font-weight: 600; line-height: 1.25; color: #dbe9df; }
.side-brand .side-scope { font-size: 11.5px; color: #dbe9df; margin-top: 1px; }
.side-group { font-size: 11.5px; font-weight: 500; color: #dbe9df; padding: 12px 9px 4px; letter-spacing: 0.01em; }
.side-account { border-top: 1px solid rgba(255,255,255,0.2); margin-top: 10px; padding: 10px 2px 2px; display: flex; align-items: center; gap: 9px; }
.side-account .avatar {
  width: 26px; height: 26px; border-radius: 6px; background: #e8f1f3; color: #10382c;
  font-size: 12px; font-weight: 600; display: flex; align-items: center; justify-content: center; flex: none;
}
.side-account .acc-name { font-size: 12.5px; font-weight: 500; color: #dbe9df; line-height: 1.2; }
.side-account .acc-role { font-size: 11.5px; color: #dbe9df; }
.side-foot { font-size: 11px; color: #dbe9df; padding: 10px 9px 2px; }

/* ---------- responsive ---------- */
@media (max-width: 900px) {
  [data-testid="stMainBlockContainer"] { width: 100%; min-width: 0; padding: 20px 20px 48px; margin: 0.25rem 0.5rem 1rem; border-radius: 12px; }
  .kpi-strip { grid-auto-flow: row; grid-template-columns: repeat(3, 1fr); }
  .page-head { flex-direction: column; gap: 8px; }
  .page-meta { padding-top: 0; }
}
@media (max-width: 560px) {
  [data-testid="stMainBlockContainer"] { width: 100%; min-width: 0; padding: 16px 18px 40px; }
  [data-testid="stHeader"] { padding-left: 10px; }
  .kpi-strip { grid-auto-flow: row; grid-template-columns: repeat(2, 1fr); }
  .kpi { padding: 12px 14px; }
  .kpi-value { font-size: 24px; }
  .page-head h1 { font-size: 22px !important; }
  .matrix th, .matrix td { min-width: 0; }
  .bar-row { grid-template-columns: minmax(84px, 108px) 1fr 28px; gap: 9px; }
  .login-brand { min-height: 0; padding: 26px 22px; }
  .login-brand h2 { font-size: 23px !important; margin-top: 18px; }
}
"""


def apply_custom_styles(login: bool = False) -> None:
    """Inject the app stylesheet once per run, before any other output."""
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)
    if login:
        # The marker lets :has() hide Streamlit's own chrome on this screen only.
        st.markdown('<div id="login-screen" aria-hidden="true"></div>', unsafe_allow_html=True)



