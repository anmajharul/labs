#!/usr/bin/env python3
"""
pipeline_utils.py
=================
Universal core statistical engine for the test-selection pipeline.

All functions are generic — no hard-coded variable names, group labels,
dataset names, or expected results.

Author  : Majharul Islam (BUBT)
Date    : 2026-08-11
Python  : 3.10+
"""

from __future__ import annotations

import logging
import os
import re
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import (
    chi2, f as f_dist, kruskal, levene, norm, shapiro, f_oneway
)

logger = logging.getLogger("pipeline_utils")

# ═══════════════════════════════════════════════════════════════
# CONSTANTS  (heuristic thresholds — all changeable)
# ═══════════════════════════════════════════════════════════════
MIN_GROUP_SIZE          = 5     # minimum n per group for a grouping variable
MAX_GROUPING_CATEGORIES = 10    # upper bound on groups for a grouping variable
MIN_UNIQUE_NUMERIC      = 7     # below this -> treat numeric as ordinal/Likert
MAX_FREE_TEXT_UNIQUE    = 30    # above this -> string column is free-text, exclude
MAX_ID_UNIQUE_RATIO     = 0.90  # unique/N > this -> likely ID column
LIKERT_MAX              = 7     # max value for a Likert-like scale
SHAPIRO_MAX_N           = 5000  # scipy shapiro limitation
OUTLIER_IQR_FACTOR      = 1.5   # for boxplot whisker outlier rule
SIGNIFICANCE            = 0.05  # default alpha


# ═══════════════════════════════════════════════════════════════
# VARIABLE CLASSIFICATION
# ═══════════════════════════════════════════════════════════════
class VariableType:
    DATETIME   = "datetime"
    ID         = "id"
    CONSTANT   = "constant"
    FREE_TEXT  = "free_text"
    BINARY_CAT = "binary_categorical"
    NOMINAL    = "nominal_categorical"
    ORDINAL    = "ordinal_categorical"
    LIKERT     = "likert_ordinal"
    DISCRETE   = "discrete_numeric"
    CONTINUOUS = "continuous_numeric"
    UNKNOWN    = "unknown"


def classify_column(series: pd.Series, col_name: str) -> Dict:
    """
    Automatically classify a single column.
    Returns a dict with type, measurement_level, and suitability flags.
    """
    n_total  = len(series)
    n_miss   = series.isna().sum()
    n_valid  = n_total - n_miss
    valid    = series.dropna()
    n_unique = valid.nunique()

    result = {
        "column":          col_name,
        "n_total":         n_total,
        "n_missing":       n_miss,
        "pct_missing":     round(100 * n_miss / n_total, 2) if n_total > 0 else 0.0,
        "n_unique":        n_unique,
        "var_type":        VariableType.UNKNOWN,
        "suitable_outcome":    False,
        "suitable_grouping":   False,
        "grouping_excluded_reason": None,
    }

    # ── Constant ──────────────────────────────────────────────────────────────
    if n_unique <= 1:
        result["var_type"] = VariableType.CONSTANT
        result["grouping_excluded_reason"] = "constant — no variation"
        return result

    # ── Datetime detection ────────────────────────────────────────────────────
    if _looks_like_datetime(valid, col_name):
        result["var_type"] = VariableType.DATETIME
        result["grouping_excluded_reason"] = "datetime variable"
        return result

    # ── Numeric branch ────────────────────────────────────────────────────────
    if pd.api.types.is_numeric_dtype(series):
        num_vals = valid.astype(float)

        # ID check: high unique ratio and float-looking
        unique_ratio = n_unique / n_valid if n_valid > 0 else 0
        if unique_ratio > MAX_ID_UNIQUE_RATIO and n_unique > 50:
            result["var_type"] = VariableType.ID
            result["grouping_excluded_reason"] = f"unique ratio {unique_ratio:.2f} > {MAX_ID_UNIQUE_RATIO} — likely ID"
            return result

        mn, mx = num_vals.min(), num_vals.max()
        result["min"] = float(mn)
        result["max"] = float(mx)
        result["mean"] = float(num_vals.mean())
        result["median"] = float(num_vals.median())
        result["sd"] = float(num_vals.std())
        result["iqr"] = float(num_vals.quantile(0.75) - num_vals.quantile(0.25))

        # Likert / ordinal detection: integer, bounded 1–7, few unique
        all_int = (num_vals % 1 == 0).all()
        if (all_int and 1 <= mn and mx <= LIKERT_MAX
                and n_unique <= LIKERT_MAX and n_unique >= 2):
            result["var_type"] = VariableType.LIKERT
            result["suitable_outcome"]  = True
            result["suitable_grouping"] = False   # grouping on Likert rarely useful
            result["measurement_level"] = "ordinal"
            return result

        # Discrete count
        if all_int and n_unique < MIN_UNIQUE_NUMERIC:
            result["var_type"] = VariableType.DISCRETE
            result["suitable_outcome"]  = True
            result["suitable_grouping"] = (2 <= n_unique <= MAX_GROUPING_CATEGORIES
                                           and n_valid >= MIN_GROUP_SIZE * 2)
            result["measurement_level"] = "interval/ratio (discrete)"
            return result

        # Continuous
        result["var_type"] = VariableType.CONTINUOUS
        result["suitable_outcome"]  = True
        result["suitable_grouping"] = False
        result["measurement_level"] = "interval/ratio (continuous)"
        return result

    # ── String / object branch ────────────────────────────────────────────────
    else:
        str_vals = valid.astype(str).str.strip()
        result["sample_values"] = list(str_vals.value_counts().head(5).index)

        # Free-text: too many unique values
        if n_unique > MAX_FREE_TEXT_UNIQUE:
            result["var_type"] = VariableType.FREE_TEXT
            result["grouping_excluded_reason"] = (
                f"{n_unique} unique values > {MAX_FREE_TEXT_UNIQUE} — free-text"
            )
            return result

        # Binary
        if n_unique == 2:
            result["var_type"] = VariableType.BINARY_CAT
            result["suitable_grouping"] = True
            result["measurement_level"] = "nominal (binary)"
            # Check minimum group sizes
            counts = str_vals.value_counts()
            if counts.min() < MIN_GROUP_SIZE:
                result["suitable_grouping"] = False
                result["grouping_excluded_reason"] = (
                    f"smallest group n={counts.min()} < {MIN_GROUP_SIZE}"
                )
            return result

        # Ordinal / nominal with manageable categories
        if n_unique <= MAX_GROUPING_CATEGORIES:
            counts = str_vals.value_counts()
            min_count = counts.min()
            if min_count < MIN_GROUP_SIZE:
                result["var_type"] = VariableType.NOMINAL
                result["suitable_grouping"] = False
                result["grouping_excluded_reason"] = (
                    f"smallest group n={min_count} < {MIN_GROUP_SIZE}"
                )
            else:
                result["var_type"] = VariableType.NOMINAL
                result["suitable_grouping"] = True
                result["measurement_level"] = "nominal"
            return result

        # Many nominal categories — flag
        result["var_type"] = VariableType.NOMINAL
        result["suitable_grouping"] = False
        result["grouping_excluded_reason"] = (
            f"{n_unique} unique categories — too many for grouping"
        )
        return result


