import base64

# ==============================================================================
# SVG ICON HELPER
# ==============================================================================
_SVG_CACHE: dict = {}

def svg(name: str, size: int = 18, color: str = "#3b82f6") -> str:
    """Load an SVG from assets/, recolor it, and return an inline <img> tag."""
    path = f"assets/{name}_24dp_000000_FILL0_wght400_GRAD0_opsz24.svg"
    if path not in _SVG_CACHE:
        try:
            with open(path, "r") as f:
                _SVG_CACHE[path] = f.read()
        except FileNotFoundError:
            return ""
    content = _SVG_CACHE[path].replace('fill="#000000"', f'fill="{color}"')
    b64 = base64.b64encode(content.encode()).decode()
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{size}" height="{size}" style="vertical-align:middle; display:inline-block; margin-right:4px;"/>'

# ==============================================================================
# PREMIUM LIGHT MODE STYLING SYSTEM
# ==============================================================================
LIGHT_CSS = """
    <style>
    /* Hide default Streamlit top header and footer */
    [data-testid="stHeader"] {
        display: none !important;
    }
    footer {
        visibility: hidden !important;
        height: 0 !important;
        padding: 0 !important;
    }
    
    /* Main Layout Spacing Optimization */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: 'Inter', 'Roboto', sans-serif;
    }
    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 0.75rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Global Spacing and Gap Compression */
    [data-testid="stVerticalBlock"] > div {
        padding-top: 0.12rem !important;
        padding-bottom: 0.12rem !important;
    }
    [data-testid="stVerticalBlock"] {
        gap: 0.35rem !important;
    }
    
    /* Plain transparent inline branding header */
    .branding-banner {
        background: transparent !important;
        border: none !important;
        padding: 0px 0px 10px 0px !important;
        margin-bottom: 8px !important;
        box-shadow: none !important;
    }
    .branding-title {
        color: #0f172a !important;
        font-size: 1.50rem !important;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        padding: 0;
        text-transform: uppercase;
    }
    .branding-subtitle {
        color: #475569 !important;
        font-size: 0.85rem !important;
        margin-top: 2px !important;
        font-weight: 400;
    }
    
    /* Custom Card Style for KPIs */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #2563eb !important;
        border-radius: 10px;
        padding: 12px 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        text-align: left;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #3b82f6;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.08);
    }
    .metric-card-outline {
        background-color: #ffffff;
        border: 2px solid #2563eb !important;
        border-radius: 10px;
        padding: 12px 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        text-align: left;
    }
    .metric-card-outline:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.08);
    }
    .metric-label {
        font-size: 0.78rem !important;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.5px;
        margin-bottom: 4px !important;
    }
    .metric-value {
        font-size: 2.2rem !important;
        font-weight: 800;
        color: #1e3a8a;
        line-height: 1.1 !important;
    }
    
    /* Glassmorphic Takeaways / Bullet Box */
    .takeaways-box {
        background: #ffffff;
        border: 1px solid rgba(37, 99, 235, 0.18);
        border-radius: 12px;
        padding: 16px 24px !important;
        margin-top: 20px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
    }
    .takeaways-title {
        color: #1e3a8a;
        font-size: 1.25rem !important;
        font-weight: 700;
        margin-bottom: 12px !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .takeaway-bullet {
        margin-bottom: 8px !important;
        line-height: 1.5;
        color: #334155;
        font-size: 0.9rem !important;
    }
    .takeaway-bullet strong {
        color: #0f172a;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* Filter Section Title */
    .filter-header {
        color: #0f172a;
        font-size: 0.95rem !important;
        font-weight: 700;
        margin-bottom: 6px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Container override for st.container(border=True) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #ffffff !important;
    }
    
    /* Fix multiselect dropdown: style for light mode */
    [data-baseweb="select"] > div:first-child {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
    }
    [data-baseweb="select"] span,
    [data-baseweb="select"] input,
    [data-baseweb="select"] input::placeholder {
        color: #0f172a !important;
    }
    [data-baseweb="popover"] {
        background-color: #ffffff !important;
    }
    [data-baseweb="menu"] li {
        color: #0f172a !important;
        background-color: #ffffff !important;
    }
    [data-baseweb="menu"] li:hover {
        background-color: #f1f5f9 !important;
    }

    /* Premium Styled Multiselect Pills */
    [data-baseweb="tag"] {
        background-color: rgba(37, 99, 235, 0.08) !important;
        border: 1px solid rgba(37, 99, 235, 0.2) !important;
        border-radius: 6px !important;
        padding: 1px 4px !important;
    }
    [data-baseweb="tag"] span {
        color: #2563eb !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-baseweb="tag"] svg {
        fill: #2563eb !important;
    }
    
    /* Premium Styled Buttons */
    .stApp div.stButton > button,
    .stApp div.stButton > button:focus,
    .stApp div.stButton > button:focus-visible {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease !important;
        padding: 4px 10px !important;
        min-height: 32px !important;
        height: 32px !important;
        font-size: 0.9rem !important;
    }
    .stApp div.stButton > button:hover {
        background-color: #f8fafc !important;
        border-color: #94a3b8 !important;
        color: #0f172a !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        transform: translateY(-1px) !important;
    }
    .stApp div.stButton > button:active {
        transform: translateY(0) !important;
        background-color: #f1f5f9 !important;
    }

    /* Premium Styled Segmented Control (Pills) */
    div[data-testid="stSegmentedControl"] {
        gap: 6px !important;
    }
    div[data-testid="stSegmentedControl"] button {
        background-color: #ffffff !important;
        color: #475569 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease !important;
        padding: 4px 12px !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stSegmentedControl"] button:hover {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        border-color: #94a3b8 !important;
    }
    div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-color: #2563eb !important;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
    }
    div[data-testid="stSegmentedControl"] button[aria-checked="true"]:hover {
        background-color: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
        color: #ffffff !important;
    }
    
    /* Slider overrides */
    div[data-testid="stSlider"] label {
        color: #475569 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #2563eb !important;
        border: 2px solid #ffffff !important;
    }
    div[data-testid="stSlider"] div[data-testid="stSliderTrack"] > div {
        background: #2563eb !important;
    }
    div[data-testid="stSlider"] div[data-testid="stSliderTrack"] {
        background: #e2e8f0 !important;
    }
    div[data-testid="stSlider"] div[data-testid="stSliderTickBar"] {
        color: #64748b !important;
    }
    </style>
"""

