
import os
import ssl
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patheffects as pe
from matplotlib.colors import LinearSegmentedColormap
import contextily as ctx

# --- SSL fix for some environments ---
ssl._create_default_https_context = ssl._create_unverified_context

# --- COLOR CONFIG (light vectorized editorial theme) ---
BACKGROUND_COLOR = "#F8FAFC"
OCEAN_COLOR = "#F1F5F9"
BORDER_COLOR = "#CBD5E1"
TEXT_COLOR = "#0F172A"
ACCENT_COLOR = "#0284C7"
SUBTITLE_COLOR = "#475569"


# =========================
# DATA LOADING
# =========================
def load_data(current_dir: str):
    url_prov = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province-simple.json"
    print("Loading GeoJSON...")
    prov_map = gpd.read_file(url_prov)

    csv_path = os.path.join(current_dir, "..", "data", "processed", "banjir_konsolidasi_provinsi.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    print("Loading CSV...")
    df_banjir = pd.read_csv(csv_path)

    return prov_map, df_banjir


def merge_data(prov_map: gpd.GeoDataFrame, df_banjir: pd.DataFrame):
    merged = prov_map.merge(df_banjir, on="Propinsi", how="left")
    merged["total_kejadian"] = merged["total_kejadian"].fillna(0)
    return merged


# =========================
# COLORMAP (GRADIENT STYLE)
# =========================
def build_colormap(values: pd.Series):
    vmin = values.min()
    vmax = values.max()

    # Menggunakan gradient warna biru yang mulus (Light Blue -> Dark Navy)
    cmap = plt.get_cmap("Blues")

    # Improve contrast for skewed data
    norm = mcolors.PowerNorm(gamma=0.6, vmin=vmin, vmax=vmax)

    return cmap, norm


# =========================
# MAP DRAWING (TERRAIN STYLE)
# =========================
def draw_map(ax, merged, cmap, norm):
    merged_web = merged.to_crs(epsg=3857)

    # fix extent
    xmin, ymin, xmax, ymax = merged_web.total_bounds
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # basemap vektor terang tanpa label (hanya jalan & batas wilayah)
    ctx.add_basemap(
        ax,
        source=ctx.providers.CartoDB.PositronNoLabels,
        zoom=5,
        alpha=0.8, 
        zorder=1
    )

    # borders (dihilangkan agar transisi antar daerah terlihat lebih mulus/gradient)
    # merged_web.boundary.plot(
    #     ax=ax,
    #     edgecolor="#64748B",
    #     linewidth=0.3,
    #     zorder=3
    # )

    # heatmap (lapisan warna banjir)
    merged_web.plot(
        column="total_kejadian",
        ax=ax,
        cmap=cmap,
        norm=norm,
        alpha=0.85,  # Solid enough to show the colors clearly
        edgecolor="none", # Hilangkan border agar warna nge-blend secara visual
        linewidth=0,
        zorder=4
    )


# =========================
# LABELS
# =========================
def draw_labels(ax, merged):
    merged_web = merged.to_crs(epsg=3857)

    top_n = merged_web.nlargest(8, "total_kejadian")

    for _, row in top_n.iterrows():
        centroid = row.geometry.centroid

        label = row["Propinsi"]
        if len(label) > 12:
            label = label.replace(" ", "\n")

        ax.annotate(
            label,
            xy=(centroid.x, centroid.y),
            fontsize=5,
            color=TEXT_COLOR,
            ha="center",
            va="center",
            fontfamily="monospace",
            path_effects=[
                pe.withStroke(linewidth=2, foreground=BACKGROUND_COLOR)
            ],
            zorder=5
        )


# =========================
# COLORBAR
# =========================
def draw_colorbar(fig, ax, cmap, norm, vmax):
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    cbar = fig.colorbar(
        sm,
        ax=ax,
        orientation="horizontal",
        fraction=0.025,
        pad=0.02,
        aspect=40,
        shrink=0.45,
        location="bottom",
    )

    cbar.ax.tick_params(
        color=SUBTITLE_COLOR,
        labelsize=7,
        labelcolor=SUBTITLE_COLOR
    )

    cbar.outline.set_edgecolor(BORDER_COLOR)
    cbar.ax.set_facecolor(BACKGROUND_COLOR)

    ticks = np.linspace(0, vmax, 5)
    cbar.set_ticks(ticks)
    cbar.set_ticklabels([f"{int(t):,}" for t in ticks])


# =========================
# ANNOTATIONS
# =========================
def draw_annotations(ax, merged):
    total = int(merged["total_kejadian"].sum())
    provinces = int((merged["total_kejadian"] > 0).sum())

    ax.text(
        0.99, 0.04,
        f"Total kejadian: {total:,}\nProvinsi terdampak: {provinces}",
        transform=ax.transAxes,
        fontsize=7,
        color=SUBTITLE_COLOR,
        ha="right",
        va="bottom",
        fontfamily="monospace"
    )

    ax.text(
        0.01, 0.02,
        "Sumber: BNPB (processed)",
        transform=ax.transAxes,
        fontsize=6,
        color=SUBTITLE_COLOR,
        ha="left",
        va="bottom",
        fontfamily="monospace"
    )


# =========================
# MAIN
# =========================
def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    prov_map, df_banjir = load_data(current_dir)
    merged = merge_data(prov_map, df_banjir)

    cmap, norm = build_colormap(merged["total_kejadian"])

    # --- FIGURE SETUP ---
    fig = plt.figure(figsize=(20, 10), facecolor=BACKGROUND_COLOR)

    ax_title = fig.add_axes([0.0, 0.82, 1.0, 0.16])
    ax_title.set_facecolor(BACKGROUND_COLOR)
    ax_title.axis("off")

    ax_map = fig.add_axes([0.02, 0.04, 0.96, 0.80])
    ax_map.set_facecolor(OCEAN_COLOR)

    # --- TITLE ---
    ax_title.text(
        0.5, 0.75,
        "PETA BANJIR INDONESIA",
        fontsize=26,
        color=TEXT_COLOR,
        ha="center",
        fontweight="bold",
        fontfamily="serif"
    )

    ax_title.text(
        0.5, 0.30,
        "Distribusi Kejadian Banjir per Provinsi (2000–2026)",
        fontsize=11,
        color=SUBTITLE_COLOR,
        ha="center",
        fontfamily="monospace"
    )

    ax_title.axhline(
        y=0.05,
        xmin=0.2,
        xmax=0.8,
        color=ACCENT_COLOR,
        linewidth=1
    )

    # --- DRAW MAP ---
    draw_map(ax_map, merged, cmap, norm)
    # Label daerah dihilangkan sesuai permintaan:
    # draw_labels(ax_map, merged)
    draw_colorbar(fig, ax_map, cmap, norm, merged["total_kejadian"].max())
    draw_annotations(ax_map, merged)

    ax_map.set_axis_off()

    # --- OUTPUT ---
    png_path = os.path.join(current_dir, "peta_banjir_terrain.png")
    pdf_path = os.path.join(current_dir, "peta_banjir_terrain.pdf")

    plt.savefig(
        png_path,
        dpi=300,
        bbox_inches="tight",
        facecolor=BACKGROUND_COLOR,
        pad_inches=0.3
    )

    plt.savefig(
        pdf_path,
        format="pdf",
        bbox_inches="tight",
        facecolor=BACKGROUND_COLOR,
        pad_inches=0.3
    )

    print(f"Saved PNG: {png_path}")
    print(f"Saved PDF: {pdf_path}")

    plt.close()


if __name__ == "__main__":
    main()