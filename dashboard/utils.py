import re
import pandas as pd
import numpy as np
import xarray as xr
import rioxarray as rxr

from scripts.modules.emit_tools import emit_xarray
from scripts.modules.emit_aqua import mask_aqua

def extract_date_from_emit_filename(filename):
    match = re.search(r"_(\d{8}T\d{6})_", filename)
    if not match:
        raise ValueError(f"Could not extract timestamp from filename: {filename}")
    datetime_str = match.group(1)
    return pd.to_datetime(datetime_str, format="%Y%m%dT%H%M%S")

def load_emit_granule(path, wavelength_nm=620):
    """
    Loads and processes an EMIT NetCDF granule:
    - Orthorectifies
    - Applies good_wavelengths mask
    - Applies cloud/cirrus/land mask
    - Selects nearest wavelength band
    """
    ds = emit_xarray(path, ortho=True)

    if "good_wavelengths" in ds:
        ds['reflectance'].data[:, :, ds['good_wavelengths'].data == 0] = np.nan

    ds = mask_aqua(ds)

    band = ds['reflectance'].sel(wavelengths=wavelength_nm, method="nearest")
    band = band.where(band > 0)  # Mask negatives if needed
    return band

def load_cyan_geotiff(path):
    """
    Loads CyAN GeoTIFF, masks invalid values.
    """
    da = rxr.open_rasterio(path, masked=True).squeeze()
    da.name = "band_data"
    da = da.rio.write_crs("EPSG:4326")
    return da
