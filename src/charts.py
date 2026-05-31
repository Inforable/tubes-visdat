import plotly.express as px

# ==============================================================================
# PREMIUM GEOSPATIAL MAP GENERATOR (OPTIMIZED FOR REAL-TIME STREAMING)
# ==============================================================================
def create_map(df_province_summary, geojson_data, range_color=None, zoom_to_selection=False):
    """
    Returns fig_map configured with:
    - Pre-parsed cached GeoJSON data to ensure extremely fast render loop.
    - Premium slate-to-navy sequential color scale.
    - Transparent background.
    - Horizontal custom colorbar.
    - Custom HTML hover tooltips.
    - stable uirevision to avoid resetting zoom and pan coordinates when dragging.
    """
    # Premium sequential scale from clean off-white (#f8fafc) up to deep navy (#1e3a8a)
    custom_navy_scale = [
        [0.0, "#f8fafc"],      # Clean off-white for exactly 0 occurrences (dry/safe land)
        [0.00001, "#dbeafe"],  # Extremely soft light blue for starting cases
        [0.2, "#93c5fd"],      # Light blue
        [0.5, "#3b82f6"],      # Vibrant royal blue
        [0.8, "#1d4ed8"],      # Medium navy blue
        [1.0, "#1e3a8a"]       # Deep navy blue highlight
    ]
    
    if df_province_summary.empty:
        range_color = range_color or (0, 1)
    elif range_color is None:
        min_val = int(df_province_summary["total_kejadian"].min())
        max_val = int(df_province_summary["total_kejadian"].max())
        if max_val <= min_val:
            max_val = min_val + 1
        range_color = (min_val, max_val)
    else:
        min_val, max_val = range_color
        if max_val <= min_val:
            range_color = (min_val, min_val + 1)
    
    fig_map = px.choropleth(
        df_province_summary,
        geojson=geojson_data,
        locations="Propinsi",
        featureidkey="properties.Propinsi",
        color="total_kejadian",
        color_continuous_scale=custom_navy_scale,
        range_color=range_color,
        hover_data=["Propinsi", "total_area_km2"]
    )

    geos_kwargs = dict(
        projection_type="mercator",
        visible=False,
        showcoastlines=False,
        showcountries=False,
        showframe=False,
        bgcolor="rgba(0,0,0,0)"
    )
    if zoom_to_selection:
        geos_kwargs["fitbounds"] = "locations"
    else:
        geos_kwargs["lonaxis_range"] = [94.0, 142.0]
        geos_kwargs["lataxis_range"] = [-11.0, 8.0]

    fig_map.update_geos(**geos_kwargs)
    
    fig_map.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        uirevision="constant",  # 🔒 CRITICAL: Keeps zoom/pan locked during real-time dragging!
        margin={"r": 0, "t": 10, "l": 0, "b": 10},
        coloraxis_colorbar=dict(
            orientation="h",
            y=-0.15,
            x=0.5,
            xanchor="center",
            title=dict(
                text="Tingkat Kejadian Banjir",
                side="top",
                font=dict(color="#475569", size=10)
            ),
            tickfont=dict(color="#475569", size=9),
            thickness=10,
            len=0.7
        )
    )
    
    fig_map.update_traces(
        marker_line_color="#cbd5e1",  # Crisp border to distinguish adjacent/inactive provinces
        marker_line_width=0.6,
        hovertemplate="<span style='font-size: 14px; font-weight: bold; color: #2563eb;'>%{customdata[0]}</span><br><br>" +
                      "Total Kejadian: <b>%{z:,}</b> kasus<br>" +
                      "Luas Area Banjir: <b>%{customdata[1]:,.1f}</b> km²<extra></extra>",
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#2563eb",
            font_size=13,
            font_family="Inter, system-ui, -apple-system, sans-serif",
            font_color="#0f172a",
            align="left"
        )
    )
    
    return fig_map

