#!/usr/bin/env python3
"""
analysis.py - ASHES TMPSF Temperature Timeseries Analysis

Analyzes diffuse hydrothermal vent temperature data from the ASHES vent field
at Axial Seamount for 2015-2026, computing daily average temperatures for all
24 thermistor channels with channel characterization and publication-quality figures.

Usage:
    python analysis.py
"""

import re
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Matplotlib style settings for publication-quality figures
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 100,
    'savefig.dpi': 300,
})

# Data paths
DATA_DIR = Path('/home/jovyan/ooi/kdata/RS03ASHS-MJ03B-07-TMPSFA301-streamed-tmpsf_sample')

# Output directories
OUTPUT_DIR = Path(__file__).parent / 'outputs'
DATA_OUTPUT_DIR = OUTPUT_DIR / 'data'
FIGURES_DIR = OUTPUT_DIR / 'figures'

# Time range (extended to capture April 2015 eruption through present)
TIME_START = '2015-01-01'
TIME_END = '2026-01-25'

# Temperature channels
TEMP_VARS = [f'temperature{i:02d}' for i in range(1, 25)]

# QARTOD QC variables (1=pass, 2=not evaluated, 3=suspect, 4=fail, 9=missing)
QARTOD_VARS = [f'{v}_qartod_results' for v in TEMP_VARS]
QARTOD_PASS = 1

# Cross-channel consistency threshold (°C above median to flag as suspect)
# Single-channel spikes exceeding this threshold above the median of other channels are flagged
CONSISTENCY_THRESHOLD = 10.0

# Regex pattern to extract year from filename
YEAR_PATTERN = re.compile(r'(\d{4})\d{4}T')


def extract_years_from_filename(filename: str) -> set:
    """Extract years covered by a NetCDF file from its filename.

    Args:
        filename: NetCDF filename containing date ranges

    Returns:
        Set of years covered by the file
    """
    matches = YEAR_PATTERN.findall(filename)
    return set(int(y) for y in matches)


def load_data() -> tuple[pd.DataFrame, dict]:
    """Load NetCDF files containing data within the time range.

    Uses regex-based year extraction for file filtering, QARTOD QC filtering,
    and hourly resampling for memory-efficient loading of multi-year data.

    Returns:
        Tuple of (DataFrame with QC-filtered temperature data, QC statistics dict)
    """
    print('=' * 60)
    print('ASHES TMPSF Temperature Analysis')
    print(f'Time range: {TIME_START} to {TIME_END}')
    print('=' * 60)

    print(f'\nData directory: {DATA_DIR}')

    # Parse target year range
    start_year = int(TIME_START[:4])
    end_year = int(TIME_END[:4])
    target_years = set(range(start_year, end_year + 1))

    # Filter files by year using regex extraction
    nc_files = sorted(DATA_DIR.glob('*.nc'))
    files = []
    for f in nc_files:
        file_years = extract_years_from_filename(f.name)
        if file_years & target_years:  # intersection
            files.append(f)

    print(f'Found {len(files)} files containing {start_year}-{end_year} data')

    dfs = []
    qc_counts = {var: {'total': 0, 'passed': 0, 'failed': 0} for var in TEMP_VARS}

    for i, f in enumerate(files):
        if i % 10 == 0:
            print(f'  Loading file {i+1}/{len(files)}...')

        ds = xr.open_dataset(f)
        ds = ds.swap_dims({'obs': 'time'})

        # Get available temperature and QC variables
        available_temp = [v for v in TEMP_VARS if v in ds.data_vars]
        available_qc = [v for v in QARTOD_VARS if v in ds.data_vars]

        # Load both temp and QC data
        vars_to_load = available_temp + available_qc
        ds_filt = ds[vars_to_load].sel(time=slice(TIME_START, TIME_END))

        if ds_filt.sizes['time'] > 0:
            df_chunk = ds_filt.to_dataframe()

            # Apply QARTOD filtering: mask values where QC != 1 (pass)
            for temp_var in available_temp:
                qc_var = f'{temp_var}_qartod_results'
                if qc_var in df_chunk.columns:
                    n_total = df_chunk[temp_var].notna().sum()
                    qc_mask = df_chunk[qc_var] != QARTOD_PASS
                    n_failed = qc_mask.sum()

                    # Set failed QC values to NaN
                    df_chunk.loc[qc_mask, temp_var] = np.nan

                    qc_counts[temp_var]['total'] += n_total
                    qc_counts[temp_var]['failed'] += n_failed
                    qc_counts[temp_var]['passed'] += (n_total - n_failed)

            # Keep only temperature columns and resample to hourly
            df_chunk = df_chunk[available_temp]
            df_hourly = df_chunk.resample('h').mean()
            dfs.append(df_hourly)
        ds.close()

    print('Concatenating data chunks...')
    df = pd.concat(dfs).sort_index()
    df = df[~df.index.duplicated(keep='first')]

    print(f'Loaded {len(df):,} hourly observations')
    return df, qc_counts


