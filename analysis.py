#!/usr/bin/env python3
"""
analysis.py - ASHES TMPSF Temperature Timeseries Analysis

Analyzes diffuse hydrothermal vent temperature data from the ASHES vent field
at Axial Seamount for 2018-2019, computing daily average temperatures for all
24 thermistor channels.

Usage:
    python analysis.py
"""

import xarray as xr
import pandas as pd
import numpy as np
import hvplot.pandas
from pathlib import Path

# Data paths
DATA_DIR = Path('/home/jovyan/ooi/kdata/RS03ASHS-MJ03B-07-TMPSFA301-streamed-tmpsf_sample')

# Output directories
OUTPUT_DIR = Path(__file__).parent / 'outputs'
DATA_OUTPUT_DIR = OUTPUT_DIR / 'data'
FIGURES_DIR = OUTPUT_DIR / 'figures'

# Time range
TIME_START = '2018-01-01'
TIME_END = '2019-12-31'

# Temperature channels
TEMP_VARS = [f'temperature{i:02d}' for i in range(1, 25)]


def load_data() -> pd.DataFrame:
    """Load NetCDF files containing 2018-2019 data.

    Returns:
        DataFrame with all 24 temperature channels, indexed by time
    """
    print('=' * 60)
    print('ASHES TMPSF Temperature Analysis')
    print(f'Time range: {TIME_START} to {TIME_END}')
    print('=' * 60)

    print(f'\nData directory: {DATA_DIR}')

    nc_files = sorted(DATA_DIR.glob('*.nc'))
    files = [f for f in nc_files if '2018' in f.name or '2019' in f.name]
    print(f'Found {len(files)} files containing 2018-2019 data')

    dfs = []
    for i, f in enumerate(files):
        if i % 5 == 0:
            print(f'  Loading file {i+1}/{len(files)}...')

        ds = xr.open_dataset(f)
        ds = ds.swap_dims({'obs': 'time'})

        available_temp = [v for v in TEMP_VARS if v in ds.data_vars]
        ds_filt = ds[available_temp].sel(time=slice(TIME_START, TIME_END))

        if ds_filt.sizes['time'] > 0:
            dfs.append(ds_filt.to_dataframe())
        ds.close()

    print('Concatenating data chunks...')
    df = pd.concat(dfs).sort_index()
    df = df[~df.index.duplicated(keep='first')]

    print(f'Loaded {len(df):,} observations')
    return df


def validate_data(df: pd.DataFrame) -> None:
    """Run QC checks on the loaded data."""
    print('\nValidating data...')

    # Check time range
    time_min, time_max = df.index.min(), df.index.max()
    assert time_min.year == 2018, f'Data does not start in 2018: {time_min}'
    assert time_max.year == 2019, f'Data does not end in 2019: {time_max}'
    print(f'  Time range: {time_min.date()} to {time_max.date()}')

    # Check temperature channels
    available = [v for v in TEMP_VARS if v in df.columns]
    assert len(available) == 24, f'Missing channels: {len(available)}/24'
    print(f'  All 24 temperature channels present')

    # Check temperature range
    temp_min = df[TEMP_VARS].min().min()
    temp_max = df[TEMP_VARS].max().max()
    print(f'  Temperature range: {temp_min:.2f}°C to {temp_max:.2f}°C')

    if temp_min < 0 or temp_max > 400:
        print(f'  WARNING: Temperature values outside expected range (0-400°C)')


def compute_daily_mean(df: pd.DataFrame) -> pd.DataFrame:
    """Compute daily average temperature for all 24 channels.

    Returns:
        DataFrame with daily mean temperatures
    """
    print('\nComputing daily averages...')
    df_daily = df[TEMP_VARS].resample('D').mean()

    print(f'  {len(df_daily)} daily observations')
    return df_daily


def export_parquet(df: pd.DataFrame, df_daily: pd.DataFrame) -> None:
    """Export cleaned data to Parquet files."""
    print('\nExporting data...')
    DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Export raw (high-frequency) data
    raw_path = DATA_OUTPUT_DIR / 'tmpsf_2018-2019_raw.parquet'
    df.to_parquet(raw_path)
    print(f'  Exported: data/{raw_path.name} ({len(df):,} rows)')

    # Export daily averages
    daily_path = DATA_OUTPUT_DIR / 'tmpsf_2018-2019_daily.parquet'
    df_daily.to_parquet(daily_path)
    print(f'  Exported: data/{daily_path.name} ({len(df_daily)} rows)')


def create_plot(df_daily: pd.DataFrame) -> None:
    """Create interactive timeseries plot with all 24 channels."""
    print('\nGenerating plot...')
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    plot = df_daily.hvplot.line(
        title='ASHES Vent Field - All 24 Temperature Channels (2018-2019)',
        xlabel='Date',
        ylabel='Temperature (°C)',
        width=1000,
        height=500,
        legend='right',
        grid=True
    )

    output_path = FIGURES_DIR / 'tmpsf_2018-2019_all_channels.html'
    hvplot.save(plot, output_path)
    print(f'  Saved: figures/{output_path.name}')


def print_summary(df_daily: pd.DataFrame) -> None:
    """Print analysis summary."""
    print('\n' + '=' * 60)
    print('Summary')
    print('=' * 60)
    print(f'Date range: {df_daily.index.min().date()} to {df_daily.index.max().date()}')
    print(f'Number of days: {len(df_daily)}')
    print(f'Number of channels: 24')

    all_temps = df_daily[TEMP_VARS].values.flatten()
    all_temps = all_temps[~np.isnan(all_temps)]
    print(f'Temperature range: {all_temps.min():.2f}°C to {all_temps.max():.2f}°C')
    print(f'Mean temperature: {all_temps.mean():.2f}°C')
    print(f'Std deviation: {all_temps.std():.2f}°C')


def main():
    """Run the full analysis pipeline."""
    # Load data
    df = load_data()

    # Validate
    validate_data(df)

    # Compute daily stats
    df_daily = compute_daily_mean(df)

    # Export to Parquet
    export_parquet(df, df_daily)

    # Create plot
    create_plot(df_daily)

    # Print summary
    print_summary(df_daily)

    print('\nDone!')
    return df, df_daily


if __name__ == '__main__':
    df, df_daily = main()
