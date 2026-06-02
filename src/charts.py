import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _iter_lon_lat_pairs(coordinates):
    if not coordinates:
        return

    first_item = coordinates[0]
    if isinstance(first_item, (int, float)):
        yield coordinates[0], coordinates[1]
        return

    for nested_coordinates in coordinates:
        yield from _iter_lon_lat_pairs(nested_coordinates)


def _geojson_centroid(geometry):
    points = list(_iter_lon_lat_pairs(geometry.get("coordinates", [])))
    if not points:
        return None

    lon = sum(point[0] for point in points) / len(points)
    lat = sum(point[1] for point in points) / len(points)
    return lon, lat


def create_map(df_province_summary, geojson_data, range_color=None):
    custom_navy_scale = [
        [0.0, "#f8fafc"],
        [0.00001, "#dbeafe"],
        [0.2, "#93c5fd"],
        [0.5, "#3b82f6"],
        [0.8, "#1d4ed8"],
        [1.0, "#1e3a8a"],
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
        hover_name="Propinsi",
        custom_data=["Propinsi", "total_area_km2"],
    )

    fig_map.update_geos(
        projection_type="mercator",
        visible=False,
        showcoastlines=False,
        showcountries=False,
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
        lonaxis_range=[94.0, 142.0],
        lataxis_range=[-11.5, 8.5],
    )

    fig_map.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="closest",
        uirevision="constant",
        margin={"r": 0, "t": 10, "l": 0, "b": 10},
        coloraxis_colorbar=dict(
            orientation="h",
            y=-0.15,
            x=0.5,
            xanchor="center",
            title=dict(
                text="Tingkat Kejadian Banjir",
                side="top",
                font=dict(color="#475569", size=10),
            ),
            tickfont=dict(color="#475569", size=9),
            thickness=10,
            len=0.7,
        ),
    )

    fig_map.update_traces(
        marker_line_color="#cbd5e1",
        marker_line_width=0.6,
        hoverinfo="skip",
    )

    if not df_province_summary.empty and geojson_data:
        province_lookup = df_province_summary.set_index("Propinsi")
        centroid_rows = []

        for feature in geojson_data.get("features", []):
            province_name = feature.get("properties", {}).get("Propinsi")
            if province_name not in province_lookup.index:
                continue

            centroid = _geojson_centroid(feature.get("geometry", {}))
            if centroid is None:
                continue

            province_row = province_lookup.loc[province_name]
            centroid_rows.append(
                {
                    "Propinsi": province_name,
                    "lon": centroid[0],
                    "lat": centroid[1],
                    "total_kejadian": province_row["total_kejadian"],
                    "total_area_km2": province_row["total_area_km2"],
                }
            )

        if centroid_rows:
            centroid_df = pd.DataFrame(centroid_rows)
            fig_map.add_trace(
                go.Scattergeo(
                    lon=centroid_df["lon"],
                    lat=centroid_df["lat"],
                    mode="markers",
                    marker=dict(size=14, color="rgba(0,0,0,0.01)"),
                    customdata=centroid_df[["total_kejadian", "total_area_km2"]],
                    text=centroid_df["Propinsi"],
                    hovertemplate="Provinsi: %{text}<br>Total Kejadian: %{customdata[0]:,} kasus<br>Luas Area Banjir: %{customdata[1]:,.1f} km²<extra></extra>",
                    showlegend=False,
                )
            )

    return fig_map


def create_bar(df_province_summary):
    df_top10 = (
        df_province_summary[df_province_summary["total_kejadian"] > 0]
        .nlargest(10, "total_kejadian")
        .sort_values(by="total_kejadian", ascending=True)
    )

    fig_bar = px.bar(
        df_top10,
        x="total_kejadian",
        y="Propinsi",
        orientation="h",
        text="total_kejadian",
        labels={"total_kejadian": "Total Kejadian", "Propinsi": "Provinsi"},
        hover_name="Propinsi",
        custom_data=["Propinsi"],
    )
    fig_bar.update_traces(
        marker_color="#2563eb",
        marker_line_color="#1d4ed8",
        marker_line_width=1.5,
        opacity=0.95,
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="Provinsi: %{y}<br>Total Kejadian: %{x:,} kasus<extra></extra>",
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#2563eb",
            font_size=13,
            font_family="Inter, system-ui, -apple-system, sans-serif",
            font_color="#0f172a",
            align="left",
        ),
    )

    fig_bar.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#0f172a",
        hovermode="closest",
        uirevision="constant",
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
            tickfont=dict(color="#334155", weight="bold"),
        ),
    )

    return fig_bar


def create_line(df_yearly_trend, active_year, timeline_mode, start_year, end_year):
    fig_line = px.line(
        df_yearly_trend,
        x="year",
        y="total_kejadian",
        labels={"total_kejadian": "Kejadian Banjir", "year": "Tahun"},
        custom_data=["year"],
    )

    fig_line.update_traces(
        line=dict(color="#3b82f6", width=3, shape="spline"),
        mode="lines+markers",
        marker=dict(color="#ffffff", size=6, line=dict(color="#2563eb", width=2)),
        fill="tozeroy",
        fillcolor="rgba(37, 99, 235, 0.06)",
        hovertemplate="Tahun %{x}<br>Total Kejadian: %{y:,} kasus<extra></extra>",
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#2563eb",
            font_size=13,
            font_family="Inter, system-ui, -apple-system, sans-serif",
            font_color="#0f172a",
            align="left",
        ),
    )

    if timeline_mode == "Per Tahun" and len(df_yearly_trend) > 0:
        window_min = max(start_year, active_year - 2)
        window_max = min(end_year, active_year + 2)
        df_window = df_yearly_trend[
            (df_yearly_trend["year"] >= window_min) & (df_yearly_trend["year"] <= window_max)
        ]

        if len(df_window) > 0:
            fig_line.add_trace(
                go.Scatter(
                    x=df_window["year"],
                    y=df_window["total_kejadian"],
                    mode="lines+markers",
                    name="Jendela 5 Tahun",
                    line=dict(color="#1d4ed8", width=5, shape="spline"),
                    marker=dict(color="#ffffff", size=8, line=dict(color="#1d4ed8", width=2.5)),
                    hovertemplate="Tahun %{x}<br>Total Kejadian: %{y:,} kasus<extra></extra>",
                    showlegend=False,
                )
            )

            fig_line.add_vrect(
                x0=window_min,
                x1=window_max,
                fillcolor="rgba(37, 99, 235, 0.06)",
                line_width=0,
                layer="below",
            )

    if timeline_mode == "Animasi (Play)":
        fig_line.add_vline(
            x=active_year,
            line_width=2,
            line_dash="dash",
            line_color="#2563eb",
            annotation_text=f"Tahun {active_year}",
            annotation_position="top left",
            annotation_font=dict(color="#2563eb", size=11, family="Inter"),
        )

    fig_line.update_layout(
        height=560,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#0f172a",
        hovermode="x",
        hoverdistance=20,
        uirevision="constant",
        margin={"r": 15, "t": 15, "l": 15, "b": 15},
        xaxis=dict(
            title="Tahun",
            title_font=dict(color="#475569", size=11),
            tickfont=dict(color="#475569"),
            gridcolor="#e2e8f0",
            dtick=2 if (end_year - start_year) > 10 or timeline_mode == "Animasi (Play)" else 1,
            zeroline=False,
        ),
        yaxis=dict(
            title="Frekuensi Kejadian",
            title_font=dict(color="#475569", size=11),
            tickfont=dict(color="#475569"),
            gridcolor="#e2e8f0",
            zeroline=False,
        ),
    )

    return fig_line
