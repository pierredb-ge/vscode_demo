# -*- coding: utf-8 -*-
"""
Created on Sun May 04, 2026

Overview:
    FOR DEMO PURPOSES ONLY! Loads a daily CIMIS hydrology time series, fits a
    linear regression of cumulative ET as a function of cumulative precipitation
    using NumPy, and produces two plots: a scatter of cumulative ET vs cumulative
    P with the regression line, and a time series of daily P, ET, and cumulative totals.

Instructions:
    1. Update input_path to point to the Excel file if it has moved.

Notes:
    1. Cumulative sums are computed over the full period of record; NaNs are
       treated as zero for the running total.
    2. The regression slope is directly interpretable as the fraction of
       cumulative P that becomes ET over the period.
    3. All regression math uses NumPy (np.polyfit / np.polyval).


@authors: PDalBianco
"""
# %%
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# %%
###############################################################################
### File paths ################################################################
###############################################################################
# Import path
input_path = Path(
    r"C:\_DE\Davids Engineering\DE_Development - Documents"
    r"\Training\20260430_DE_Techathon\Spatial Hydrology\Python"
    r"\exports\daily_timeseries_cimis_techathon_v1.xlsx"
)

# %%
###############################################################################
### Load data #################################################################
###############################################################################

raw_df = pd.read_excel(input_path, sheet_name="Daily Timeseries")

date_arr = raw_df["date"].values.astype("datetime64[D]")
p_arr = raw_df["P_in"].values.astype(float)
et_arr = raw_df["ET_in"].values.astype(float)

# Compute cumulative sums

cum_p_arr = np.nancumsum(p_arr)
cum_et_arr = np.nancumsum(et_arr)

# %%
###############################################################################
### Fit linear regression on cumulative values ################################
###############################################################################

# Force regression through origin: ET_cum = slope * P_cum
# Using least-squares: slope = sum(x*y) / sum(x*x)
# Important: work on cumulated rasters!!
slope = np.dot(p_arr, cum_et_arr) / np.dot(cum_p_arr, cum_p_arr)

reg_cum_arr = slope * cum_p_arr # regression-predicted cumulative ET

ss_res = np.sum((cum_et_arr - reg_cum_arr) ** 2)
ss_tot = np.sum((cum_et_arr - np.mean(cum_et_arr)) ** 2)
r_sq = 1.0 - ss_res / ss_tot

print(f"Slope (ET/P fraction): {slope:.4f}")

# # %%
# ###############################################################################
# ### Regression residual statistics ############################################
# ###############################################################################

# residuals_arr = cum_et_arr - reg_cum_arr
# rmse = np.sqrt(np.mean(residuals_arr ** 2))
# mae = np.mean(np.abs(residuals_arr))
# max_err = np.max(np.abs(residuals_arr))

# print(f"RMSE (cumulative ET) : {rmse:.4f} in")
# print(f"MAE  (cumulative ET) : {mae:.4f} in")
# print(f"Max error            : {max_err:.4f} in")

# %%
###############################################################################
### Plot ######################################################################
###############################################################################

fig, (ax_scatter, ax_ts) = plt.subplots(
    2, 1, figsize=(12, 8), constrained_layout=True
)

# --- scatter: cumulative ET vs cumulative P with regression line ---
p_line_arr = np.linspace(0, np.nanmax(cum_p_arr), 200)
et_line_arr = slope * p_line_arr

ax_scatter.scatter(
    cum_p_arr, cum_et_arr,
    s=12, alpha=0.5, color="steelblue", label="Observed (cumulative)"
)
ax_scatter.plot(
    p_line_arr, et_line_arr,
    color="tomato", linewidth=2,
    label=f"Regression  ET = {slope:.3f} P  (R² = {r_sq:.4f})"
)
ax_scatter.set_xlabel("Cumulative P (in)")
ax_scatter.set_ylabel("Cumulative ET (in)")
ax_scatter.set_title("Cumulative ET vs Cumulative P -- Linear Regression (through origin)")
ax_scatter.legend(fontsize=9)
ax_scatter.grid(True, linewidth=0.4, alpha=0.6)

# --- time series: daily P & ET (bars) + cumulative totals (lines) ---
date_plot = date_arr.astype("datetime64[ms]").astype(object)

ax_ts2 = ax_ts.twinx()

ax_ts.bar(date_plot, p_arr, color="steelblue", alpha=0.4, width=1.0, label="Daily P (in)")
ax_ts.bar(date_plot, et_arr, color="seagreen", alpha=0.4, width=1.0, label="Daily ET (in)")
ax_ts2.plot(date_plot, cum_p_arr, color="steelblue", linewidth=1.5, label="Cumulative P (in)")
ax_ts2.plot(date_plot, cum_et_arr, color="seagreen", linewidth=1.5, label="Cumulative ET (in)")
ax_ts2.plot(
    date_plot, reg_cum_arr,
    color="tomato", linewidth=1.5, linestyle="--", label="Cumulative ET regression (in)"
)

ax_ts.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax_ts.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.setp(ax_ts.xaxis.get_majorticklabels(), rotation=45, ha="right")
ax_ts.set_xlabel("Date")
ax_ts.set_ylabel("Daily (in)")
ax_ts2.set_ylabel("Cumulative (in)")
ax_ts.set_title("Daily and Cumulative P & ET Time Series")

lines1, labels1 = ax_ts.get_legend_handles_labels()
lines2, labels2 = ax_ts2.get_legend_handles_labels()
ax_ts.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc="upper left")
ax_ts.grid(True, linewidth=0.4, alpha=0.6)

# %%
plt.show()

# %%
