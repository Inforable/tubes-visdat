import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# ==============================================================================
# SVG ICON HELPER
# ==============================================================================
_SVG_CACHE: dict = {}

def svg(name: str, size: int = 18, color: str = "#1e3a8a") -> str:
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
# 2. PREMIUM LIGHT SLATE-NAVY DESIGN SYSTEM (CUSTOM CSS)
# ==============================================================================
st.markdown("""
    <style>
    /* Main Layout Styling */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: 'Inter', 'Roboto', sans-serif;
    }
    
    /* Header & Branding Banner */
    .branding-banner {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-left: 5px solid #1e3a8a;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
    }
    .branding-title {
        color: #1e3a8a !important;
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        padding: 0;
        text-transform: uppercase;
    }
    .branding-subtitle {
        color: #475569 !important;
        font-size: 1.1rem;
        margin-top: 4px;
        font-weight: 400;
    }
    
    /* Custom Card Style for KPIs */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #2563eb;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05);
    }
    .metric-label {
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
    }
    
    /* Glassmorphic Takeaways / Bullet Box */
    .takeaways-box {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(37, 99, 235, 0.15);
        border-radius: 16px;
        padding: 24px 32px;
        margin-top: 36px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    .takeaways-title {
        color: #1e3a8a;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .takeaway-bullet {
        margin-bottom: 12px;
        line-height: 1.6;
        color: #334155;
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
        color: #1e3a8a;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Fix multiselect dropdown: force white background and dark text */
    [data-baseweb="select"] > div:first-child {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }
    [data-baseweb="select"] span,
    [data-baseweb="select"] input,
    [data-baseweb="select"] input::placeholder {
        color: #475569 !important;
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
        border: 1px solid rgba(37, 99, 235, 0.25) !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
    }
    [data-baseweb="tag"] span {
        color: #1e3a8a !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-baseweb="tag"] svg {
        fill: #1e3a8a !important;
    }
    
    /* Premium Styled Buttons — use higher specificity chain to beat Streamlit defaults */
    .stApp div.stButton > button,
    .stApp div.stButton > button:focus,
    .stApp div.stButton > button:focus-visible {
        background-color: #ffffff !important;
        color: #1e3a8a !important;
        border: 1.5px solid #bfdbfe !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
        transition: all 0.2s ease !important;
    }
    .stApp div.stButton > button:hover {
        background-color: #eff6ff !important;
        border-color: #3b82f6 !important;
        color: #1d4ed8 !important;
        box-shadow: 0 4px 8px rgba(37, 99, 235, 0.12) !important;
        transform: translateY(-1px) !important;
    }
    .stApp div.stButton > button:active {
        transform: translateY(0) !important;
        background-color: #dbeafe !important;
    }

    /* Active tab button (mode selector) */
    .stApp div.stButton > button.tab-active {
        background-color: #1e3a8a !important;
        color: #ffffff !important;
        border-color: #1e3a8a !important;
    }

    /* Custom mode-toggle pill buttons */
    .mode-tab {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 18px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.9rem;
        cursor: pointer;
        border: 1.5px solid #bfdbfe;
        background-color: #ffffff;
        color: #1e3a8a;
        margin-right: 8px;
        transition: all 0.2s ease;
        font-family: 'Inter', sans-serif;
        text-decoration: none;
    }
    .mode-tab.active {
        background-color: #1e3a8a;
        color: #ffffff;
        border-color: #1e3a8a;
    }
    .mode-tab:hover {
        border-color: #3b82f6;
        background-color: #eff6ff;
        color: #1d4ed8;
    }
    .mode-tab.active:hover {
        background-color: #1d4ed8;
        color: #ffffff;
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
# Passing the URL string directly to Plotly Express allows the browser to download and cache the GeoJSON.
# This eliminates sending megabytes of GeoJSON over the WebSocket on every user slide event, ensuring instant, real-time updates.
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
        # A. BRANDING HEADER
        # ==============================================================================
        st.markdown(f"""
            <div class="branding-banner">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                    <div>
                        <h1 class="branding-title" style="color: #1e3a8a !important; margin: 0; padding: 0;">Total Kejadian Banjir di Indonesia</h1>
                        <p class="branding-subtitle" style="color: #475569 !important; margin: 4px 0 0 0;">Visualisasi Data Interaktif Kejadian Banjir Regional (2000 - 2025)</p>
                    </div>
                    <div style="font-weight: 700; color: #1e3a8a; font-size: 1.1rem; border: 1px solid rgba(30, 58, 138, 0.25); padding: 6px 16px; border-radius: 20px; background: rgba(30, 58, 138, 0.05);">
                        IF4061 - VISUALISASI DATA
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # ==============================================================================
        # B. DYNAMIC HORIZONTAL FILTER PANEL (MAIN PAGE)
        # ==============================================================================
        # Initialize session state for animation
        if 'active_year' not in st.session_state:
            st.session_state.active_year = 2000
        if 'is_playing' not in st.session_state:
            st.session_state.is_playing = False
        if 'timeline_mode' not in st.session_state:
            st.session_state.timeline_mode = "Rentang Tahun"

        st.markdown(f'<p class="filter-header" style="margin-bottom: 8px;">{svg("search", 18, "#1e3a8a")} Panel Filter Analisis</p>', unsafe_allow_html=True)
        filter_col1, filter_col2 = st.columns([1, 1])
        
        provinces_available = sorted(list(df_prov_annual['Propinsi'].unique()))
        
        with filter_col1:
            st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: #475569; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.4px;">Mode Analisis Waktu</p>', unsafe_allow_html=True)
            
            # Use two buttons side-by-side as a segmented tab control.
            # Inject a scoped <style> that highlights the ACTIVE button with a navy fill,
            # and leaves the inactive one as a ghost button — no emojis needed.
            is_range_active = st.session_state.timeline_mode == "Rentang Tahun"
            active_nth = "1" if is_range_active else "2"
            st.markdown(f"""
                <style>
                div[data-testid="stHorizontalBlock"] div[data-testid="stButton"]:nth-child({active_nth}) > button {{
                    background-color: #1e3a8a !important;
                    color: #ffffff !important;
                    border-color: #1e3a8a !important;
                    box-shadow: 0 2px 8px rgba(30, 58, 138, 0.25) !important;
                }}
                </style>
            """, unsafe_allow_html=True)

            tab_c1, tab_c2, _ = st.columns([1.6, 2.1, 2.3])
            with tab_c1:
                if st.button(
                    "Rentang Tahun",
                    use_container_width=True,
                    key="tab_range",
                    help="Mode rentang tahun statis"
                ):
                    st.session_state.timeline_mode = "Rentang Tahun"
                    st.session_state.is_playing = False
                    st.rerun()
            with tab_c2:
                if st.button(
                    "Animasi (Play)",
                    use_container_width=True,
                    key="tab_anim",
                    help="Mode animasi kronologis"
                ):
                    st.session_state.timeline_mode = "Animasi Kronologis"
                    st.rerun()

            if st.session_state.timeline_mode == "Rentang Tahun":
                st.session_state.is_playing = False
                year_range = st.slider(
                    "Pilih Rentang Tahun",
                    min_value=2000,
                    max_value=2025,
                    value=(2000, 2025),
                    step=1
                )
                start_year, end_year = year_range
            else:
                # Animasi Kronologis Mode — single year slider
                active_year = st.slider(
                    "Pilih Tahun",
                    min_value=2000,
                    max_value=2025,
                    value=st.session_state.active_year,
                    step=1
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
                    play_label = "Pause" if st.session_state.is_playing else "Play"
                    if st.button(play_label, use_container_width=True, key="btn_play"):
                        st.session_state.is_playing = not st.session_state.is_playing
                        st.rerun()
                        
                with btn_col3:
                    if st.button("Maju »", use_container_width=True, key="btn_fwd"):
                        st.session_state.is_playing = False
                        st.session_state.active_year = st.session_state.active_year + 1 if st.session_state.active_year < 2025 else 2000
                        st.rerun()
                        
                with btn_col4:
                    st.markdown(f"""
                        <div style="font-weight: 700; font-size: 1rem; color: #1e3a8a; background: rgba(37, 99, 235, 0.07); border: 1.5px solid rgba(37, 99, 235, 0.2); padding: 7px 12px; border-radius: 8px; text-align: center; margin-top: 2px;">
                            {svg("calendar_month", 16, "#1e3a8a")} Tahun: <span style="font-size:1.15rem;">{st.session_state.active_year}</span>
                        </div>
                    """, unsafe_allow_html=True)
            
        with filter_col2:
            # Province Selector (Multi-select)
            selected_provinces = st.multiselect(
                "Pilih Provinsi",
                options=provinces_available,
                default=[],
                placeholder="Pilih Provinsi",
                help="Biarkan kosong untuk menampilkan semua provinsi secara regional."
            )
        
        # ==============================================================================
        # C. DATA FILTERING ENGINE (ALWAYS KEEP MAP FULL WITH GREY INACTIVE PROVINCES)
        # ==============================================================================
        # Filter by selected Year range
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
                    <div class="metric-label">{svg('waves', 16, '#64748b')} Total Kejadian Banjir</div>
                    <div class="metric-value">{total_events:,}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with kpi_col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{svg('map_search', 16, '#64748b')} Provinsi Terdampak</div>
                    <div class="metric-value">{affected_prov_count}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with kpi_col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{svg('flag', 16, '#64748b')} Kasus Terbanyak ({max_prov_name})</div>
                    <div class="metric-value">{max_prov_val:,}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)

        # ==============================================================================
        # 7. INTERACTIVE GEOSPATIAL MAP (MIDDLE SECTION)
        # ==========================================================        st.markdown("### 🗺️ Peta Distribusi Kejadian Banjir Regional")
        
        if len(df_province_summary) > 0:
            with st.container(border=True):
                # Build Plotly Choropleth Map using GeoJSON
                # Sophisticated light-theme Navy/Royal Blue sequential heat scale
                # ⚠️ 0 occurrences will map exactly to #cbd5e1 (distinct slate grey)
                # Any values above 0 will map dynamically to sequential blue gradients
                custom_navy_scale = [
                    [0.0, "#cbd5e1"],      # Beautiful slate-grey for exactly 0 occurrences
                    [0.00001, "#f8fafc"],  # Clean off-white matching page background
                    [0.15, "#dbeafe"],     # Very light blue accent
                    [0.4, "#93c5fd"],      # Soft sky blue
                    [0.65, "#3b82f6"],     # Vibrant royal blue
                    [0.85, "#1d4ed8"],     # Rich deep blue
                    [1.0, "#1e3a8a"]       # Premium deep navy highlight
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
                
                # Manually frame the map to Indonesia's coordinates (longitudes 94°-142°E, latitudes -11° to 8°N)
                # This completely avoids the expensive browser-side calculation of fitbounds="locations" on every rerun,
                # dramatically speeding up the real-time slider responsiveness.
                fig_map.update_geos(
                    projection_type="mercator",
                    lonaxis_range=[94.0, 142.0],
                    lataxis_range=[-11.0, 8.0],
                    visible=False,
                    bgcolor="#ffffff"
                )
                
                fig_map.update_layout(
                    paper_bgcolor="#ffffff",
                    plot_bgcolor="#ffffff",
                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                    coloraxis_colorbar=dict(
                        title="Kejadian",
                        title_font_color="#475569",
                        tickfont_color="#475569"
                    )
                )
                
                # Polish the on-province-hover popup tooltip to match our premium navy theme
                fig_map.update_traces(
                    hovertemplate="<b>📍 %{customdata[0]}</b><br>" +
                                  "🌊 Kejadian: <b>%{z:,}</b> kasus<br>" +
                                  "📐 Luas Area: <b>%{customdata[1]:,.1f}</b> km²<extra></extra>",
                    hoverlabel=dict(
                        bgcolor="#0f172a",
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

        st.markdown("<br>", unsafe_allow_html=True)

        # ==============================================================================
        # 8. ANALYTICAL CHARTS SECTION (BOTTOM ROW: TWO COLUMNS)
        # ==============================================================================
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown(f"### {svg('analytics', 20, '#1e3a8a')} Top 10 Provinsi Kasus Terbanyak", unsafe_allow_html=True)
            
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
                    
                    # Styling bar colors (premium deep navy and royal blue accents)
                    fig_bar.update_traces(
                        marker_color='#2563eb',
                        marker_line_color='#1e3a8a',
                        marker_line_width=1.5,
                        opacity=0.9,
                        hovertemplate="<b>📍 %{y}</b><br>" +
                                      "🌊 Kejadian: <b>%{x:,}</b> kasus<extra></extra>",
                        hoverlabel=dict(
                            bgcolor="#0f172a",
                            bordercolor="#3b82f6",
                            font_size=13,
                            font_family="Inter, system-ui, -apple-system, sans-serif",
                            font_color="#ffffff",
                            align="left"
                        )
                    )
                    
                    fig_bar.update_layout(
                        paper_bgcolor="#ffffff",
                        plot_bgcolor="#ffffff",
                        font_color="#0f172a",
                        margin={"r": 10, "t": 10, "l": 10, "b": 10},
                        xaxis=dict(
                            title="Total Kejadian",
                            title_font=dict(color="#475569", size=12),
                            tickfont=dict(color="#475569"),
                            gridcolor="#f1f5f9"
                        ),
                        yaxis=dict(
                            title="",
                            tickfont=dict(color="#0f172a", weight="bold")
                        )
                    )
                    
                    st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("Tidak ada data untuk diagram batang.")
                
        with chart_col2:
            st.markdown(f"### {svg('chart_data', 20, '#1e3a8a')} Tren Kejadian Banjir Tahunan", unsafe_allow_html=True)
            
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
                    
                    # Smooth line & glowing filled area styling (Navy and Royal Blue theme)
                    fig_line.update_traces(
                        line=dict(color='#2563eb', width=3, shape='spline'),
                        mode='lines+markers',
                        marker=dict(color='#1e3a8a', size=7, line=dict(color='#ffffff', width=1.5)),
                        fill='tozeroy',
                        fillcolor='rgba(37, 99, 235, 0.06)',
                        hovertemplate="<b>📅 Tahun %{x}</b><br>" +
                                      "🌊 Kejadian: <b>%{y:,}</b> kasus<extra></extra>",
                        hoverlabel=dict(
                            bgcolor="#0f172a",
                            bordercolor="#3b82f6",
                            font_size=13,
                            font_family="Inter, system-ui, -apple-system, sans-serif",
                            font_color="#ffffff",
                            align="left"
                        )
                    )
                    
                    # If in animation mode, add an elegant vertical dashed line indicating the active year
                    if st.session_state.timeline_mode == "Animasi Kronologis":
                        fig_line.add_vline(
                            x=st.session_state.active_year,
                            line_width=2,
                            line_dash="dash",
                            line_color="#1e3a8a",
                            annotation_text=f"Tahun {st.session_state.active_year}",
                            annotation_position="top left",
                            annotation_font=dict(color="#1e3a8a", size=11, family="Inter")
                        )
                    
                    fig_line.update_layout(
                        paper_bgcolor="#ffffff",
                        plot_bgcolor="#ffffff",
                        font_color="#0f172a",
                        margin={"r": 10, "t": 10, "l": 10, "b": 10},
                        xaxis=dict(
                            title="Tahun",
                            title_font=dict(color="#475569", size=12),
                            tickfont=dict(color="#475569"),
                            gridcolor="#f1f5f9",
                            dtick=2 if (end_year - start_year) > 10 or st.session_state.timeline_mode == "Animasi Kronologis" else 1
                        ),
                        yaxis=dict(
                            title="Frekuensi Kejadian",
                            title_font=dict(color="#475569", size=12),
                            tickfont=dict(color="#475569"),
                            gridcolor="#f1f5f9"
                        )
                    )
                    
                    st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("Tidak ada data untuk diagram garis tren.")
                
        # Handle animation playback rerun
        if st.session_state.is_playing and st.session_state.timeline_mode == "Animasi Kronologis":
            import time
            time.sleep(0.7)  # Dynamic, fluid frame transitions
            st.session_state.active_year += 1
            if st.session_state.active_year > 2025:
                st.session_state.active_year = 2000  # Seamless wrap-around
            st.rerun()

    # Render dynamic fragment
    render_dashboard()

    # ==============================================================================
    # 9. GLASSMORPHIC INSIGHTS & TAKEAWAYS SECTION (BOTTOM)
    # ==============================================================================
    st.markdown(f"""
        <div class="takeaways-box">
            <div class="takeaways-title">
                <span>{svg('lightbulb', 22, '#1e3a8a')} Informasi Kunci &amp; Wawasan Data</span>
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
