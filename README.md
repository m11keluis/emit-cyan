# EMIT vs. CyAN Surface Reflectance Comparison

This repository supports a rapid and high-resolution visual comparison between EMIT and CyAN surface reflectance products, focused on Harmful Algal Blooms (HABs). It also sets the foundation for an eventual interactive visualization platform.

## 🚀 Purpose

- Compare NASA's EMIT hyperspectral data with NOAA's CyAN product
- Highlight spatial resolution, spectral features, and signal differences
- Produce visuals for web integration (e.g., HABs section)
- Prepare for long-term deployment as an interactive tool

##  Repository Structure

```text
emit-cyan-reflectance-comparison/
├── data/            # Raw and processed data (GeoTIFF, NetCDF)
├── figures/         # Output plots for web use
├── notebooks/       # Jupyter analysis notebooks
├── scripts/         # Query and processing scripts
├── test.py          # Debug/test script for querying both datasets
├── environment.yml  # Conda environment config
└── README.md

```

## Setup

```bash
conda env create -f environment.yml
conda activate emit_cyan_env
```

## Notes
- EMIT provides high-resolution (~60m) VSWIR hyperspectral data.
- CyAN (based on MERIS/Sentinel 3) provides lower-res (~300m) chlorophyll indices.
- CI values from CyAN are transformed via log-scaling for visualization.
- Granule queries rely on Earthaccess.

## Future

- Static comparison visuals
- Difference plots and QA/QC overlays
- Streamlit or Dash interactive comparison tool