# ==============================================================================
# TOP 10 HORIZONTAL BAR CHART GENERATOR (WITH LABELS & INSTANT FEEDBACK)
# ==============================================================================
def create_bar(df_province_summary):
    """
    Returns fig_bar configured with:
    - Sort & selection of top 10 provinces.
    - Exact event numbers rendered on each bar label (outside).
    - Royal blue horizontal bars.
    - Custom hover tooltips.
    - Soft slate gridlines.
    - stable uirevision to avoid redraw flashes.
    """
    df_top10 = (
        df_province_summary[df_province_summary["total_kejadian"] > 0]
        .nlargest(10, "total_kejadian")
        .sort_values(by="total_kejadian", ascending=True)
    )
    
    fig_bar = px.bar(
        df_top10,
        x="total_kejadian",
        y="Propinsi",
        orientation='h',
        text="total_kejadian",  # 🏷️ CRITICAL: Sets the bar text source to display values directly!
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
        marker_line_color='#1d4ed8',
        marker_line_width=1.5,
        opacity=0.95,
        texttemplate='%{text:,}',     # 🏷️ Beautiful thousands separators formatting
        textposition='outside',        # 🏷️ Places labels on the outside right of bars
        cliponaxis=False,              # 🚫 Prevents labels from being cropped by axis limits!
        hovertemplate="<span style='font-size: 14px; font-weight: bold; color: #2563eb;'>%{y}</span><br><br>" +
                      "Total Kejadian: <b>%{x:,}</b> kasus<extra></extra>",
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#2563eb",
            font_size=13,
            font_family="Inter, system-ui, -apple-system, sans-serif",
            font_color="#0f172a",
            align="left"
        )
    )
    
    fig_bar.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#0f172a",
        uirevision="constant",  # 🔒 CRITICAL: Keeps interactions locked during real-time updates!
        margin={"r": 50, "t": 15, "l": 15, "b": 15},
        xaxis=dict(
            title="Total Kejadian",
            title_font=dict(color="#475569", size=11),
            tickfont=dict(color="#475569"),
            gridcolor="#e2e8f0",
            zeroline=False,
            range=[0, max(1, int(df_top10["total_kejadian"].max())) * 1.15] if len(df_top10) > 0 else None,
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color="#334155", weight="bold")
        )
    )
    
    return fig_bar

# ==============================================================================
# ANNUAL LINE CHART GENERATOR (WITH DYNAMIC FILL & MARKERS)
# ==============================================================================
def create_line(df_yearly_trend, active_year, timeline_mode, start_year, end_year):
    """
    Returns fig_line configured with:
    - Custom smooth splines and filled blue markers.
    - Soft underfill.
    - Vertical dashed guidance indicator if timeline_mode is animation.
    - stable uirevision to avoid layout jumps on slider drags.
    """
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
        fillcolor='rgba(37, 99, 235, 0.06)',
        hovertemplate="<span style='font-size: 14px; font-weight: bold; color: #2563eb;'>Tahun %{x}</span><br><br>" +
                      "Total Kejadian: <b>%{y:,}</b> kasus<extra></extra>",
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#2563eb",
            font_size=13,
            font_family="Inter, system-ui, -apple-system, sans-serif",
            font_color="#0f172a",
            align="left"
        )
    )
    
    # If in animation mode, add an elegant vertical dashed line indicating the active year
    if timeline_mode == "Animasi (Play)":
        fig_line.add_vline(
            x=active_year,
            line_width=2,
            line_dash="dash",
            line_color="#2563eb",
            annotation_text=f"Tahun {active_year}",
            annotation_position="top left",
            annotation_font=dict(color="#2563eb", size=11, family="Inter")
        )
    
    fig_line.update_layout(
        height=560,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#0f172a",
        uirevision="constant",  # 🔒 CRITICAL: Keeps interactions locked during real-time updates!
        margin={"r": 15, "t": 15, "l": 15, "b": 15},
        xaxis=dict(
            title="Tahun",
            title_font=dict(color="#475569", size=11),
            tickfont=dict(color="#475569"),
            gridcolor="#e2e8f0",
            dtick=2 if (end_year - start_year) > 10 or timeline_mode == "Animasi (Play)" else 1,
            zeroline=False
        ),
        yaxis=dict(
            title="Frekuensi Kejadian",
            title_font=dict(color="#475569", size=11),
            tickfont=dict(color="#475569"),
            gridcolor="#e2e8f0",
            zeroline=False
        )
    )
    
    return fig_line
