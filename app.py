import streamlit as st
import pandas as pd
import time
from src.data_loader import load_data, load_geojson
from src.ui_components import LIGHT_CSS, render_header, render_kpi_card, render_takeaways, svg
from src.charts import create_map, create_bar, create_line

# ==============================================================================
# 1. PAGE INITIALIZATION & CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Visualisasi Banjir Indonesia",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Premium Custom Light Style CSS System
st.markdown(LIGHT_CSS, unsafe_allow_html=True)

# ==============================================================================
# 2. DATA LOADING
# ==============================================================================
try:
    df_prov_annual, df_trend_global = load_data()
    geojson_data = load_geojson()
    data_loaded = True
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    data_loaded = False

# ==============================================================================
# 3. INTERACTIVE DASHBOARD FRAGMENT RENDERER
# ==============================================================================
if data_loaded:
    @st.fragment
    def render_dashboard():
        # Initialize session state for playback timeline controls
        if 'active_year' not in st.session_state:
            st.session_state.active_year = 2002  # Default to 2002 as shown in the reference image
        if 'year_slider' not in st.session_state:
            st.session_state.year_slider = 2002
        if 'is_playing' not in st.session_state:
            st.session_state.is_playing = False
        if 'timeline_mode' not in st.session_state:
            st.session_state.timeline_mode = "Per Tahun"
        if 'year_range' not in st.session_state:
            st.session_state.year_range = (2000, 2025)
            
        # Get active range/year for branding header
        if st.session_state.timeline_mode == "Rentang Kustom":
            start_year, end_year = st.session_state.year_range
            year_badge = f"Rentang: {start_year} – {end_year}"
        else:
            start_year = st.session_state.active_year
            end_year = st.session_state.active_year
            year_badge = f"Tahun: {start_year}"

        # A. BRANDING HEADER
        st.markdown(render_header(year_badge), unsafe_allow_html=True)

        # B. DYNAMIC HORIZONTAL FILTER PANEL
        st.markdown(f'<p class="filter-header" style="margin-bottom: 8px;">{svg("calendar_month", 18, "#2563eb")} PANEL KONTROL & FILTER ANALISIS</p>', unsafe_allow_html=True)
        
        with st.container(border=True):
            filter_col1, filter_col2, filter_col3 = st.columns([1.1, 1.3, 2.2])
            provinces_available = sorted(list(df_prov_annual['Propinsi'].unique()))
            
            with filter_col1:
                st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: #475569; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.4px;">Mode Analisis</p>', unsafe_allow_html=True)
                
                mode_options = ["Per Tahun", "Rentang Kustom"]
                selected_mode = st.segmented_control(
                    "Mode",
                    options=mode_options,
                    default=st.session_state.timeline_mode if st.session_state.timeline_mode in mode_options else "Per Tahun",
                    label_visibility="collapsed",
                    key="mode_segmented"
                )
                
                # Defensive handling: prevent deselection from returning None
                if selected_mode is None:
                    selected_mode = st.session_state.timeline_mode
                    
                if selected_mode != st.session_state.timeline_mode:
                    st.session_state.timeline_mode = selected_mode
                    if selected_mode == "Rentang Kustom":
                        st.session_state.is_playing = False
                    st.rerun()

            with filter_col2:
                st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: #475569; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.4px;">Pilih Provinsi</p>', unsafe_allow_html=True)
                selected_provinces = st.multiselect(
                    "Pilih Provinsi",
                    options=provinces_available,
                    default=[],
                    placeholder="Semua Provinsi",
                    label_visibility="collapsed"
                )
                
            with filter_col3:
                if st.session_state.timeline_mode == "Rentang Kustom":
                    st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: #475569; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.4px;">Timeline Waktu</p>', unsafe_allow_html=True)
                    year_range = st.slider(
                        "Pilih Rentang Tahun",
                        min_value=2000,
                        max_value=2025,
                        value=st.session_state.year_range,
                        step=1,
                        key="year_range_slider",
                        label_visibility="collapsed"
                    )
                    start_year, end_year = year_range
                    st.session_state.year_range = year_range
                else:
                    st.markdown('<p style="font-weight: 600; margin-bottom: 8px; color: #475569; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.4px;">Timeline Waktu (Live)</p>', unsafe_allow_html=True)
                    
                    slider_subcol, controls_subcol = st.columns([55, 45])
                    
                    with slider_subcol:
                        # Dynamic key forces re-initialization from the value parameter on programmatical updates!
                        active_year = st.slider(
                            "Pilih Tahun",
                            min_value=2000,
                            max_value=2025,
                            value=st.session_state.active_year,
                            step=1,
                            key=f"year_slider_{st.session_state.active_year}",
                            label_visibility="collapsed"
                        )
                        st.session_state.active_year = active_year
                        start_year = active_year
                        end_year = active_year
                        
                    with controls_subcol:
                        c1, c2, c3, c4 = st.columns([1, 1, 1, 1.5])
                        with c1:
                            if st.button("«", use_container_width=True, key="btn_back"):
                                st.session_state.is_playing = False
                                st.session_state.active_year = max(2000, st.session_state.active_year - 1) if st.session_state.active_year > 2000 else 2025
                                st.rerun()
                        with c2:
                            is_playing = st.session_state.is_playing
                            play_label = "❚❚" if is_playing else "▶"
                            play_type = "primary" if is_playing else "secondary"
                            if st.button(play_label, type=play_type, use_container_width=True, key="btn_play"):
                                st.session_state.is_playing = not is_playing
                                st.rerun()
                        with c3:
                            if st.button("»", use_container_width=True, key="btn_fwd"):
                                st.session_state.is_playing = False
                                st.session_state.active_year = st.session_state.active_year + 1 if st.session_state.active_year < 2025 else 2000
                                st.rerun()
                        with c4:
                            st.markdown(f"""
                                <div style="font-weight: 700; font-size: 0.9rem; color: #10b981; background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); padding: 5px 8px; border-radius: 6px; text-align: center; font-family: 'Inter', sans-serif;">
                                    {st.session_state.active_year}
                                </div>
                            """, unsafe_allow_html=True)

        # C. DATA FILTERING ENGINE
        df_filtered = df_prov_annual[
            (df_prov_annual['year'] >= start_year) & 
            (df_prov_annual['year'] <= end_year)
        ]
        
        if selected_provinces:
            df_filtered_agg = df_filtered[df_filtered['Propinsi'].isin(selected_provinces)]
        else:
            df_filtered_agg = df_filtered
            
        df_province_summary = (
            df_filtered_agg.groupby('Propinsi')
            .agg(
                total_kejadian=('frekuensi_banjir', 'sum'),
                total_area_km2=('total_area_km2', 'sum'),
                median_durasi=('median_durasi_hari', 'median')
            )
            .reset_index()
        )
        
        df_master_provinces = pd.DataFrame({"Propinsi": provinces_available})
        df_province_summary = pd.merge(df_master_provinces, df_province_summary, on="Propinsi", how="left")
        
        df_province_summary["total_kejadian"] = df_province_summary["total_kejadian"].fillna(0).astype(int)
        df_province_summary["total_area_km2"] = df_province_summary["total_area_km2"].fillna(0.0)
        df_province_summary["median_durasi"] = df_province_summary["median_durasi"].fillna(0.0)
        
        total_events = df_province_summary['total_kejadian'].sum()
        affected_prov_count = df_province_summary[df_province_summary['total_kejadian'] > 0]['Propinsi'].nunique()
        
        if len(df_province_summary[df_province_summary['total_kejadian'] > 0]) > 0:
            max_prov_row = df_province_summary[df_province_summary['total_kejadian'] > 0].loc[
                df_province_summary[df_province_summary['total_kejadian'] > 0]['total_kejadian'].idxmax()
            ]
            max_prov_name = max_prov_row['Propinsi']
            max_prov_val = max_prov_row['total_kejadian']
        else:
            max_prov_name = "N/A"
            max_prov_val = 0

        # D. DISPLAY KPI METRICS
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
            st.markdown(render_kpi_card("Total Kejadian Banjir", f"{total_events:,}", "waves"), unsafe_allow_html=True)
            
        with kpi_col2:
            st.markdown(render_kpi_card("Provinsi Terdampak", f"{affected_prov_count}", "map_search"), unsafe_allow_html=True)
            
        with kpi_col3:
            st.markdown(render_kpi_card(f"Kasus Terbanyak ({max_prov_name})", f"{max_prov_val:,}", "flag"), unsafe_allow_html=True)
            
        # E. MIDDLE SECTION: GEOSPATIAL MAP (LEFT) & TOP 10 BAR CHART (RIGHT)
        col_mid1, col_mid2 = st.columns([1.3, 0.7])
        
        with col_mid1:
            st.markdown(f'<h4 style="color: #0f172a; font-size: 1.05rem; margin-top: 6px; margin-bottom: 2px; font-weight: 700;">{svg("map_search", 16, "#2563eb")} Peta Distribusi Kejadian Banjir Regional</h4>', unsafe_allow_html=True)
            
            if len(df_province_summary) > 0:
                with st.container(border=True):
                    fig_map = create_map(df_province_summary, geojson_data)
                    st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.info("Tidak ada data spasial untuk filter yang dipilih.")
                
        with col_mid2:
            st.markdown(f'<h4 style="color: #0f172a; font-size: 1.05rem; margin-top: 6px; margin-bottom: 2px; font-weight: 700;">{svg("analytics", 16, "#2563eb")} Top 10 Provinsi Kasus Terbanyak</h4>', unsafe_allow_html=True)
            
            if len(df_province_summary) > 0:
                with st.container(border=True):
                    fig_bar = create_bar(df_province_summary)
                    st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("Tidak ada data untuk diagram batang.")
 
        # F. BOTTOM SECTION: TREN KEJADIAN BANJIR TAHUNAN (FULL-WIDTH)
        st.markdown(f'<h4 style="color: #0f172a; font-size: 1.05rem; margin-top: 6px; margin-bottom: 2px; font-weight: 700;">{svg("chart_data", 16, "#2563eb")} Tren Kejadian Banjir Tahunan</h4>', unsafe_allow_html=True)
        
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
                fig_line = create_line(
                    df_yearly_trend,
                    st.session_state.active_year,
                    st.session_state.timeline_mode,
                    start_year,
                    end_year
                )
                st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Tidak ada data untuk diagram garis tren.")
                
        # Handle animation playback rerun loop
        if st.session_state.is_playing and st.session_state.timeline_mode == "Per Tahun":
            time.sleep(0.7)  # Dynamic, fluid frame transitions
            next_year = st.session_state.active_year + 1
            if next_year > 2025:
                next_year = 2000  # Seamless wrap-around
            st.session_state.active_year = next_year
            st.rerun()

    # Executing fragment dashboard
    render_dashboard()

    # G. GLASSMORPHIC INSIGHTS & TAKEAWAYS SECTION (BOTTOM)
    st.markdown(render_takeaways(), unsafe_allow_html=True)
