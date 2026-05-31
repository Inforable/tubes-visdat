import base64

_SVG_CACHE: dict = {}

def svg(name: str, size: int = 16, color: str = "#3d6ef5") -> str:
    path = f"assets/{name}_24dp_000000_FILL0_wght400_GRAD0_opsz24.svg"
    if path not in _SVG_CACHE:
        try:
            with open(path, "r") as f:
                _SVG_CACHE[path] = f.read()
        except FileNotFoundError:
            return ""
    content = _SVG_CACHE[path].replace('fill="#000000"', f'fill="{color}"')
    b64 = base64.b64encode(content.encode()).decode()
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{size}" height="{size}" style="vertical-align:middle;display:inline-block;margin-right:5px;"/>'

LIGHT_CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&display=swap');

    /* 1. RESET GLOBAL & HIDE DEFAULT ELEMENTS */
    [data-testid="stHeader"], footer { display: none !important; visibility: hidden !important; height: 0 !important; }
    * { font-family: 'Geist', sans-serif !important; }
    
    .stApp {
        background-color: #edf1f7 !important;
        color: #0c1425 !important;
    }

    /* 2. SPACING & GHOST MARGIN FIX */
    .block-container {
        padding: 1rem !important;
        max-width: 100% !important;
    }
    
    [data-testid="stVerticalBlock"] {
        gap: 0.75rem !important;
    }
    
    .element-container .stMarkdown p {
        margin-bottom: 0 !important;
    }
    .stMarkdown div {
        margin-bottom: 0 !important;
    }

    /* 3. PEMBUNUHAN BORDER ABU-ABU SECARA TOTAL (EXTREME OVERRIDE) */
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background: #ffffff !important;
        background-color: #ffffff !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 0px solid transparent !important; /* Force kill border */
        border-top: none !important;
        border-right: none !important;
        border-bottom: none !important;
        border-left: none !important;
        border-radius: 12px !important;
        box-shadow: 0px 4px 24px rgba(0, 0, 0, 0.04) !important; /* Shadow halus sebagai pengganti border */
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 1.25rem !important;
        background-color: transparent !important;
    }

    /* 4. KPI CARDS UI - TANPA BORDER */
    .metric-card {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border: 0px solid transparent !important;
        border-radius: 12px !important;
        padding: 20px 24px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        box-shadow: 0px 4px 24px rgba(0, 0, 0, 0.04) !important;
    }
    .metric-label { font-size: 0.75rem !important; font-weight: 700 !important; color: #8290a8 !important; margin-bottom: 8px !important; text-transform: uppercase !important; display: flex !important; align-items: center !important; }
    .metric-value { font-size: 2.2rem !important; font-weight: 800 !important; color: #0c1425 !important; line-height: 1 !important; }

    /* 5. TYPOGRAPHY & HEADER */
    .branding-banner { padding: 0 10px 10px 10px !important; margin: 0 !important; }
    .branding-title { font-size: 2rem !important; font-weight: 800 !important; color: #0c1425 !important; margin: 0 0 4px 0 !important; line-height: 1.1 !important; }
    .branding-subtitle { font-size: 0.9rem !important; font-weight: 400 !important; color: #8290a8 !important; margin: 0 !important; }
    .year-badge { font-size: 0.875rem !important; font-weight: 600 !important; color: #3d6ef5 !important; background: rgba(61,110,245,0.08) !important; padding: 6px 18px !important; border-radius: 8px !important; border: none !important; }
    .filter-col-label { font-size: 0.7rem !important; font-weight: 700 !important; letter-spacing: 0.8px !important; text-transform: uppercase !important; color: #8290a8 !important; margin: 0 0 8px 0 !important; }
    .chart-title { font-size: 1.1rem !important; font-weight: 700 !important; color: #0c1425 !important; margin: 0 0 10px 0 !important; display: flex !important; align-items: center !important; }

    .header-shell {
        background: #f8fafc !important;
        border-radius: 12px !important;
        box-shadow: inset 0 0 0 1px #e4eaf3 !important;
        padding: 1rem 1.05rem 0.95rem 1.05rem !important;
        margin: 0 !important;
    }

    .header-shell .header-title-row {
        display: flex !important;
        justify-content: space-between !important;
        align-items: flex-start !important;
        gap: 1rem !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .header-shell .header-title-block {
        min-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .header-shell .branding-title {
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        color: #0c1425 !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.1 !important;
    }

    .header-shell .branding-subtitle {
        font-size: 0.9rem !important;
        font-weight: 400 !important;
        color: #64748b !important;
        margin: 0.2rem 0 0 0 !important;
        padding: 0 !important;
        line-height: 1.35 !important;
    }

    .header-shell .header-year-badge {
        width: fit-content !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        margin-top: 0.15rem !important;
        white-space: nowrap !important;
        background: rgba(61,110,245,0.08) !important;
    }

    .header-shell .header-divider {
        height: 1px !important;
        width: 100% !important;
        background: linear-gradient(90deg, rgba(228,234,243,0), #e4eaf3, rgba(228,234,243,0)) !important;
        margin: 0.45rem 0 0.35rem 0 !important;
    }

    .header-shell [data-testid="stHorizontalBlock"] {
        gap: 0.65rem !important;
        align-items: end !important;
    }

    .header-shell [data-testid="stSelectbox"],
    .header-shell [data-testid="stSelectbox"] > div,
    .header-shell [data-baseweb="select"] {
        width: 100% !important;
        margin-top: 0 !important;
    }

    .header-shell [data-testid="stSelectbox"] label,
    .header-shell .stSelectbox label {
        display: none !important;
    }

    .header-shell [data-testid="stSelectbox"] > div:first-child,
    .header-shell [data-baseweb="select"] > div:first-child {
        min-height: 40px !important;
        align-items: center !important;
        background-color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #dbe3ee !important;
        color: #2563eb !important;
    }

    .header-shell [data-testid="stSelectbox"] [data-baseweb="select"] * {
        color: #2563eb !important;
    }

    .header-shell [data-testid="stSelectbox"] [aria-selected="true"],
    .header-shell [data-testid="stSelectbox"] [role="option"] {
        color: #2563eb !important;
    }

    .header-shell [data-testid="stSelectbox"] svg {
        color: #2563eb !important;
        fill: #2563eb !important;
    }

    .header-shell .filter-col-label {
        margin: 0 0 0.35rem 0 !important;
    }

    .top-hero-row {
        display: flex !important;
        align-items: flex-start !important;
        justify-content: space-between !important;
        gap: 1.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    .top-hero-left {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    .top-hero-right {
        flex: 0 0 28% !important;
        min-width: 280px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 0.55rem !important;
        align-items: stretch !important;
        justify-content: flex-start !important;
    }

    .compact-filter-panel {
        background: #ffffff !important;
        border: 1px solid #dce2ed !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 16px rgba(12, 20, 37, 0.04) !important;
        padding: 0.9rem 1rem !important;
    }

    .compact-filter-grid {
        display: grid !important;
        grid-template-columns: 1fr !important;
        gap: 0.6rem !important;
    }

    .compact-filter-panel .filter-col-label {
        margin-bottom: 6px !important;
        font-size: 0.68rem !important;
    }

    /* 6. PLOTLY FULL WIDTH HACKS & IFRAME BORDER KILLER */
    iframe {
        border: none !important; /* Membunuh border bawaan iframe browser */
    }
    iframe[title="streamlit_plotly_events.plotly_events"], .stPlotlyChart iframe {
        width: 100% !important;
        border: none !important;
    }
    .stPlotlyChart { margin-bottom: -1rem !important; }
    
    /* 7. UI CONTROLS - TANPA BORDER ABU */
    [data-baseweb="select"] > div:first-child { background-color: #f5f7fb !important; border: none !important; border-radius: 8px !important; box-shadow: 0 1px 4px rgba(0,0,0,0.02) !important; }
    .stApp div.stButton > button { background-color: #ffffff !important; color: #374258 !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 0.875rem !important; padding: 3px 10px !important; height: 32px !important; box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important; }
    .stApp div.stButton > button[data-testid="baseButton-secondary"],
    .stApp div.stButton > button[data-testid="baseButton-primary"] {
        background-color: #f5f7fb !important;
        border: 1px solid #dce2ed !important;
        border-radius: 8px !important;
        color: #334155 !important;
        min-height: 36px !important;
        padding: 0.4rem 0.8rem !important;
    }

    .stApp div.stButton > button[data-testid="baseButton-primary"] {
        background-color: #3d6ef5 !important;
        color: #ffffff !important;
        border-color: #3d6ef5 !important;
    }
    div[data-testid="stSegmentedControl"],
    div[data-testid="stSegmentedControl"] > div,
    div[data-testid="stSegmentedControl"] div[role="radiogroup"],
    div[data-baseweb="radio"] [role="radiogroup"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        align-items: stretch !important;
        width: 100% !important;
        gap: 0 !important;
        overflow: hidden !important;
    }

    div[data-testid="stSegmentedControl"] button,
    div[data-baseweb="radio"] [role="radiogroup"] label {
        flex: 1 1 0 !important;
        min-width: 0 !important;
        white-space: nowrap !important;
        margin: 0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
        border: 1px solid #d5ddea !important;
        background: #f7f9fc !important;
        color: #334155 !important;
    }

    div[data-testid="stSegmentedControl"] button:not(:last-child) {
        border-right: 0 !important;
    }

    div[data-testid="stSegmentedControl"] button:first-child,
    div[data-baseweb="radio"] [role="radiogroup"] label:first-child {
        border-radius: 8px 0 0 8px !important;
    }

    div[data-testid="stSegmentedControl"] button:last-child,
    div[data-baseweb="radio"] [role="radiogroup"] label:last-child {
        border-radius: 0 8px 8px 0 !important;
    }

    div[data-testid="stSegmentedControl"] button[aria-checked="true"],
    div[data-baseweb="radio"] [role="radiogroup"] input:checked + div,
    div[data-baseweb="radio"] [role="radiogroup"] label:has(input:checked) {
        background-color: #3d6ef5 !important;
        color: #ffffff !important;
        border-color: #3d6ef5 !important;
        position: relative !important;
        z-index: 1 !important;
    }

    div[data-testid="stSegmentedControl"] button:focus-visible,
    div[data-baseweb="radio"] [role="radiogroup"] label:focus-within {
        outline: 2px solid rgba(61,110,245,0.35) !important;
        outline-offset: 2px !important;
    }

    div[data-testid="stSegmentedControl"] button:hover,
    div[data-baseweb="radio"] [role="radiogroup"] label:hover {
        border-color: #b9c7f6 !important;
        background: #eef3ff !important;
    }

    @media (max-width: 640px) {
        div[data-testid="stSegmentedControl"],
        div[data-testid="stSegmentedControl"] > div,
        div[data-testid="stSegmentedControl"] div[role="radiogroup"],
        div[data-baseweb="radio"] [role="radiogroup"] {
            flex-direction: column !important;
        }

        div[data-testid="stSegmentedControl"] button,
        div[data-baseweb="radio"] [role="radiogroup"] label {
            width: 100% !important;
            border-right: 1px solid #d5ddea !important;
        }

        div[data-testid="stSegmentedControl"] button:first-child,
        div[data-baseweb="radio"] [role="radiogroup"] label:first-child {
            border-radius: 8px 8px 0 0 !important;
        }

        div[data-testid="stSegmentedControl"] button:last-child,
        div[data-baseweb="radio"] [role="radiogroup"] label:last-child {
            border-radius: 0 0 8px 8px !important;
            border-top: 0 !important;
        }

        div[data-testid="stSegmentedControl"] button:not(:last-child),
        div[data-baseweb="radio"] [role="radiogroup"] label:not(:last-child) {
            border-right: 1px solid #d5ddea !important;
            border-bottom: 0 !important;
        }
    }
    div[data-testid="stSlider"] div[role="slider"] { background-color: #3d6ef5 !important; border: 2px solid #ffffff !important; }
    div[data-testid="stSlider"] div[data-testid="stSliderTrack"] > div { background-color: #3d6ef5 !important; }
    
    .year-display { font-size: 0.9rem !important; font-weight: 700 !important; color: #0fa876 !important; background: rgba(15,168,118,0.09) !important; border: none !important; padding: 5px 10px !important; border-radius: 8px !important; text-align: center !important; }
    .takeaways-box { background-color: #ffffff !important; border: none !important; border-radius: 12px !important; padding: 24px 28px !important; margin-top: 10px !important; box-shadow: 0px 4px 24px rgba(0, 0, 0, 0.04) !important; }
    .takeaways-title { font-size: 1rem !important; font-weight: 700 !important; color: #0c1425 !important; margin-bottom: 12px !important; display: flex !important; align-items: center !important; gap: 8px !important; }
    .takeaway-item { padding: 10px 0 !important; border-bottom: 1px solid #edf1f7 !important; font-size: 0.875rem !important; color: #374258 !important; }
    .takeaway-item:last-child { border-bottom: none !important; padding-bottom: 0 !important; }

    .insight-card {
        background: #ffffff !important;
        border: 0px solid transparent !important;
        border-radius: 12px !important;
        box-shadow: 0px 4px 24px rgba(0, 0, 0, 0.04) !important;
        padding: 18px 18px 16px 18px !important;
        min-height: 190px !important;
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        gap: 10px !important;
    }

    .insight-head {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        font-size: 0.78rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.6px !important;
        text-transform: uppercase !important;
        color: #8290a8 !important;
    }

    .insight-icon {
        font-size: 1.05rem !important;
        line-height: 1 !important;
        display: inline-flex !important;
        align-items: center !important;
    }

    .insight-value {
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        color: #0c1425 !important;
        line-height: 1.1 !important;
    }

    .insight-body {
        font-size: 0.88rem !important;
        color: #475569 !important;
        line-height: 1.5 !important;
    }
    </style>
"""

def render_header(year_badge: str) -> str:
    return f"""
        <div class="branding-banner">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
                <div>
                    <h1 class="branding-title">Total Kejadian Banjir di Indonesia</h1>
                    <p class="branding-subtitle">Visualisasi Data Interaktif Kejadian Banjir Regional (2000 - 2025)</p>
                </div>
                <div class="year-badge">{year_badge}</div>
            </div>
        </div>
    """

def render_kpi_card(label: str, value: str, icon_name: str) -> str:
    return f"""
        <div class="metric-card">
            <div class="metric-label">{svg(icon_name, 13, '#8290a8')}&thinsp;{label}</div>
            <div class="metric-value">{value}</div>
        </div>
    """

def render_chart_title(icon_name: str, label: str) -> str:
    return f'<p class="chart-title">{svg(icon_name, 20, "#3d6ef5")}&thinsp;{label}</p>'

def render_year_display(year: int) -> str:
    return f'<div class="year-display">{year}</div>'


def render_insight_card(icon_name: str, label: str, value: str, body: str) -> str:
    return f"""
        <div class="insight-card">
            <div class="insight-head"><span class="insight-icon">{svg(icon_name, 16, '#3d6ef5')}</span><span>{label}</span></div>
            <div class="insight-value">{value}</div>
            <div class="insight-body">{body}</div>
        </div>
    """

def render_takeaways() -> str:
    return f"""
        <div class="takeaways-box">
            <div class="takeaways-title">
                {svg('lightbulb', 17, '#3d6ef5')}&thinsp;Informasi Kunci &amp; Wawasan Data
            </div>
            <div class="takeaway-item">
                <strong>Total Beban Risiko</strong> Dampak banjir di Indonesia sangat masif dengan ratusan ribu kejadian terdistribusi di berbagai pulau. Skala yang tinggi dan berulang menandakan kerentanan lingkungan yang terstruktur, bukan anomali cuaca sporadis.
            </div>
            <div class="takeaway-item">
                <strong>Konsentrasi Geografis</strong> Pulau Jawa memikul risiko tertinggi, dipimpin <strong>Jawa Barat</strong>, <strong>Jawa Timur</strong>, dan <strong>Jawa Tengah</strong>. Hal ini berkorelasi kuat dengan kepadatan populasi, urbanisasi, alih fungsi lahan, dan menurunnya daya dukung hidrologis DAS.
            </div>
            <div class="takeaway-item">
                <strong>Tren Ekskalasi Waktu</strong> Kasus meningkat eksponensial sejak 2016, dengan puncak pada 2020&ndash;2025. Ini mencerminkan intensifikasi curah hujan ekstrem akibat perubahan iklim dan perluasan cakupan pelaporan. <em>(Data 2026 dikecualikan untuk objektivitas analisis.)</em>
            </div>
            <div class="takeaway-item">
                <strong>Rekomendasi Kebijakan Spasial</strong> Kerentanan yang bervariasi antar wilayah mengindikasikan perlunya beralih dari kebijakan seragam ke zonasi berbasis karakteristik kepulauan, dengan prioritas pada wilayah luar Jawa yang trennya terus naik.
            </div>
        </div>
    """