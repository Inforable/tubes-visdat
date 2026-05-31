import streamlit as st
import pandas as pd
import json
import urllib.request
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"

ALL_PULAU_LABEL = "Semua Pulau"
PULAU_OPTIONS = [
    ALL_PULAU_LABEL,
    "Sumatera",
    "Jawa",
    "Kalimantan",
    "Sulawesi",
    "Bali & Nusa Tenggara",
    "Maluku",
    "Papua",
]

PROVINCE_TO_PULAU = {
    "DI. ACEH": "Sumatera",
    "SUMATERA UTARA": "Sumatera",
    "SUMATERA BARAT": "Sumatera",
    "RIAU": "Sumatera",
    "JAMBI": "Sumatera",
    "SUMATERA SELATAN": "Sumatera",
    "BENGKULU": "Sumatera",
    "LAMPUNG": "Sumatera",
    "DKI JAKARTA": "Jawa",
    "JAWA BARAT": "Jawa",
    "JAWA TENGAH": "Jawa",
    "DAERAH ISTIMEWA YOGYAKARTA": "Jawa",
    "JAWA TIMUR": "Jawa",
    "PROBANTEN": "Jawa",
    "BALI": "Bali & Nusa Tenggara",
    "NUSATENGGARA BARAT": "Bali & Nusa Tenggara",
    "NUSA TENGGARA BARAT": "Bali & Nusa Tenggara",
    "NUSA TENGGARA TIMUR": "Bali & Nusa Tenggara",
    "KALIMANTAN BARAT": "Kalimantan",
    "KALIMANTAN TENGAH": "Kalimantan",
    "KALIMANTAN SELATAN": "Kalimantan",
    "KALIMANTAN TIMUR": "Kalimantan",
    "SULAWESI UTARA": "Sulawesi",
    "SULAWESI TENGAH": "Sulawesi",
    "SULAWESI SELATAN": "Sulawesi",
    "SULAWESI TENGGARA": "Sulawesi",
    "GORONTALO": "Sulawesi",
    "MALUKU": "Maluku",
    "MALUKU UTARA": "Maluku",
    "IRIAN JAYA BARAT": "Papua",
    "IRIAN JAYA TENGAH": "Papua",
    "IRIAN JAYA TIMUR": "Papua",
    "PAPUA": "Papua",
}


def clean_province_name(name):
    if pd.isna(name):
        return name
    cleaned = re.sub(r"\s+[O0]$", "", str(name).strip())
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def add_island_mapping(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Propinsi"] = df["Propinsi"].apply(clean_province_name)
    df["Pulau"] = df["Propinsi"].map(PROVINCE_TO_PULAU).fillna("Lainnya")
    return df

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
    df_prov_annual = add_island_mapping(df_prov_annual)
    
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
