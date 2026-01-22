# Tasks: ASHES TMPSF Timeseries

**Spec**: `specs/001-ashes-tmpsf-timeseries/spec.md`
**Plan**: `specs/001-ashes-tmpsf-timeseries/plan.md`
**Generated**: 2026-01-22

## Format

```text
- [ ] T### Description with file path or specific action
```

- Task IDs are sequential (T001, T002, ...)
- QC tasks are labeled explicitly
- Each task should be completable independently

---

## Phase 1: Setup

**Purpose**: Environment and project structure ready

- [x] T001 Create directory structure: `notebooks/`, `/home/jovyan/my_data/axial/axial_tmpsf/`, `outputs/figures/`
- [x] T002 Verify uv environment has required packages (xarray, netCDF4, hvplot, pandas)
- [x] T003 Create notebook `notebooks/01_explore_tmpsf.ipynb` with initial setup cell

**Checkpoint**: Directories exist, notebook runs import cell without errors

---

## Phase 2: Data Loading

**Purpose**: NetCDF files loaded and filtered to 2018

- [ ] T004 Implement data loading cell: `xr.open_mfdataset()` for all 253 NetCDF files
- [ ] T005 Select temperature variables (temperature01-24) and QC flag variables
- [ ] T006 Filter to 2018 (2018-01-01 to 2018-12-31) using time coordinate
- [ ] T007 QC: Verify loaded dataset has expected time range (2018)
- [ ] T008 QC: Check that all 24 temperature channels are present

**Checkpoint**: xarray Dataset loaded with 2018 data, all temperature channels available

---

## Phase 3: QC Assessment

**Purpose**: Data quality flags examined and applied

- [ ] T009 Examine QARTOD flag values and their distribution
- [ ] T010 Create mask for suspect/failed data (QARTOD flags 3 and 4)
- [ ] T011 Document QC flag handling approach in notebook markdown
- [ ] T012 QC: Verify temperature values fall within reasonable range (diffuse vents: ~2-50°C)
- [ ] T013 QC: Check for duplicate timestamps after concatenation

**Checkpoint**: QC flags understood, mask created, temperature ranges validated

---

## Phase 4: DataFrame Creation & Daily Averaging

**Purpose**: Data converted to pandas DataFrame and daily averages computed

- [ ] T014 Convert xarray Dataset to pandas DataFrame
- [ ] T015 Inspect DataFrame structure (columns, dtypes, shape)
- [ ] T016 Compute daily average temperature for each day in 2018
- [ ] T017 QC: Verify daily averages DataFrame has 365 rows (or 366 if leap year)
- [ ] T018 Optionally save DataFrame to `/home/jovyan/my_data/axial/axial_tmpsf/tmpsf_2018_daily.parquet`

**Checkpoint**: pandas DataFrame with daily averages available for exploration

---

## Phase 5: Visualization

**Purpose**: Interactive timeseries plot of daily averages generated

- [ ] T019 Create interactive hvplot timeseries for daily average temperature vs time
- [ ] T020 Add plot title, axis labels, and appropriate styling
- [ ] T021 Optionally save plot to `outputs/figures/tmpsf_2018_daily.html`
- [ ] T022 QC: Verify plot displays full 2018 time range
- [ ] T023 QC: Verify plot shows expected temperature variability patterns

**Checkpoint**: Interactive hvplot figure of daily averages generated, displays correctly in notebook

---

## Phase 6: Documentation & Reproducibility

**Purpose**: Analysis is reproducible and documented

- [ ] T024 Add markdown documentation cells explaining each analysis step
- [ ] T025 Verify notebook runs end-to-end: Kernel → Restart & Run All
- [ ] T026 Final check against spec.md completion criteria

**Checkpoint**: Notebook reproduces all outputs from raw data

---

## Dependencies

```text
Phase 1 (Setup)
     ↓
Phase 2 (Data Loading)
     ↓
Phase 3 (QC Assessment)
     ↓
Phase 4 (DataFrame Creation)
     ↓
Phase 5 (Visualization)
     ↓
Phase 6 (Documentation)
```

Phases are sequential. Complete each checkpoint before proceeding.

---

## Completion Criteria

From spec.md - all must be satisfied:

- [ ] NetCDF files loaded and concatenated
- [ ] Data filtered to 2018 timeframe
- [ ] QC flags applied to identify suspect data
- [ ] Concatenated DataFrame available for exploration
- [ ] Daily average temperature computed
- [ ] Interactive timeseries plot of daily averages generated
- [ ] Results reproducible from raw data

---

## Notes

- No Phase 0 (Research) needed - all method decisions resolved in plan.md
- Data is already local - no download/acquisition phase required
- Single notebook approach keeps exploratory workflow simple
- Commit after completing each phase
