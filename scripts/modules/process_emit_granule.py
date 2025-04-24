from .emit_tools import emit_xarray
import numpy as np
from .emit_aqua import mask_aqua

def process_emit_granule(filepath, bounds=None):
    """
    Opens and processes an EMIT RFL file: orthorectifies, applies good_wavelength mask,
    and subsets spatially.

    Parameters:
    - filepath: path to EMIT RFL NetCDF
    - bounds: (W, S, E, N) tuple for subsetting

    Returns:
    - ds_sub: processed xarray.Dataset (orthorectified and masked)
    """
    print(f"📂 Opening EMIT granule: {filepath}")
    ds = emit_xarray(filepath, ortho=True)

    if "good_wavelengths" in ds:
        print("✅ Applying good_wavelengths mask...")
        ds['reflectance'].data[:, :, ds['good_wavelengths'].data == 0] = np.nan

    if bounds:
        W, S, E, N = bounds
        print(f"🔍 Subsetting EMIT data to bounds: {bounds}")
        ds = ds.sel(longitude=slice(W, E), latitude=slice(N, S))

    # Optionally apply additional masks here (e.g., cloud/cirrus/land)
    if hasattr(ds, "mask_aqua"):  # only if integrated
        print("🛡️ Applying cloud/cirrus/land mask...")
        ds = mask_aqua(ds)

    print(f"✅ Finished EMIT processing. Shape: {ds['reflectance'].shape}")
    return ds
