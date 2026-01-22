# Diffuse Hydrothermal Temperature Timeseries Analysis

## Research Context

This project analyzes diffuse hydrothermal vent temperature variability using TMPSF (Temperature Mooring Sea Floor) sensor data. The primary goal is to understand how diffuse temperature varies as a function of time for the year 2018.

Outputs:
1. A concatenated pandas DataFrame containing the 2018 timeseries for exploration
2. An interactive timeseries plot showing the daily average temperature for 2018
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

- **Purpose**: Exploratory analysis
- **Plotting library**: hvplot (interactive)
- **Color palette**: Default (colorblind-safe preferred for publication)
- **Format**: Interactive HTML/notebook widgets

## Quality Checks

- **Primary QC**: Use OOI QARTOD and QC flags included in data files
- **Handling**: Filter or flag data based on QC results before plotting

## Project Notes

- **Status**: Exploratory analysis, no constraints
- **Data sharing**: OOI data is publicly available