# ==============================================================================
# HTML VIEW RENDERERS
# ==============================================================================
def render_header(year_badge: str) -> str:
    return f"""
        <div class="branding-banner">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                <div>
                    <h1 class="branding-title">Total Kejadian Banjir di Indonesia</h1>
                    <p class="branding-subtitle">Visualisasi Data Interaktif Kejadian Banjir Regional (2000 - 2025)</p>
                </div>
                <div style="font-weight: 700; color: #2563eb; font-size: 1.15rem; border: 1px solid rgba(37, 99, 235, 0.2); padding: 6px 16px; border-radius: 20px; background: rgba(37, 99, 235, 0.05); font-family: 'Inter', sans-serif;">
                    {year_badge}
                </div>
            </div>
        </div>
    """

def render_kpi_card(label: str, value: str, icon_name: str, outline: bool = False) -> str:
    card_class = "metric-card-outline" if outline else "metric-card"
    icon_color = "#2563eb" if outline else "#64748b"
    return f"""
        <div class="{card_class}">
            <div class="metric-label">{svg(icon_name, 16, icon_color)} {label}</div>
            <div class="metric-value">{value}</div>
        </div>
    """

def render_takeaways() -> str:
    return f"""
        <div class="takeaways-box">
            <div class="takeaways-title">
                <span>{svg('lightbulb', 22, '#2563eb')} Informasi Kunci &amp; Wawasan Data</span>
            </div>
            <div class="takeaway-bullet">
                • <strong>Total Beban Risiko:</strong> Dampak kebencanaan banjir di Indonesia tergolong sangat masif dengan ratusan ribu kejadian terdistribusi di berbagai pulau. Skala kejadian yang tinggi dan berulang ini menandakan adanya kerentanan lingkungan yang terstruktur dan konsisten, bukan sekadar anomali cuaca sporadis.
            </div>
            <div class="takeaway-bullet">
                • <strong>Konsentrasi Geografis:</strong> Pulau Jawa memikul konsentrasi risiko bencana banjir tertinggi di Indonesia, dipimpin berturut-turut oleh provinsi <strong>Jawa Barat</strong>, <strong>Jawa Timur</strong>, dan <strong>Jawa Tengah</strong>. Konsentrasi ekstrem ini berkorelasi kuat dengan tingginya kepadatan populasi, akselerasi urbanisasi, alih fungsi lahan masif, serta menurunnya daya dukung hidrologis daerah aliran sungai (DAS).
            </div>
            <div class="takeaway-bullet">
                • <strong>Tren Ekskalasi Waktu:</strong> Grafik tren kejadian tahunan menunjukkan grafik peningkatan kasus secara eksponensial sejak tahun 2016, dengan fluktuasi puncak berada pada rentang tahun 2020-2025. Ekskalasi tajam ini mencerminkan meningkatnya frekuensi curah hujan ekstrem akibat perubahan iklim global serta perluasan basis pelaporan data berita nasional. <em>(Catatan: Data tahun 2026 secara sengaja dikecualikan untuk memastikan objektivitas analisis tahunan yang lengkap).</em>
            </div>
            <div class="takeaway-bullet">
                • <strong>Rekomendasi Kebijakan Spasial:</strong> Mengingat kerentanan regional yang sangat bervariasi—di mana Pulau Jawa mendominasi secara kuantitas kasus namun wilayah luar Jawa (seperti Sumatra dan Kalimantan) terus mengalami tren kenaikan konstan—mitigasi banjir nasional harus dialihkan dari pendekatan seragam menjadi kebijakan zonasi berbasis karakteristik kepulauan.
            </div>
        </div>
    """
