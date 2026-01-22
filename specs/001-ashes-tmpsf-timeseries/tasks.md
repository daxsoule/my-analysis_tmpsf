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

- [ ] T001 Create directory structure: `notebooks/`, `my_data/axial/axial_tmpsf/`, `outputs/figures/`
- [ ] T002 Verify uv environment has required packages (xarray, netCDF4, hvplot, pandas)
- [ ] T003 Create notebook `notebooks/01_explore_tmpsf.ipynb` with initial setup cell

**Checkpoint**: Directories exist, notebook runs import cell without errors

---

## Phase 2: Data Loading

**Purpose**: NetCDF files loaded and filtered to analysis timeframe

- [ ] T004 Implement data loading cell: `xr.open_mfdataset()` for all 253 NetCDF files
- [ ] T005 Select temperature variables (temperature01-24) and QC flag variables
- [ ] T006 Filter to 2016-01-01 onward using time coordinate
- [ ] T007 QC: Verify loaded dataset has expected time range (2016-present)
- [ ] T008 QC: Check that all 24 temperature channels are present

**Checkpoint**: xarray Dataset loaded with 2016+ data, all temperature channels available

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

## Phase 4: DataFrame Creation

**Purpose**: Data converted to pandas DataFrame for exploration

- [ ] T014 Convert xarray Dataset to pandas DataFrame
- [ ] T015 Inspect DataFrame structure (columns, dtypes, shape)
- [ ] T016 Optionally save DataFrame to `my_data/axial/axial_tmpsf/tmpsf_concatenated.parquet`
- [ ] T017 QC: Verify DataFrame has expected number of rows and columns

**Checkpoint**: pandas DataFrame available for exploration, optionally cached as parquet

---

## Phase 5: Visualization

**Purpose**: Interactive timeseries plot generated

- [ ] T018 Create interactive hvplot timeseries for temperature01 vs time
- [ ] T019 Add plot title, axis labels, and appropriate styling
- [ ] T020 Optionally save plot to `outputs/figures/tmpsf_timeseries.html`
- [ ] T021 QC: Verify plot displays full 2016-present time range
- [ ] T022 QC: Verify plot shows expected temperature variability patterns

**Checkpoint**: Interactive hvplot figure generated, displays correctly in notebook

---

## Phase 6: Documentation & Reproducibility

**Purpose**: Analysis is reproducible and documented

- [ ] T023 Add markdown documentation cells explaining each analysis step
- [ ] T024 Verify notebook runs end-to-end: Kernel → Restart & Run All
- [ ] T025 Final check against spec.md completion criteria

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

- [ ] All 253 NetCDF files loaded and concatenated
- [ ] Data filtered to 2016-present timeframe
- [ ] QC flags applied to identify suspect data
- [ ] Concatenated DataFrame available for exploration
- [ ] Interactive timeseries plot generated
- [ ] Results reproducible from raw data

---

## Notes

- No Phase 0 (Research) needed - all method decisions resolved in plan.md
- Data is already local - no download/acquisition phase required
- Single notebook approach keeps exploratory workflow simple
- Commit after completing each phase
