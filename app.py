import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================================================
# 1. PAGE INITIALIZATION & CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Visualisasi Banjir Indonesia",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. PREMIUM SLATE-ORANGE DESIGN SYSTEM (CUSTOM CSS)
# ==============================================================================
st.markdown("""
    <style>
    /* Main Layout Styling */
    .stApp {
        background-color: #0f1319;
        color: #ffffff;
        font-family: 'Inter', 'Roboto', sans-serif;
    }
    
    /* Header & Branding Banner */
    .branding-banner {
        background: linear-gradient(135deg, #1b222c 0%, #0f1319 100%);
        border-bottom: 2px solid #ff5e14;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .branding-title {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        padding: 0;
        text-transform: uppercase;
    }
    .branding-subtitle {
        color: #a0aec0;
        font-size: 1.1rem;
        margin-top: 4px;
        font-weight: 400;
    }
    
    /* Custom Card Style for KPIs */
    .metric-card {
        background-color: #161c24;
        border: 1px solid #ff5e1422;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, border-color 0.3s ease;
        text-align: center;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #ff5e1488;
    }
    .metric-label {
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #a0aec0;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ff5e14;
    }
    
    /* Glassmorphic Takeaways / Bullet Box */
    .takeaways-box {
        background: rgba(22, 28, 36, 0.7);
        border: 1px solid rgba(255, 94, 20, 0.15);
        border-radius: 16px;
        padding: 24px 32px;
        margin-top: 36px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    .takeaways-title {
        color: #ff5e14;
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
        color: #e2e8f0;
    }
    .takeaway-bullet strong {
        color: #ffffff;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161c24 !important;
        border-right: 1px solid #2d3748 !important;
    }
    .css-1d391tw, .css-k3g6vf {
        color: #ffffff !important;
    }
    
    /* Filter Section Title */
    .filter-header {
        color: #ff5e14;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
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
        st.sidebar.markdown('<p class="filter-header">🔍 Filter Analisis</p>', unsafe_allow_html=True)
        
        # Year Range Slider (2000 - 2025)
        year_range = st.sidebar.slider(
            "Pilih Rentang Tahun",
            min_value=2000,
            max_value=2025,
            value=(2000, 2025),
            step=1
        )
        start_year, end_year = year_range
        
        # Province Selector (Multi-select)
        provinces_available = sorted(list(df_prov_annual['Propinsi'].unique()))
        selected_provinces = st.sidebar.multiselect(
            "Pilih Wilayah/Provinsi",
            options=provinces_available,
            default=[],
            help="Biarkan kosong untuk menampilkan semua provinsi secara regional."
        )
        
        # ==============================================================================
        # 5. DATA FILTERING ENGINE
        # ==============================================================================
        # Filter by selected Year range
        df_filtered = df_prov_annual[
            (df_prov_annual['year'] >= start_year) & 
            (df_prov_annual['year'] <= end_year)
        ]
        
        # Apply Province filter if specified
        if selected_provinces:
            df_filtered = df_filtered[df_filtered['Propinsi'].isin(selected_provinces)]
            
        # Aggregate data across the filtered year range per province
        df_province_summary = (
            df_filtered.groupby('Propinsi')
            .agg(
                total_kejadian=('frekuensi_banjir', 'sum'),
                total_area_km2=('total_area_km2', 'sum'),
                median_durasi=('median_durasi_hari', 'median')
            )
            .reset_index()
        )
        
        # ==============================================================================
        # 6. HEADER & KPI METRICS SECTION
        # ==============================================================================
        # Premium Header Banner
        st.markdown(f"""
            <div class="branding-banner">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <h1 class="branding-title">Total Kejadian Banjir di Indonesia</h1>
                        <p class="branding-subtitle">Visualisasi Data Interaktif Kejadian Banjir • Rentang {start_year} - {end_year}</p>
                    </div>
                    <div style="font-weight: 700; color: #ff5e14; font-size: 1.1rem; border: 1px solid #ff5e1444; padding: 6px 16px; border-radius: 20px; background: rgba(255, 94, 20, 0.05);">
                        IF4061 - VISUALISASI DATA
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Compute dynamic values for KPI Metrics
        total_events = df_province_summary['total_kejadian'].sum()
        affected_prov_count = df_province_summary[df_province_summary['total_kejadian'] > 0]['Propinsi'].nunique()
        
        if len(df_province_summary) > 0:
            max_prov_row = df_province_summary.loc[df_province_summary['total_kejadian'].idxmax()]
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
                    <div class="metric-label">🌊 Total Kejadian Banjir</div>
                    <div class="metric-value">{total_events:,}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with kpi_col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🗺️ Provinsi Terdampak</div>
                    <div class="metric-value">{affected_prov_count}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with kpi_col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🚩 Kasus Terbanyak ({max_prov_name})</div>
                    <div class="metric-value">{max_prov_val:,}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)

        # ==============================================================================
        # 7. INTERACTIVE GEOSPATIAL MAP (MIDDLE SECTION)
        # ==============================================================================
        st.markdown("### 🗺️ Peta Distribusi Kejadian Banjir Regional")
        
        if len(df_province_summary) > 0:
            # Build Plotly Choropleth Map using GeoJSON
            # Custom elegant color scale mirroring the slate/blue-teal aesthetic
            custom_blues = [
                [0.0, "#ebf4f6"],
                [0.2, "#b2d1d9"],
                [0.5, "#6b9cb0"],
                [0.8, "#2d607a"],
                [1.0, "#0f2e42"]
            ]
            
            fig_map = px.choropleth(
                df_province_summary,
                geojson=GEOJSON_URL,
                locations="Propinsi",
                featureidkey="properties.Propinsi",
                color="total_kejadian",
                color_continuous_scale=custom_blues,
                range_color=[0, df_province_summary['total_kejadian'].max()],
                labels={
                    "total_kejadian": "Jumlah Kejadian",
                    "total_area_km2": "Total Area (km²)",
                    "Propinsi": "Provinsi"
                },
                hover_data={
                    "Propinsi": True,
                    "total_kejadian": ":,",
                    "total_area_km2": ":,.2f"
                }
            )
            
            # Manually frame the map to Indonesia's coordinates (longitudes 94°-142°E, latitudes -11° to 8°N)
            # This completely avoids the expensive browser-side calculation of fitbounds="locations" on every rerun,
            # dramatically speeding up the real-time slider responsiveness.
            fig_map.update_geos(
                projection_type="mercator",
                lonaxis_range=[94.0, 142.0],
                lataxis_range=[-11.0, 8.0],
                visible=False,
                bgcolor="#0f1319"
            )
            
            fig_map.update_layout(
                paper_bgcolor="#0f1319",
                plot_bgcolor="#0f1319",
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                coloraxis_colorbar=dict(
                    title="Kejadian",
                    title_font_color="#a0aec0",
                    tickfont_color="#a0aec0"
                )
            )
            
            st.plotly_chart(fig_map, width='stretch')
        else:
            st.info("Tidak ada data spasial untuk filter yang dipilih.")

        st.markdown("<br>", unsafe_allow_html=True)

        # ==============================================================================
        # 8. ANALYTICAL CHARTS SECTION (BOTTOM ROW: TWO COLUMNS)
        # ==============================================================================
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("### 📊 Top 10 Provinsi Kasus Terbanyak")
            
            if len(df_province_summary) > 0:
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
                
                # Styling bar colors (premium orange accent)
                fig_bar.update_traces(
                    marker_color='#ff5e14',
                    marker_line_color='#ffffff',
                    marker_line_width=0.5,
                    opacity=0.9
                )
                
                fig_bar.update_layout(
                    paper_bgcolor="#161c24",
                    plot_bgcolor="#161c24",
                    font_color="#ffffff",
                    margin={"r": 10, "t": 10, "l": 10, "b": 10},
                    xaxis=dict(
                        title="Total Kejadian",
                        title_font=dict(color="#a0aec0"),
                        tickfont=dict(color="#a0aec0"),
                        gridcolor="#2d3748"
                    ),
                    yaxis=dict(
                        title="",
                        tickfont=dict(color="#ffffff")
                    )
                )
                
                st.plotly_chart(fig_bar, width='stretch')
            else:
                st.info("Tidak ada data untuk diagram batang.")
                
        with chart_col2:
            st.markdown("### 📈 Tren Kejadian Banjir Tahunan")
            
            # Calculate yearly aggregate for selected filters
            df_yearly_trend = (
                df_filtered.groupby('year')
                .agg(total_kejadian=('frekuensi_banjir', 'sum'))
                .reset_index()
                .sort_values('year')
            )
            
            if len(df_yearly_trend) > 0:
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
                
                # Smooth line & markers styling
                fig_line.update_traces(
                    line=dict(color='#ff5e14', width=3),
                    mode='lines+markers',
                    marker=dict(color='#ffffff', size=6, line=dict(color='#ff5e14', width=1.5))
                )
                
                fig_line.update_layout(
                    paper_bgcolor="#161c24",
                    plot_bgcolor="#161c24",
                    font_color="#ffffff",
                    margin={"r": 10, "t": 10, "l": 10, "b": 10},
                    xaxis=dict(
                        title="Tahun",
                        title_font=dict(color="#a0aec0"),
                        tickfont=dict(color="#a0aec0"),
                        gridcolor="#2d3748",
                        dtick=2 if (end_year - start_year) > 10 else 1
                    ),
                    yaxis=dict(
                        title="Frekuensi Kejadian",
                        title_font=dict(color="#a0aec0"),
                        tickfont=dict(color="#a0aec0"),
                        gridcolor="#2d3748"
                    )
                )
                
                st.plotly_chart(fig_line, width='stretch')
            else:
                st.info("Tidak ada data untuk diagram garis tren.")

    # Render dynamic fragment
    render_dashboard()

    # ==============================================================================
    # 9. GLASSMORPHIC INSIGHTS & TAKEAWAYS SECTION (BOTTOM)
    # ==============================================================================
    st.markdown("""
        <div class="takeaways-box">
            <div class="takeaways-title">
                <span>💡 Informasi Kunci & Wawasan Data</span>
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
