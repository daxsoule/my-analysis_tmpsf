# Analysis Plan: ASHES TMPSF Timeseries

**Spec**: `specs/001-ashes-tmpsf-timeseries/spec.md`
**Created**: 2026-01-22
**Status**: Draft

## Summary

This analysis loads and concatenates 253 NetCDF files (~20GB) of TMPSF temperature data from the ASHES vent field to create a single pandas DataFrame for exploration and an interactive hvplot timeseries visualization. The focus is on data from 2016 to present, with QC flags used to identify suspect measurements.

## Analysis Environment

**Language/Version**: Python 3.12
**Key Packages**: xarray, netCDF4, hvplot, pandas, numpy
**Environment File**: `pyproject.toml` (managed by uv)

## Compute Environment

**Where will this run?**
- [x] Shared server (JupyterHub)

**Data scale**: ~20GB of NetCDF files (253 files)

**Timeline pressure**: Exploratory, no deadline

**Known bottlenecks**: Loading and concatenating 20GB of data may require chunked/lazy loading with xarray+dask to avoid memory issues.

## Constitution Check

- [x] Data sources match those defined in constitution
- [x] Coordinate systems/units are consistent (UTC, °C, NaN)
- [x] Figure standards will be followed (hvplot interactive)
- [x] Quality checks are incorporated (QARTOD flags)

**Issues to resolve**: None - plan aligns with constitution.

## Project Structure

```text
specs/001-ashes-tmpsf-timeseries/
├── spec.md              # Analysis specification
├── plan.md              # This file
└── tasks.md             # Task breakdown (created by /speckit.tasks)

notebooks/
└── 01_explore_tmpsf.ipynb    # Main exploration notebook

my_data/axial/axial_tmpsf/
└── tmpsf_concatenated.parquet  # Concatenated DataFrame (optional cache)

outputs/
└── figures/
    └── tmpsf_timeseries.html       # Interactive plot (if saved)
```

**Structure notes**: Single notebook approach for exploratory analysis. Data is read from existing local files (no download stage needed). Processed parquet file is optional - can be regenerated from source.

## Data Pipeline

### Stage 1: Data Loading
- **Input**: `/home/jovyan/ooi/kdata/RS03ASHS-MJ03B-07-TMPSFA301-streamed-tmpsf_sample/*.nc`
- **Processing**:
  - Use `xarray.open_mfdataset()` with parallel loading
  - Select temperature variables and QC flags
  - Filter to 2016-01-01 onward
- **Output**: xarray Dataset (in memory, lazy-loaded)
- **Script**: `notebooks/01_explore_tmpsf.ipynb` (Cell 1-2)

### Stage 2: QC Filtering
- **Input**: xarray Dataset
- **Processing**:
  - Examine QARTOD flag values
  - Create mask for suspect/failed data (flags 3, 4)
  - Apply mask or add QC column
- **Output**: QC-annotated Dataset
- **Script**: `notebooks/01_explore_tmpsf.ipynb` (Cell 3)

### Stage 3: DataFrame Conversion
- **Input**: QC-annotated Dataset
- **Processing**:
  - Convert to pandas DataFrame
  - Optionally resample/downsample for memory efficiency
  - Optionally save as parquet to `my_data/axial/axial_tmpsf/` for faster reload
- **Output**: pandas DataFrame ready for exploration
- **Script**: `notebooks/01_explore_tmpsf.ipynb` (Cell 4)

### Stage 4: Visualization
- **Input**: pandas DataFrame
- **Processing**:
  - Create interactive timeseries with hvplot
  - Plot temperature vs time for selected channel(s)
- **Output**: Interactive hvplot figure
- **Script**: `notebooks/01_explore_tmpsf.ipynb` (Cell 5)

## Script/Notebook Plan

| Artifact | Purpose | Inputs | Outputs |
|----------|---------|--------|---------|
| `notebooks/01_explore_tmpsf.ipynb` | Load, concatenate, QC, explore TMPSF data | 253 NetCDF files | DataFrame + hvplot figure |

### Notebook Cell Structure

1. **Setup**: Import packages, define paths
2. **Load Data**: `xr.open_mfdataset()` with time filter
3. **QC Assessment**: Examine and apply QARTOD flags
4. **DataFrame Creation**: Convert to pandas, inspect structure
5. **Visualization**: Interactive hvplot timeseries
6. **Exploration**: Additional cells for ad-hoc investigation

## Dependencies

```text
Load NetCDF files
       ↓
Apply time filter (2016+)
       ↓
Assess QC flags
       ↓
Convert to DataFrame
       ↓
Generate hvplot
```

**Parallel opportunities**: None needed - this is a linear exploratory workflow.

## Open Questions

- [x] Which temperature channel(s) to plot initially? → Start with temperature01, expand as needed
- [x] Need downsampling for performance? → Try full resolution first, downsample if slow

## Notes

- Data is already local, no download step needed
- 24 temperature channels available - may want to explore spatial arrangement in future work
- Consider saving concatenated DataFrame as parquet to `my_data/axial/axial_tmpsf/` if reload is needed frequently
