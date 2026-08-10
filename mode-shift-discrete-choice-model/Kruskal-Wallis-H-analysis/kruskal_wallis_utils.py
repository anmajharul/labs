#!/usr/bin/env python3
"""
kw_utils.py
===========
Core statistical engine for the Kruskal-Wallis H reproducibility pipeline.

All calculations are implemented manually for full transparency and auditability.
scipy/statsmodels are used ONLY for independent cross-validation.

Author  : Majharul Islam (BUBT)
Date    : 2026-08-11
Python  : 3.10+
Chapter : 4 — Kruskal-Wallis H Analysis
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy.stats import kruskal, levene, norm, shapiro

logger = logging.getLogger("kw_utils")

# ============================================================
# COLUMN MAP  (raw Excel header → short name)
# ============================================================
RAW_COLUMN_MAP: Dict[str, str] = {
    "primary_mode":      "What is your PRIMARY mode of transport?",
    "one_way_cost":      "What is the TOTAL One-Way Cost of this trip?",
    "access_time":       'What is your total "Access Time" Time needed to reach the Station/Stop in Minutes ?',
    "in_vehicle_time":   'What is yout total "In-Vehicle Time" Time spent inside the main bus/train/car in Minutes?',
    # Total Travel Time = Access Time + In-Vehicle Time (derived)
}

# Expected mode labels (as they appear after stripping whitespace)
EXPECTED_MODES: List[str] = [
    "Public Bus",
    "MRT (Metro Rail)",
    "Personal Motorcycle",
    "Ridesharing (Uber/Pathao)",
]

# Chapter 4 REPORTED values — used ONLY for validation tables, never in calculations
CHAPTER4_REPORTED: Dict[str, Dict] = {
    "one_way_cost":      {"H": 97.911,  "p": "<0.001", "F": 191.638},
    "access_time":       {"H": 169.538, "p": "<0.001", "F": 54.490},
    "in_vehicle_time":   {"H": 110.929, "p": "<0.001", "F": 41.411},
    "total_travel_time": {"H": 73.325,  "p": "<0.001", "F": 32.168},
}

CHAPTER4_GROUP_SIZES: Dict[str, int] = {
    "Public Bus":                   120,
    "MRT (Metro Rail)":             96,
    "Personal Motorcycle":          62,
    "Ridesharing (Uber/Pathao)":    41,
}

VARIABLE_LABELS: Dict[str, str] = {
    "one_way_cost":      "One-Way Cost (BDT)",
    "access_time":       "Access Time (min)",
    "in_vehicle_time":   "In-Vehicle Time (min)",
    "total_travel_time": "Total Travel Time (min)",
}


# ============================================================
# DATA LOADING
# ============================================================
def load_raw_data(data_path: str) -> pd.DataFrame:
    """Load raw Excel dataset and normalise column names (strip whitespace)."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found: {data_path}")
    df = pd.read_excel(data_path)
    df.columns = df.columns.str.strip()
    logger.info(
        "Loaded %d rows × %d columns from %s",
        len(df), len(df.columns), data_path
    )
    return df


def detect_column(df: pd.DataFrame, short_name: str) -> str:
    """Find the raw column matching a short analysis name (substring match)."""
    target = RAW_COLUMN_MAP[short_name]
    for col in df.columns:
        if target.lower() in col.strip().lower():
            return col
    # fuzzy second pass — split on key words
    keywords = [w for w in target.split() if len(w) > 4]
    for col in df.columns:
        col_clean = col.strip().lower()
        if all(kw.lower() in col_clean for kw in keywords[:3]):
            return col
    raise ValueError(
        f"Cannot find column for '{short_name}'.\n"
        f"Searched for: '{target}'\n"
        f"Available columns: {list(df.columns)}"
    )


