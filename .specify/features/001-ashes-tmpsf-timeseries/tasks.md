# Tasks: ASHES TMPSF Timeseries

**Spec**: `.specify/features/001-ashes-tmpsf-timeseries/spec.md`
**Plan**: `.specify/features/001-ashes-tmpsf-timeseries/plan.md`
**Generated**: 2026-01-22
**Last updated**: 2026-03-05

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

- [x] T001 Create directory structure: `outputs/data/`, `outputs/figures/`, `outputs/notebooks/`
- [x] T002 Verify uv environment has required packages (xarray, netCDF4, hvplot, pandas, numpy, matplotlib, scipy)
- [x] T003 Create notebook `outputs/notebooks/01_explore_tmpsf.ipynb` with initial setup cell
- [x] T004 Add CLAUDE.md with security guardrails (matching miso_my-analysis conventions)

**Checkpoint**: Directories exist, notebook runs import cell without errors

---

## Phase 2: Data Loading (2018-2019 scope)

**Purpose**: Initial exploratory analysis of 2018-2019 data

- [x] T005 Implement data loading in notebook: load NetCDF files for 2018 data
- [x] T006 Select temperature variables (temperature01-24) and QC flag variables
- [x] T007 Filter to 2018 using time coordinate
- [x] T008 Convert to pandas DataFrame, compute daily averages
- [x] T009 Create interactive hvplot timeseries of all 24 channels
- [x] T010 Save interactive figure to `outputs/figures/tmpsf_2018-2019_all_channels.html`
- [x] T011 Export raw and daily data to `outputs/data/tmpsf_2018-2019_raw.parquet` and `tmpsf_2018-2019_daily.parquet`

**Checkpoint**: 2018-2019 interactive plot and parquet files generated

---

## Phase 3: Extended Analysis (2015-2026 scope)

**Purpose**: Expand analysis to capture the April 2015 eruption through present

- [x] T012 Create `analysis.py` — standalone script for full 2015-2026 pipeline
- [x] T013 Implement regex-based year extraction for efficient file filtering
- [x] T014 Load all NetCDF files for 2015-2026 with hourly resampling for memory efficiency
- [x] T015 QC: Verify loaded dataset spans 2015-2026 time range
- [x] T016 QC: Confirm all 24 temperature channels present

**Checkpoint**: Full 11-year dataset loaded as hourly DataFrame

---

## Phase 4: Quality Control

**Purpose**: Two-stage QC pipeline applied and documented

### Stage 1: QARTOD Filtering
- [x] T017 Implement QARTOD flag filtering (keep only flag=1, set others to NaN)
- [x] T018 Report QC statistics: total observations, failure rates per channel
- [x] T019 QC: Verify overall failure rate (~0.49%)
- [x] T020 QC: Identify high-failure channels (Ch06: 8.9%, Ch02: 2.9%)

### Stage 2: Cross-Channel Consistency Check
- [x] T021 Implement cross-channel consistency filter (flag values > median + 10C)
- [x] T022 QC: Verify filter catches Ch02 single-channel spikes (4.54% flagged)
- [x] T023 QC: Verify filter catches Ch07 intermittent spikes (1.37% flagged)
- [x] T024 QC: Confirm final temperature range is physically reasonable (2.3-13.4C)

### Documentation
- [x] T025 Document QC methodology in constitution.md (both stages, thresholds, results)
- [x] T026 Document known sensor issues table (Ch06 failure, Ch02 drift, Ch07 spikes)
- [x] T027 Create `outputs/figures/channel06_investigation.png` — sensor failure diagnostic figure

**Checkpoint**: Two-stage QC applied, temperature range 2.3-13.4C, methodology documented

---

## Phase 5: Channel Characterization

**Purpose**: Per-channel statistics computed and channels classified

- [x] T028 Compute per-channel statistics (mean, std, min, max, range, CV)
- [x] T029 Classify channels as "hot" vs "cool" relative to median mean temperature
- [x] T030 Rank channels by mean temperature and variability
- [x] T031 Export to `outputs/data/channel_statistics.csv`

**Checkpoint**: 12 hot + 12 cool channels identified, statistics exported

---

## Phase 6: Publication-Quality Figures

**Purpose**: Matplotlib figures at 300 DPI with full borders

- [x] T032 Figure: `tmpsf_all_channels.png` — full 11-year timeseries, color-coded by mean temp (coolwarm colormap)
- [x] T033 Figure: `channel_characterization.png` — bar chart of mean temps with std error bars, blue/red for cool/hot
- [x] T034 Figure: `hot_vs_cool_channels.png` — top 3 hottest and coolest channels overlaid
- [x] T035 Apply figure style: 6x3 aspect ratio, full borders (all 4 spines), 300 DPI

