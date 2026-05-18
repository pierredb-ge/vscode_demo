# Data Science and modeling Demo

> **Toy project, for demo purposes only.** This repo was built for a live coding demonstration on VSCode for a working group. The code and data are not intended for production use or technical conclusions.

Live demo script fitting a cumulative ET vs cumulative precipitation regression from a CIMIS daily hydrology time series.

## Overview

This demo illustrates a water balance regression approach where cumulative evapotranspiration is modeled as a linear function of cumulative precipitation (forced through the origin). The slope is directly interpretable as the fraction of precipitation that becomes ET over the period of record. Intended as a live coding demonstration for the DE Techathon (April 2026).

## Environment

`geos2025`

## Pipeline

- `0001_et_p_regression.py`: load daily CIMIS time series, fit cumulative ET = slope * cumulative P using NumPy, and plot scatter and time series results

## Paths

- Input data: `C:\_DE\Davids Engineering\DE_Development - Documents\Training\20260430_DE_Techathon\Spatial Hydrology\Python\exports\`

## Data

### Inputs

| Name | Source | Resolution | Periodicity |
|---|---|---|---|
| `daily_timeseries_cimis_techathon_v2.xlsx` | CIMIS / internal water balance model | Daily | Water year 2024-2025 |

### Outputs

None, plots displayed interactively.

## References

- CIMIS: California Irrigation Management Information System, CA Dept. of Water Resources
