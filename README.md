# ASHES Diffuse Hydrothermal Temperature Analysis

Analyzing diffuse hydrothermal vent temperature variability using TMPSF (Temperature Mooring Sea Floor) sensor data from the Ocean Observatories Initiative (OOI) Cabled Array.

## Overview

This project analyzes temperature data from 24 thermistor channels deployed at the ASHES vent field on Axial Seamount. The analysis focuses on the 2018-2019 period to understand diffuse hydrothermal temperature variability.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/daxsoule/my-analysis_tmpsf.git
cd my-analysis_tmpsf

# Install dependencies
pip install -r requirements.txt

# Run the analysis
python analysis.py
```

## Data Source

- **Instrument**: TMPSF (Temperature Mooring Sea Floor)
- **Site**: ASHES vent field, Axial Seamount
- **Reference designator**: RS03ASHS-MJ03B-07-TMPSFA301-streamed-tmpsf_sample
- **Location**: 45.933653°N, 130.013688°W
- **Channels**: 24 thermistor sensors

## Outputs

### Data Products

| File | Description |
|------|-------------|
| `outputs/data/tmpsf_2018-2019_raw.parquet` | High-frequency cleaned data |
| `outputs/data/tmpsf_2018-2019_daily.parquet` | Daily averaged temperatures |

**Columns:** `temperature01` through `temperature24` (24 thermistor channels)

### Figures

- `outputs/figures/tmpsf_2018-2019_all_channels.html` - Interactive timeseries plot showing all 24 channels

## Reproducible Notebook

For detailed methodology with full annotations, see the Jupyter notebook:

```bash
cd outputs/notebooks
conda env create -f environment.yml
conda activate ashes-tmpsf-analysis
jupyter lab 01_explore_tmpsf.ipynb
```

## Using the Data

```python
import pandas as pd

# Load daily temperatures
tmpsf = pd.read_parquet('outputs/data/tmpsf_2018-2019_daily.parquet')

# Join with other instruments
other = pd.read_parquet('path/to/other_data.parquet')
merged = tmpsf.join(other, how='inner')
```

## Project Structure

```
my-analysis_tmpsf/
├── analysis.py                     # Main analysis script
├── requirements.txt                # Python dependencies
├── outputs/
│   ├── constitution.pdf            # PDF reference document
│   ├── data/                       # Parquet data products
│   ├── figures/                    # Interactive HTML plots
│   └── notebooks/                  # Reproducible Jupyter notebook
└── .specify/
    ├── features/                   # Spec, plan, tasks
    └── memory/constitution.md      # Project constitution
```

## References

- OOI Cabled Array: https://oceanobservatories.org/array/cabled-array/

## License

This analysis uses data from the Ocean Observatories Initiative, funded by the National Science Foundation.

## Author

Dax Soule
January 2026
