# ASHES Diffuse Hydrothermal Temperature Analysis

Analyzing diffuse hydrothermal vent temperature variability using TMPSF (Temperature Mooring Sea Floor) sensor data from the Ocean Observatories Initiative (OOI) Cabled Array.

## Overview

This project analyzes temperature data from 24 thermistor channels deployed at the ASHES vent field on Axial Seamount. The analysis covers 2015-2026 (11 years) to capture long-term diffuse hydrothermal temperature variability, including the April 2015 eruption period.

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
- **Location**: 45.933653N, 130.013688W
- **Channels**: 24 thermistor sensors
- **Time range**: 2015-01-01 to 2026-01-25

## Data Quality Control

### The Problem

Raw TMPSF data contains sensor artifacts that can corrupt analysis results. During initial exploration, we discovered temperature spikes reaching 114C - far exceeding physically plausible values for diffuse hydrothermal vents (typically 2-15C).

### How We Identified Bad Data

**1. Temporal analysis**: Channel 06 showed extreme temperatures only in 2017, then returned to normal in 2018 - indicating sensor failure, not a real thermal event.

**2. Spatial analysis**: When Channel 02 showed 22C, neighboring channels (01, 03, 04) showed normal 3C temperatures. Real hydrothermal events affect multiple nearby thermistors; single-channel spikes indicate sensor malfunction.

**3. OOI quality flags**: The QARTOD system had already flagged much of the Channel 06 data as FAIL (flag=4), confirming sensor issues.

### Two-Stage QC Process

**Stage 1: QARTOD Filtering**
- Use OOI's built-in quality flags (1=pass, 4=fail)
- Set values with QARTOD != 1 to NaN
- Result: Removed 0.49% of data (Channel 06: 8.9%, Channel 02: 2.9%)

**Stage 2: Cross-Channel Consistency Check**
- For each measurement, compare to median of other 23 channels
- Flag values exceeding median + 10C as sensor artifacts
- Result: Removed additional 0.25% of data that passed QARTOD

### Before vs After QC

| Metric | Before QC | After QC |
|--------|-----------|----------|
| Max temperature | 113.6C | 13.4C |
| Mean temperature | 3.31C | 3.02C |
| Std deviation | 5.09C | 0.95C |

### Known Sensor Issues

| Channel | Issue | Period | Notes |
|---------|-------|--------|-------|
| 06 | Complete failure | 2017 | Temps jumped to 90-114C, flagged by QARTOD |
| 02 | Offset/drift | 2015-2017 | Running 15-20C hot, caught by consistency check |
| 07 | Intermittent spikes | Various | Minor, mostly caught by consistency check |

## Outputs

### Data Products

| File | Description |
|------|-------------|
| `outputs/data/tmpsf_2015-2026_hourly.parquet` | Hourly averaged, QC-filtered data |
| `outputs/data/tmpsf_2015-2026_daily.parquet` | Daily averaged temperatures |
| `outputs/data/channel_statistics.csv` | Per-channel statistics and characterization |

**Columns:** `temperature01` through `temperature24` (24 thermistor channels)

### Figures

| File | Description |
|------|-------------|
| `outputs/figures/tmpsf_all_channels.png` | Full 11-year timeseries, color-coded by mean temp |
| `outputs/figures/channel_characterization.png` | Bar chart of mean temps with error bars |
| `outputs/figures/hot_vs_cool_channels.png` | Top/bottom 3 channel comparison |

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

# Load daily temperatures (QC-filtered)
tmpsf = pd.read_parquet('outputs/data/tmpsf_2015-2026_daily.parquet')

# Check channel statistics
stats = pd.read_csv('outputs/data/channel_statistics.csv')
print(stats[['channel', 'mean', 'std', 'regime']])

# Join with other instruments
other = pd.read_parquet('path/to/other_data.parquet')
merged = tmpsf.join(other, how='inner')
```

## Project Structure

```
my-analysis_tmpsf/
├── analysis.py                     # Main analysis script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── outputs/
│   ├── constitution.pdf            # PDF reference document
│   ├── data/                       # Parquet data products
│   ├── figures/                    # Publication-quality PNG figures
│   └── notebooks/                  # Reproducible Jupyter notebook
└── .specify/
    ├── features/                   # Spec, plan, tasks
    └── memory/constitution.md      # Project constitution
```

## References

- OOI Cabled Array: https://oceanobservatories.org/array/cabled-array/
- QARTOD: https://ioos.noaa.gov/project/qartod/

## License

This analysis uses data from the Ocean Observatories Initiative, funded by the National Science Foundation.

## Author

Dax Soule
January 2026
