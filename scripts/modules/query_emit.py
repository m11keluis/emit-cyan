from pathlib import Path
import earthaccess
import os

def query_and_download_emit(bbox, start, end, output_folder="data"):
    """
    Query and download EMIT RFL granules using Earthaccess.

    Parameters:
    - bbox: (west, south, east, north)
    - start, end: date strings (YYYY-MM-DD)
    - output_folder: destination directory for downloads
    """
    print("Logging into Earthdata...")
    earthaccess.login(strategy="interactive", persist=True)

    print(f"Querying EMIT RFL granules for {bbox} from {start} to {end}...")
    results = earthaccess.search_data(
        short_name="EMITL2ARFL",
        bounding_box=bbox,
        temporal=(start, end),
        cloud_hosted=True,
    )

    desired_assets = ['EMIT_L2A_RFL_']
    print(f"📦 Filtering granules for assets containing: {desired_assets}...")

    filtered_links = []
    for granule in results:
        links = granule.data_links()
        matching = [
            url for url in links
            if url.split('/')[-1].startswith("EMIT_L2A_RFL_") and url.endswith(".nc")
        ]
        if matching:
            filtered_links.extend(matching)

    if not filtered_links:
        print(" No matching EMIT RFL assets found.")
        return []

    fs = earthaccess.get_requests_https_session()
    output_dir = Path(output_folder) / "emit"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f" Downloading {len(filtered_links)} granules to: {output_dir}")

    for i, url in enumerate(filtered_links, 1):
        fname = url.split('/')[-1]
        local_path = output_dir / fname

        if local_path.exists():
            print(f" [{i}/{len(filtered_links)}] Skipping {fname} (already exists)")
            continue

        print(f" [{i}/{len(filtered_links)}] Downloading {fname}...")
        try:
            with fs.get(url, stream=True) as r, open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=64 * 1024 * 1024):
                    f.write(chunk)
            print(f"  Saved to {local_path}")
        except Exception as e:
            print(f"  Failed to download {fname}: {e}")


    print(f"Downloaded {len(filtered_links)} EMIT RFL files to {output_dir}")
    return [str(output_dir / url.split('/')[-1]) for url in filtered_links]
