import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Olist Analytics",
    layout="wide",
    page_icon="⬡",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. THEME STATE
# ==========================================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

TOKENS = {
    "dark": {
        "bg_app":        "#0b0d12",
        "bg_sidebar":    "#0e1018",
        "bg_card":       "#13161f",
        "bg_card_hover": "#181c28",
        "text_primary":  "#f0f4ff",
        "text_secondary":"#c9d1e0",
        "text_muted":    "#6b7a99",
        "text_faint":    "#4a556e",
        "border":        "rgba(255,255,255,0.07)",
        "border_hover":  "rgba(255,255,255,0.14)",
        "border_tab":    "rgba(255,255,255,0.08)",
        "scrollbar":     "rgba(255,255,255,0.10)",
        "plot_bg":       "#13161f",
        "paper_bg":      "#13161f",
        "grid":          "rgba(255,255,255,0.06)",
        "axis_text":     "#8892aa",
        "accent":        "#5eead4",
        "accent_bg":     "rgba(94,234,212,0.10)",
        "accent_border": "rgba(94,234,212,0.25)",
    },
    "light": {
        "bg_app":        "#f4f5f9",
        "bg_sidebar":    "#ffffff",
        "bg_card":       "#ffffff",
        "bg_card_hover": "#f0f2f8",
        "text_primary":  "#0f1117",
        "text_secondary":"#2d3348",
        "text_muted":    "#6b7a99",
        "text_faint":    "#9aa3b8",
        "border":        "rgba(0,0,0,0.08)",
        "border_hover":  "rgba(0,0,0,0.15)",
        "border_tab":    "rgba(0,0,0,0.09)",
        "scrollbar":     "rgba(0,0,0,0.12)",
        "plot_bg":       "#ffffff",
        "paper_bg":      "#ffffff",
        "grid":          "rgba(0,0,0,0.05)",
        "axis_text":     "#9aa3b8",
        "accent":        "#0d9488",
        "accent_bg":     "rgba(13,148,136,0.08)",
        "accent_border": "rgba(13,148,136,0.22)",
    },
}

T  = TOKENS[st.session_state.theme]
IS_DARK = st.session_state.theme == "dark"


# ==========================================
# 3. CSS  — no more manual div wrappers;
#    use data-card attribute injected via
#    st.container() key trick instead.
#    Chart cards are styled via a wrapper
#    class on the stVerticalBlock element.
# ==========================================
def build_css(t):
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'DM Sans', sans-serif !important;
    background-color: {t['bg_app']} !important;
    color: {t['text_secondary']} !important;
}}
.block-container {{
    padding: 1.8rem 2rem 2rem !important;
    max-width: 1400px !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {t['bg_sidebar']} !important;
    border-right: 1px solid {t['border']} !important;
}}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label {{
    color: {t['text_muted']} !important;
    font-size: 12px !important;
}}
[data-testid="stSidebarContent"] h2,
[data-testid="stSidebarContent"] h3 {{
    color: {t['text_primary']} !important;
}}
.stMultiSelect [data-baseweb="tag"] {{
    background-color: {t['accent_bg']} !important;
    color: {t['accent']} !important;
    border: 1px solid {t['accent_border']} !important;
}}

/* ── Tabs ── */
[data-testid="stTabs"] {{
    background: transparent !important;
    margin-bottom: 16px;
}}
[data-testid="stTabList"] {{
    background: transparent !important;
    border-bottom: 1px solid {t['border_tab']} !important;
    gap: 4px;
}}
[data-testid="stTab"] {{
    background: transparent !important;
    color: {t['text_muted']} !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
    border: none !important;
    transition: color 0.15s, background-color 0.15s;
}}
[data-testid="stTab"]:hover {{
    color: {t['text_primary']} !important;
    background-color: {t['border']} !important;
    border-radius: 6px 6px 0 0 !important;
}}
[data-testid="stTab"][aria-selected="true"] {{
    color: {t['accent']} !important;
    background-color: {t['accent_bg']} !important;
    border-bottom: 2px solid {t['accent']} !important;
    border-radius: 6px 6px 0 0 !important;
}}
[data-testid="stTabHighlight"] {{
    background-color: transparent !important;
}}

