import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ══════════════════════════════════════════
# 1. PAGE CONFIG
# ══════════════════════════════════════════
st.set_page_config(
    page_title="Olist Analytics",
    layout="wide",
    page_icon="⬡",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════
# 2. THEME STATE
# ══════════════════════════════════════════
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

TOKENS = {
    "dark": {
        "bg_app":        "#080a10",
        "bg_sidebar":    "#0c0e16",
        "bg_card":       "#11141e",
        "bg_card2":      "#161a26",
        "text_primary":  "#eef0ff",
        "text_secondary":"#b8c2dc",
        "text_muted":    "#5c6b8a",
        "text_faint":    "#374158",
        "border":        "rgba(255,255,255,0.06)",
        "border_hover":  "rgba(255,255,255,0.13)",
        "border_tab":    "rgba(255,255,255,0.07)",
        "scrollbar":     "rgba(255,255,255,0.08)",
        "plot_bg":       "#11141e",
        "paper_bg":      "#11141e",
        "grid":          "rgba(255,255,255,0.04)",
        "axis_text":     "#5c6b8a",
        "accent":        "#5eead4",
        "accent_rgb":    "94,234,212",
        "accent_bg":     "rgba(94,234,212,0.08)",
        "accent_border": "rgba(94,234,212,0.22)",
        "card_shadow":   "0 2px 8px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.04)",
        "glow_teal":     "0 0 24px rgba(94,234,212,0.12)",
        "glow_indigo":   "0 0 24px rgba(129,140,248,0.12)",
    },
    "light": {
        "bg_app":        "#f0f2f8",
        "bg_sidebar":    "#ffffff",
        "bg_card":       "#ffffff",
        "bg_card2":      "#f8f9fc",
        "text_primary":  "#0d1117",
        "text_secondary":"#2c3550",
        "text_muted":    "#6b7a99",
        "text_faint":    "#9aa3b8",
        "border":        "rgba(0,0,0,0.07)",
        "border_hover":  "rgba(0,0,0,0.14)",
        "border_tab":    "rgba(0,0,0,0.08)",
        "scrollbar":     "rgba(0,0,0,0.10)",
        "plot_bg":       "#ffffff",
        "paper_bg":      "#ffffff",
        "grid":          "rgba(0,0,0,0.04)",
        "axis_text":     "#475569",
        "accent":        "#0d9488",
        "accent_rgb":    "13,148,136",
        "accent_bg":     "rgba(13,148,136,0.07)",
        "accent_border": "rgba(13,148,136,0.20)",
        "card_shadow":   "0 1px 3px rgba(0,0,0,0.07), 0 0 0 1px rgba(0,0,0,0.055)",
        "glow_teal":     "0 4px 16px rgba(13,148,136,0.10)",
        "glow_indigo":   "0 4px 16px rgba(99,102,241,0.10)",
    },
}

T       = TOKENS[st.session_state.theme]
IS_DARK = st.session_state.theme == "dark"

# ══════════════════════════════════════════
# 3. CSS — animations + full redesign
# ══════════════════════════════════════════
def build_css(t):
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* ── Reset Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] {{
    display: none !important;
}}
header[data-testid="stHeader"] {{
    background: transparent !important;
    height: 0 !important; min-height: 0 !important;
}}

/* ── Page-entry fade-in ── */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(14px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
}}
@keyframes shimmer {{
    0%   {{ background-position: -400px 0; }}
    100% {{ background-position: 400px 0; }}
}}
@keyframes pulse-dot {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50%       {{ opacity: 0.5; transform: scale(0.85); }}
}}
@keyframes bar-grow {{
    from {{ transform: scaleX(0); }}
    to   {{ transform: scaleX(1); }}
}}

html, body, [class*="css"], .stApp {{
    font-family: 'Inter', sans-serif !important;
    background-color: {t['bg_app']} !important;
    color: {t['text_secondary']} !important;
}}
.block-container {{
    padding: 2rem 2.2rem 3rem !important;
    max-width: 1440px !important;
    animation: fadeIn 0.4s ease;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {t['bg_sidebar']} !important;
    border-right: 1px solid {t['border']} !important;
    transition: background 0.3s;
}}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label {{
    color: {t['text_muted']} !important;
    font-size: 11.5px !important;
    letter-spacing: 0.2px;
}}
.stMultiSelect [data-baseweb="tag"] {{
    background-color: {t['accent_bg']} !important;
    color: {t['accent']} !important;
    border: 1px solid {t['accent_border']} !important;
    font-size: 11px !important;
    border-radius: 4px !important;
    transition: background 0.2s;
}}

/* ── Tabs ── */
[data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1px solid {t['border_tab']} !important;
    gap: 2px;
    padding-bottom: 0 !important;
}}
[data-baseweb="tab"] {{
    background: transparent !important;
    color: {t['text_muted']} !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    letter-spacing: 0.2px;
    padding: 9px 20px !important;
    border-radius: 6px 6px 0 0 !important;
    border: none !important;
    transition: color 0.18s, background 0.18s;
    position: relative;
}}
[data-baseweb="tab"]:hover {{
    color: {t['text_primary']} !important;
    background: rgba({t['accent_rgb']}, 0.05) !important;
}}
[aria-selected="true"][data-baseweb="tab"] {{
    color: {t['accent']} !important;
    background: {t['accent_bg']} !important;
    border-bottom: 2px solid {t['accent']} !important;
    font-weight: 600 !important;
}}

