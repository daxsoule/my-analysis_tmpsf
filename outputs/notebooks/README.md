# ASHES TMPSF Temperature Analysis Notebook

This folder contains a reproducible Jupyter notebook for analyzing diffuse hydrothermal vent temperature data from the ASHES vent field at Axial Seamount.

## Contents

- `01_explore_tmpsf.ipynb` - Exploratory analysis notebook
- `environment.yml` - Conda environment specification
- `README.md` - This file

## Quick Start

1. **Create the conda environment:**
   ```bash
   conda env create -f environment.yml
   conda activate ashes-tmpsf-analysis
   ```

2. **Launch Jupyter:**
   ```bash
   jupyter lab
   ```

3. **Open the notebook** and update the data paths if needed.

## Data Requirements

You will need access to OOI TMPSF data from:
- RS03ASHS-MJ03B-07-TMPSFA301-streamed-tmpsf_sample

Data can be obtained from the OOI Data Portal: https://ooinet.oceanobservatories.org/
