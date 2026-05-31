import streamlit as st
import pandas as pd
import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"

# ==============================================================================
# DATA LOADING & CACHING (EXCLUDING 2026)
# ==============================================================================
@st.cache_data
def load_data():
    # Load aggregated province & annual datasets
    df_prov_annual = pd.read_csv(DATA_DIR / "banjir_provinsi_tahunan.csv")
    df_trend_global = pd.read_csv(DATA_DIR / "trend_banjir_indonesia_2000_2026.csv")
    
    # ⚠️ CRITICAL: Exclude 2026 entirely as per user feedback
    df_prov_annual = df_prov_annual[df_prov_annual['year'] < 2026]
    df_trend_global = df_trend_global[df_trend_global['year'] < 2026]
    
    return df_prov_annual, df_trend_global

# Indonesian Province GeoJSON boundary maps URL
GEOJSON_URL = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province-simple.json"
LOCAL_GEOJSON_PATH = DATA_DIR / "indonesia_province_simple.geojson"

@st.cache_data
def load_geojson():
    """Loads and caches the Indonesian Province GeoJSON dict once from the URL to optimize map rendering performance."""
    try:
        req = urllib.request.Request(
            GEOJSON_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception:
        # Fallback to local file if network/SSL blocks remote GeoJSON access.
        try:
            with LOCAL_GEOJSON_PATH.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # Return empty dictionary only when both remote and local sources fail.
            return {}