**Checkpoint**: Three publication-quality PNG figures generated

---

## Phase 7: Data Products for Cross-Project Integration

**Purpose**: Parquet files consumable by sibling projects (miso_my-analysis, my-analysis_botpt, earthquakes_my-analysis)

- [x] T036 Export `outputs/data/tmpsf_2015-2026_hourly.parquet` — hourly averaged, QC-filtered
- [x] T037 Export `outputs/data/tmpsf_2015-2026_daily.parquet` — daily averaged temperatures
- [x] T038 Verify data is loadable from MISO project via `pd.read_parquet('../my-analysis_tmpsf/outputs/data/tmpsf_2015-2026_daily.parquet')`

**Checkpoint**: Parquet files used by miso_my-analysis for poster Figure 3

---

## Phase 8: Documentation & Constitution

**Purpose**: Project fully documented and reproducible

- [x] T039 Create README.md with QC methodology, data products, usage examples
- [x] T040 Write constitution.md with research context, data sources, technical environment
- [x] T041 Add vent field coordinates and individual vent coordinates to constitution
- [x] T042 Document figure standards in constitution (matplotlib, 300 DPI, coolwarm palette)
- [x] T043 Add figure evaluation rubric adoption to constitution workflow
- [x] T044 Export constitution to `outputs/constitution.pdf`

**Checkpoint**: All documentation complete, constitution PDF generated

---

## Phase 9: Reproducibility & Sharing

**Purpose**: Repository ready to share

- [x] T045 Verify `analysis.py` runs end-to-end from raw NetCDF to all outputs
- [x] T046 Add `requirements.txt` with Python dependencies
- [x] T047 Add `outputs/notebooks/environment.yml` for conda environment
- [ ] T048 Add CLAUDE.md with security guardrails (matching miso_my-analysis)
- [ ] T049 Update tasks.md to reflect all completed work
- [ ] T050 Final review: verify all outputs listed in constitution exist in outputs/

**Checkpoint**: Repository reproducible and shareable

---

## Dependencies

```text
Phase 1 (Setup)
     |
Phase 2 (2018-2019 Exploration)
     |
Phase 3 (2015-2026 Extension)
     |
Phase 4 (Quality Control)
     |
Phase 5 (Channel Characterization)
    / \
Phase 6   Phase 7
(Figures)  (Data Products)
    \ /
Phase 8 (Documentation)
     |
Phase 9 (Reproducibility)
```

Phases 6 and 7 can run in parallel after Phase 5.

---

## Completion Criteria

From spec.md and expanded scope — all satisfied:

- [x] NetCDF files loaded and concatenated (253 files, 2 deployments)
- [x] Data filtered to analysis timeframe (expanded: 2015-2026)
- [x] QC flags applied — two-stage pipeline (QARTOD + cross-channel consistency)
- [x] Concatenated DataFrame available for exploration (hourly + daily parquet)
- [x] Daily average temperature computed for all 24 channels
- [x] Publication-quality timeseries figures generated (3 matplotlib PNGs)
- [x] Interactive timeseries plot generated (hvplot HTML for 2018-2019)
- [x] Channel characterization with hot/cool classification
- [x] Data products consumed by sibling project (miso_my-analysis poster Figure 3)
- [x] Results reproducible from raw data (`python analysis.py`)

---

## Cross-Project Integration

TMPSF data products from this repository are used by:

| Project | File Used | Purpose |
|---------|-----------|---------|
| `miso_my-analysis` | `tmpsf_2015-2026_daily.parquet` | Poster Figure 3: MISO temps + BPR + TMPSF diffuse flow |
| `miso_my-analysis` | `channel_statistics.csv` | Channel regime classification reference |

Exploratory TMPSF figures generated in `miso_my-analysis`:
- `outputs/figures/poster/fig3_poster_temp_bpr_tmpsf.png` — poster figure with TMPSF panel
- `outputs/figures/exploratory/tmpsf_2024_channels_maxima.png`
- `outputs/figures/exploratory/tmpsf_bpr_2024_channels.png`
- `outputs/figures/exploratory/tmpsf_bpr_miso_2024.png`
- `outputs/figures/exploratory/tmpsf_bpr_miso_2024_jul_oct.png`

---

## Notes

- Original scope was 2018-2019; expanded to 2015-2026 to capture April 2015 eruption
- Notebook (Phase 2) preserved as exploratory record; `analysis.py` is the canonical pipeline
- MISO project references TMPSF data via relative path `../my-analysis_tmpsf/outputs/data/`
- Commit after completing each phase
