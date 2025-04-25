import streamlit as st
import xarray as xr
import numpy as np
from pathlib import Path
import sys
import os

# Make sure 'scripts' can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.modules.process_emit_granule import process_emit_granule
from scripts.modules.process_cyan_granule import process_cyan_granule

from components import (
    summarize_data,
    plot_dual_maps,
    display_summary_table
)

# --- Load data ---
@st.cache_data
def load_data(wavelength_nm):
    emit_path = Path("data/emit/EMIT_L2A_RFL_001_20240725T230728_2420715_006.nc")
    cyan_path = Path("data/cyan/L2024207.L3m_DAY_CYAN_CI_cyano_CYAN_CONUS_300m.tif")

    # Load full reflectance dataset
    emit_ds = process_emit_granule(emit_path)

    cyan_ds = process_cyan_granule(cyan_path)

    return emit_ds, cyan_ds

# --- Sidebar controls ---
st.sidebar.title("🛰️ CyAN-EMIT Dashboard")
st.sidebar.markdown("### 📅 Date")
st.sidebar.markdown("2024-07-25")

layer_choice = st.sidebar.radio("Select Layer to View:", ["EMIT Reflectance", "CyAN CI"])
wavelength_nm = st.sidebar.slider("Wavelength (nm)", 400, 900, 620, step=5)

# --- Main logic ---
st.title("Upper Klamath Lake: CyAN vs EMIT Comparison")

emit_band, cyan_da = load_data(wavelength_nm)

# --- Plotting ---
fig = plot_dual_maps(emit_band, cyan_da, band_nm=wavelength_nm)
st.pyplot(fig)

# --- Summary stats ---
st.markdown("### 🔍 Summary Statistics")
col3, col4 = st.columns(2)

with col3:
    emit_stats = summarize_data(emit_band)
    display_summary_table("EMIT Reflectance", emit_stats)

with col4:
    cyan_stats = summarize_data(cyan_da["band_data"])
    display_summary_table("CyAN CI", cyan_stats)

st.markdown("\n---\n*Interactive pixel inspection coming soon...*")
