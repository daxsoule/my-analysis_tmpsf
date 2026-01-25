# Diffuse Hydrothermal Temperature Timeseries Analysis

## Research Context

This project analyzes diffuse hydrothermal vent temperature variability using TMPSF (Temperature Mooring Sea Floor) sensor data. The primary goal is to understand how diffuse temperature varies as a function of time for 2015-2026, capturing the April 2015 eruption through present.

Outputs:
1. A concatenated pandas DataFrame containing the 2015-2026 timeseries for exploration
2. Channel characterization with per-channel statistics (mean, std, min, max, CV)
3. Publication-quality matplotlib figures (300 DPI) showing temperature timeseries and channel comparisons
<!-- Who are the intended users of the outputs? -->

## Core Principles

### I. Reproducibility

Analysis should be fully reproducible from raw data to final outputs.
Scripts run without manual intervention. Random seeds are fixed and
documented. Environment dependencies are explicit (requirements.txt,
environment.yml, or equivalent).

### II. Data Integrity

Raw data is immutable - all transformations produce new files, never
overwrite sources. Data lineage is traceable through the analysis chain.
Missing or suspect values are flagged, not silently dropped or filled.

### III. Provenance

Every output links back to: the code that produced it, the input data,
and key parameter choices. Figures and tables can be regenerated from
tracked artifacts. If you can't trace how a number was made, it doesn't
belong in the paper.

## Data Sources

### TMPSF Sensor Data
- **Source**: Ocean Observatories Initiative (OOI)
- **Site**: ASHES vent field, Axial Seamount
- **Reference designator**: RS03ASHS-MJ03B-07-TMPSFA301-streamed-tmpsf_sample
- **Access method**: Local files at `/home/jovyan/ooi/kdata/RS03ASHS-MJ03B-07-TMPSFA301-streamed-tmpsf_sample/`
- **Temporal coverage**: 2016 to present
- **Instrument**: TMPSF (Temperature Mooring Sea Floor)
- **Documentation**: https://oceanobservatories.org/

- **File format**: NetCDF (.nc), 253 files across 2 deployments
- **File pattern**: `deployment{NNNN}_RS03ASHS-MJ03B-07-TMPSFA301-streamed-tmpsf_sample_{starttime}-{endtime}.nc`
- **Actual temporal range**: 2014-09-29 to 2026-01-22 (present)

- **Variables**: temperature01-24 (24 thermistor channels), with QARTOD and QC flags
- **Location**: 45.933653°N, 130.013688°W (Axial Seamount)
- **Coordinate**: time (datetime64[ns])

<!-- TODO: Known quality issues or data gaps -->

## Technical Environment

- **Language**: Python 3.12
- **Package manager**: uv (use `uv add` for dependencies)
- **Key packages**: xarray, netCDF4, hvplot, pandas, numpy, matplotlib, scipy
- **Compute environment**: JupyterHub server
- **Data storage (raw)**: `/home/jovyan/ooi/kdata/`
- **Data storage (processed)**: `/home/jovyan/my_data/axial/axial_tmpsf/`
- **Version control**: Git

## Coordinate Systems & Units

- **Time zone**: UTC (OOI standard)
- **Calendar**: Gregorian
- **Temperature units**: °C
- **Missing data**: NaN

## Figure Standards

- **Purpose**: Publication-quality analysis
- **Plotting library**: matplotlib (static, 300 DPI)
- **Color palette**: coolwarm for temperature gradients, diverging blue/red for hot/cool channels
- **Format**: PNG at 300 DPI for publication
- **Style**: Clean spines (top/right removed), consistent font sizes

## Quality Control

### Overview

The TMPSF sensor data contains artifacts from sensor failures that must be identified and removed before analysis. We apply a two-stage QC process:

1. **QARTOD filtering**: Use OOI's built-in quality flags
2. **Cross-channel consistency check**: Flag single-channel spikes that passed QARTOD

### Stage 1: QARTOD Filtering

OOI provides QARTOD (Quality Assurance of Real-Time Oceanographic Data) flags for each temperature channel:
- 1 = Pass
- 2 = Not evaluated
- 3 = Suspect
- 4 = Fail
- 9 = Missing

**Implementation**: Values with QARTOD != 1 are set to NaN before analysis.

**Results**:
- Total observations: 815,810,256
- Failed QARTOD: 3,989,716 (0.49%)
- Channel 06: 8.9% failed (sensor failure throughout 2017)
- Channel 02: 2.9% failed (intermittent issues)

### Stage 2: Cross-Channel Consistency Check

Some sensor artifacts passed QARTOD QC but showed physically implausible behavior. We identified these by examining single-channel temperature spikes.

**Problem identified**: Channel 02 showed temperatures of 20-50°C while all neighboring channels (01, 03, 04) showed normal temps of ~3°C. This single-channel spike pattern is characteristic of sensor malfunction, not real hydrothermal events (which would affect multiple nearby thermistors).

**Evidence**:
- Channel 02 mean temperature in 2015: 16.6°C (other channels: ~3°C)
- Channel 02 max in 2017: 49.2°C (neighbors showed 3-4°C)
- Pattern: isolated single-channel spikes, not correlated with neighbors

**Solution**: Cross-channel consistency filter that flags values exceeding the median of all other channels by more than 10°C.

**Implementation**:
```
For each timestamp and channel:
  median_others = median of all other 23 channels
  if channel_value > median_others + 10°C:
    set to NaN (flagged as inconsistent)
```

**Results**:
- Total flagged: 5,547 values (0.25% of QARTOD-passed data)
- Channel 02: 4,168 values flagged (4.54%)
- Channel 07: 1,276 values flagged (1.37%)
- Channel 06: 99 values flagged (0.11%)

### Final Data Quality

After both QC stages:
- Temperature range: 2.3°C to 13.4°C (physically reasonable for diffuse vents)
- Mean: 3.02°C
- Std deviation: 0.95°C

### Known Sensor Issues

| Channel | Issue | Period | Detection Method |
|---------|-------|--------|------------------|
| 06 | Complete sensor failure | 2017 | QARTOD flagged as FAIL |
| 02 | Intermittent high readings | 2015-2017 | Cross-channel consistency |
| 07 | Some high spikes | Various | Cross-channel consistency |

## Outputs

### Data Products

| File | Description |
|------|-------------|
| `outputs/data/tmpsf_2015-2026_hourly.parquet` | Hourly averaged data (memory-efficient) |
| `outputs/data/tmpsf_2015-2026_daily.parquet` | Daily averaged temperatures |
| `outputs/data/channel_statistics.csv` | Per-channel statistics and characterization |

**Columns:** `temperature01` through `temperature24` (24 thermistor channels)

### Figures

| File | Description |
|------|-------------|
| `outputs/figures/tmpsf_all_channels.png` | Full 11-year timeseries, color-coded by mean temp |
| `outputs/figures/channel_characterization.png` | Bar chart of mean temps with error bars |
| `outputs/figures/hot_vs_cool_channels.png` | Top/bottom 3 channel comparison |

### Notebooks

| File | Description |
|------|-------------|
| `outputs/notebooks/01_explore_tmpsf.ipynb` | Exploratory analysis notebook |
| `outputs/notebooks/environment.yml` | Conda environment for notebook |

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

## Project Notes

- **Status**: Exploratory analysis, no constraints
- **Data sharing**: OOI data is publicly available
