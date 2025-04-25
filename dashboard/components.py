import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import streamlit as st

@st.cache_data
def summarize_data(_da: xr.DataArray):
    valid = _da.where(np.isfinite(_da), drop=True)
    return {
        "min": float(valid.min()),
        "max": float(valid.max()),
        "mean": float(valid.mean()),
        "std": float(valid.std())
    }

def plot_dual_maps(emit_da: xr.DataArray, cyan_da: xr.DataArray, band_nm=620):
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    emit_band = emit_da.sel(wavelengths=band_nm, method="nearest")
    emit_band = emit_band.where(emit_da.land_mask == 1).where(emit_band > 0)

    cyan_data = cyan_da["band_data"]

    vmin, vmax = 0.01, 0.03
    cyan_vmin, cyan_vmax = 0.01, 0.03
    cmap = "RdYlGn_r"

    emit_band['reflectance'].plot(ax=axs[0], cmap=cmap, vmin=vmin, vmax=vmax, add_colorbar=False)
    axs[0].set_title(f"EMIT Reflectance ~{band_nm} nm")
    axs[0].set_xticks([])
    axs[0].set_yticks([])

    cyan_data.plot(ax=axs[1], cmap=cmap, vmin=cyan_vmin, vmax=cyan_vmax, add_colorbar=False)
    axs[1].set_title("CyAN CI")
    axs[1].set_xticks([])
    axs[1].set_yticks([])

    plt.tight_layout()
    return fig

def display_summary_table(label: str, stats: dict):
    st.subheader(label)
    st.metric("Min", f"{stats['min']:.4f}")
    st.metric("Max", f"{stats['max']:.4f}")
    st.metric("Mean", f"{stats['mean']:.4f}")
    st.metric("Std. Dev.", f"{stats['std']:.4f}")
