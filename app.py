import streamlit as st
import pandas as pd
import time
from src.data_loader import load_data, load_geojson, PULAU_OPTIONS, ALL_PULAU_LABEL
from src.ui_components import (
    LIGHT_CSS,
    render_kpi_card,
    render_chart_title,
    render_insight_card,
)
from src.charts import create_map, create_bar, create_line

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="Visualisasi Banjir Indonesia",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(LIGHT_CSS, unsafe_allow_html=True)

# ==============================================================================
# DATA LOADING
# ==============================================================================
try:
    df_prov_annual, df_trend_global = load_data()
    geojson_data = load_geojson()
    data_loaded = True
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    data_loaded = False

# ==============================================================================
# HELPERS
# ==============================================================================
def col_label(text: str):
    st.markdown(
        f'<p class="filter-col-label">{text}</p>',
        unsafe_allow_html=True,
    )

# ==============================================================================
# DASHBOARD FRAGMENT
# ==============================================================================
if data_loaded:
    @st.fragment
    def render_dashboard():
        defaults = {
            "active_year": 2025,
            "year_slider": 2025,
            "pending_year_slider": None,
            "is_playing": False,
            "timeline_mode": "Rentang Kustom",
            "year_range": (2000, 2025),
            "year_range_slider": (2000, 2025),
            "pulau_filter": ALL_PULAU_LABEL,
        }
        for k, v in defaults.items():
            if k not in st.session_state:
                st.session_state[k] = v

        if st.session_state.pending_year_slider is not None:
            st.session_state.year_slider = st.session_state.pending_year_slider
            st.session_state.active_year = st.session_state.pending_year_slider
            st.session_state.pending_year_slider = None

        if "year_slider" in st.session_state:
            st.session_state.active_year = st.session_state.year_slider
        if "year_range_slider" in st.session_state:
            st.session_state.year_range = st.session_state.year_range_slider

        if st.session_state.timeline_mode == "Rentang Kustom":
            s, e = st.session_state.year_range
            year_badge = f"Rentang: {s} – {e}"
        else:
            s = e = st.session_state.active_year
            year_badge = f"Tahun: {s}"

        # ── TOP HERO: TITLE LEFT, FILTER RIGHT ─────────────────────────
        provinces_available = sorted(df_prov_annual["Propinsi"].unique().tolist())

        top_left, top_right = st.columns([1.35, 1.1], gap="large", vertical_alignment="top")

        with top_left:
            st.markdown(
                """
                <div class="branding-banner" style="padding:0 !important;">
                    <h1 class="branding-title">Total Kejadian Banjir di Indonesia</h1>
                    <p class="branding-subtitle">Visualisasi Data Interaktif Kejadian Banjir Regional (2000 - 2025)</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with top_right:
            st.markdown(f'<div class="year-badge" style="width: fit-content; margin-left:auto; margin-bottom: 0.5rem;">{year_badge}</div>', unsafe_allow_html=True)

            mode_col, pulau_col, province_col = st.columns([0.9, 0.95, 1.05], gap="small")

            with mode_col:
                col_label("Mode Analisis")
                mode_options = ["Per Tahun", "Rentang Kustom"]
                selected_mode = st.segmented_control(
                    "Mode",
                    options=mode_options,
                    default=st.session_state.timeline_mode
                    if st.session_state.timeline_mode in mode_options
                    else "Per Tahun",
                    label_visibility="collapsed",
                    key="mode_segmented",
                )
                if selected_mode is None:
                    selected_mode = st.session_state.timeline_mode
                if selected_mode != st.session_state.timeline_mode:
                    st.session_state.timeline_mode = selected_mode
                    if selected_mode == "Rentang Kustom":
                        st.session_state.is_playing = False
                    st.rerun()

            with pulau_col:
                col_label("Filter Pulau")
                selected_pulau = st.selectbox(
                    "Pulau",
                    options=PULAU_OPTIONS,
                    index=PULAU_OPTIONS.index(st.session_state.pulau_filter)
                    if st.session_state.pulau_filter in PULAU_OPTIONS else 0,
                    label_visibility="collapsed",
                    key="pulau_filter",
                )

            province_scope = df_prov_annual if selected_pulau == ALL_PULAU_LABEL else df_prov_annual[df_prov_annual["Pulau"] == selected_pulau]
            province_options = sorted(province_scope["Propinsi"].dropna().unique().tolist())

            with province_col:
                col_label("Filter Provinsi")
                selected_provinces = st.multiselect(
                    "Provinsi",
                    options=province_options,
                    default=[],
                    placeholder="Semua Provinsi",
                    label_visibility="collapsed",
                    key="province_filter",
                )

        st.markdown('<div class="section-gap-lg"></div>', unsafe_allow_html=True)

        # ── TIMELINE CONTROLS: FULL WIDTH BELOW ────────────────────────
        with st.container():
            if st.session_state.timeline_mode == "Rentang Kustom":
                col_label("Rentang Tahun")
                year_range = st.slider(
                    "Rentang",
                    min_value=2000,
                    max_value=2025,
                    step=1,
                    key="year_range_slider",
                    label_visibility="collapsed",
                )
                s, e = year_range
            else:
                col_label("Timeline Waktu")
                slider_col, ctrl_col = st.columns([6, 2], gap="large")

                with slider_col:
                    active_year = st.slider(
                        "Tahun",
                        min_value=2000,
                        max_value=2025,
                        step=1,
                        key="year_slider",
                        label_visibility="collapsed",
                    )
                    st.session_state.active_year = active_year
                    s = e = active_year

                with ctrl_col:
                    c1, c2, c3, c4 = st.columns([1, 1, 1, 1.4])
                    with c1:
                        if st.button("«", use_container_width=True, key="btn_back"):
                            st.session_state.is_playing = False
                            st.session_state.pending_year_slider = (
                                max(2000, st.session_state.active_year - 1)
                                if st.session_state.active_year > 2000 else 2025
                            )
                            st.rerun()
                    with c2:
                        is_playing = st.session_state.is_playing
                        if st.button(
                            "❚❚" if is_playing else "▶",
                            type="primary" if is_playing else "secondary",
                            use_container_width=True,
                            key="btn_play",
                        ):
                            st.session_state.is_playing = not is_playing
                            st.rerun()
                    with c3:
                        if st.button("»", use_container_width=True, key="btn_fwd"):
                            st.session_state.is_playing = False
                            st.session_state.pending_year_slider = (
                                st.session_state.active_year + 1
                                if st.session_state.active_year < 2025 else 2000
                            )
                            st.rerun()
        # ── DATA FILTERING ──────────────────────────────────────────────
        df_filtered = df_prov_annual[
            (df_prov_annual["year"] >= s) & (df_prov_annual["year"] <= e)
        ]
        if selected_pulau != ALL_PULAU_LABEL:
            df_filtered = df_filtered[df_filtered["Pulau"] == selected_pulau]
        if selected_provinces:
            df_filtered = df_filtered[df_filtered["Propinsi"].isin(selected_provinces)]

        df_province_summary = (
            df_filtered.groupby("Propinsi")
            .agg(
                total_kejadian=("frekuensi_banjir", "sum"),
                total_area_km2=("total_area_km2", "sum"),
                median_durasi=("median_durasi_hari", "median"),
            )
            .reset_index()
        )

        master_provinces = province_options if (selected_pulau != ALL_PULAU_LABEL or selected_provinces) else provinces_available
        df_master = pd.DataFrame({"Propinsi": master_provinces})
        df_province_summary = pd.merge(df_master, df_province_summary, on="Propinsi", how="left")
        df_province_summary["total_kejadian"] = df_province_summary["total_kejadian"].fillna(0).astype(int)
        df_province_summary["total_area_km2"] = df_province_summary["total_area_km2"].fillna(0.0)
        df_province_summary["median_durasi"] = df_province_summary["median_durasi"].fillna(0.0)

        total_events = int(df_province_summary["total_kejadian"].sum())
        affected_prov_count = int((df_province_summary["total_kejadian"] > 0).sum())

        nonzero = df_province_summary[df_province_summary["total_kejadian"] > 0]
        if len(nonzero) > 0:
            max_row = nonzero.loc[nonzero["total_kejadian"].idxmax()]
            max_prov_name, max_prov_val = max_row["Propinsi"], int(max_row["total_kejadian"])
        else:
            max_prov_name, max_prov_val = "N/A", 0

        # ── KPI CARDS ───────────────────────────────────────────────────
        kc1, kc2, kc3 = st.columns(3)
        with kc1:
            st.markdown(render_kpi_card("Total Kejadian Banjir", f"{total_events:,}", "waves"), unsafe_allow_html=True)
        with kc2:
            st.markdown(render_kpi_card("Provinsi Terdampak", str(affected_prov_count), "map_search"), unsafe_allow_html=True)
        with kc3:
            st.markdown(
                render_kpi_card(f"Kasus Terbanyak ({max_prov_name})", f"{max_prov_val:,}", "flag"),
                unsafe_allow_html=True,
            )

        # ── MAP — NO BORDER & PURE WHITE BACKGROUND ─────────────────────
        if len(df_province_summary) > 0:
            map_col, bar_col = st.columns([1.35, 0.75], gap="large")

            with map_col:
                st.markdown(render_chart_title("map_search", "Peta Distribusi Kejadian Banjir Regional"), unsafe_allow_html=True)

                map_min = int(df_province_summary["total_kejadian"].min()) if len(df_province_summary) > 0 else 0
                map_max = int(df_province_summary["total_kejadian"].max()) if len(df_province_summary) > 0 else 1
                fig_map = create_map(
                    df_province_summary,
                    geojson_data,
                    range_color=(map_min, map_max),
                    zoom_to_selection=(selected_pulau != ALL_PULAU_LABEL or len(selected_provinces) > 0),
                )

                fig_map.update_layout(
                    height=360,
                    margin=dict(l=0, r=0, t=10, b=0),
                    autosize=True,
                    paper_bgcolor="#ffffff",
                    plot_bgcolor="#ffffff"
                )

                st.plotly_chart(
                    fig_map,
                    use_container_width=True,
                    config={"responsive": True, "displayModeBar": False, "scrollZoom": False}
                )

            with bar_col:
                st.markdown(render_chart_title("analytics", "Top 10 Provinsi Kasus Terbanyak"), unsafe_allow_html=True)
                fig_bar = create_bar(df_province_summary)
                fig_bar.update_layout(
                    margin=dict(l=0, r=16, t=8, b=0),
                    paper_bgcolor="#ffffff",
                    plot_bgcolor="#ffffff"
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Tidak ada data spasial untuk filter yang dipilih.")

        st.markdown('<div class="section-gap-lg"></div>', unsafe_allow_html=True)

        # ── LINE — FULL WIDTH BELOW ────────────────────────────────────
        df_line_filtered = df_filtered
        df_yearly_trend = (
            df_line_filtered.groupby("year")
            .agg(total_kejadian=("frekuensi_banjir", "sum"))
            .reset_index()
            .sort_values("year")
        )
        if len(df_yearly_trend) > 0:
            st.markdown(render_chart_title("chart_data", "Tren Kejadian Banjir Tahunan"), unsafe_allow_html=True)
            fig_line = create_line(
                df_yearly_trend,
                st.session_state.active_year,
                st.session_state.timeline_mode,
                s, e,
            )

            fig_line.update_layout(
                margin=dict(l=0, r=16, t=8, b=0),
                paper_bgcolor="#ffffff",
                plot_bgcolor="#ffffff"
            )

            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.markdown(render_chart_title("chart_data", "Tren Kejadian Banjir Tahunan"), unsafe_allow_html=True)
            st.info("Tidak ada data untuk diagram garis tren.")

        st.divider()

        st.markdown(render_chart_title("lightbulb", "Informasi Kunci & Wawasan Data"), unsafe_allow_html=True)

        if len(df_yearly_trend) > 0:
            first_window = df_yearly_trend.head(min(3, len(df_yearly_trend)))['total_kejadian'].mean()
            last_window = df_yearly_trend.tail(min(3, len(df_yearly_trend)))['total_kejadian'].mean()
            if first_window and first_window > 0:
                trend_value = f"{((last_window - first_window) / first_window) * 100:+.0f}%"
                trend_body = "Rata-rata 3 tahun terakhir dibanding 3 tahun awal pada filter terpilih."
            else:
                trend_value = "Stabil"
                trend_body = "Data awal terlalu kecil untuk mengukur eskalasi secara andal."
        else:
            trend_value = "N/A"
            trend_body = "Tidak ada data tren untuk filter terpilih."

        recommendation_value = selected_pulau if selected_pulau != ALL_PULAU_LABEL else "Prioritas Jawa"

        insight_cols = st.columns(4)
        with insight_cols[0]:
            st.markdown(render_insight_card("🚨", "Total Beban Risiko", f"{total_events:,}", "Akumulasi kejadian banjir pada wilayah dan rentang waktu yang dipilih."), unsafe_allow_html=True)
        with insight_cols[1]:
            st.markdown(render_insight_card("📍", "Konsentrasi Geografis", max_prov_name, f"Provinsi dengan kejadian tertinggi: {max_prov_val:,} kasus."), unsafe_allow_html=True)
        with insight_cols[2]:
            st.markdown(render_insight_card("📈", "Tren Eskalasi", trend_value, trend_body), unsafe_allow_html=True)
        with insight_cols[3]:
            st.markdown(render_insight_card("💡", "Rekomendasi", recommendation_value, "Fokus pada zona dengan kejadian tertinggi, lalu turun ke level provinsi untuk mitigasi spesifik."), unsafe_allow_html=True)

        # ── PLAYBACK LOOP ───────────────────────────────────────────────
        if st.session_state.is_playing and st.session_state.timeline_mode == "Per Tahun":
            time.sleep(0.7)
            next_year = st.session_state.active_year + 1
            if next_year > 2025:
                next_year = 2000
            st.session_state.pending_year_slider = next_year
            st.rerun()

    render_dashboard()