def _looks_like_datetime(valid: pd.Series, col_name: str) -> bool:
    """Heuristic: detect Excel serial dates or timestamp-like numerics."""
    name_lower = col_name.lower()
    if any(kw in name_lower for kw in ("timestamp", "date", "time", "datetime")):
        return True
    if pd.api.types.is_numeric_dtype(valid):
        # Excel serial date range: 40000–50000 (approx 2009–2036)
        if valid.between(40000, 60000).mean() > 0.9:
            return True
    return False


def classify_all_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Classify every column in the dataframe. Returns a classification table."""
    rows = []
    for col in df.columns:
        info = classify_column(df[col], col)
        rows.append(info)
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════
def load_dataset(data_path: str) -> pd.DataFrame:
    """Load Excel or CSV dataset and normalise column names."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found: {data_path}")
    ext = Path(data_path).suffix.lower()
    if ext in (".xlsx", ".xls"):
        df = pd.read_excel(data_path)
    elif ext == ".csv":
        df = pd.read_csv(data_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    df.columns = df.columns.str.strip()
    logger.info("Loaded %d rows × %d columns from %s", len(df), len(df.columns), data_path)
    return df


# ═══════════════════════════════════════════════════════════════
# ANALYSIS MATRIX
# ═══════════════════════════════════════════════════════════════
def build_analysis_matrix(
    df: pd.DataFrame,
    classification: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate all scientifically valid (outcome × grouping) combinations.
    Applies screening rules and annotates suitability.
    """
    outcomes  = classification[classification["suitable_outcome"] == True]["column"].tolist()
    groupings = classification[classification["suitable_grouping"] == True]["column"].tolist()

    rows = []
    for outcome in outcomes:
        for grouper in groupings:
            if outcome == grouper:
                continue

            group_vals  = df[grouper].dropna().astype(str).str.strip()
            group_counts = group_vals.value_counts()
            n_groups     = len(group_counts)
            min_n        = int(group_counts.min())
            valid_n      = df[[outcome, grouper]].dropna().shape[0]

            suitable = True
            reason   = "All screening criteria met"

            if n_groups < 2:
                suitable = False; reason = "Only 1 group — no comparison possible"
            elif min_n < MIN_GROUP_SIZE:
                suitable = False; reason = f"Smallest group n={min_n} < {MIN_GROUP_SIZE}"
            elif valid_n < 20:
                suitable = False; reason = f"Valid N={valid_n} — insufficient"

            rows.append({
                "Outcome":          outcome,
                "Grouping":         grouper,
                "N_groups":         n_groups,
                "Group_labels":     list(group_counts.index),
                "Group_sizes":      list(group_counts.values),
                "Min_group_n":      min_n,
                "Valid_N":          valid_n,
                "Suitable":         suitable,
                "Reason":           reason,
            })

    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════
# DESCRIPTIVE STATISTICS
# ═══════════════════════════════════════════════════════════════
def group_descriptives(
    df: pd.DataFrame,
    outcome: str,
    grouper: str,
) -> pd.DataFrame:
    """Compute group-wise descriptive statistics."""
    rows = []
    groups = df[grouper].dropna().astype(str).str.strip().unique()
    for grp in sorted(groups):
        mask = df[grouper].astype(str).str.strip() == grp
        vals = df.loc[mask, outcome].dropna().astype(float)
        if len(vals) == 0:
            continue
        q1, q3 = vals.quantile([0.25, 0.75])
        rows.append({
            "Grouping":  grouper,
            "Group":     grp,
            "Outcome":   outcome,
            "N":         len(vals),
            "Mean":      round(float(vals.mean()), 4),
            "Median":    round(float(vals.median()), 4),
            "SD":        round(float(vals.std()), 4),
            "Min":       round(float(vals.min()), 4),
            "Max":       round(float(vals.max()), 4),
            "Q1":        round(float(q1), 4),
            "Q3":        round(float(q3), 4),
            "IQR":       round(float(q3 - q1), 4),
            "Skewness":  round(float(vals.skew()), 4),
            "Kurtosis":  round(float(vals.kurt()), 4),
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════
# OUTLIER DETECTION
# ═══════════════════════════════════════════════════════════════
def detect_outliers_iqr(values: pd.Series) -> Dict:
    """IQR-based outlier detection. Returns info dict."""
    vals = values.dropna().astype(float)
    q1, q3 = vals.quantile([0.25, 0.75])
    iqr  = q3 - q1
    lb   = q1 - OUTLIER_IQR_FACTOR * iqr
    ub   = q3 + OUTLIER_IQR_FACTOR * iqr
    outliers = vals[(vals < lb) | (vals > ub)]
    return {
        "Q1": q1, "Q3": q3, "IQR": iqr,
        "Lower_fence": lb, "Upper_fence": ub,
        "N_outliers": len(outliers),
        "Outlier_values": list(outliers),
        "Pct_outliers": round(100 * len(outliers) / len(vals), 2),
    }


# ═══════════════════════════════════════════════════════════════
# NORMALITY: SHAPIRO-WILK
# ═══════════════════════════════════════════════════════════════
def shapiro_wilk_by_group(
    df: pd.DataFrame,
    outcome: str,
    grouper: str,
) -> pd.DataFrame:
    """Run Shapiro-Wilk within each group. Correct interpretation applied."""
    rows = []
    groups = df[grouper].dropna().astype(str).str.strip().unique()
    for grp in sorted(groups):
        mask = df[grouper].astype(str).str.strip() == grp
        vals = df.loc[mask, outcome].dropna().astype(float)
        n    = len(vals)
        if n < 3:
            W, p, note = np.nan, np.nan, "n < 3 — S-W cannot be computed"
        elif n > SHAPIRO_MAX_N:
            W, p, note = np.nan, np.nan, f"n > {SHAPIRO_MAX_N} — use KS test"
        else:
            W, p = shapiro(vals)
            W, p = float(W), float(p)
            if p < SIGNIFICANCE:
                note = "p<0.05: evidence against normality (does not prove non-normality)"
            else:
                note = "p>=0.05: insufficient evidence to reject normality"
        rows.append({
            "Outcome":    outcome,
            "Grouping":   grouper,
            "Group":      grp,
            "N":          n,
            "SW_W":       round(W, 4) if not np.isnan(W) else "N/A",
            "SW_p":       round(p, 4) if not np.isnan(p) else "N/A",
            "Note":       note,
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════
# HOMOGENEITY: LEVENE (BROWN-FORSYTHE by default)
# ═══════════════════════════════════════════════════════════════
def run_levene(
    df: pd.DataFrame,
    outcome: str,
    grouper: str,
    center: str = "median",  # "median" = Brown-Forsythe; "mean" = classical Levene
) -> Dict:
    """
    Levene's test for equality of variances.
    center='median' (default) -> Brown-Forsythe variant — more robust.
    center='mean' -> classical Levene.
    """
    groups = [
        df.loc[df[grouper].astype(str).str.strip() == g, outcome].dropna().astype(float).values
        for g in sorted(df[grouper].dropna().astype(str).str.strip().unique())
    ]
    groups = [g for g in groups if len(g) >= 2]
    if len(groups) < 2:
        return {"F": np.nan, "p": np.nan, "df1": np.nan, "df2": np.nan, "center": center}
    F, p = levene(*groups, center=center)
    k  = len(groups)
    N  = sum(len(g) for g in groups)
    return {
        "Outcome":      outcome,
        "Grouping":     grouper,
        "F":            round(float(F), 4),
        "df1":          k - 1,
        "df2":          N - k,
        "p":            round(float(p), 4),
        "center":       center,
        "variant":      "Brown-Forsythe (median)" if center == "median" else "Classical Levene (mean)",
        "equal_var":    float(p) >= SIGNIFICANCE,
        "interpretation": (
            f"p={'<0.001' if p<0.001 else round(p,4)}: "
            + ("No significant evidence of unequal variances." if p >= SIGNIFICANCE
               else "Evidence of unequal variances across groups.")
        ),
    }


# ═══════════════════════════════════════════════════════════════
# TEST SELECTION LOGIC
# ═══════════════════════════════════════════════════════════════
def select_test(
    df: pd.DataFrame,
    outcome: str,
    grouper: str,
    var_type: str,
    sw_results: pd.DataFrame,
    levene_result: Dict,
    descriptives: pd.DataFrame,
) -> Dict:
    """
    Data-driven test selection.

    Decision criteria evaluated in this order:
    1. Measurement level (ordinal/Likert -> KW preferred)
    2. Group sizes (all large -> ANOVA more robust)
    3. Normality evidence (S-W + skewness + visual)
    4. Variance homogeneity (Levene result)
    5. Outlier severity

    Returns: primary test, sensitivity test, reason.
    """
    k      = df[grouper].dropna().astype(str).str.strip().nunique()
    n_min  = descriptives["N"].min() if len(descriptives) > 0 else 0
    n_total = descriptives["N"].sum() if len(descriptives) > 0 else 0

    # ── 1. Measurement level ─────────────────────────────────────────────────
    if var_type in (VariableType.LIKERT, VariableType.ORDINAL):
        return {
            "primary":     "KRUSKAL-WALLIS",
            "sensitivity": "ONE-WAY ANOVA",
            "decision":    "NON-PARAMETRIC PREFERRED",
            "reason": (
                f"Outcome '{outcome}' is an ordinal/Likert variable. "
                "Kruskal-Wallis is preferred regardless of S-W results because "
                "parametric ANOVA assumes interval measurement, which ordinal "
                "scales do not guarantee. ANOVA is reported as robustness check."
            ),
        }

    # ── 2. Insufficient data ──────────────────────────────────────────────────
    if n_min < MIN_GROUP_SIZE or n_total < 20:
        return {
            "primary":     "INSUFFICIENT DATA",
            "sensitivity": "N/A",
            "decision":    "INSUFFICIENT EVIDENCE",
            "reason": f"Min group n={n_min} — insufficient for reliable inference.",
        }

    # ── 3. Normality evidence ─────────────────────────────────────────────────
    sw_p_vals = []
    if len(sw_results) > 0:
        sw_p_raw = sw_results["SW_p"].tolist()
        sw_p_vals = [p for p in sw_p_raw if isinstance(p, (int, float)) and not np.isnan(float(p))]

    skew_vals = descriptives["Skewness"].abs().tolist() if "Skewness" in descriptives.columns else []
    max_skew  = max(skew_vals) if skew_vals else 0.0

    n_non_normal = sum(1 for p in sw_p_vals if float(p) < SIGNIFICANCE)
    frac_non_normal = n_non_normal / len(sw_p_vals) if sw_p_vals else 0.0

    # Highly skewed -> non-parametric
    strongly_skewed = max_skew > 2.0
    # Most groups fail S-W
    mostly_non_normal = frac_non_normal > 0.5

    # ── 4. Variance homogeneity ───────────────────────────────────────────────
    levene_p = levene_result.get("p", np.nan)
    equal_var = (not np.isnan(levene_p)) and (float(levene_p) >= SIGNIFICANCE)

    # ── 5. Large n -> ANOVA robust to non-normality ───────────────────────────
    large_n = n_min >= 30  # CLT provides reasonable protection

    # ── Decision tree ─────────────────────────────────────────────────────────
    if large_n and not strongly_skewed:
        if equal_var:
            return {
                "primary":     "ONE-WAY ANOVA",
                "sensitivity": "KRUSKAL-WALLIS",
                "decision":    "PARAMETRIC PREFERRED",
                "reason": (
                    f"Large group sizes (min n={n_min}) ensure ANOVA robustness via CLT. "
                    f"Max absolute skewness={max_skew:.2f} (not extreme). "
                    f"Levene p={levene_p:.4f} — equal variances supported. "
                    "Classical ANOVA is preferred; KW reported as robustness check."
                ),
            }
        else:
            return {
                "primary":     "WELCH ANOVA",
                "sensitivity": "KRUSKAL-WALLIS",
                "decision":    "WELCH PREFERRED",
                "reason": (
                    f"Large group sizes (min n={n_min}) but Levene p={levene_p:.4f} — "
                    "unequal variances. Welch ANOVA relaxes the equal-variance assumption "
                    "while retaining parametric power. KW reported as robustness check."
                ),
            }

    if mostly_non_normal or strongly_skewed:
        return {
            "primary":     "KRUSKAL-WALLIS",
            "sensitivity": "WELCH ANOVA" if not equal_var else "ONE-WAY ANOVA",
            "decision":    "NON-PARAMETRIC PREFERRED",
            "reason": (
                f"{n_non_normal}/{len(sw_p_vals)} groups fail S-W (p<0.05). "
                f"Max absolute skewness={max_skew:.2f}. "
                "Combined evidence from S-W, skewness, and visual inspection "
                "indicates departure from normality. KW is preferred. "
                "ANOVA reported as robustness analysis."
            ),
        }

    if not equal_var:
        return {
            "primary":     "WELCH ANOVA",
            "sensitivity": "KRUSKAL-WALLIS",
            "decision":    "WELCH PREFERRED",
            "reason": (
                f"Levene p={levene_p:.4f} — unequal variances. "
                f"S-W evidence mixed ({n_non_normal}/{len(sw_p_vals)} fail). "
                "Welch ANOVA is preferred for unequal-variance scenarios."
            ),
        }

    return {
        "primary":     "ONE-WAY ANOVA",
        "sensitivity": "KRUSKAL-WALLIS",
        "decision":    "BOTH DEFENSIBLE",
        "reason": (
            f"Mixed evidence: {n_non_normal}/{len(sw_p_vals)} groups fail S-W. "
            f"Levene p={levene_p:.4f} — variances approximately equal. "
            f"Max skewness={max_skew:.2f}. "
            "Both ANOVA and KW are defensible; ANOVA reported as primary with KW robustness."
        ),
    }


# ═══════════════════════════════════════════════════════════════
# RANKING (manual)
# ═══════════════════════════════════════════════════════════════
def compute_ranks_manual(values: np.ndarray) -> np.ndarray:
    """Average-rank tie handling — implemented from scratch."""
    n     = len(values)
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(n, dtype=float)
    ranks[order] = np.arange(1, n + 1, dtype=float)
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


# ═══════════════════════════════════════════════════════════════
# TIE CORRECTION
# ═══════════════════════════════════════════════════════════════
def compute_tie_correction(values: np.ndarray) -> Tuple[float, pd.DataFrame, float, float]:
    """
    Compute KW tie correction factor C.
    C = 1 - Sum_(t_j³ - t_j) / (N³ - N)
    Returns (C, tie_table_df, sum_t3t, N3_minus_N).
    """
    N   = len(values)
    uniq, counts = np.unique(values, return_counts=True)
    t3t = counts.astype(float)**3 - counts
    sum_t3t = float(t3t.sum())
    denom   = float(N**3 - N)
    C       = 1.0 - (sum_t3t / denom) if denom > 0 else 1.0

    tie_rows = [
        {"Value": float(v), "Frequency_tj": int(c), "t3_minus_t": float(t)}
        for v, c, t in zip(uniq, counts, t3t)
        if c > 1
    ]
    tie_df = pd.DataFrame(tie_rows) if tie_rows else pd.DataFrame(
        columns=["Value", "Frequency_tj", "t3_minus_t"]
    )
    return C, tie_df, sum_t3t, denom


# ═══════════════════════════════════════════════════════════════
# KRUSKAL-WALLIS (manual)
# ═══════════════════════════════════════════════════════════════
def kruskal_wallis_manual(
    df: pd.DataFrame,
    outcome: str,
    grouper: str,
) -> Dict:
    """
    Manual KW H calculation.
    H = [12 / N(N+1)] × Sum_(R_i² / n_i) - 3(N+1)
    H_corrected = H / C
    """
    valid = df[[outcome, grouper]].dropna().copy()
    valid[outcome] = valid[outcome].astype(float)
    valid[grouper] = valid[grouper].astype(str).str.strip()

    all_vals = valid[outcome].values
    N        = len(all_vals)
    ranks    = compute_ranks_manual(all_vals)
    valid["_rank"] = ranks

    group_stats = {}
    for grp, sub in valid.groupby(grouper, sort=True):
        n_i = len(sub)
        R_i = sub["_rank"].sum()
        group_stats[str(grp)] = {
            "n": int(n_i), "rank_sum": float(R_i),
            "mean_rank": float(R_i / n_i) if n_i > 0 else np.nan,
        }

    sigma = sum(gs["rank_sum"]**2 / gs["n"] for gs in group_stats.values() if gs["n"] > 0)
    H_unc = (12.0 / (N * (N + 1))) * sigma - 3.0 * (N + 1)

    C, tie_df, sum_t3t, denom = compute_tie_correction(all_vals)
    H_cor = H_unc / C if C != 0 else np.nan

    k     = len(group_stats)
    df_kw = k - 1
    p_val = float(1.0 - chi2.cdf(H_cor, df=df_kw)) if not np.isnan(H_cor) else np.nan

    return {
        "outcome":        outcome,
        "grouper":        grouper,
        "N":              N,
        "k":              k,
        "group_stats":    group_stats,
        "H_uncorrected":  float(H_unc),
        "tie_correction": float(C),
        "sum_t3t":        float(sum_t3t),
        "N3_minus_N":     float(denom),
        "H_corrected":    float(H_cor),
        "df":             df_kw,
        "p_value":        p_val,
        "tie_table":      tie_df,
    }


def kruskal_wallis_scipy(df: pd.DataFrame, outcome: str, grouper: str) -> Dict:
    """scipy.stats.kruskal cross-validation."""
    groups = [
        df.loc[df[grouper].astype(str).str.strip() == g, outcome].dropna().astype(float).values
        for g in sorted(df[grouper].dropna().astype(str).str.strip().unique())
    ]
    groups = [g for g in groups if len(g) >= 1]
    H, p = kruskal(*groups)
    return {"H_scipy": float(H), "p_scipy": float(p)}


# ═══════════════════════════════════════════════════════════════
# ONE-WAY ANOVA (manual + scipy cross-check)
# ═══════════════════════════════════════════════════════════════
def one_way_anova_manual(df: pd.DataFrame, outcome: str, grouper: str) -> Dict:
    """
    Manual one-way ANOVA.
    SS_between, SS_within, SS_total, F, p.
    """
    valid = df[[outcome, grouper]].dropna().copy()
    valid[outcome] = valid[outcome].astype(float)
    valid[grouper] = valid[grouper].astype(str).str.strip()

    grand_mean = valid[outcome].mean()
    N          = len(valid)
    groups_gb  = valid.groupby(grouper)
    k          = groups_gb.ngroups

    SS_between = sum(
        len(sub) * (sub[outcome].mean() - grand_mean)**2
        for _, sub in groups_gb
    )
    SS_within  = sum(
        ((sub[outcome] - sub[outcome].mean())**2).sum()
        for _, sub in groups_gb
    )
    SS_total   = ((valid[outcome] - grand_mean)**2).sum()

    df_between = k - 1
    df_within  = N - k
    MS_between = SS_between / df_between if df_between > 0 else np.nan
    MS_within  = SS_within  / df_within  if df_within  > 0 else np.nan
    F          = MS_between / MS_within  if MS_within and MS_within > 0 else np.nan
    p_val      = float(1 - f_dist.cdf(F, df_between, df_within)) if not np.isnan(F) else np.nan

    # scipy cross-check
    grp_arrays = [sub[outcome].values for _, sub in groups_gb]
    F_scipy, p_scipy = f_oneway(*grp_arrays)

    # Effect size eta^2 = SS_between / SS_total
    eta2 = float(SS_between / SS_total) if SS_total > 0 else np.nan
    # omega^2 (bias-corrected)
    omega2 = float((SS_between - (k - 1) * MS_within) / (SS_total + MS_within)) if MS_within else np.nan

    return {
        "outcome":     outcome,
        "grouper":     grouper,
        "N":           N,
        "k":           k,
        "SS_between":  round(float(SS_between), 4),
        "SS_within":   round(float(SS_within), 4),
        "SS_total":    round(float(SS_total), 4),
        "df_between":  df_between,
        "df_within":   df_within,
        "MS_between":  round(float(MS_between), 4),
        "MS_within":   round(float(MS_within), 4),
        "F_manual":    round(float(F), 4),
        "p_manual":    round(float(p_val), 6),
        "F_scipy":     round(float(F_scipy), 4),
        "p_scipy":     round(float(p_scipy), 6),
        "eta_sq":      round(float(eta2), 6) if not np.isnan(eta2) else np.nan,
        "omega_sq":    round(float(omega2), 6) if not np.isnan(omega2) else np.nan,
    }


# ═══════════════════════════════════════════════════════════════
# WELCH ANOVA
# ═══════════════════════════════════════════════════════════════
def welch_anova(df: pd.DataFrame, outcome: str, grouper: str) -> Dict:
    """Welch's one-way ANOVA (F* with Welch-Satterthwaite df)."""
    valid  = df[[outcome, grouper]].dropna().copy()
    valid[outcome] = valid[outcome].astype(float)
    valid[grouper] = valid[grouper].astype(str).str.strip()
    groups_gb = valid.groupby(grouper)
    k = groups_gb.ngroups

    # Weighted grand mean
    group_data = [(sub[outcome].mean(), sub[outcome].var(ddof=1), len(sub))
                  for _, sub in groups_gb]
    # Welch weights w_i = n_i / s_i^2
    weights = [n / v if v > 0 else 0.0 for (_, v, n) in group_data]
    W       = sum(weights)
    x_tilde = sum(w * m for w, (m, _, __) in zip(weights, group_data)) / W if W > 0 else np.nan

    # Numerator
    SS_num = sum(w * (m - x_tilde)**2 for w, (m, _, __) in zip(weights, group_data))

    # Denominator correction
    h = sum((1 - wi / W)**2 / (n - 1) for wi, (_, __, n) in zip(weights, group_data))
    F_welch = (SS_num / (k - 1)) / (1 + 2 * (k - 2) / 3 * h) if h and k > 1 else np.nan

    # Satterthwaite denominator df
    df_denom = 1.0 / (3 / (k**2 - 1) * h) if h else np.nan
    p_val = float(1 - f_dist.cdf(F_welch, k - 1, df_denom)) if not np.isnan(F_welch) else np.nan

    return {
        "outcome":     outcome,
        "grouper":     grouper,
        "k":           k,
        "F_welch":     round(float(F_welch), 4) if not np.isnan(F_welch) else np.nan,
        "df_num":      k - 1,
        "df_denom":    round(float(df_denom), 2) if not np.isnan(df_denom) else np.nan,
        "p_value":     round(float(p_val), 6) if not np.isnan(p_val) else np.nan,
        "reason":      "Welch ANOVA: relaxes equal-variance assumption (Welch, 1951)",
    }


# ═══════════════════════════════════════════════════════════════
# DUNN POST-HOC (Bonferroni)
# ═══════════════════════════════════════════════════════════════
def dunn_bonferroni(
    df: pd.DataFrame,
    outcome: str,
    grouper: str,
    correction: str = "bonferroni",
) -> pd.DataFrame:
    """
    Dunn's pairwise post-hoc test.
    Uses pooled ranks from all N observations (NOT pair-wise ranking).
    Reports ALL pairwise comparisons regardless of significance.
    """
    valid  = df[[outcome, grouper]].dropna().copy()
    valid[outcome] = valid[outcome].astype(float)
    valid[grouper] = valid[grouper].astype(str).str.strip()

    all_vals = valid[outcome].values
    N        = len(all_vals)
    ranks    = compute_ranks_manual(all_vals)
    valid["_rank"] = ranks

    groups   = sorted(valid[grouper].unique())
    group_mr = {g: valid.loc[valid[grouper] == g, "_rank"].mean() for g in groups}
    group_ns = {g: (valid[grouper] == g).sum() for g in groups}

    # Tie term
    uniq, counts = np.unique(all_vals, return_counts=True)
    sum_t3t  = float((counts.astype(float)**3 - counts).sum())
    tie_term = sum_t3t / (12.0 * (N - 1)) if N > 1 else 0.0
    base_var = N * (N + 1) / 12.0

    pairs = list(combinations(groups, 2))
    m     = len(pairs)
    rows  = []
    for (A, B) in pairs:
        inv  = 1.0 / group_ns[A] + 1.0 / group_ns[B]
        SE   = np.sqrt((base_var - tie_term) * inv)
        z    = (group_mr[A] - group_mr[B]) / SE if SE > 0 else np.nan
        p_raw = float(2.0 * (1.0 - norm.cdf(abs(z)))) if not np.isnan(z) else np.nan
        if correction == "bonferroni":
            p_adj = min(p_raw * m, 1.0) if not np.isnan(p_raw) else np.nan
        elif correction == "holm":
            # Will be finalised after all pairs computed
            p_adj = p_raw  # placeholder
        else:
            p_adj = p_raw
        rows.append({
            "Comparison":    f"{A} vs {B}",
            "Group_A":       A,
            "Group_B":       B,
            "MeanRank_A":    round(group_mr[A], 3),
            "MeanRank_B":    round(group_mr[B], 3),
            "z":             round(z, 4) if not np.isnan(z) else np.nan,
            "p_raw":         round(p_raw, 4) if not np.isnan(p_raw) else np.nan,
            "p_adjusted":    round(p_adj, 4) if not np.isnan(p_adj) else np.nan,
            "Correction":    correction,
            "m_comparisons": m,
            "Significant":   "Yes" if (not np.isnan(p_adj) and p_adj < SIGNIFICANCE) else "No",
        })

    dunn_df = pd.DataFrame(rows)

    # Holm correction (sort and apply step-down)
    if correction == "holm" and len(dunn_df) > 0:
        dunn_df = dunn_df.sort_values("p_raw")
        for i, idx in enumerate(dunn_df.index):
            p_adj_holm = min(dunn_df.loc[idx, "p_raw"] * (m - i), 1.0)
            dunn_df.loc[idx, "p_adjusted"] = round(p_adj_holm, 4)
            dunn_df.loc[idx, "Significant"] = "Yes" if p_adj_holm < SIGNIFICANCE else "No"

    return dunn_df


# ═══════════════════════════════════════════════════════════════
# TUKEY HSD POST-HOC (for ANOVA)
# ═══════════════════════════════════════════════════════════════
def tukey_hsd(df: pd.DataFrame, outcome: str, grouper: str) -> pd.DataFrame:
    """Tukey HSD using statsmodels (requires statsmodels >= 0.13)."""
    try:
        from statsmodels.stats.multicomp import pairwise_tukeyhsd
        valid = df[[outcome, grouper]].dropna().copy()
        valid[outcome] = valid[outcome].astype(float)
        valid[grouper] = valid[grouper].astype(str).str.strip()
        result = pairwise_tukeyhsd(valid[outcome], valid[grouper], alpha=SIGNIFICANCE)
        summary = result.summary()
        rows = []
        for row in summary.data[1:]:
            rows.append({
                "Comparison":  f"{row[0]} vs {row[1]}",
                "Group_A":     str(row[0]),
                "Group_B":     str(row[1]),
                "Mean_Diff":   round(float(row[2]), 4),
                "p_adjusted":  round(float(row[3]), 4),
                "Lower_CI":    round(float(row[4]), 4),
                "Upper_CI":    round(float(row[5]), 4),
                "Significant": "Yes" if row[6] else "No",
            })
        return pd.DataFrame(rows)
    except ImportError:
        logger.warning("statsmodels not available — Tukey HSD skipped")
        return pd.DataFrame()


# ═══════════════════════════════════════════════════════════════
# EFFECT SIZES
# ═══════════════════════════════════════════════════════════════
def effect_size_kw(H: float, N: int, k: int) -> Dict:
    """
    eta^2 = (H - k + 1) / (N - k)
    Tomczak & Tomczak (2014). Trends in Sport Sciences, 1(21), 19-25.
    Thresholds: Large >= 0.14; Medium >= 0.06; Small >= 0.01
    """
    eta2 = (H - k + 1) / (N - k) if (N - k) > 0 else np.nan
    if np.isnan(eta2):
        label = "N/A"
    elif eta2 >= 0.14:
        label = "Large (eta^2>=0.14)"
    elif eta2 >= 0.06:
        label = "Medium (0.06<=eta^2<0.14)"
    elif eta2 >= 0.01:
        label = "Small (0.01<=eta^2<0.06)"
    else:
        label = "Negligible (eta^2<0.01)"
    return {
        "measure":        "eta_squared (KW)",
        "value":          round(float(eta2), 6) if not np.isnan(eta2) else np.nan,
        "interpretation": label,
        "formula":        "eta2 = (H - k + 1) / (N - k)",
        "citation":       "Tomczak & Tomczak (2014). Trends in Sport Sciences, 1(21), 19-25.",
    }


def effect_size_anova_eta2(SS_between: float, SS_total: float) -> Dict:
    """eta^2 = SS_between / SS_total. Cohen (1988) thresholds."""
    eta2 = SS_between / SS_total if SS_total > 0 else np.nan
    if np.isnan(eta2):
        label = "N/A"
    elif eta2 >= 0.14:
        label = "Large (eta^2>=0.14)"
    elif eta2 >= 0.06:
        label = "Medium (0.06<=eta^2<0.14)"
    elif eta2 >= 0.01:
        label = "Small (0.01<=eta^2<0.06)"
    else:
        label = "Negligible"
    return {
        "measure":        "eta_squared (ANOVA)",
        "value":          round(float(eta2), 6) if not np.isnan(eta2) else np.nan,
        "interpretation": label,
        "formula":        "eta2 = SS_between / SS_total",
        "citation":       "Cohen (1988). Statistical Power Analysis. 2nd ed.",
    }


# ═══════════════════════════════════════════════════════════════
# UTILITY: p-value formatter
# ═══════════════════════════════════════════════════════════════
def fmt_p(p: float) -> str:
    if np.isnan(p):
        return "N/A"
    if p < 0.001:
        return "< 0.001"
    return f"{p:.4f}"
