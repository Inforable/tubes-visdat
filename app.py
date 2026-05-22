import streamlit as st
import pandas as pd
import plotly.express as px
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
# 1. PAGE INITIALIZATION & CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Visualisasi Banjir Indonesia",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. PREMIUM DARK SLATE-CHARCOAL DESIGN SYSTEM (CUSTOM CSS)
# ==============================================================================
st.markdown("""
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
        background-color: #0f0f11;
        color: #ffffff;
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
        color: #ffffff !important;
        font-size: 1.50rem !important;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        padding: 0;
        text-transform: uppercase;
    }
    .branding-subtitle {
        color: #a1a1aa !important;
        font-size: 0.85rem !important;
        margin-top: 2px !important;
        font-weight: 400;
    }
    
    /* Custom Card Style for KPIs */
    .metric-card {
        background-color: #18181b;
        border: 1px solid #27272a;
        border-left: 4px solid #2563eb !important;
        border-radius: 10px;
        padding: 12px 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        text-align: left;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #3b82f6;
        box-shadow: 0 6px 12px -3px rgba(0, 0, 0, 0.3), 0 2px 4px -4px rgba(0, 0, 0, 0.3);
    }
    .metric-label {
        font-size: 0.78rem !important;
        font-weight: 600;
        text-transform: uppercase;
        color: #a1a1aa;
        letter-spacing: 0.5px;
        margin-bottom: 4px !important;
    }
    .metric-value {
        font-size: 2.2rem !important;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.1 !important;
    }
    
    /* Glassmorphic Takeaways / Bullet Box */
    .takeaways-box {
        background: rgba(24, 24, 27, 0.75);
        border: 1px solid rgba(37, 99, 235, 0.25);
        border-radius: 12px;
        padding: 16px 24px !important;
        margin-top: 20px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    .takeaways-title {
        color: #ffffff;
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
        color: #d4d4d8;
        font-size: 0.9rem !important;
    }
    .takeaway-bullet strong {
        color: #ffffff;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #18181b !important;
        border-right: 1px solid #27272a !important;
    }
    
    /* Filter Section Title */
    .filter-header {
        color: #ffffff;
        font-size: 0.95rem !important;
        font-weight: 700;
        margin-bottom: 6px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Container override for st.container(border=True) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 12px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #18181b !important;
    }
    
    /* Fix multiselect dropdown: force dark background and white text */
    [data-baseweb="select"] > div:first-child {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 6px !important;
    }
    [data-baseweb="select"] span,
    [data-baseweb="select"] input,
    [data-baseweb="select"] input::placeholder {
        color: #ffffff !important;
    }
    [data-baseweb="popover"] {
        background-color: #18181b !important;
    }
    [data-baseweb="menu"] li {
        color: #ffffff !important;
        background-color: #18181b !important;
    }
    [data-baseweb="menu"] li:hover {
        background-color: #27272a !important;
    }

    /* Premium Styled Multiselect Pills */
    [data-baseweb="tag"] {
        background-color: rgba(37, 99, 235, 0.15) !important;
        border: 1px solid rgba(37, 99, 235, 0.35) !important;
        border-radius: 6px !important;
        padding: 1px 4px !important;
    }
    [data-baseweb="tag"] span {
        color: #3b82f6 !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-baseweb="tag"] svg {
        fill: #3b82f6 !important;
    }
    
    /* Premium Styled Buttons */
    .stApp div.stButton > button,
    .stApp div.stButton > button:focus,
    .stApp div.stButton > button:focus-visible {
        background-color: #18181b !important;
        color: #ffffff !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    .stApp div.stButton > button:hover {
        background-color: #27272a !important;
        border-color: #3f3f46 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    .stApp div.stButton > button:active {
        transform: translateY(0) !important;
        background-color: #3f3f46 !important;
    }

    /* Premium Styled Segmented Control (Pills) */
    div[data-testid="stSegmentedControl"] {
        gap: 6px !important;
    }
    div[data-testid="stSegmentedControl"] button {
        background-color: #18181b !important;
        color: #a1a1aa !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
        padding: 4px 12px !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stSegmentedControl"] button:hover {
        background-color: #27272a !important;
        color: #ffffff !important;
        border-color: #3f3f46 !important;
    }
    div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-color: #2563eb !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3) !important;
    }
    div[data-testid="stSegmentedControl"] button[aria-checked="true"]:hover {
        background-color: #3b82f6 !important;
        border-color: #3b82f6 !important;
        color: #ffffff !important;
    }
    
    /* Slider overrides */
    div[data-testid="stSlider"] label {
        color: #a1a1aa !important;
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
        background: #27272a !important;
    }
    div[data-testid="stSlider"] div[data-testid="stSliderTickBar"] {
        color: #a1a1aa !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. DATA LOADING & CACHING (EXCLUDING 2026)
# ==============================================================================
@st.cache_data
def load_data():
    # Load aggregated province & annual datasets
    df_prov_annual = pd.read_csv("data/processed/banjir_provinsi_tahunan.csv")
    df_trend_global = pd.read_csv("data/processed/trend_banjir_indonesia_2000_2026.csv")
    
    # ⚠️ CRITICAL: Exclude 2026 entirely as per user feedback
    df_prov_annual = df_prov_annual[df_prov_annual['year'] < 2026]
    df_trend_global = df_trend_global[df_trend_global['year'] < 2026]
    
    return df_prov_annual, df_trend_global

# Indonesian Province GeoJSON boundary maps URL
GEOJSON_URL = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province-simple.json"

try:
    df_prov_annual, df_trend_global = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    data_loaded = False

# ==============================================================================
# 4. INTERACTIVE SIDEBAR FILTERS
# ==============================================================================
if data_loaded:
    @st.fragment
    def render_dashboard():
        # ==============================================================================
        # PRE-INITIALIZE SESSION STATE FOR LINEAR BRANDING HEADER INLINE VALUE RENDERING
        # ==============================================================================
        if 'active_year' not in st.session_state:
            st.session_state.active_year = 2000
        if 'is_playing' not in st.session_state:
            st.session_state.is_playing = False
        if 'timeline_mode' not in st.session_state:
            st.session_state.timeline_mode = "Rentang Tahun"
        if 'year_range' not in st.session_state:
            st.session_state.year_range = (2000, 2025)
            
        # Get active range/year for the branding header badge
        if st.session_state.timeline_mode == "Rentang Tahun":
            start_year, end_year = st.session_state.year_range
            year_badge = f"{start_year} – {end_year}"
        else:
            start_year = st.session_state.active_year
            end_year = st.session_state.active_year
            year_badge = f"{start_year}"

        # ==============================================================================
        # A. BRANDING HEADER
        # ==============================================================================
        st.markdown(f"""
            <div class="branding-banner">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                    <div>
                        <h1 class="branding-title">Total Kejadian Banjir di Indonesia</h1>
                        <p class="branding-subtitle">Visualisasi Data Interaktif Kejadian Banjir Regional (2000 - 2025)</p>
                    </div>
                    <div style="font-weight: 700; color: #3b82f6; font-size: 1.15rem; border: 1.5px solid rgba(59, 130, 246, 0.4); padding: 6px 16px; border-radius: 20px; background: rgba(59, 130, 246, 0.15); font-family: 'Inter', sans-serif;">
                        {year_badge}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # ==============================================================================
        # B. DYNAMIC HORIZONTAL FILTER PANEL (MAIN PAGE)
        # ==============================================================================
        st.markdown(f'<p class="filter-header" style="margin-bottom: 8px;">{svg("search", 18, "#3b82f6")} Panel Filter Analisis</p>', unsafe_allow_html=True)
        
        with st.container(border=True):
            filter_col1, filter_col2 = st.columns([1, 1])
            provinces_available = sorted(list(df_prov_annual['Propinsi'].unique()))
            
            with filter_col1:
                st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: #a1a1aa; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.4px;">Mode Analisis Waktu</p>', unsafe_allow_html=True)
                
                mode_options = ["Rentang Tahun", "Animasi (Play)"]
                selected_mode = st.segmented_control(
                    "Mode",
                    options=mode_options,
                    default=st.session_state.timeline_mode if st.session_state.timeline_mode in mode_options else "Rentang Tahun",
                    label_visibility="collapsed",
                    key="mode_segmented"
                )
                
                # Defensive handling: prevent deselection from returning None
                if selected_mode is None:
                    selected_mode = st.session_state.timeline_mode
                    
                if selected_mode != st.session_state.timeline_mode:
                    st.session_state.timeline_mode = selected_mode
                    if selected_mode == "Rentang Tahun":
                        st.session_state.is_playing = False
                    st.rerun()

                if st.session_state.timeline_mode == "Rentang Tahun":
                    st.session_state.is_playing = False
                    year_range = st.slider(
                        "Pilih Rentang Tahun",
                        min_value=2000,
                        max_value=2025,
                        value=st.session_state.year_range,
                        step=1,
                        key="year_range"
                    )
                    start_year, end_year = year_range
                else:
                    # Animasi Kronologis Mode — single year slider
                    active_year = st.slider(
                        "Pilih Tahun",
                        min_value=2000,
                        max_value=2025,
                        value=st.session_state.active_year,
                        step=1,
                        key="active_year"
                    )
                    st.session_state.active_year = active_year
                    start_year = st.session_state.active_year
                    end_year = st.session_state.active_year
                    
                    # Playback buttons row
                    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1.3, 1.5, 1.3, 2.9])
                    
                    with btn_col1:
                        if st.button("« Mundur", use_container_width=True, key="btn_back"):
                            st.session_state.is_playing = False
                            st.session_state.active_year = max(2000, st.session_state.active_year - 1) if st.session_state.active_year > 2000 else 2025
                            st.rerun()
                    
                    with btn_col2:
                        is_playing = st.session_state.is_playing
                        play_label = "Pause" if is_playing else "Play"
                        play_type = "primary" if is_playing else "secondary"
                        if st.button(play_label, type=play_type, use_container_width=True, key="btn_play"):
                            st.session_state.is_playing = not is_playing
                            st.rerun()
                            
                    with btn_col3:
                        if st.button("Maju »", use_container_width=True, key="btn_fwd"):
                            st.session_state.is_playing = False
                            st.session_state.active_year = st.session_state.active_year + 1 if st.session_state.active_year < 2025 else 2000
                            st.rerun()
                            
                    with btn_col4:
                        st.markdown(f"""
                            <div style="font-weight: 700; font-size: 1rem; color: #3b82f6; background: rgba(37, 99, 235, 0.15); border: 1.5px solid rgba(37, 99, 235, 0.3); padding: 7px 12px; border-radius: 8px; text-align: center; margin-top: 2px;">
                                {svg("calendar_month", 16, "#3b82f6")} Tahun: <span style="font-size:1.15rem; font-weight:800; color:#ffffff;">{st.session_state.active_year}</span>
                            </div>
                        """, unsafe_allow_html=True)
                
            with filter_col2:
                st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: #a1a1aa; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.4px;">Pilih Provinsi</p>', unsafe_allow_html=True)
                # Province Selector (Multi-select)
                selected_provinces = st.multiselect(
                    "Pilih Provinsi",
                    options=provinces_available,
                    default=[],
                    placeholder="Pilih Provinsi (Biarkan kosong untuk regional)",
                    label_visibility="collapsed",
                    help="Biarkan kosong untuk menampilkan semua provinsi secara regional."
                )
        
        # ==============================================================================
        # C. DATA FILTERING ENGINE (ALWAYS KEEP MAP FULL WITH GREY INACTIVE PROVINCES)
        # ==============================================================================
        df_filtered = df_prov_annual[
            (df_prov_annual['year'] >= start_year) & 
            (df_prov_annual['year'] <= end_year)
        ]
        
        # Apply Province filter only for the statistics of active provinces,
        # but keep all provinces on the map by merging with the master list.
        if selected_provinces:
            df_filtered_agg = df_filtered[df_filtered['Propinsi'].isin(selected_provinces)]
        else:
            df_filtered_agg = df_filtered
            
        # Aggregate data across the filtered year range per province
        df_province_summary = (
            df_filtered_agg.groupby('Propinsi')
            .agg(
                total_kejadian=('frekuensi_banjir', 'sum'),
                total_area_km2=('total_area_km2', 'sum'),
                median_durasi=('median_durasi_hari', 'median')
            )
            .reset_index()
        )
        
        # Create a master DataFrame of all provinces to ensure full map visualization at all times
        df_master_provinces = pd.DataFrame({"Propinsi": provinces_available})
        df_province_summary = pd.merge(df_master_provinces, df_province_summary, on="Propinsi", how="left")
        
        # Fill NaN values to render as grey (value=0) rather than disappearing/leaving holes
        df_province_summary["total_kejadian"] = df_province_summary["total_kejadian"].fillna(0).astype(int)
        df_province_summary["total_area_km2"] = df_province_summary["total_area_km2"].fillna(0.0)
        df_province_summary["median_durasi"] = df_province_summary["median_durasi"].fillna(0.0)
        
        # Compute dynamic values for KPI Metrics
        total_events = df_province_summary['total_kejadian'].sum()
        affected_prov_count = df_province_summary[df_province_summary['total_kejadian'] > 0]['Propinsi'].nunique()
        
        # Only check maximum occurrences province if there is at least one active event
        if len(df_province_summary[df_province_summary['total_kejadian'] > 0]) > 0:
            max_prov_row = df_province_summary[df_province_summary['total_kejadian'] > 0].loc[
                df_province_summary[df_province_summary['total_kejadian'] > 0]['total_kejadian'].idxmax()
            ]
            max_prov_name = max_prov_row['Propinsi']
            max_prov_val = max_prov_row['total_kejadian']
        else:
            max_prov_name = "N/A"
            max_prov_val = 0

        # Display KPI Metrics
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{svg('waves', 16, '#a1a1aa')} Total Kejadian Banjir</div>
                    <div class="metric-value">{total_events:,}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with kpi_col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{svg('map_search', 16, '#a1a1aa')} Provinsi Terdampak</div>
                    <div class="metric-value">{affected_prov_count}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with kpi_col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{svg('flag', 16, '#a1a1aa')} Kasus Terbanyak ({max_prov_name})</div>
                    <div class="metric-value">{max_prov_val:,}</div>
                </div>
            """, unsafe_allow_html=True)
            
        # ==============================================================================
        # 5. MIDDLE SECTION: GEOSPATIAL MAP (LEFT) & TOP 10 BAR CHART (RIGHT)
        # ==============================================================================
        col_mid1, col_mid2 = st.columns(2)
        
        with col_mid1:
            st.markdown(f'<h4 style="color: #ffffff; font-size: 1.05rem; margin-top: 6px; margin-bottom: 2px; font-weight: 700;">{svg("map_search", 16, "#3b82f6")} Peta Distribusi Kejadian Banjir Regional</h4>', unsafe_allow_html=True)
            
            if len(df_province_summary) > 0:
                with st.container(border=True):
                    # Premium sequential scale from dark charcoal (#27272a) up to bright ice-blue (#93c5fd)
                    custom_navy_scale = [
                        [0.0, "#27272a"],      # Beautiful slate-dark for exactly 0 occurrences
                        [0.00001, "#1c1c1f"],  # Slightly lighter card blending shade
                        [0.15, "#1e3a8a"],     # Deep navy blue
                        [0.4, "#2563eb"],      # Vibrant blue
                        [0.7, "#60a5fa"],      # Sky blue
                        [1.0, "#93c5fd"]       # Bright ice blue highlight
                    ]
                    
                    fig_map = px.choropleth(
                        df_province_summary,
                        geojson=GEOJSON_URL,
                        locations="Propinsi",
                        featureidkey="properties.Propinsi",
                        color="total_kejadian",
                        color_continuous_scale=custom_navy_scale,
                        range_color=[0, max(1, df_province_summary['total_kejadian'].max())],
                        hover_data=["Propinsi", "total_area_km2"]
                    )
                    
                    fig_map.update_geos(
                        projection_type="mercator",
                        lonaxis_range=[94.0, 142.0],
                        lataxis_range=[-11.0, 8.0],
                        visible=False,
                        showcoastlines=False,
                        showcountries=False,
                        showframe=False,
                        bgcolor="rgba(0,0,0,0)"
                    )
                    
                    fig_map.update_layout(
                        height=360,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin={"r": 0, "t": 10, "l": 0, "b": 10},
                        coloraxis_colorbar=dict(
                            orientation="h",
                            y=-0.15,
                            x=0.5,
                            xanchor="center",
                            title="Tingkat Kejadian Banjir",
                            title_font=dict(color="#a1a1aa", size=10),
                            tickfont=dict(color="#a1a1aa", size=9),
                            thickness=10,
                            len=0.7
                        )
                    )
                    
                    fig_map.update_traces(
                        hovertemplate="<span style='font-size: 14px; font-weight: bold; color: #60a5fa;'>%{customdata[0]}</span><br><br>" +
                                      "Total Kejadian: <b>%{z:,}</b> kasus<br>" +
                                      "Luas Area Banjir: <b>%{customdata[1]:,.1f}</b> km²<extra></extra>",
                        hoverlabel=dict(
                            bgcolor="#18181b",
                            bordercolor="#3b82f6",
                            font_size=13,
                            font_family="Inter, system-ui, -apple-system, sans-serif",
                            font_color="#ffffff",
                            align="left"
                        )
                    )
                    
                    st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.info("Tidak ada data spasial untuk filter yang dipilih.")
                
        with col_mid2:
            st.markdown(f'<h4 style="color: #ffffff; font-size: 1.05rem; margin-top: 6px; margin-bottom: 2px; font-weight: 700;">{svg("analytics", 16, "#3b82f6")} Top 10 Provinsi Kasus Terbanyak</h4>', unsafe_allow_html=True)
            
            if len(df_province_summary) > 0:
                with st.container(border=True):
                    # Sort and select Top 10
                    df_top10 = df_province_summary.sort_values(by='total_kejadian', ascending=True).tail(10)
                    
                    fig_bar = px.bar(
                        df_top10,
                        x="total_kejadian",
                        y="Propinsi",
                        orientation='h',
                        labels={
                            "total_kejadian": "Total Kejadian",
                            "Propinsi": "Provinsi"
                        },
                        hover_data={
                            "Propinsi": True,
                            "total_kejadian": ":,"
                        }
                    )
                    
                    fig_bar.update_traces(
                        marker_color='#2563eb',
                        marker_line_color='#3b82f6',
                        marker_line_width=1.5,
                        opacity=0.95,
                        hovertemplate="<span style='font-size: 14px; font-weight: bold; color: #60a5fa;'>%{y}</span><br><br>" +
                                      "Total Kejadian: <b>%{x:,}</b> kasus<extra></extra>",
                        hoverlabel=dict(
                            bgcolor="#18181b",
                            bordercolor="#3b82f6",
                            font_size=13,
                            font_family="Inter, system-ui, -apple-system, sans-serif",
                            font_color="#ffffff",
                            align="left"
                        )
                    )
                    
                    fig_bar.update_layout(
                        height=360,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#ffffff",
                        margin={"r": 15, "t": 15, "l": 15, "b": 15},
                        xaxis=dict(
                            title="Total Kejadian",
                            title_font=dict(color="#a1a1aa", size=11),
                            tickfont=dict(color="#a1a1aa"),
                            gridcolor="#27272a",
                            zeroline=False
                        ),
                        yaxis=dict(
                            title="",
                            tickfont=dict(color="#d4d4d8", weight="bold")
                        )
                    )
                    
                    st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("Tidak ada data untuk diagram batang.")

        # ==============================================================================
        # 6. BOTTOM SECTION: TREN KEJADIAN BANJIR TAHUNAN (FULL-WIDTH)
        # ==============================================================================
        st.markdown(f'<h4 style="color: #ffffff; font-size: 1.05rem; margin-top: 6px; margin-bottom: 2px; font-weight: 700;">{svg("chart_data", 16, "#3b82f6")} Tren Kejadian Banjir Tahunan</h4>', unsafe_allow_html=True)
        
        # For the line chart, we always want to show the full trend (2000-2025)
        # for the selected provinces so the user has historical context!
        df_line_filtered = df_prov_annual
        if selected_provinces:
            df_line_filtered = df_line_filtered[df_line_filtered['Propinsi'].isin(selected_provinces)]
            
        df_yearly_trend = (
            df_line_filtered.groupby('year')
            .agg(total_kejadian=('frekuensi_banjir', 'sum'))
            .reset_index()
            .sort_values('year')
        )
        
        if len(df_yearly_trend) > 0:
            with st.container(border=True):
                fig_line = px.line(
                    df_yearly_trend,
                    x="year",
                    y="total_kejadian",
                    labels={
                        "total_kejadian": "Kejadian Banjir",
                        "year": "Tahun"
                    },
                    hover_data={"year": True, "total_kejadian": ":,"}
                )
                
                fig_line.update_traces(
                    line=dict(color='#3b82f6', width=3, shape='spline'),
                    mode='lines+markers',
                    marker=dict(color='#ffffff', size=6, line=dict(color='#2563eb', width=2)),
                    fill='tozeroy',
                    fillcolor='rgba(37, 99, 235, 0.12)',
                    hovertemplate="<span style='font-size: 14px; font-weight: bold; color: #60a5fa;'>Tahun %{x}</span><br><br>" +
                                  "Total Kejadian: <b>%{y:,}</b> kasus<extra></extra>",
                    hoverlabel=dict(
                        bgcolor="#18181b",
                        bordercolor="#3b82f6",
                        font_size=13,
                        font_family="Inter, system-ui, -apple-system, sans-serif",
                        font_color="#ffffff",
                        align="left"
                    )
                )
                
                # If in animation mode, add an elegant vertical dashed line indicating the active year
                if st.session_state.timeline_mode == "Animasi (Play)":
                    fig_line.add_vline(
                        x=st.session_state.active_year,
                        line_width=2,
                        line_dash="dash",
                        line_color="#2563eb",
                        annotation_text=f"Tahun {st.session_state.active_year}",
                        annotation_position="top left",
                        annotation_font=dict(color="#3b82f6", size=11, family="Inter")
                    )
                
                fig_line.update_layout(
                    height=240,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#ffffff",
                    margin={"r": 15, "t": 15, "l": 15, "b": 15},
                    xaxis=dict(
                        title="Tahun",
                        title_font=dict(color="#a1a1aa", size=11),
                        tickfont=dict(color="#a1a1aa"),
                        gridcolor="#27272a",
                        dtick=2 if (end_year - start_year) > 10 or st.session_state.timeline_mode == "Animasi (Play)" else 1,
                        zeroline=False
                    ),
                    yaxis=dict(
                        title="Frekuensi Kejadian",
                        title_font=dict(color="#a1a1aa", size=11),
                        tickfont=dict(color="#a1a1aa"),
                        gridcolor="#27272a",
                        zeroline=False
                    )
                )
                
                st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Tidak ada data untuk diagram garis tren.")
                
        # Handle animation playback rerun
        if st.session_state.is_playing and st.session_state.timeline_mode == "Animasi (Play)":
            import time
            time.sleep(0.7)  # Dynamic, fluid frame transitions
            st.session_state.active_year += 1
            if st.session_state.active_year > 2025:
                st.session_state.active_year = 2000  # Seamless wrap-around
            st.rerun()

    # Render dynamic fragment
    render_dashboard()

    # ==============================================================================
    # 7. GLASSMORPHIC INSIGHTS & TAKEAWAYS SECTION (BOTTOM)
    # ==============================================================================
    st.markdown(f"""
        <div class="takeaways-box">
            <div class="takeaways-title">
                <span>{svg('lightbulb', 22, '#3b82f6')} Informasi Kunci &amp; Wawasan Data</span>
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
    """, unsafe_allow_html=True)