def report_qc_stats(qc_counts: dict) -> None:
    """Report QC filtering statistics."""
    print('\nQARTOD QC filtering results:')
    print('  (1=pass, 4=fail - failed values set to NaN)')

    total_all = sum(c['total'] for c in qc_counts.values())
    failed_all = sum(c['failed'] for c in qc_counts.values())
    pct_failed = (failed_all / total_all * 100) if total_all > 0 else 0

    print(f'  Total observations: {total_all:,}')
    print(f'  Failed QC: {failed_all:,} ({pct_failed:.2f}%)')

    # Report channels with high failure rates
    high_fail = []
    for var, counts in qc_counts.items():
        if counts['total'] > 0:
            fail_pct = counts['failed'] / counts['total'] * 100
            if fail_pct > 1.0:  # More than 1% failed
                channel = int(var.replace('temperature', ''))
                high_fail.append((channel, fail_pct, counts['failed']))

    if high_fail:
        print('\n  Channels with >1% QC failures:')
        for ch, pct, n in sorted(high_fail, key=lambda x: -x[1]):
            print(f'    Channel {ch:02d}: {pct:5.1f}% failed ({n:,} values)')


def apply_cross_channel_consistency(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Apply cross-channel consistency check to flag single-channel spikes.

    For each observation, compares each channel's value to the median of all
    other channels. Values exceeding the median by more than CONSISTENCY_THRESHOLD
    are set to NaN as likely sensor artifacts.

    This catches sensor issues that passed QARTOD QC but show physically
    implausible single-channel behavior.

    Args:
        df: DataFrame with temperature data (all 24 channels)

    Returns:
        Tuple of (filtered DataFrame, statistics dict with flagged counts per channel)
    """
    print(f'\nApplying cross-channel consistency check (threshold: {CONSISTENCY_THRESHOLD}C)...')

    df_filtered = df.copy()
    consistency_stats = {var: {'flagged': 0, 'total': 0} for var in TEMP_VARS}

    # Get temperature data as array for efficient computation
    temp_data = df_filtered[TEMP_VARS].values  # shape: (n_times, 24)
    n_times, n_channels = temp_data.shape

    # For each channel, compute median of OTHER channels and compare
    flagged_mask = np.zeros_like(temp_data, dtype=bool)

    for i, var in enumerate(TEMP_VARS):
        # Get indices of other channels
        other_indices = [j for j in range(n_channels) if j != i]

        # Compute median of other channels for each timestamp
        other_median = np.nanmedian(temp_data[:, other_indices], axis=1)

        # Flag where this channel exceeds median + threshold
        channel_values = temp_data[:, i]
        exceeds_threshold = channel_values > (other_median + CONSISTENCY_THRESHOLD)

        # Only flag non-NaN values
        valid_mask = ~np.isnan(channel_values)
        flagged = exceeds_threshold & valid_mask

        flagged_mask[:, i] = flagged
        consistency_stats[var]['flagged'] = int(flagged.sum())
        consistency_stats[var]['total'] = int(valid_mask.sum())

    # Apply mask - set flagged values to NaN
    temp_data_filtered = temp_data.copy()
    temp_data_filtered[flagged_mask] = np.nan
    df_filtered[TEMP_VARS] = temp_data_filtered

    # Report results
    total_flagged = sum(s['flagged'] for s in consistency_stats.values())
    total_obs = sum(s['total'] for s in consistency_stats.values())
    pct_flagged = (total_flagged / total_obs * 100) if total_obs > 0 else 0

    print(f'  Total values checked: {total_obs:,}')
    print(f'  Flagged as inconsistent: {total_flagged:,} ({pct_flagged:.3f}%)')

    # Report channels with flagged values
    channels_flagged = []
    for var, stats in consistency_stats.items():
        if stats['flagged'] > 0:
            channel = int(var.replace('temperature', ''))
            pct = stats['flagged'] / stats['total'] * 100 if stats['total'] > 0 else 0
            channels_flagged.append((channel, pct, stats['flagged']))

    if channels_flagged:
        print('\n  Channels with flagged values:')
        for ch, pct, n in sorted(channels_flagged, key=lambda x: -x[2]):
            print(f'    Channel {ch:02d}: {n:,} values ({pct:.2f}%)')

    return df_filtered, consistency_stats


def validate_data(df: pd.DataFrame) -> None:
    """Run QC checks on the loaded data."""
    print('\nValidating data...')

    # Check time range
    time_min, time_max = df.index.min(), df.index.max()
    start_year = int(TIME_START[:4])
    end_year = int(TIME_END[:4])

    assert time_min.year >= start_year - 1, f'Data starts too early: {time_min}'
    assert time_max.year <= end_year + 1, f'Data ends too late: {time_max}'
    print(f'  Time range: {time_min.date()} to {time_max.date()}')

    # Calculate data coverage
    total_days = (time_max - time_min).days
    print(f'  Data spans {total_days:,} days ({total_days / 365.25:.1f} years)')

    # Check temperature channels
    available = [v for v in TEMP_VARS if v in df.columns]
    assert len(available) == 24, f'Missing channels: {len(available)}/24'
    print(f'  All 24 temperature channels present')

    # Check temperature range
    temp_min = df[TEMP_VARS].min().min()
    temp_max = df[TEMP_VARS].max().max()
    print(f'  Temperature range: {temp_min:.2f}C to {temp_max:.2f}C')

    if temp_min < 0 or temp_max > 400:
        print(f'  WARNING: Temperature values outside expected range (0-400C)')


def compute_daily_mean(df: pd.DataFrame) -> pd.DataFrame:
    """Compute daily average temperature for all 24 channels.

    Returns:
        DataFrame with daily mean temperatures
    """
    print('\nComputing daily averages...')
    df_daily = df[TEMP_VARS].resample('D').mean()

    print(f'  {len(df_daily)} daily observations')
    return df_daily


def characterize_channels(df_daily: pd.DataFrame) -> pd.DataFrame:
    """Compute per-channel statistics and characterization.

    Calculates mean, std, min, max, range, and coefficient of variation
    for each channel. Identifies "hot" vs "cool" channels and ranks by
    variability.

    Args:
        df_daily: DataFrame with daily mean temperatures

    Returns:
        DataFrame with channel statistics, sorted by mean temperature
    """
    print('\nCharacterizing channels...')

    stats = []
    for var in TEMP_VARS:
        data = df_daily[var].dropna()
        channel_num = int(var.replace('temperature', ''))

        mean_temp = data.mean()
        std_temp = data.std()
        min_temp = data.min()
        max_temp = data.max()
        range_temp = max_temp - min_temp
        cv = (std_temp / mean_temp * 100) if mean_temp > 0 else np.nan

        stats.append({
            'channel': channel_num,
            'variable': var,
            'mean': mean_temp,
            'std': std_temp,
            'min': min_temp,
            'max': max_temp,
            'range': range_temp,
            'cv_percent': cv,
            'n_obs': len(data)
        })

    df_stats = pd.DataFrame(stats)

    # Classify channels by temperature regime
    median_mean = df_stats['mean'].median()
    df_stats['regime'] = df_stats['mean'].apply(
        lambda x: 'hot' if x > median_mean else 'cool'
    )

    # Rank by mean temperature (1 = coolest)
    df_stats['temp_rank'] = df_stats['mean'].rank(method='min').astype(int)

    # Rank by variability (1 = most variable)
    df_stats['variability_rank'] = df_stats['cv_percent'].rank(
        method='min', ascending=False
    ).astype(int)

    # Sort by mean temperature
    df_stats = df_stats.sort_values('mean').reset_index(drop=True)

    print(f'  Channel temperature range: {df_stats["mean"].min():.2f}C to {df_stats["mean"].max():.2f}C')
    print(f'  Hot channels (above median): {(df_stats["regime"] == "hot").sum()}')
    print(f'  Cool channels (below median): {(df_stats["regime"] == "cool").sum()}')
    print(f'  Most variable channel: temperature{df_stats.loc[df_stats["variability_rank"] == 1, "channel"].values[0]:02d}')

    return df_stats


def get_date_range_str() -> str:
    """Get date range string for filenames."""
    start_year = TIME_START[:4]
    end_year = TIME_END[:4]
    return f'{start_year}-{end_year}'


def export_parquet(df: pd.DataFrame, df_daily: pd.DataFrame) -> None:
    """Export cleaned data to Parquet files."""
    print('\nExporting data...')
    DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    date_range = get_date_range_str()

    # Export hourly data (memory-efficient version of raw)
    hourly_path = DATA_OUTPUT_DIR / f'tmpsf_{date_range}_hourly.parquet'
    df.to_parquet(hourly_path)
    print(f'  Exported: data/{hourly_path.name} ({len(df):,} rows)')

    # Export daily averages
    daily_path = DATA_OUTPUT_DIR / f'tmpsf_{date_range}_daily.parquet'
    df_daily.to_parquet(daily_path)
    print(f'  Exported: data/{daily_path.name} ({len(df_daily)} rows)')


def export_channel_stats(df_stats: pd.DataFrame) -> None:
    """Export channel statistics to CSV."""
    DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stats_path = DATA_OUTPUT_DIR / 'channel_statistics.csv'
    df_stats.to_csv(stats_path, index=False, float_format='%.3f')
    print(f'  Exported: data/{stats_path.name}')


def plot_all_channels(df_daily: pd.DataFrame, df_stats: pd.DataFrame) -> None:
    """Create full timeseries overview with all 24 channels.

    Color-coded by mean temperature (hot=red, cool=blue).
    """
    print('\nGenerating full timeseries plot...')
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Create colormap based on mean temperature
    temp_means = df_stats.set_index('variable')['mean']
    norm = plt.Normalize(temp_means.min(), temp_means.max())
    cmap = plt.cm.coolwarm

    for var in TEMP_VARS:
        color = cmap(norm(temp_means[var]))
        ax.plot(df_daily.index, df_daily[var], color=color, alpha=0.7, linewidth=0.5)

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, label='Mean Temperature (C)')

    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (C)')
    ax.set_title(f'ASHES Vent Field - All 24 Temperature Channels ({get_date_range_str()})')

    # Clean up spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = FIGURES_DIR / 'tmpsf_all_channels.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'  Saved: figures/{output_path.name}')


def plot_channel_stats(df_stats: pd.DataFrame) -> None:
    """Create bar chart of mean temperatures by channel with error bars."""
    print('Generating channel characterization plot...')
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 4))

    # Sort by mean temperature for the plot
    df_sorted = df_stats.sort_values('mean')

    x = range(len(df_sorted))
    colors = ['#2166ac' if r == 'cool' else '#b2182b' for r in df_sorted['regime']]

    bars = ax.bar(x, df_sorted['mean'], yerr=df_sorted['std'],
                  color=colors, capsize=2, alpha=0.8, edgecolor='black', linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels([f'{c:02d}' for c in df_sorted['channel']], fontsize=8)
    ax.set_xlabel('Channel Number')
    ax.set_ylabel('Mean Temperature (C)')
    ax.set_title('Channel Mean Temperatures (ranked coolest to hottest)')

    # Clean up spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2166ac', label='Cool channels'),
        Patch(facecolor='#b2182b', label='Hot channels')
    ]
    ax.legend(handles=legend_elements, loc='upper left')

    plt.tight_layout()
    output_path = FIGURES_DIR / 'channel_characterization.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'  Saved: figures/{output_path.name}')


def plot_hot_vs_cool(df_daily: pd.DataFrame, df_stats: pd.DataFrame) -> None:
    """Create overlay of hottest 3 and coolest 3 channels."""
    print('Generating hot vs cool comparison plot...')
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Get top 3 hottest and coolest
    df_sorted = df_stats.sort_values('mean')
    coolest_3 = df_sorted.head(3)['variable'].tolist()
    hottest_3 = df_sorted.tail(3)['variable'].tolist()

    fig, ax = plt.subplots(figsize=(8, 4))

    # Plot cool channels in blue shades
    cool_colors = ['#4393c3', '#2166ac', '#053061']
    for i, var in enumerate(coolest_3):
        channel = int(var.replace('temperature', ''))
        ax.plot(df_daily.index, df_daily[var], color=cool_colors[i],
                alpha=0.8, linewidth=0.8, label=f'Ch {channel:02d} (cool)')

    # Plot hot channels in red shades
    hot_colors = ['#d6604d', '#b2182b', '#67001f']
    for i, var in enumerate(hottest_3):
        channel = int(var.replace('temperature', ''))
        ax.plot(df_daily.index, df_daily[var], color=hot_colors[i],
                alpha=0.8, linewidth=0.8, label=f'Ch {channel:02d} (hot)')

    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (C)')
    ax.set_title(f'Hot vs Cool Channels Comparison ({get_date_range_str()})')

    # Clean up spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.legend(loc='upper right', fontsize=8, ncol=2)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = FIGURES_DIR / 'hot_vs_cool_channels.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'  Saved: figures/{output_path.name}')


def print_summary(df_daily: pd.DataFrame, df_stats: pd.DataFrame) -> None:
    """Print analysis summary."""
    print('\n' + '=' * 60)
    print('Summary')
    print('=' * 60)
    print(f'Date range: {df_daily.index.min().date()} to {df_daily.index.max().date()}')
    print(f'Number of days: {len(df_daily)}')
    print(f'Number of channels: 24')

    all_temps = df_daily[TEMP_VARS].values.flatten()
    all_temps = all_temps[~np.isnan(all_temps)]
    print(f'Temperature range: {all_temps.min():.2f}C to {all_temps.max():.2f}C')
    print(f'Mean temperature: {all_temps.mean():.2f}C')
    print(f'Std deviation: {all_temps.std():.2f}C')

    print('\nChannel Summary:')
    print(f'  Coolest channel: temperature{df_stats.iloc[0]["channel"]:02.0f} ({df_stats.iloc[0]["mean"]:.2f}C)')
    print(f'  Hottest channel: temperature{df_stats.iloc[-1]["channel"]:02.0f} ({df_stats.iloc[-1]["mean"]:.2f}C)')


def main():
    """Run the full analysis pipeline."""
    # Load data with QARTOD QC filtering
    df, qc_counts = load_data()

    # Report QARTOD QC statistics
    report_qc_stats(qc_counts)

    # Apply cross-channel consistency check
    df, consistency_stats = apply_cross_channel_consistency(df)

    # Validate
    validate_data(df)

    # Compute daily stats
    df_daily = compute_daily_mean(df)

    # Characterize channels
    df_stats = characterize_channels(df_daily)

    # Export to Parquet
    export_parquet(df, df_daily)
    export_channel_stats(df_stats)

    # Create publication-quality figures
    plot_all_channels(df_daily, df_stats)
    plot_channel_stats(df_stats)
    plot_hot_vs_cool(df_daily, df_stats)

    # Print summary
    print_summary(df_daily, df_stats)

    print('\nDone!')
    return df, df_daily, df_stats


if __name__ == '__main__':
    df, df_daily, df_stats = main()
