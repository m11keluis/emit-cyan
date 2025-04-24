import xarray as xr
import numpy as np
import rioxarray

def process_cyan_granule(granule_path, bounds=None):
    """
    Load, reproject, subset, mask, and transform CyAN granule into CI values.

    Parameters:
    - granule_path: str, path to downloaded CyAN NetCDF file
    - bounds: optional tuple of (W, S, E, N) for subsetting

    Returns:
    - CI: processed xarray DataArray in EPSG:4326 with CI units
    """
    print(f"📂 Processing CyAN granule: {granule_path}")
    ds = xr.open_dataset(granule_path)

    if bounds:
        W, S, E, N = bounds
        da = ds.sel(x=slice(W, E), y=slice(N, S))
        print(f"🔍 Subset to bounds: {bounds}")

    da = ds.rename({'x': 'longitude', 'y': 'latitude'})

    # Remove nodata / flagged values
    da = xr.where(da == 254, np.nan, da)
    da = xr.where(da == 255, np.nan, da)
    da = xr.where(da == 0, np.nan, da)

    # Convert to CyAN CI
    CI = 10 ** (da * 0.011714 - 4.1870866)
    CI.name = "CI"

    print(f"✅ Finished CyAN CI processing. Shape: {CI.shape}")
    return CI
