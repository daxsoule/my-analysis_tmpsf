"""
ASHES TMPSF Timeseries Analysis - 2018 Daily Averages

Analyzes diffuse hydrothermal vent temperature data from the ASHES vent field
for the year 2018, computing daily average temperatures across all 24 thermistor
channels and generating an interactive plot.

Usage:
    uv run python analyze_tmpsf_2018.py
"""

import xarray as xr
import pandas as pd
import numpy as np
import hvplot.pandas
from pathlib import Path

# Configuration
DATA_DIR = Path('/home/jovyan/ooi/kdata/RS03ASHS-MJ03B-07-TMPSFA301-streamed-tmpsf_sample')
OUTPUT_DIR = Path('/home/jovyan/my_data/axial/axial_tmpsf')
FIGURE_DIR = Path('outputs/figures')
START_DATE = '2018-01-01'
END_DATE = '2018-12-31'


def load_2018_data():
    """Load NetCDF files containing 2018 data."""
    print('=== Phase 1: Setup ===')
    print(f'Data directory: {DATA_DIR}')
    print(f'Analysis period: {START_DATE} to {END_DATE}')

    print('\n=== Phase 2: Data Loading ===')
    nc_files = sorted(DATA_DIR.glob('*.nc'))
    files_2018 = [f for f in nc_files if '2018' in f.name]
    print(f'Found {len(files_2018)} files containing 2018 data')

    temp_vars = [f'temperature{i:02d}' for i in range(1, 25)]
    dfs = []
    available_temp = None

    for i, f in enumerate(files_2018):
        print(f'  [{i+1}/{len(files_2018)}] Loading {f.name[:50]}...')
        ds = xr.open_dataset(f)
        ds = ds.swap_dims({'obs': 'time'})

        available_temp = [v for v in temp_vars if v in ds.data_vars]
        ds_filt = ds[available_temp].sel(time=slice(START_DATE, END_DATE))

        if ds_filt.sizes['time'] > 0:
            dfs.append(ds_filt.to_dataframe())
        ds.close()

    print('Concatenating data chunks...')
    df = pd.concat(dfs)
    print(f'Combined DataFrame shape: {df.shape}')

    return df, available_temp


def validate_data(df, available_temp):
    """Run QC checks on the loaded data."""
    print('\n=== Phase 2 QC: Verification ===')

    # T007: Check time range
    time_min, time_max = df.index.min(), df.index.max()
    assert time_min.year == 2018, f'Data starts before 2018: {time_min}'
    assert time_max.year == 2018, f'Data ends after 2018: {time_max}'
    print(f'✓ T007: Time range verified: {time_min.date()} to {time_max.date()}')

    # T008: Check temperature channels
    assert len(available_temp) == 24, f'Missing channels: {len(available_temp)}/24'
    print(f'✓ T008: All 24 temperature channels present')

    print('\n=== Phase 3: QC Assessment ===')
    temp_min = df[available_temp].min().min()
    temp_max = df[available_temp].max().max()
    print(f'Temperature range: {temp_min:.2f}°C to {temp_max:.2f}°C')

    if 0 < temp_min and temp_max < 100:
        print('✓ T012: Temperature values within reasonable range')


def compute_daily_averages(df, available_temp):
    """Compute daily average temperature across all channels."""
    print('\n=== Phase 4: Daily Averaging ===')

    df['temp_mean'] = df[available_temp].mean(axis=1)
    df_daily = df['temp_mean'].resample('D').mean().to_frame()
    df_daily.columns = ['daily_avg_temp']

    print(f'Daily averages shape: {df_daily.shape}')
    print(f'Date range: {df_daily.index.min().date()} to {df_daily.index.max().date()}')
    print(f'Number of days: {len(df_daily)}')

    # T017 QC
    expected_days = 365
    if len(df_daily) == expected_days:
        print(f'✓ T017: Daily averages has {len(df_daily)} rows (full year)')
    else:
        print(f'⚠ T017: Missing {expected_days - len(df_daily)} days')

    return df_daily


def create_plot(df_daily):
    """Create interactive timeseries plot."""
    print('\n=== Phase 5: Visualization ===')

    plot = df_daily.hvplot.line(
        y='daily_avg_temp',
        title='ASHES Vent Field - Daily Average Temperature (2018)',
        xlabel='Date',
        ylabel='Temperature (°C)',
        width=900,
        height=400,
        grid=True
    )

    # Save plot
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURE_DIR / 'tmpsf_2018_daily.html'
    hvplot.save(plot, output_path)
    print(f'Plot saved to: {output_path}')

    return plot


def print_summary(df_daily):
    """Print analysis summary."""
    print('\n=== Summary ===')
    print(f'Date range: {df_daily.index.min().date()} to {df_daily.index.max().date()}')
    print(f'Number of days: {len(df_daily)}')
    print(f'Temperature range: {df_daily["daily_avg_temp"].min():.2f}°C to {df_daily["daily_avg_temp"].max():.2f}°C')
    print(f'Mean temperature: {df_daily["daily_avg_temp"].mean():.2f}°C')
    print(f'Std deviation: {df_daily["daily_avg_temp"].std():.2f}°C')


def main():
    """Run the full analysis pipeline."""
    # Load data
    df, available_temp = load_2018_data()

    # Validate
    validate_data(df, available_temp)

    # Compute daily averages
    df_daily = compute_daily_averages(df, available_temp)

    # Create plot
    create_plot(df_daily)

    # Print summary
    print_summary(df_daily)

    print('\n✓ Analysis complete!')

    return df_daily


if __name__ == '__main__':
    df_daily = main()
