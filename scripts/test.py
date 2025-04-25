from pathlib import Path
from scripts.modules.query_emit import query_and_download_emit
from scripts.modules.query_cyan import download_cyan_data
from scripts.modules.process_emit_granule import process_emit_granule
from scripts.modules.process_cyan_granule import process_cyan_granule
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import matplotlib.pyplot as plt
import xarray as xr

# Bounding box and date of interest
N, S = 42.579491, 42.235078
W, E = -122.105267, -121.785509
bbox = (W, S, E, N)
start = "2024-07-24"
end = "2024-07-26"

# Query EMIT and CyAN data
emit_files = query_and_download_emit(bbox, start, end, "../data")

# Use the first EMIT file to trigger CyAN download
cyan_tiles = download_cyan_data(emit_files[0], bounds=bbox, output_dir="../data/cyan")

# Process EMIT file
emit_ds = process_emit_granule(emit_files[0], bounds=bbox)
cyan_ds = process_cyan_granule(cyan_tiles[0], bounds=bbox)


#e

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import xarray as xr
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm


def plot_emit_cyan_comparison(emit_ds, cyan_da, wavelength_nm=620, output_path="figures/emit_vs_cyan_clean.png", title_prefix=""):
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    emit_native = emit_ds['reflectance'].sel(wavelengths=wavelength_nm, method='nearest')
    emit_native = emit_native.where(emit_ds.land_mask == 1).where(emit_native > 0)

    # Adjust color scale ranges
    reflectance_vmin, reflectance_vmax = 0.01, 0.03
    ci_vmin, ci_vmax = 0.0, 0.025  # tighter CI range for contrast
    shared_cmap = cm.get_cmap("RdYlGn_r")  # same for both for visual alignment

    fig, axs = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

    # EMIT native plot
    emit_native.plot(ax=axs[0], cmap=shared_cmap, vmin=reflectance_vmin, vmax=reflectance_vmax, add_colorbar=False)
    axs[0].set_title(f"{title_prefix}EMIT Reflectance @ 620 nm", fontsize=14, weight="bold")

    # CyAN CI plot
    cyan_da["band_data"].plot(ax=axs[1], cmap=shared_cmap, vmin=ci_vmin, vmax=ci_vmax, add_colorbar=False)
    axs[1].set_title(f"{title_prefix}CyAN CI", fontsize=14, weight="bold")

    # Clean up axes
    for ax in axs:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")

    plt.savefig(output_path, dpi=600)
    plt.close()
    print(f"✅ Saved cleaned plot to: {output_path}")

plot_emit_cyan_comparison(emit_ds, cyan_ds, wavelength_nm=620, output_path="../figures/uL", title_prefix="")
