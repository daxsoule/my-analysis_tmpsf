# Analysis Specification: ASHES TMPSF Timeseries

**Directory**: `specs/001-ashes-tmpsf-timeseries`
**Created**: 2026-01-22
**Status**: Draft

## Research Question(s)

1. How does diffuse hydrothermal vent temperature vary as a function of time for the years 2018-2019 at the ASHES vent field?

## Data Description

### Primary Data

- **Source**: Ocean Observatories Initiative (OOI) TMPSF sensor
- **Site**: ASHES vent field, Axial Seamount (45.933653°N, 130.013688°W)
- **Reference designator**: RS03ASHS-MJ03B-07-TMPSFA301-streamed-tmpsf_sample
- **Coverage**: 2014-09-29 to 2026-01-22 (analysis focus: 2018-2019)
- **Format**: NetCDF (.nc), 253 files across 2 deployments
- **Access**: Local files at `/home/jovyan/ooi/kdata/RS03ASHS-MJ03B-07-TMPSFA301-streamed-tmpsf_sample/`
- **Variables**: temperature01-24 (24 thermistor channels), with QARTOD and QC flags
- **Known issues**: [TODO: Document any data gaps or quality issues discovered during analysis]

## Methods Overview

1. **Data preparation**:
   - Load all NetCDF files from the data directory
   - Concatenate into a single xarray Dataset
   - Filter to 2018-2019 timeframe
   - Apply QC flags to identify suspect data
   - Convert to pandas DataFrame for exploration

2. **Analysis approach**:
   - Compute daily average temperature for all 24 channels
   - Exploratory visualization of the 2018-2019 temperature timeseries
   - Interactive plotting of all 24 channels to examine temporal patterns and anomalies

3. **Validation**:
   - Check that temperature values fall within reasonable range for diffuse vents
   - Verify temporal continuity and identify any gaps
   - Use QARTOD/QC flags to assess data quality

**Justification**: Interactive visualization enables rapid exploration of a multi-year, high-frequency dataset to identify patterns, gaps, and features of interest before more detailed analysis.

## Expected Outputs

### Data Products

- **Concatenated DataFrame**: Pandas DataFrame containing the 2018-2019 timeseries (time, temperature channels, QC flags) for interactive exploration

### Figures

- **Figure 1**: Interactive hvplot timeseries showing all 24 temperature channels vs. time for 2018-2019

## Validation Approach

- Temperature values should be within reasonable range for diffuse hydrothermal vents (typically 2-50°C, but verify against literature)
- Time coordinate should be monotonically increasing within each file
- QARTOD flags should be checked: flag values of 1 (pass) or 2 (not evaluated) are acceptable; 3 (suspect) and 4 (fail) should be flagged or filtered
- No duplicate timestamps after concatenation

## Completion Criteria

- [ ] NetCDF files loaded and concatenated
- [ ] Data filtered to 2018-2019 timeframe
- [ ] QC flags applied to identify suspect data
- [ ] Concatenated DataFrame available for exploration
- [ ] Daily average temperature computed for all 24 channels
- [ ] Interactive timeseries plot showing all 24 channels generated
- [ ] Results reproducible from raw data

## Assumptions & Limitations

**Assumptions**:
- Local NetCDF files are complete and uncorrupted copies of OOI data
- QARTOD/QC flags in the data files are reliable for quality assessment
- All 24 temperature channels are relevant (may focus on subset if needed)

**Limitations**:
- This is exploratory analysis only - no statistical modeling or hypothesis testing
- Does not address causes of temperature variability (e.g., tidal, volcanic, seasonal)
- Limited to single site (ASHES vent field) and single instrument

## Notes

- Data actually extends back to 2014-09-29, but analysis focus is 2018-2019 per user specification
- 24 thermistor channels may represent different probe locations - spatial arrangement TBD
- Future work may expand to other TMPSF instruments at Axial Seamount