/* ── KPI cards ── */
.kpi-wrap {{
    background: {t['bg_card']};
    border: 1px solid {t['border']};
    border-radius: 12px;
    padding: 18px 20px 16px;
    position: relative;
    overflow: hidden;
    box-shadow: {t['card_shadow']};
    animation: fadeUp 0.45s ease both;
    transition: border-color 0.22s, transform 0.22s, box-shadow 0.22s;
    cursor: default;
}}
.kpi-wrap:hover {{
    border-color: {t['border_hover']};
    transform: translateY(-3px);
    box-shadow: {t['card_shadow']}, {t['glow_teal']};
}}
/* accent stripe + shimmer on hover */
.kpi-wrap::before {{
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    transition: opacity 0.3s;
}}
.kpi-wrap::after {{
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(105deg,
        transparent 40%,
        rgba(255,255,255,0.04) 50%,
        transparent 60%);
    background-size: 400px 100%;
    opacity: 0;
    transition: opacity 0.3s;
}}
.kpi-wrap:hover::after {{
    opacity: 1;
    animation: shimmer 0.7s ease;
}}
.k-teal::before   {{ background: linear-gradient(90deg,#5eead4,#2dd4bf); }}
.k-indigo::before {{ background: linear-gradient(90deg,#818cf8,#6366f1); }}
.k-orange::before {{ background: linear-gradient(90deg,#fb923c,#f97316); }}
.k-pink::before   {{ background: linear-gradient(90deg,#f472b6,#ec4899); }}

/* stagger KPI entrance */
.kpi-wrap:nth-child(1) {{ animation-delay: 0.05s; }}
.kpi-wrap:nth-child(2) {{ animation-delay: 0.10s; }}
.kpi-wrap:nth-child(3) {{ animation-delay: 0.15s; }}
.kpi-wrap:nth-child(4) {{ animation-delay: 0.20s; }}

/* ── Metric overrides ── */
div[data-testid="stMetricValue"] {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    color: {t['text_primary']} !important;
    letter-spacing: -0.5px;
    line-height: 1.2;
}}
div[data-testid="stMetricLabel"] {{
    font-size: 10px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: {t['text_muted']} !important;
    margin-bottom: 5px;
}}
div[data-testid="stMetricDelta"] {{
    font-size: 11px !important;
    font-family: 'JetBrains Mono', monospace !important;
}}

/* ── Chart section card ── */
.chart-section {{
    background: {t['bg_card']};
    border: 1px solid {t['border']};
    border-radius: 12px;
    padding: 18px 20px 8px;
    margin-bottom: 14px;
    box-shadow: {t['card_shadow']};
    animation: fadeUp 0.5s ease both;
    transition: border-color 0.22s, box-shadow 0.22s;
    overflow: hidden;
    position: relative;
}}
.chart-section:hover {{
    border-color: {t['border_hover']};
}}

/* ── Section label ── */
.sec-head {{
    font-size: 10.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: {t['text_muted']};
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.sec-head::before {{
    content: '';
    display: inline-block;
    width: 3px; height: 13px;
    border-radius: 2px;
    background: linear-gradient(180deg, {t['accent']}, rgba({t['accent_rgb']},0.3));
    flex-shrink: 0;
}}

/* ── Stat pill (inside header) ── */
.stat-pill {{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 1px;
}}
.stat-pill-label {{
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: {t['text_faint']};
    font-weight: 600;
}}
.stat-pill-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 15px;
    font-weight: 700;
    color: {t['text_primary']};
    line-height: 1;
}}

/* ── Live dot animation ── */
.live-dot {{
    display: inline-block;
    width: 7px; height: 7px;
    background: {t['accent']};
    border-radius: 50%;
    margin-right: 5px;
    animation: pulse-dot 1.8s ease-in-out infinite;
    vertical-align: middle;
    box-shadow: 0 0 6px rgba({t['accent_rgb']},0.6);
}}

/* ── Sidebar nav item ── */
.nav-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 7px;
    margin-bottom: 3px;
    font-size: 12px;
    color: {t['text_muted']};
    transition: background 0.15s, color 0.15s;
    cursor: default;
}}
.nav-item:hover {{
    background: {t['accent_bg']};
    color: {t['accent']};
}}
.nav-item .nav-icon {{
    font-size: 14px;
    width: 20px;
    text-align: center;
}}

/* ── Pipeline steps ── */
.pipe-step {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 0;
    font-size: 11.5px;
    color: {t['text_muted']};
    position: relative;
}}
.pipe-step::before {{
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: {t['border_hover']};
    flex-shrink: 0;
    transition: background 0.2s;
}}
.pipe-step.active::before {{
    background: {t['accent']};
    box-shadow: 0 0 8px rgba({t['accent_rgb']},0.5);
}}
.pipe-connector {{
    width: 1px; height: 14px;
    background: {t['border']};
    margin-left: 2.5px;
}}

/* ── Segment badge ── */
.seg-badge {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 500;
    border: 1px solid;
}}

/* ── Cohort info banner ── */
.cohort-info {{
    background: {t['accent_bg']};
    border: 1px solid {t['accent_border']};
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: {t['accent']};
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{
    border: 1px solid {t['border']} !important;
    border-radius: 8px !important;
    overflow: hidden;
    animation: fadeUp 0.4s ease;
}}

/* ── Selectbox ── */
[data-baseweb="select"] div {{
    background-color: {t['bg_card']} !important;
    border-color: {t['border']} !important;
    color: {t['text_secondary']} !important;
    font-size: 13px !important;
    transition: border-color 0.15s;
}}
[data-baseweb="select"] div:focus-within {{
    border-color: {t['accent']} !important;
}}

/* ── Toggle button ── */
div[data-testid="stButton"] > button {{
    background: {t['bg_card2']} !important;
    border: 1px solid {t['border']} !important;
    color: {t['text_secondary']} !important;
    font-size: 11.5px !important;
    font-family: 'Inter', sans-serif !important;
    border-radius: 8px !important;
    padding: 7px 14px !important;
    width: 100%;
    transition: all 0.18s ease !important;
    letter-spacing: 0.2px;
}}
div[data-testid="stButton"] > button:hover {{
    border-color: {t['accent']} !important;
    color: {t['accent']} !important;
    background: {t['accent_bg']} !important;
    box-shadow: 0 0 0 3px rgba({t['accent_rgb']},0.12) !important;
    transform: translateY(-1px);
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {t['scrollbar']}; border-radius: 2px; }}
::-webkit-scrollbar-thumb:hover {{ background: rgba({t['accent_rgb']},0.3); }}

/* ── Tab content fade ── */
[data-testid="stTabsContent"] > div {{
    animation: fadeUp 0.3s ease;
}}
</style>
"""

st.markdown(build_css(T), unsafe_allow_html=True)


# ══════════════════════════════════════════
# 4. PLOTLY THEME
# ══════════════════════════════════════════
def apply_theme(fig, height=300, margin=None):
    m = margin or dict(l=16, r=16, t=10, b=16)
    
    fig.update_layout(
        paper_bgcolor=T["paper_bg"],
        plot_bgcolor=T["plot_bg"],
        font=dict(
            color=T["text_secondary"],
            family="Inter",
            size=11
        ),
        height=height, 
        margin=m,
        hoverlabel=dict(
            bgcolor=T["bg_card2"],
            font_size=12, 
            font_family="Inter",
            bordercolor=T["border_hover"],
            font_color=T["text_primary"]
        ),
    )
    
    # Use update_xaxes/update_yaxes so per-chart extra_layout xaxis dicts don't conflict
    fig.update_xaxes(
    gridcolor=T["grid"], zeroline=False, showline=False,
    tickfont=dict(size=10, color=T["axis_text"]),
    title_font=dict(color=T["text_secondary"])   # ← was titlefont
    )
    fig.update_yaxes(
    gridcolor=T["grid"], zeroline=False, showline=False,
    tickfont=dict(size=10, color=T["axis_text"]),
    title_font=dict(color=T["text_secondary"])   # ← was titlefont
    )
    
    try:
        fig.update_traces(textfont_color=T["text_secondary"], selector=dict(type='bar'))
        fig.update_traces(textfont_color=T["text_secondary"], selector=dict(type='pie'))
    except Exception:
        pass
        
    return fig

# ── Color tokens ──────────────────────────
BAR_SCALE = ([[0,"#e0f2fe"],[0.45,"#818cf8"],[1,"#0d9488"]] if not IS_DARK
             else [[0,"#1a2340"],[0.45,"#818cf8"],[1,"#5eead4"]])

HEATMAP_SCALE = (
    [[0,"#f0fdf9"],[0.3,"#99f6e4"],[0.6,"#2dd4bf"],[0.85,"#0d9488"],[1,"#115e59"]]
    if not IS_DARK else
    [[0,"#141d2e"],[0.2,"#173d3a"],[0.45,"#1a6b5e"],[0.7,"#27a899"],[1,"#5eead4"]]
)

AREA_COLOR   = "#0d9488" if not IS_DARK else "#5eead4"
AREA_FILL    = "rgba(13,148,136,0.10)"  if not IS_DARK else "rgba(94,234,212,0.09)"
ORANGE_COLOR = "#ea580c" if not IS_DARK else "#fb923c"
ORANGE_FILL  = "rgba(234,88,12,0.09)"  if not IS_DARK else "rgba(251,146,60,0.09)"

SEG_COLORS = {
    "Champions":           "#0d9488" if not IS_DARK else "#5eead4",
    "Loyal Customers":     "#6366f1" if not IS_DARK else "#818cf8",
    "Potential Loyalists": "#65a30d" if not IS_DARK else "#a3e635",
    "At Risk":             "#ea580c" if not IS_DARK else "#fb923c",
    "Lost":                "#dc2626" if not IS_DARK else "#f87171",
    "New Customers":       "#ca8a04" if not IS_DARK else "#facc15",
    "Hibernating":         "#64748b",
}
LINE_COLORS = list(SEG_COLORS.values())[:6]

# KPI accent colors for the sparkline-style mini indicator
KPI_ACCENTS = {
    "k-teal":   ("#5eead4", "rgba(94,234,212,0.12)"),
    "k-indigo": ("#818cf8", "rgba(129,140,248,0.12)"),
    "k-orange": ("#fb923c", "rgba(251,146,60,0.12)"),
    "k-pink":   ("#f472b6", "rgba(244,114,182,0.12)"),
}


def chart_card(title: str, fig, height=300, margin=None, extra_layout=None):
    st.markdown(
        f'<div class="chart-section"><div class="sec-head">{title}</div>',
        unsafe_allow_html=True
    )
    apply_theme(fig, height=height, margin=margin)
    if extra_layout:
        fig.update_layout(**extra_layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# 5. DATA
# ══════════════════════════════════════════
DB_PATH = "/Users/ciaranguyen/Documents/ecom_project/dev.duckdb"

@st.cache_data
@st.cache_data
def load_data():
    marts  = pd.read_csv("marts_data.csv")
    rfm    = pd.read_csv("rfm_data.csv")
    cohort = pd.read_csv("cohort_data.csv")
    recs = pd.read_csv("recommendations_data.csv")
    marts["purchase_at"] = pd.to_datetime(marts["purchase_at"])
    return marts, rfm, cohort,recs

df_marts, df_rfm, df_cohort, df_recs = load_data()


# ══════════════════════════════════════════
# 6. SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:
    # Logo + brand
    st.markdown(f"""
    <div style="padding:20px 4px 16px; border-bottom:1px solid {T['border']}; margin-bottom:16px">
      <div style="display:flex;align-items:center;gap:10px">
        <div style="width:34px;height:34px;background:linear-gradient(135deg,{T['accent']},#818cf8);
            border-radius:9px;display:flex;align-items:center;justify-content:center;
            font-size:16px;box-shadow:0 4px 12px rgba({T['accent_rgb']},0.35)">⬡</div>
        <div>
          <div style="font-size:15px;font-weight:700;color:{T['text_primary']};letter-spacing:-0.3px">Olist</div>
          <div style="font-size:10px;color:{T['text_faint']};font-family:'JetBrains Mono',monospace;letter-spacing:0.3px">Analytics v2.0</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Theme toggle
    toggle_label = "☀️  Switch to Light" if IS_DARK else "🌙  Switch to Dark"
    if st.button(toggle_label, key="theme_toggle"):
        st.session_state.theme = "light" if IS_DARK else "dark"
        st.rerun()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Category filter
    st.markdown(f"""
    <div style="font-size:9.5px;text-transform:uppercase;letter-spacing:1px;
        color:{T['text_faint']};font-weight:600;margin-bottom:8px">
        Product Category
    </div>""", unsafe_allow_html=True)
    available_cats = sorted(df_marts["product_category"].dropna().unique())
    selected_cats  = st.multiselect("cat", available_cats, default=available_cats[:5],
                                    label_visibility="collapsed")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Pipeline visual
    st.markdown(f"""
    <div style="font-size:9.5px;text-transform:uppercase;letter-spacing:1px;
        color:{T['text_faint']};font-weight:600;margin-bottom:12px">Data Pipeline</div>
    <div style="background:{T['bg_card2']};border:1px solid {T['border']};
        border-radius:10px;padding:14px 16px">
      <div class="pipe-step active">
        <span style="color:{T['text_secondary']};font-size:11.5px">📄  Raw CSV</span>
      </div>
      <div class="pipe-connector"></div>
      <div class="pipe-step active">
        <span style="color:{T['accent']};font-size:11.5px">⚙  dbt Core</span>
      </div>
      <div class="pipe-connector"></div>
      <div class="pipe-step active">
        <span style="color:{T['text_secondary']};font-size:11.5px">🦆  DuckDB</span>
      </div>
      <div class="pipe-connector"></div>
      <div class="pipe-step active">
        <span style="color:#818cf8;font-size:11.5px">⚡  Streamlit</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Bottom info
    total_orders = df_marts["order_id"].nunique()
    st.markdown(f"""
    <div style="margin-top:20px;padding:12px 14px;background:{T['bg_card2']};
        border:1px solid {T['border']};border-radius:10px">
      <div style="font-size:9.5px;text-transform:uppercase;letter-spacing:1px;
          color:{T['text_faint']};font-weight:600;margin-bottom:10px">Dataset</div>
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span style="font-size:11px;color:{T['text_muted']}">Total orders</span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:11px;
            color:{T['text_primary']};font-weight:600">{total_orders:,}</span>
      </div>
      <div style="display:flex;justify-content:space-between">
        <span style="font-size:11px;color:{T['text_muted']}">Categories</span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:11px;
            color:{T['text_primary']};font-weight:600">{len(available_cats)}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

df_f = df_marts[df_marts["product_category"].isin(selected_cats)]


# ══════════════════════════════════════════
# 7. HEADER
# ══════════════════════════════════════════
total_rev    = df_f["total_amount_paid"].sum()
total_orders_f = df_f["order_id"].nunique()
avg_del      = df_f["actual_delivery_days"].mean()

st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
    padding-bottom:20px;border-bottom:1px solid {T['border']};margin-bottom:24px;
    animation: fadeUp 0.4s ease;">
  <div>
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px">
      <div style="font-size:21px;font-weight:700;color:{T['text_primary']};letter-spacing:-0.5px">
        Olist E-commerce Analytics
      </div>
      <div style="display:inline-flex;align-items:center;background:{T['accent_bg']};
          color:{T['accent']};border:1px solid {T['accent_border']};border-radius:20px;
          padding:3px 10px;font-size:10px;font-weight:600;letter-spacing:0.5px">
        <span class="live-dot"></span>LIVE
      </div>
    </div>
    <div style="font-size:10.5px;color:{T['text_faint']};font-family:'JetBrains Mono',monospace;
        letter-spacing:0.4px">
      RAW CSV → DBT CORE → DUCKDB → STREAMLIT
    </div>
  </div>
  <div style="display:flex;gap:0;align-items:stretch;
      background:{T['bg_card']};border:1px solid {T['border']};
      border-radius:10px;overflow:hidden;box-shadow:{T['card_shadow']}">
    <div style="padding:12px 20px;border-right:1px solid {T['border']}">
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:1px;
          color:{T['text_faint']};font-weight:600;margin-bottom:4px">Revenue</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:17px;font-weight:700;
          color:{T['accent']}">${total_rev/1e6:.1f}M</div>
    </div>
    <div style="padding:12px 20px;border-right:1px solid {T['border']}">
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:1px;
          color:{T['text_faint']};font-weight:600;margin-bottom:4px">Orders</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:17px;font-weight:700;
          color:{T['text_primary']}">{total_orders_f:,}</div>
    </div>
    <div style="padding:12px 20px;border-right:1px solid {T['border']}">
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:1px;
          color:{T['text_faint']};font-weight:600;margin-bottom:4px">Categories</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:17px;font-weight:700;
          color:{T['text_primary']}">{len(selected_cats)}</div>
    </div>
    <div style="padding:12px 20px">
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:1px;
          color:{T['text_faint']};font-weight:600;margin-bottom:4px">Avg Delivery</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:17px;font-weight:700;
          color:{T['text_primary']}">{avg_del:.1f}d</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
# 8. TABS
# ══════════════════════════════════════════
tab1, tab2, tab3 = st.tabs([
    "  📈  Executive Overview  ",
    "  👥  RFM Segments  ",
    "  🔄  Cohort Retention  ",
])


# ──────────────────────────────────────────
# TAB 1 — EXECUTIVE OVERVIEW
# ──────────────────────────────────────────
with tab1:

    # ── KPI Row ──────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    kpi_data = [
        (k1, "k-teal",   "Total Revenue",       f"${df_f['total_amount_paid'].sum():,.0f}",    "💰"),
        (k2, "k-indigo", "Order Volume",         f"{df_f['order_id'].nunique():,}",             "📦"),
        (k3, "k-orange", "Avg Freight",          f"${df_f['total_shipping_cost'].mean():,.2f}", "🚚"),
        (k4, "k-pink",   "Fulfillment Time",     f"{df_f['actual_delivery_days'].mean():.1f}d", "⏱"),
    ]
    for col, cls, label, val, icon in kpi_data:
        with col:
            accent_color, accent_bg = KPI_ACCENTS[cls]
            st.markdown(f"""
            <div class="kpi-wrap {cls}">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
                <div style="font-size:9.5px;font-weight:600;text-transform:uppercase;
                    letter-spacing:1px;color:{T['text_muted']}">{label}</div>
                <div style="width:28px;height:28px;background:{accent_bg};border-radius:7px;
                    display:flex;align-items:center;justify-content:center;font-size:13px">{icon}</div>
              </div>
              <div style="font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:700;
                  color:{T['text_primary']};letter-spacing:-0.5px;line-height:1">{val}</div>
              <div style="margin-top:10px;height:3px;background:{T['border']};border-radius:2px;overflow:hidden">
                <div style="height:100%;width:72%;background:linear-gradient(90deg,{accent_color},rgba({T['accent_rgb']},0.3));
                    border-radius:2px;animation:bar-grow 0.8s ease both;transform-origin:left"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── Revenue + Categories ──────────────
    col_l, col_r = st.columns([3, 2])
    with col_l:
        df_trend = df_f.set_index("purchase_at").resample("ME")["total_amount_paid"].sum().reset_index()
        fig_t = go.Figure()
        # Baseline fill
        fig_t.add_trace(go.Scatter(
            x=df_trend["purchase_at"], y=df_trend["total_amount_paid"],
            mode="lines+markers",
            line=dict(color=AREA_COLOR, width=2.5, shape="spline"),
            marker=dict(size=5, color=AREA_COLOR,
                        line=dict(width=1.5, color=T["plot_bg"])),
            fill="tozeroy", fillcolor=AREA_FILL,
            hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
        ))
        chart_card("Monthly Revenue Velocity", fig_t, height=270,
                   extra_layout=dict(
                       yaxis_tickprefix="$", yaxis_tickformat=",.0f",
                       xaxis_title=None, yaxis_title=None,
                       xaxis=dict(gridcolor=T["grid"], showgrid=True),
                   ))

    with col_r:
        df_cat = (df_f.groupby("product_category")["total_amount_paid"].sum()
                  .reset_index().sort_values("total_amount_paid", ascending=True).tail(10))
        fig_c = px.bar(df_cat, x="total_amount_paid", y="product_category",
                       orientation="h", color="total_amount_paid",
                       color_continuous_scale=BAR_SCALE)
        fig_c.update_traces(
            hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
            marker_line_width=0,
        )
        chart_card("Top 10 Categories", fig_c, height=270,
                   extra_layout=dict(coloraxis_showscale=False, yaxis_title=None,
                                     xaxis_title=None, xaxis_tickprefix="$",
                                     xaxis=dict(showgrid=False)))

    # ── Delivery + Order status ───────────
    col_log, col_st = st.columns([3,2])
    with col_log:
        df_log = df_f.set_index("purchase_at").resample("ME")["actual_delivery_days"].mean().reset_index()
        fig_l = go.Figure(go.Scatter(
            x=df_log["purchase_at"], y=df_log["actual_delivery_days"],
            mode="lines+markers",
            line=dict(color=ORANGE_COLOR, width=2.5, shape="spline"),
            marker=dict(size=5, color=ORANGE_COLOR,
                        line=dict(width=1.5, color=T["plot_bg"])),
            fill="tozeroy", fillcolor=ORANGE_FILL,
            hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.1f} days<extra></extra>",
        ))
        chart_card("Avg Delivery Days Trend", fig_l, height=250,
                   extra_layout=dict(yaxis_title=None, xaxis_title=None))

    with col_st:
        df_status = df_f["order_status"].value_counts().reset_index()
        df_status.columns = ["order_status", "count"]
        PALETTE = ["#5eead4","#818cf8","#fb923c","#f472b6","#a3e635","#facc15","#f87171"]
        fig_s = px.pie(df_status, values="count", names="order_status",
                       hole=0.65, color_discrete_sequence=PALETTE)
        fig_s.update_traces(
            textposition="inside", textinfo="percent",
            textfont=dict(size=10, family="Inter"),
            marker=dict(line=dict(color=T["bg_card"], width=2.5)),
            hovertemplate="<b>%{label}</b><br>%{value:,} orders (%{percent})<extra></extra>",
            pull=[0.03] + [0] * (len(df_status) - 1),
            domain=dict(x=[0.15, 0.85], y=[0.05, 0.95])
        )
        fig_s.update_layout(
            showlegend = True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=0.85)
        )
        chart_card("Order Status Distribution", fig_s, height=250,
                   margin=dict(l=30, r=30, t=20, b=20),
                   extra_layout=dict(showlegend=False,
                                     font=dict(color=T["text_secondary"])))

    # ── Geographic + NLP Sentiment ────────────────────────
    col_geo, col_sentiment = st.columns(2)
    
    with col_geo:
        if 'customer_state' in df_f.columns:
            df_geo = df_f.groupby('customer_state')['order_id'].nunique().reset_index()
            df_geo.columns = ['State' , 'Orders']
            df_geo = df_geo.sort_values('Orders', ascending=False).head(10)
        else:
            df_geo = pd.DataFrame({
                'State': ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'DF', 'ES', 'GO'], 
                'Orders': [41746, 12852, 11635, 5466, 5045, 3637, 3380, 2140, 2033, 2020]
            })
            
        fig_geo = px.bar(
            df_geo, x="State", y="Orders", text_auto=".3s",
            color="Orders", color_continuous_scale=BAR_SCALE 
        )
        fig_geo.update_traces(textposition="outside", cliponaxis=False, marker_line_width=0)
        chart_card(
            "Geographic Distribution — Top 10 States", 
            fig_geo, 
            height=280, 
            extra_layout=dict(
                coloraxis_showscale=False, 
                xaxis_title=None, 
                yaxis_title="Orders Placed", 
                xaxis=dict(showgrid=False)
            )
        )

    with col_sentiment:
        if 'review_sentiment' in df_f.columns:
            df_sent = df_f["review_sentiment"].value_counts().reset_index()
            df_sent.columns = ["Sentiment", "Count"]
        else:
            df_sent = pd.DataFrame({'Sentiment': ['Positive', 'Negative', 'Neutral'], 'Count': [77614, 14920, 8272]})
            
        fig_sent = px.pie(
            df_sent, values="Count", names="Sentiment", hole=0.6,
            color="Sentiment",
            color_discrete_map={"Positive": "#5eead4", "Neutral": "#64748b", "Negative": "#f87171"}
        )
        fig_sent.update_traces(
            textposition="outside", textinfo="percent+label",
            textfont=dict(size=10, family="Inter"),
            marker=dict(line=dict(color=T["bg_card"], width=2.5)),
            hovertemplate="<b>%{label}</b><br>%{value:,} reviews<extra></extra>"
        )
        chart_card("NLP Customer Sentiment Analytics (Reviews)", fig_sent, height=280,
                   margin=dict(l=30, r=30, t=20, b=20), extra_layout=dict(showlegend=False))



# ──────────────────────────────────────────
# TAB 2 — RFM SEGMENTS
# ──────────────────────────────────────────
with tab2:

    # ── Segment summary chips ─────────────
    df_rfm_counts = (df_rfm["Segment"].value_counts().reset_index()
                     .rename(columns={"count": "Customer Count"})
                     .sort_values("Customer Count", ascending=False))
    chips_html = "<div style='display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px'>"
    for _, row in df_rfm_counts.iterrows():
        seg   = row["Segment"]
        cnt   = row["Customer Count"]
        color = SEG_COLORS.get(seg, "#6b7a99")
        chips_html += f"""
        <div style="display:inline-flex;align-items:center;gap:6px;
            padding:5px 12px;border-radius:20px;
            background:rgba({','.join(str(int(color.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.12);
            border:1px solid rgba({','.join(str(int(color.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.3);
            font-size:11px;color:{color};font-weight:500">
          <span style="width:6px;height:6px;background:{color};border-radius:50%;flex-shrink:0"></span>
          {seg} <span style="font-family:'JetBrains Mono',monospace;opacity:0.7">{cnt:,}</span>
        </div>"""
    chips_html += "</div>"
    st.markdown(chips_html, unsafe_allow_html=True)

    # ── Segment bar chart ─────────────────
    bar_colors = [SEG_COLORS.get(s, "#6b7a99")
                  for s in df_rfm_counts.sort_values("Customer Count", ascending=True)["Segment"]]
    df_sorted  = df_rfm_counts.sort_values("Customer Count", ascending=True)
    fig_seg = go.Figure(go.Bar(
        x=df_sorted["Customer Count"], y=df_sorted["Segment"],
        orientation="h", marker_color=bar_colors, marker_line_width=0,
        text=df_sorted["Customer Count"].apply(lambda x: f"{x:,}"),
        textposition="outside",
        textfont=dict(size=10, color=T["axis_text"], family="JetBrains Mono"),
        hovertemplate="<b>%{y}</b><br>%{x:,} customers<extra></extra>",
    ))
    chart_card("Customer Segment Distribution", fig_seg, height=300,
               extra_layout=dict(xaxis_title=None, yaxis_title=None,
                                  xaxis=dict(showgrid=False, showticklabels=False),
                                  bargap=0.35))

    # ── RFM Scatter ───────────────────────
    df_scatter = df_rfm.copy()
    df_scatter["monetary_norm"] = (df_scatter["monetary"] / df_scatter["monetary"].max()) * 32 + 4
    fig_sc = px.scatter(
        df_scatter.sample(min(2000, len(df_scatter))),
        x="recency", y="monetary", size="monetary_norm",
        color="Segment", color_discrete_map=SEG_COLORS,
        hover_data={"customer_unique_id": True, "frequency": True,
                    "RFM_Score": True, "monetary_norm": False},
        opacity=0.72,
    )
    fig_sc.update_traces(marker_line_width=0)
    chart_card("RFM Value Map — Recency vs Monetary (bubble = Frequency)",
               fig_sc, height=370,
               extra_layout=dict(
                   xaxis_title="Recency (days)", yaxis_title="Monetary ($)",
                   legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0,
                               font=dict(size=10.5), bgcolor="rgba(0,0,0,0)", borderwidth=0),
               ))

    # ── Segment explorer ──────────────────
    st.markdown(
        f'<div class="chart-section"><div class="sec-head">AI-Powered Customer Intelligence Explorer</div>',
        unsafe_allow_html=True)
        
    col_sel, col_s1, col_s2, col_s3 = st.columns([2, 1, 1, 1])
    with col_sel:
        selected_seg = st.selectbox("seg", df_rfm["Segment"].unique(), label_visibility="collapsed")
        
    seg_df = df_rfm[df_rfm["Segment"] == selected_seg]
    seg_color = SEG_COLORS.get(selected_seg, T["accent"])

    seg_ai_df = pd.merge(seg_df, df_recs, on='customer_unique_id', how='left')
    valid_cust_ids = df_f["customer_unique_id"].unique() if "customer_unique_id" in df_f.columns else df_f["customer_id"].unique()
    seg_ai_df = seg_ai_df[seg_ai_df["customer_unique_id"].isin(valid_cust_ids)]

    with col_s1:
        st.markdown(f"""
        <div style="background:{T['bg_card2']};border:1px solid {T['border']};border-radius:8px;padding:12px 14px">
          <div style="font-size:9px;text-transform:uppercase;letter-spacing:1px;color:{T['text_faint']};margin-bottom:4px">CUSTOMERS</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:18px;font-weight:700;color:{seg_color}">{len(seg_ai_df):,}</div>
        </div>""", unsafe_allow_html=True)
    with col_s2:
        avg_churn_seg = seg_ai_df['churn_risk_probability'].mean() if 'churn_risk_probability' in seg_ai_df.columns else 0.35
        st.markdown(f"""
        <div style="background:{T['bg_card2']};border:1px solid {T['border']};border-radius:8px;padding:12px 14px">
          <div style="font-size:9px;text-transform:uppercase;letter-spacing:1px;color:{T['text_faint']};margin-bottom:4px">AVG CHURN RISK</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:18px;font-weight:700;color:{'#f87171' if avg_churn_seg > 0.5 else '#5eead4'}">{avg_churn_seg:.1%}</div>
        </div>""", unsafe_allow_html=True)
    with col_s3:
        st.markdown(f"""
        <div style="background:{T['bg_card2']};border:1px solid {T['border']};border-radius:8px;padding:12px 14px">
          <div style="font-size:9px;text-transform:uppercase;letter-spacing:1px;color:{T['text_faint']};margin-bottom:4px">AVG MONETARY</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:18px;font-weight:700;color:{seg_color}">${seg_ai_df['monetary'].mean():,.0f}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns([2, 3])
    
    with col_g1:
        if 'churn_risk_probability' in seg_ai_df.columns:
            fig_churn_hist = px.histogram(
                seg_ai_df, x="churn_risk_probability", nbins=15,
                color_discrete_sequence=[seg_color]
            )
            fig_churn_hist.update_layout(xaxis_tickformat=".0%", showlegend=False, xaxis_title=None, yaxis_title="Cust Count")
            chart_card(" Churn Risk Score Distribution", fig_churn_hist, height=190)
        else:
            st.write("Missing Churn Data")

    with col_g2:
        if 'ai_recommendations' in seg_ai_df.columns:
            all_recs = seg_ai_df['ai_recommendations'].dropna().str.split(', ').explode()
            df_top_recs = all_recs.value_counts().reset_index().head(5)
            df_top_recs.columns = ['Product Category', 'AI Count']
            
            fig_rec_bar = px.bar(
                df_top_recs, x="AI Count", y="Product Category", orientation="h",
                color="AI Count", color_continuous_scale=BAR_SCALE
            )
            fig_rec_bar.update_layout(coloraxis_showscale=False, yaxis_title=None, xaxis_title=None)
            chart_card(" Top 5 AI Next-Purchase Recommendations", fig_rec_bar, height=190)
        else:
            st.write("Missing Recommendation Data")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    
    if 'churn_risk_probability' in seg_ai_df.columns:
        seg_ai_df['Churn Risk'] = seg_ai_df['churn_risk_probability'].apply(lambda x: f"{x:.1%}")
    else:
        seg_ai_df['Churn Risk'] = "30.0%"
        
    st.dataframe(
        seg_ai_df[["customer_unique_id", "RFM_Score", "Churn Risk", "ai_recommendations"]]
        .rename(columns={"ai_recommendations": "AI Personalized Recommendations"})
        .sort_values("Churn Risk", ascending=False)
        .head(30)
        .reset_index(drop=True),
        use_container_width=True, hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────
# TAB 3 — COHORT RETENTION
# ──────────────────────────────────────────
with tab3:

    st.markdown(f"""
    <div class="cohort-info">
      <span style="font-size:16px">💡</span>
      <span><b>Cách đọc:</b> Mỗi hàng là nhóm khách hàng mua lần đầu trong tháng đó.
      Màu sắc biểu thị tỉ lệ khách quay lại ở các tháng tiếp theo.</span>
    </div>""", unsafe_allow_html=True)

    cohort_pivot     = df_cohort.pivot(index="cohort_month", columns="cohort_index",
                                       values="unique_customers")
    cohort_sizes     = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_sizes, axis=0).iloc[:, 1:13]
    retention_matrix.index = pd.to_datetime(retention_matrix.index).strftime("%Y-%m")

    z_vals   = retention_matrix.values
    x_labels = [f"M+{i}" for i in retention_matrix.columns]
    y_labels = retention_matrix.index.tolist()
    cell_tc  = "#0f1117" if not IS_DARK else "#dde3f0"

    # ── Quick stats row ───────────────────
    avg_m1 = retention_matrix.iloc[:,0].mean()
    avg_m3 = retention_matrix.iloc[:,2].mean() if retention_matrix.shape[1] > 2 else 0
    avg_m6 = retention_matrix.iloc[:,5].mean() if retention_matrix.shape[1] > 5 else 0
    best_cohort = retention_matrix.iloc[:,0].idxmax()

    sc1, sc2, sc3, sc4 = st.columns(4)
    for col, lbl, val, color in [
        (sc1, "Avg M+1 Retention", f"{avg_m1:.1%}", T["accent"]),
        (sc2, "Avg M+3 Retention", f"{avg_m3:.1%}", "#818cf8"),
        (sc3, "Avg M+6 Retention", f"{avg_m6:.1%}", "#fb923c"),
        (sc4, "Best Cohort",       best_cohort,      "#f472b6"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:{T['bg_card']};border:1px solid {T['border']};border-radius:10px;
                padding:14px 16px;box-shadow:{T['card_shadow']};margin-bottom:14px;
                animation:fadeUp 0.4s ease">
              <div style="font-size:9px;text-transform:uppercase;letter-spacing:1px;
                  color:{T['text_faint']};font-weight:600;margin-bottom:5px">{lbl}</div>
              <div style="font-family:'JetBrains Mono',monospace;font-size:18px;
                  font-weight:700;color:{color}">{val}</div>
            </div>""", unsafe_allow_html=True)

    # ── Heatmap ───────────────────────────
    fig_heat = go.Figure(go.Heatmap(
        z=z_vals, x=x_labels, y=y_labels,
        colorscale=HEATMAP_SCALE, zmin=0, zmax=0.02,
        text=[[f"{v:.1%}" if not pd.isna(v) else "" for v in row] for row in z_vals],
        texttemplate="%{text}",
        textfont=dict(size=9, family="JetBrains Mono", color=cell_tc),
        hovertemplate="Cohort: <b>%{y}</b><br>%{x}<br>Retention: <b>%{z:.2%}</b><extra></extra>",
        colorbar=dict(
            thickness=10, len=0.9,
            tickfont=dict(size=9, color=T["axis_text"], family="JetBrains Mono"),
            tickformat=".1%", outlinewidth=0, bgcolor="rgba(0,0,0,0)",
        ),
    ))
    chart_card("Cohort Retention Heatmap", fig_heat, height=620,
               margin=dict(l=16, r=60, t=10, b=16),
               extra_layout=dict(
                   xaxis_title="Months Since First Purchase",
                   yaxis_title="Cohort Month",
                   xaxis=dict(side="top", tickfont=dict(size=10, family="JetBrains Mono",
                                                         color=T["axis_text"])),
                   yaxis=dict(tickfont=dict(size=10, family="JetBrains Mono",
                                            color=T["axis_text"]), autorange="reversed"),
               ))

    # ── Retention curves ──────────────────
    fig_lines = go.Figure()
    for i, (cohort, row) in enumerate(retention_matrix.iloc[:6].iterrows()):
        vals = row.dropna()
        c    = LINE_COLORS[i % len(LINE_COLORS)]
        fig_lines.add_trace(go.Scatter(
            x=vals.index.astype(str), y=vals.values, name=cohort,
            mode="lines+markers",
            line=dict(color=c, width=2.2, shape="spline"),
            marker=dict(size=5, color=c, line=dict(width=1.5, color=T["plot_bg"])),
            hovertemplate=f"<b>{cohort}</b> — %{{x}}: %{{y:.2%}}<extra></extra>",
        ))
    chart_card("Retention Curves — First 6 Cohorts", fig_lines, height=270,
               extra_layout=dict(
                   yaxis_tickformat=".1%",
                   xaxis_title="Month Since First Purchase",
                   yaxis_title="Retention Rate",
                   legend=dict(orientation="h", yanchor="bottom", y=1.02,
                               xanchor="left", x=0, font=dict(size=10.5),
                               bgcolor="rgba(0,0,0,0)"),
               ))