# ============================================================
# DATA PREPARATION
# ============================================================
def prepare_analysis_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Build analysis-ready DataFrame with four variables + Primary Mode.
    Derives Total Travel Time = Access Time + In-Vehicle Time.
    Returns (clean_df, exclusion_log).
    """
    exclusions: List[str] = []

    mode_col  = detect_column(df, "primary_mode")
    cost_col  = detect_column(df, "one_way_cost")
    at_col    = detect_column(df, "access_time")
    ivt_col   = detect_column(df, "in_vehicle_time")

    work = pd.DataFrame({
        "primary_mode":    df[mode_col].str.strip() if df[mode_col].dtype == object else df[mode_col],
        "one_way_cost":    pd.to_numeric(df[cost_col],  errors="coerce"),
        "access_time":     pd.to_numeric(df[at_col],    errors="coerce"),
        "in_vehicle_time": pd.to_numeric(df[ivt_col],   errors="coerce"),
    })
    work["total_travel_time"] = work["access_time"] + work["in_vehicle_time"]

    original_n = len(work)

    # ── 1. Remove rows with invalid Primary Mode ─────────────────────────────
    invalid_mode = ~work["primary_mode"].isin(EXPECTED_MODES) | work["primary_mode"].isna()
    if invalid_mode.sum() > 0:
        for idx in work[invalid_mode].index:
            exclusions.append(
                f"Row {idx+2}: excluded — invalid Primary Mode = "
                f"{repr(work.loc[idx,'primary_mode'])}"
            )
    work = work[~invalid_mode].copy()

    # ── 2. Zero / negative cost ──────────────────────────────────────────────
    bad_cost = (work["one_way_cost"] <= 0) | work["one_way_cost"].isna()
    if bad_cost.sum() > 0:
        for idx in work[bad_cost].index:
            exclusions.append(
                f"Row {idx+2}: excluded — invalid One-Way Cost = "
                f"{work.loc[idx,'one_way_cost']}"
            )
    work = work[~bad_cost].copy()

    # ── 3. Negative / zero Access Time ──────────────────────────────────────
    bad_at = (work["access_time"] <= 0) | work["access_time"].isna()
    if bad_at.sum() > 0:
        for idx in work[bad_at].index:
            exclusions.append(
                f"Row {idx+2}: excluded — invalid Access Time = "
                f"{work.loc[idx,'access_time']}"
            )
    work = work[~bad_at].copy()

    # ── 4. Negative / zero In-Vehicle Time ──────────────────────────────────
    bad_ivt = (work["in_vehicle_time"] <= 0) | work["in_vehicle_time"].isna()
    if bad_ivt.sum() > 0:
        for idx in work[bad_ivt].index:
            exclusions.append(
                f"Row {idx+2}: excluded — invalid In-Vehicle Time = "
                f"{work.loc[idx,'in_vehicle_time']}"
            )
    work = work[~bad_ivt].copy()

    # ── 5. Recompute TTT after cleaning ─────────────────────────────────────
    work["total_travel_time"] = work["access_time"] + work["in_vehicle_time"]

    # ── 6. Duplicate check (log only, do not remove) ─────────────────────────
    dup_count = work.duplicated(
        subset=["primary_mode", "one_way_cost", "access_time", "in_vehicle_time"]
    ).sum()
    if dup_count > 0:
        logger.warning(
            "%d duplicate rows detected (same mode+cost+AT+IVT). "
            "These are RETAINED — may reflect legitimate ties.", dup_count
        )
        exclusions.append(
            f"NOTE: {dup_count} duplicate rows (same mode+cost+AT+IVT) retained "
            "as legitimate ties. Not excluded."
        )

    logger.info(
        "Final analysis N = %d (of %d original, %d excluded)",
        len(work), original_n, original_n - len(work)
    )
    work = work.reset_index(drop=True)
    return work, exclusions


# ============================================================
# RANKING
# ============================================================
def compute_ranks(values: np.ndarray) -> np.ndarray:
    """
    Compute ranks with average-rank tie handling.
    Equivalent to scipy.stats.rankdata(method='average').
    """
    n = len(values)
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(n, dtype=float)
    ranks[order] = np.arange(1, n + 1, dtype=float)

    # Average ties
    i = 0
    while i < n:
        j = i + 1
        while j < n and values[order[j]] == values[order[i]]:
            j += 1
        if j - i > 1:
            avg = (i + 1 + j) / 2.0
            ranks[order[i:j]] = avg
        i = j

    return ranks


# ============================================================
# TIE CORRECTION
# ============================================================
def compute_tie_correction(values: np.ndarray) -> Tuple[float, pd.DataFrame]:
    """
    Compute Kruskal-Wallis tie correction factor C.

    C = 1 - Σ(t_j³ - t_j) / (N³ - N)

    Returns (C, tie_table_df) where tie_table lists every tied value.
    """
    N = len(values)
    unique_vals, counts = np.unique(values, return_counts=True)

    tie_rows = []
    sum_t3_t = 0.0
    for val, freq in zip(unique_vals, counts):
        t3_t = freq**3 - freq
        sum_t3_t += t3_t
        if freq > 1:   # only document actual ties
            tie_rows.append({"Value": val, "Frequency (t_j)": freq, "t_j³ - t_j": t3_t})

    denom = N**3 - N
    C = 1.0 - (sum_t3_t / denom) if denom > 0 else 1.0

    tie_df = pd.DataFrame(tie_rows)
    if tie_df.empty:
        tie_df = pd.DataFrame(columns=["Value", "Frequency (t_j)", "t_j³ - t_j"])

    return C, tie_df


# ============================================================
# KRUSKAL-WALLIS H STATISTIC (MANUAL)
# ============================================================
def kruskal_wallis_manual(
    data: pd.DataFrame,
    variable: str,
    mode_col: str = "primary_mode",
) -> Dict:
    """
    Calculate the Kruskal-Wallis H statistic from scratch.

    Formula:
        H_uncorrected = [12 / (N(N+1))] * Σ(R_i² / n_i) - 3(N+1)
        H_corrected   = H_uncorrected / C

    where C is the tie-correction factor.

    Returns a dict with all intermediate values for full transparency.
    """
    groups = data.groupby(mode_col, sort=True)[variable].apply(list).to_dict()
    all_values = np.array(data[variable].values, dtype=float)
    N = len(all_values)

    ranks = compute_ranks(all_values)
    data_with_ranks = data[[mode_col, variable]].copy()
    data_with_ranks["rank"] = ranks

    # Rank sums and group sizes
    group_stats = {}
    for mode in sorted(groups.keys()):
        mask = data[mode_col] == mode
        n_i  = mask.sum()
        R_i  = ranks[mask.values].sum()
        group_stats[mode] = {
            "n":          int(n_i),
            "rank_sum":   float(R_i),
            "mean_rank":  float(R_i / n_i) if n_i > 0 else np.nan,
        }

    # H uncorrected
    sigma = sum(
        gs["rank_sum"]**2 / gs["n"]
        for gs in group_stats.values()
        if gs["n"] > 0
    )
    H_unc = (12.0 / (N * (N + 1))) * sigma - 3.0 * (N + 1)

    # Tie correction
    C, tie_df = compute_tie_correction(all_values)
    H_cor = H_unc / C if C != 0 else np.nan

    # p-value (chi-squared approximation)
    df_kw = len(group_stats) - 1
    from scipy.stats import chi2
    p_value = 1.0 - chi2.cdf(H_cor, df=df_kw)

    return {
        "variable":       variable,
        "N":              int(N),
        "groups":         group_stats,
        "H_uncorrected":  float(H_unc),
        "tie_correction": float(C),
        "sum_t3_t":       float((1.0 - C) * (N**3 - N)) if N > 1 else 0.0,
        "H_corrected":    float(H_cor),
        "df":             int(df_kw),
        "p_value":        float(p_value),
        "tie_table":      tie_df,
        "N3_minus_N":     float(N**3 - N),
    }


# ============================================================
# SCIPY CROSS-VALIDATION
# ============================================================
def kruskal_wallis_scipy(
    data: pd.DataFrame,
    variable: str,
    mode_col: str = "primary_mode",
) -> Dict:
    """Run scipy.stats.kruskal for independent cross-validation."""
    groups = [
        data.loc[data[mode_col] == mode, variable].dropna().values
        for mode in sorted(data[mode_col].unique())
    ]
    H, p = kruskal(*groups)
    return {
        "variable":   variable,
        "H_scipy":    float(H),
        "p_scipy":    float(p),
        "df":         len(groups) - 1,
    }


# ============================================================
# EFFECT SIZE  (η² — eta-squared)
# ============================================================
def kw_effect_size(H: float, N: int, k: int) -> Dict:
    """
    Compute Kruskal-Wallis effect size.

    Formula (Tomczak & Tomczak, 2014):
        η² = (H - k + 1) / (N - k)

    Thresholds (Cohen, 1988 adapted by Tomczak & Tomczak, 2014):
        η² ≥ 0.14  : Large
        η² ≥ 0.06  : Medium
        η² ≥ 0.01  : Small

    Citation:
        Tomczak, M. & Tomczak, E. (2014). The need to report effect size
        estimates revisited. An overview of some recommended measures of
        effect size. Trends in Sport Sciences, 1(21), 19-25.
    """
    eta2 = (H - k + 1) / (N - k)
    if eta2 >= 0.14:
        interpretation = "Large  (η² ≥ 0.14; Tomczak & Tomczak, 2014)"
    elif eta2 >= 0.06:
        interpretation = "Medium (0.06 ≤ η² < 0.14; Tomczak & Tomczak, 2014)"
    elif eta2 >= 0.01:
        interpretation = "Small  (0.01 ≤ η² < 0.06; Tomczak & Tomczak, 2014)"
    else:
        interpretation = "Negligible (η² < 0.01; Tomczak & Tomczak, 2014)"
    return {
        "H":              H,
        "k":              k,
        "N":              N,
        "eta2":           float(eta2),
        "interpretation": interpretation,
        "citation":       "Tomczak & Tomczak (2014). Trends in Sport Sciences, 1(21), 19-25.",
    }


# ============================================================
# SHAPIRO-WILK NORMALITY TEST (per group)
# ============================================================
def shapiro_wilk_by_group(
    data: pd.DataFrame,
    variable: str,
    mode_col: str = "primary_mode",
) -> pd.DataFrame:
    """Run Shapiro-Wilk within each Primary Mode group."""
    rows = []
    for mode in sorted(data[mode_col].unique()):
        vals = data.loc[data[mode_col] == mode, variable].dropna().values
        n = len(vals)
        if n >= 3:
            W, p = shapiro(vals)
        else:
            W, p = np.nan, np.nan
        rows.append({
            "Variable":     VARIABLE_LABELS.get(variable, variable),
            "Mode":         mode,
            "N":            n,
            "Shapiro-Wilk W": round(W, 4) if not np.isnan(W) else "N/A",
            "p-value":      round(p, 4) if not np.isnan(p) else "N/A",
            "Normal?":      "Yes" if (not np.isnan(p) and p >= 0.05) else "No",
            "Note":         (
                "Insufficient n for S-W" if n < 3 else
                "S-W p<0.05 → evidence against normality (does not prove non-normality)"
                if p < 0.05 else
                "S-W p≥0.05 → no evidence against normality"
            ),
        })
    return pd.DataFrame(rows)


# ============================================================
# LEVENE'S TEST
# ============================================================
def levene_test(
    data: pd.DataFrame,
    variable: str,
    center: str = "median",
    mode_col: str = "primary_mode",
) -> Dict:
    """
    Run Levene's test for equality of variances.

    center='median' → Brown-Forsythe variant (more robust)
    center='mean'   → Classical Levene

    Documented here because mixing variants between software is a
    common source of discrepancy.
    """
    groups = [
        data.loc[data[mode_col] == mode, variable].dropna().values
        for mode in sorted(data[mode_col].unique())
    ]
    F, p = levene(*groups, center=center)
    df1 = len(groups) - 1
    df2 = sum(len(g) for g in groups) - len(groups)
    return {
        "variable":  variable,
        "F":         float(F),
        "df1":       df1,
        "df2":       df2,
        "p_value":   float(p),
        "center":    center,
        "variant":   "Brown-Forsythe (median-centered)" if center == "median"
                     else "Classical Levene (mean-centered)",
        "equal_var": p >= 0.05,
    }


# ============================================================
# DUNN POST-HOC TEST (BONFERRONI)
# ============================================================
def dunn_bonferroni(
    data: pd.DataFrame,
    variable: str,
    mode_col: str = "primary_mode",
) -> pd.DataFrame:
    """
    Dunn's pairwise post-hoc test with Bonferroni correction.

    Formula for Dunn's z-statistic:
        z_ij = (R̄_i - R̄_j) / SE_ij
        SE_ij = sqrt[ N(N+1)/12 * (1/n_i + 1/n_j) - Σ(t_j³-t_j)/(12(N-1)) * (1/n_i + 1/n_j) ]

    Bonferroni α-adjusted = 0.05 / m  where m = number of comparisons.

    All 6 pairwise comparisons are always reported.
    """
    modes = sorted(data[mode_col].unique())
    all_vals = data[variable].values.astype(float)
    N = len(all_vals)
    ranks = compute_ranks(all_vals)

    # Group mean ranks
    group_mean_ranks = {}
    group_ns = {}
    for mode in modes:
        mask = data[mode_col].values == mode
        group_mean_ranks[mode] = ranks[mask].mean()
        group_ns[mode] = mask.sum()

    # Tie correction term
    unique_vals, counts = np.unique(all_vals, return_counts=True)
    sum_t3_t = np.sum(counts**3 - counts)
    tie_term = sum_t3_t / (12.0 * (N - 1)) if N > 1 else 0.0
    base_var = N * (N + 1) / 12.0

    from itertools import combinations
    pairs = list(combinations(modes, 2))
    m = len(pairs)      # 6 for 4 groups
    bonferroni_alpha = 0.05 / m

    rows = []
    for (A, B) in pairs:
        n_A = group_ns[A]
        n_B = group_ns[B]
        inv = 1.0 / n_A + 1.0 / n_B
        SE = np.sqrt((base_var - tie_term) * inv)
        z  = (group_mean_ranks[A] - group_mean_ranks[B]) / SE if SE > 0 else np.nan
        p_raw = float(2.0 * (1.0 - norm.cdf(abs(z)))) if not np.isnan(z) else np.nan
        p_adj = min(p_raw * m, 1.0) if not np.isnan(p_raw) else np.nan
        rows.append({
            "Comparison":               f"{A} vs {B}",
            "Group A":                  A,
            "Group B":                  B,
            "Mean Rank A":              round(group_mean_ranks[A], 3),
            "Mean Rank B":              round(group_mean_ranks[B], 3),
            "z-statistic":              round(z, 4) if not np.isnan(z) else "N/A",
            "Raw p-value":              round(p_raw, 4) if not np.isnan(p_raw) else "N/A",
            "Bonferroni p-value":       round(p_adj, 4) if not np.isnan(p_adj) else "N/A",
            "Bonferroni threshold":     round(bonferroni_alpha, 4),
            "Significant (Bonferroni)": "Yes" if (not np.isnan(p_adj) and p_adj < 0.05) else "No",
        })

    return pd.DataFrame(rows)


# ============================================================
# ONE-WAY ANOVA (for Table 4.13 reproduction)
# ============================================================
def one_way_anova(
    data: pd.DataFrame,
    variable: str,
    mode_col: str = "primary_mode",
) -> Dict:
    """Compute one-way ANOVA F-statistic for Table 4.13 reproduction."""
    from scipy.stats import f_oneway
    groups = [
        data.loc[data[mode_col] == mode, variable].dropna().values
        for mode in sorted(data[mode_col].unique())
    ]
    F, p = f_oneway(*groups)
    k = len(groups)
    N = sum(len(g) for g in groups)
    return {
        "variable": variable,
        "F":        float(F),
        "p_value":  float(p),
        "df1":      k - 1,
        "df2":      N - k,
    }