/* ── KPI cards: target the column containers ── */
.kpi-wrap {{
    background: {t['bg_card']};
    border: 1px solid {t['border']};
    border-radius: 10px;
    padding: 16px 18px 14px;
    position: relative;
    overflow: hidden;
    margin-bottom: 8px;
    transition: border-color 0.2s, transform 0.15s;
}}
.kpi-wrap:hover {{
    border-color: {t['border_hover']};
    transform: translateY(-2px);
}}
.kpi-wrap::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}}
.k-teal::before   {{ background: #5eead4; }}
.k-indigo::before {{ background: #818cf8; }}
.k-orange::before {{ background: #fb923c; }}
.k-pink::before   {{ background: #f472b6; }}

/* ── Metric overrides ── */
div[data-testid="stMetricValue"] {{
    font-family: 'Space Mono', monospace !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    color: {t['text_primary']} !important;
    letter-spacing: -0.8px;
}}
div[data-testid="stMetricLabel"] {{
    font-size: 10px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    color: {t['text_muted']} !important;
    margin-bottom: 4px;
}}
div[data-testid="stMetricDelta"] {{
    font-size: 11px !important;
    font-family: 'Space Mono', monospace !important;
}}

/* ── Chart card — SAFE approach:
   wrap label + chart in a styled div injected BEFORE
   the Streamlit element, floated via negative margin trick ── */
.chart-section {{
    background: {t['bg_card']};
    border: 1px solid {t['border']};
    border-radius: 10px;
    padding: 16px 20px 10px;
    margin-bottom: 12px;
}}

/* ── Section label ── */
.sec-head {{
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: {t['text_muted']};
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
}}
.sec-head::before {{
    content: '';
    display: inline-block;
    width: 3px; height: 12px;
    border-radius: 2px;
    background: {t['accent']};
    flex-shrink: 0;
}}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{
    border: 1px solid {t['border']} !important;
    border-radius: 8px !important;
    overflow: hidden;
}}

/* ── Selectbox ── */
[data-baseweb="select"] div {{
    background-color: {t['bg_card']} !important;
    border-color: {t['border']} !important;
    color: {t['text_secondary']} !important;
    font-size: 13px !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {t['scrollbar']}; border-radius: 2px; }}

/* ── Title ── */
.main-title {{
    font-size: 26px; font-weight: 600;
    color: {t['text_primary']}; letter-spacing: -0.5px; margin-bottom: 2px;
}}
.main-subtitle {{
    font-size: 11px; color: {t['text_faint']};
    font-family: 'Space Mono', monospace; letter-spacing: 0.3px; margin-bottom: 20px;
}}
.live-badge {{
    display: inline-block;
    background: {t['accent_bg']}; color: {t['accent']};
    border: 1px solid {t['accent_border']}; border-radius: 20px;
    padding: 3px 12px; font-size: 10px; font-weight: 500;
    letter-spacing: 0.5px; margin-left: 10px; vertical-align: middle;
}}

/* ── Toggle button ── */
div[data-testid="stButton"] > button {{
    background: {t['bg_card']} !important;
    border: 1px solid {t['border']} !important;
    color: {t['text_secondary']} !important;
    font-size: 12px !important; font-family: 'DM Sans', sans-serif !important;
    border-radius: 8px !important; padding: 6px 14px !important;
    transition: all 0.15s !important; width: 100%;
}}
div[data-testid="stButton"] > button:hover {{
    border-color: {t['accent']} !important;
    color: {t['accent']} !important;
    background: {t['accent_bg']} !important;
}}

/* ── Cohort info banner ── */
.cohort-info {{
    background: {t['accent_bg']}; border: 1px solid {t['accent_border']};
    border-radius: 8px; padding: 10px 16px;
    font-size: 12px; color: {t['accent']}; margin-bottom: 14px;
}}
</style>
"""

st.markdown(build_css(T), unsafe_allow_html=True)


# ==========================================
# 4. PLOTLY THEME HELPER
# ==========================================
def apply_theme(fig, height=300, margin=None):
    m = margin or dict(l=16, r=16, t=16, b=16)
    fig.update_layout(
        paper_bgcolor=T["paper_bg"],
        plot_bgcolor=T["plot_bg"],
        font=dict(color=T["axis_text"], family="DM Sans", size=11),
        height=height, margin=m,
        xaxis=dict(gridcolor=T["grid"], zeroline=False, showline=False,
                   tickfont=dict(size=10, color=T["axis_text"])),
        yaxis=dict(gridcolor=T["grid"], zeroline=False, showline=False,
                   tickfont=dict(size=10, color=T["axis_text"])),
    )
    return fig

# ── Color tokens for charts ──────────────
BAR_SCALE = ([[0,"#dbeafe"],[0.5,"#818cf8"],[1,"#0d9488"]] if not IS_DARK
             else [[0,"#1e2746"],[0.5,"#818cf8"],[1,"#5eead4"]])

# Heatmap: dark uses visible mid-tones, NOT near-black start
HEATMAP_SCALE = (
    [[0.00,"#f0fdf9"],[0.30,"#99f6e4"],[0.60,"#2dd4bf"],[0.85,"#0d9488"],[1.00,"#115e59"]]
    if not IS_DARK else
    [[0.00,"#1a2535"],[0.20,"#173d3a"],[0.45,"#1a6b5e"],[0.70,"#27a899"],[1.00,"#5eead4"]]
)

AREA_COLOR   = "#0d9488" if not IS_DARK else "#5eead4"
AREA_FILL    = "rgba(13,148,136,0.09)"  if not IS_DARK else "rgba(94,234,212,0.08)"
ORANGE_COLOR = "#ea580c" if not IS_DARK else "#fb923c"
ORANGE_FILL  = "rgba(234,88,12,0.08)"  if not IS_DARK else "rgba(251,146,60,0.08)"

SEG_COLORS = {
    "Champions":           "#0d9488" if not IS_DARK else "#5eead4",
    "Loyal Customers":     "#6366f1" if not IS_DARK else "#818cf8",
    "Potential Loyalists": "#65a30d" if not IS_DARK else "#a3e635",
    "At Risk":             "#ea580c" if not IS_DARK else "#fb923c",
    "Lost":                "#dc2626" if not IS_DARK else "#f87171",
    "New Customers":       "#ca8a04" if not IS_DARK else "#facc15",
    "Hibernating":         "#6b7a99",
}
LINE_COLORS = list(SEG_COLORS.values())[:6]

# Helper: render a titled chart section cleanly
def chart_card(title: str, fig, height=300, margin=None, extra_layout=None):
    """Render section heading + plotly chart inside a styled card div."""
    st.markdown(
        f'<div class="chart-section">'
        f'<div class="sec-head">{title}</div>',
        unsafe_allow_html=True
    )
    apply_theme(fig, height=height, margin=margin)
    if extra_layout:
        fig.update_layout(**extra_layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# 5. DATA
# ==========================================
DB_PATH = "/Users/ciaranguyen/Documents/ecom_project/dev.duckdb"

@st.cache_data
def load_data():
    con = duckdb.connect(DB_PATH, read_only=True)
    marts  = con.execute("SELECT * FROM main.marts").df()
    rfm    = con.execute("SELECT * FROM main.analytics_rfm").df()
    cohort = con.execute("SELECT * FROM main.analytics_cohort").df()
    con.close()
    marts["purchase_at"] = pd.to_datetime(marts["purchase_at"])
    return marts, rfm, cohort

df_marts, df_rfm, df_cohort = load_data()


# ==========================================
# 6. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown(f"""
    <div style='padding:14px 0 18px'>
      <div style='font-size:22px;font-weight:700;color:{T["text_primary"]};letter-spacing:-0.5px'>⬡ Olist</div>
      <div style='font-size:10px;color:{T["text_faint"]};font-family:Space Mono,monospace;margin-top:2px'>Analytics Suite v2.0</div>
    </div>""", unsafe_allow_html=True)

    toggle_label = "☀️  Light mode" if IS_DARK else "🌙  Dark mode"
    if st.button(toggle_label, key="theme_toggle"):
        st.session_state.theme = "light" if IS_DARK else "dark"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:10px;text-transform:uppercase;letter-spacing:0.9px;color:{T["text_faint"]};font-weight:600;margin-bottom:8px">PRODUCT CATEGORY</div>', unsafe_allow_html=True)

    available_cats = sorted(df_marts["product_category"].dropna().unique())
    selected_cats  = st.multiselect("cat", available_cats, default=available_cats[:5],
                                    label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background:{T["bg_card"]};border:1px solid {T["border"]};border-radius:8px;padding:12px 14px'>
      <div style='font-size:9px;text-transform:uppercase;letter-spacing:0.8px;color:{T["text_faint"]};margin-bottom:8px'>PIPELINE</div>
      <div style='font-size:11px;color:{T["text_muted"]};line-height:2.1'>
        📄 Raw CSV<br>↓<br>
        <span style='color:{T["accent"]}'>⚙ dbt Core</span><br>↓<br>
        🦆 DuckDB<br>↓<br>
        <span style='color:#818cf8'>⚡ Streamlit</span>
      </div>
    </div>""", unsafe_allow_html=True)

df_f = df_marts[df_marts["product_category"].isin(selected_cats)]


# ==========================================
# 7. HEADER
# ==========================================
st.markdown(f"""
<div class="main-title">Olist E-commerce Analytics<span class="live-badge">● LIVE</span></div>
<div class="main-subtitle">RAW CSV → DBT CORE → DUCKDB → STREAMLIT</div>
""", unsafe_allow_html=True)


# ==========================================
# 8. TABS
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "  📈  Executive Overview  ",
    "  👥  RFM Segments  ",
    "  🔄  Cohort Retention  ",
])


# ──────────────────────────────────────────
# TAB 1
# ──────────────────────────────────────────
with tab1:

    # KPI row — use kpi-wrap div directly (no Plotly inside, safe to wrap)
    k1, k2, k3, k4 = st.columns(4)
    kpi_data = [
        (k1, "k-teal",   "Total Gross Revenue",  f"${df_f['total_amount_paid'].sum():,.0f}"),
        (k2, "k-indigo", "Order Volume",          f"{df_f['order_id'].nunique():,}"),
        (k3, "k-orange", "Avg Freight Cost",      f"${df_f['total_shipping_cost'].mean():,.2f}"),
        (k4, "k-pink",   "Fulfillment Velocity",  f"{df_f['actual_delivery_days'].mean():.1f} days"),
    ]
    for col, cls, label, val in kpi_data:
        with col:
            st.markdown(f'<div class="kpi-wrap {cls}">', unsafe_allow_html=True)
            st.metric(label, val)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Revenue trend + categories
    col_l, col_r = st.columns([3, 2])
    with col_l:
        df_trend = df_f.set_index("purchase_at").resample("ME")["total_amount_paid"].sum().reset_index()
        fig_t = go.Figure(go.Scatter(
            x=df_trend["purchase_at"], y=df_trend["total_amount_paid"],
            mode="lines+markers",
            line=dict(color=AREA_COLOR, width=2.5),
            marker=dict(size=5, color=AREA_COLOR, line=dict(width=1.5, color=T["plot_bg"])),
            fill="tozeroy", fillcolor=AREA_FILL,
            hovertemplate="<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>",
        ))
        chart_card("Monthly Revenue Velocity", fig_t, height=265,
                   extra_layout=dict(yaxis_tickprefix="$", yaxis_tickformat=",.0f",
                                     xaxis_title=None, yaxis_title=None))

    with col_r:
        df_cat = (df_f.groupby("product_category")["total_amount_paid"].sum()
                  .reset_index().sort_values("total_amount_paid", ascending=True).tail(10))
        fig_c = px.bar(df_cat, x="total_amount_paid", y="product_category", orientation="h",
                       color="total_amount_paid", color_continuous_scale=BAR_SCALE)
        fig_c.update_traces(hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
                            marker_line_width=0)
        chart_card("Top 10 Categories", fig_c, height=265,
                   extra_layout=dict(coloraxis_showscale=False, yaxis_title=None,
                                     xaxis_title=None, xaxis_tickprefix="$"))

    # Logistics + status
    col_log, col_st = st.columns(2)
    with col_log:
        df_log = df_f.set_index("purchase_at").resample("ME")["actual_delivery_days"].mean().reset_index()
        fig_l = go.Figure(go.Scatter(
            x=df_log["purchase_at"], y=df_log["actual_delivery_days"],
            mode="lines+markers",
            line=dict(color=ORANGE_COLOR, width=2.5),
            marker=dict(size=5, color=ORANGE_COLOR, line=dict(width=1.5, color=T["plot_bg"])),
            fill="tozeroy", fillcolor=ORANGE_FILL,
            hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.1f} days<extra></extra>",
        ))
        chart_card("Avg Delivery Days", fig_l, height=245,
                   extra_layout=dict(yaxis_title=None, xaxis_title=None))

    with col_st:
        df_status = df_f["order_status"].value_counts().reset_index()
        df_status.columns = ["order_status", "count"]
        PALETTE = ["#5eead4","#818cf8","#fb923c","#f472b6","#a3e635","#facc15","#f87171"]
        fig_s = px.pie(df_status, values="count", names="order_status",
                       hole=0.62, color_discrete_sequence=PALETTE)
        fig_s.update_traces(
            textposition="outside", textinfo="percent+label", textfont_size=10,
            marker=dict(line=dict(color=T["bg_card"], width=2)),
            hovertemplate="<b>%{label}</b><br>%{value:,} orders (%{percent})<extra></extra>",
        )
        chart_card("Order Status", fig_s, height=245,
                   margin=dict(l=30, r=30, t=20, b=20),
                   extra_layout=dict(showlegend=False,
                                     font=dict(color=T["text_secondary"])))

    # Geographic
    con = duckdb.connect(DB_PATH, read_only=True)
    df_geo = con.execute("""
        SELECT c.customer_state AS State, COUNT(DISTINCT m.order_id) AS Orders
        FROM main.marts m
        JOIN read_csv_auto('data/raw/olist_customers_dataset.csv') c
          ON m.customer_id = c.customer_id
        GROUP BY c.customer_state ORDER BY Orders DESC LIMIT 10
    """).df()
    con.close()
    fig_g = px.bar(df_geo, x="State", y="Orders", text_auto=".3s",
                   color="Orders", color_continuous_scale=BAR_SCALE)
    fig_g.update_traces(textfont_size=11, textposition="outside", cliponaxis=False,
                        marker_line_width=0,
                        hovertemplate="<b>%{x}</b><br>%{y:,} orders<extra></extra>")
    chart_card("Geographic Distribution — Top 10 States", fig_g, height=285,
               extra_layout=dict(coloraxis_showscale=False, xaxis_title=None,
                                  yaxis_title="Orders"))


# ──────────────────────────────────────────
# TAB 2
# ──────────────────────────────────────────
with tab2:

    df_rfm_counts = (df_rfm["Segment"].value_counts().reset_index()
                     .rename(columns={"count": "Customer Count"})
                     .sort_values("Customer Count", ascending=True))
    bar_colors = [SEG_COLORS.get(s, "#6b7a99") for s in df_rfm_counts["Segment"]]

    fig_seg = go.Figure(go.Bar(
        x=df_rfm_counts["Customer Count"], y=df_rfm_counts["Segment"],
        orientation="h", marker_color=bar_colors, marker_line_width=0,
        text=df_rfm_counts["Customer Count"].apply(lambda x: f"{x:,}"),
        textposition="outside",
        textfont=dict(size=10, color=T["axis_text"], family="Space Mono"),
        hovertemplate="<b>%{y}</b><br>%{x:,} customers<extra></extra>",
    ))
    chart_card("Customer Segment Distribution", fig_seg, height=320,
               extra_layout=dict(xaxis_title=None, yaxis_title=None,
                                  xaxis=dict(showgrid=False, showticklabels=False)))

    df_scatter = df_rfm.copy()
    df_scatter["monetary_norm"] = (df_scatter["monetary"] / df_scatter["monetary"].max()) * 30 + 4
    fig_sc = px.scatter(
        df_scatter.sample(min(2000, len(df_scatter))),
        x="recency", y="monetary", size="monetary_norm",
        color="Segment", color_discrete_map=SEG_COLORS,
        hover_data={"customer_unique_id": True, "frequency": True,
                    "RFM_Score": True, "monetary_norm": False},
        opacity=0.75,
    )
    fig_sc.update_traces(marker_line_width=0)
    chart_card("RFM Value Map — Recency vs Monetary (bubble = Frequency)", fig_sc, height=360,
               extra_layout=dict(
                   xaxis_title="Recency (days)", yaxis_title="Monetary Value ($)",
                   legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0,
                               font=dict(size=10), bgcolor="rgba(0,0,0,0)", borderwidth=0),
               ))

    # Explorer — no Plotly, safe to use div wrap
    st.markdown(
        f'<div class="chart-section"><div class="sec-head">Segment Micro-Explorer</div>',
        unsafe_allow_html=True)
    col_sel, col_s1, col_s2, col_s3 = st.columns([2, 1, 1, 1])
    with col_sel:
        selected_seg = st.selectbox("seg", df_rfm["Segment"].unique(),
                                    label_visibility="collapsed")
    seg_df = df_rfm[df_rfm["Segment"] == selected_seg]
    with col_s1: st.metric("Customers",    f"{len(seg_df):,}")
    with col_s2: st.metric("Avg Monetary", f"${seg_df['monetary'].mean():,.0f}")
    with col_s3: st.metric("Avg Recency",  f"{seg_df['recency'].mean():.0f}d")
    st.dataframe(
        seg_df[["customer_unique_id","recency","frequency","monetary","RFM_Score"]]
        .sort_values("monetary", ascending=False).head(50).reset_index(drop=True),
        use_container_width=True, hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────
# TAB 3
# ──────────────────────────────────────────
with tab3:

    st.markdown("""
    <div class="cohort-info">
    💡 <b>Cách đọc:</b> Mỗi hàng là nhóm khách hàng mua lần đầu trong tháng đó.
    Màu sắc biểu thị tỉ lệ khách quay lại ở các tháng tiếp theo.
    </div>""", unsafe_allow_html=True)

    cohort_pivot     = df_cohort.pivot(index="cohort_month", columns="cohort_index",
                                       values="unique_customers")
    cohort_sizes     = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_sizes, axis=0).iloc[:, 1:13]
    retention_matrix.index = pd.to_datetime(retention_matrix.index).strftime("%Y-%m")

    z_vals   = retention_matrix.values
    x_labels = [f"M+{i}" for i in retention_matrix.columns]
    y_labels = retention_matrix.index.tolist()
    cell_text_color = "#0f1117" if not IS_DARK else "#e2e8f0"

    fig_heat = go.Figure(go.Heatmap(
        z=z_vals, x=x_labels, y=y_labels,
        colorscale=HEATMAP_SCALE, zmin=0, zmax=0.02,
        text=[[f"{v:.1%}" if not pd.isna(v) else "" for v in row] for row in z_vals],
        texttemplate="%{text}",
        textfont=dict(size=9, family="Space Mono", color=cell_text_color),
        hovertemplate="Cohort: <b>%{y}</b><br>%{x}<br>Retention: <b>%{z:.2%}</b><extra></extra>",
        colorbar=dict(thickness=10, len=0.9,
                      tickfont=dict(size=9, color=T["axis_text"], family="Space Mono"),
                      tickformat=".1%", outlinewidth=0, bgcolor="rgba(0,0,0,0)"),
    ))
    chart_card("Cohort Retention Heatmap", fig_heat, height=620,
               margin=dict(l=16, r=60, t=16, b=16),
               extra_layout=dict(
                   xaxis_title="Months Since First Purchase",
                   yaxis_title="Cohort Month",
                   xaxis=dict(side="top", tickfont=dict(size=10, family="Space Mono",
                                                         color=T["axis_text"])),
                   yaxis=dict(tickfont=dict(size=10, family="Space Mono",
                                            color=T["axis_text"]), autorange="reversed"),
               ))

    fig_lines = go.Figure()
    for i, (cohort, row) in enumerate(retention_matrix.iloc[:6].iterrows()):
        vals = row.dropna()
        c = LINE_COLORS[i % len(LINE_COLORS)]
        fig_lines.add_trace(go.Scatter(
            x=vals.index.astype(str), y=vals.values, name=cohort,
            mode="lines+markers",
            line=dict(color=c, width=2),
            marker=dict(size=4, color=c),
            hovertemplate=f"<b>{cohort}</b> — %{{x}}: %{{y:.2%}}<extra></extra>",
        ))
    chart_card("Retention Curves — First 6 Cohorts", fig_lines, height=265,
               extra_layout=dict(
                   yaxis_tickformat=".1%", xaxis_title="Month",
                   yaxis_title="Retention Rate",
                   legend=dict(orientation="h", yanchor="bottom", y=1.02,
                               xanchor="left", x=0, font=dict(size=10),
                               bgcolor="rgba(0,0,0,0)"),
               ))