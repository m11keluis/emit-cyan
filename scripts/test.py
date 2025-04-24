from pathlib import Path
from scripts.modules.query_emit import query_and_download_emit
from scripts.modules.query_cyan import download_cyan_data
from scripts.modules.process_emit_granule import process_emit_granule
from scripts.modules.process_cyan_granule import process_cyan_granule
import matplotlib.pyplot as plt

# Define bounding box for region of interest
N, S, E, W = 42.579491, 42.235078, -121.785509, -122.105267
bbox = (W, S, E, N)

start = "2024-07-24"
end = "2024-07-26"

# Query and download
emit_files = query_and_download_emit(bbox, start, end, "../data")
cyan_files = download_cyan_data(emit_files[0], bbox, output_dir="../data")

# Process the latest matching EMIT and CyAN granules
emit_path = Path("/Users/kluis/PycharmProjects/emit-cyan/data/emit") / Path(emit_files[0]).name
cyan_path = Path("/Users/kluis/PycharmProjects/emit-cyan/data/cyan") / Path(cyan_files[0]).name

cyan_path = "/Users/kluis/PycharmProjects/emit-cyan/data/cyan/L2024207.L3m_DAY_CYAN_CI_cyano_CYAN_CONUS_300m_1_2.tif"

import rioxarray as rxr
cyan_da = rxr.open_rasterio(cyan_path).squeeze()

emit_ds = process_emit_granule(emit_path, bounds=bbox)
cyan_ds = process_cyan_granule(cyan_path, bounds=bbox)

# Plot comparison
def plot_emit_cyan_comparison(
    emit_da,
    cyan_da,
    title_prefix=None,
    output_path="figures/emit_vs_cyan.png",
    target_wavelength_nm=620
):
    """
    Plot EMIT reflectance vs. CyAN CI side-by-side.

    Parameters:
    - emit_da: xarray Dataset with 'reflectance' and 'wavelengths'
    - cyan_da: xarray DataArray of CI values
    - target_wavelength_nm: optional int/float (default: 620) for plotting diagnostic EMIT band
    """
    print(f"📊 Plotting EMIT (closest to {target_wavelength_nm} nm) and CyAN CI...")

    # Select band closest to target wavelength
    wavelengths = emit_da['wavelengths'].values
    target_band_index = (abs(wavelengths - target_wavelength_nm)).argmin()
    emit_plot = emit_da.isel(band=target_band_index)

    print(f"🎯 Using EMIT band index {target_band_index} at ~{wavelengths[target_band_index]:.1f} nm")

    fig, axs = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

    vmin = min(float(emit_plot.min()), float(cyan_da.min()))
    vmax = max(float(emit_plot.max()), float(cyan_da.max()))

    emit_plot.plot(ax=axs[0], vmin=vmin, vmax=vmax, cmap="viridis")
    axs[0].set_title(f"{title_prefix or ''}EMIT Reflectance ~{wavelengths[target_band_index]:.0f} nm")

    cyan_da.plot(ax=axs[1], vmin=vmin, vmax=vmax, cmap="viridis")
    axs[1].set_title(f"{title_prefix or ''}CyAN CI")

    for ax in axs:
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

    plt.savefig(output_path, dpi=300)
    print(f"✅ Comparison plot saved: {output_path}")
    plt.close()

plot_emit_cyan_comparison(
    emit_da=emit_ds['reflectance'],
    cyan_da=cyan_ds,
    title_prefix="2024-07-25 – ",
    output_path="figures/emit_vs_cyan_20240725.png",
    target_wavelength_nm=620

)
