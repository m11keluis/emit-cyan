import os
import numpy as np
import pandas as pd
import xarray as xr
import requests
import earthaccess
import re

import os
import numpy as np
import pandas as pd
import xarray as xr
import requests
import earthaccess
import re


def download_cyan_data(emit_filename, bounds=None, output_dir="data/cyan"):
    """
    Downloads and processes CyAN granules using date extracted from EMIT filename.
    """
    print("\n🔍 Starting CyAN granule lookup based on EMIT filename...")

    # Extract datetime from EMIT filename
    basename = os.path.basename(emit_filename)
    print(f"📂 EMIT filename provided: {basename}")
    match = re.search(r"_(\d{8}T\d{6})_", basename)
    if not match:
        raise ValueError(f"❌ Could not extract timestamp from filename: {basename}")

    datetime_str = match.group(1)
    datetime_object = pd.to_datetime(datetime_str, format="%Y%m%dT%H%M%S")
    date = datetime_object.strftime('%Y-%m-%d')
    print(f"📆 Extracted acquisition date: {date}")

    # Set up search parameters
    search_kwargs = {
        "short_name": 'MERGED_S3_OLCI_L3m_CYAN',
        "temporal": (date, date),
        "count": 100
    }
    if bounds:
        print(f"📌 Using bounding box: {bounds}")
        search_kwargs["bounding_box"] = bounds
    else:
        print("🌍 No bounding box provided — searching full scene coverage.")

    print("🔎 Querying Earthdata for CyAN granules...")
    results = earthaccess.search_data(**search_kwargs)
    print(f"🔢 Retrieved {len(results)} granules from Earthdata search.")

    # Filter for specific asset names
    desired_assets = ['L3m_DAY_CYAN_CI_cyano_CYAN_CONUS_300m_']
    filtered_asset_links = [
        url for granule in results for url in granule.data_links()
        if any(asset in url for asset in desired_assets)
    ]
    print(f"✅ {len(filtered_asset_links)} granules matched desired asset pattern.")

    # Prepare download folder
    os.makedirs(output_dir, exist_ok=True)
    fs = earthaccess.get_fsspec_https_session()

    # Download matching files
    downloaded_files = []
    for i, url in enumerate(filtered_asset_links, 1):
        filename = url.split('/')[-1]
        local_path = os.path.join(output_dir, filename)

        if not os.path.isfile(local_path):
            print(f"⬇️  [{i}/{len(filtered_asset_links)}] Downloading: {filename}")
            r = requests.get(url)
            with open(local_path, 'wb') as f:
                f.write(r.content)
            print(f"📥  Saved to: {local_path}")
        else:
            print(f"🟡 [{i}/{len(filtered_asset_links)}] Skipped (already exists): {filename}")

        downloaded_files.append(local_path)

    print(f"\n🏁 Finished. {len(downloaded_files)} CyAN granules ready at: {output_dir}\n")
    return downloaded_files

def process_cyan_granule(granule_path, bounds=None):
    """
    Opens, reprojects, and (optionally) clips a downloaded CyAN file.

    Parameters:
    - granule_path: path to the downloaded CyAN NetCDF file
    - bounds: optional (W, S, E, N) bounding box

    Returns:
    - Processed xarray DataArray with cyan CI values
    """
    ds = xr.open_dataset(granule_path)
    da = ds.rio.reproject("EPSG:4326")

    if bounds:
        W, S, E, N = bounds
        da = da.sel(x=slice(W, E), y=slice(N, S))

    da = da.rename({'x': 'longitude', 'y': 'latitude'})
    da = xr.where(da == 254, np.nan, da)
    da = xr.where(da == 255, np.nan, da)
    da = xr.where(da == 0, np.nan, da)

    CI = 10 ** (da * 0.011714 - 4.1870866)
    return CI
