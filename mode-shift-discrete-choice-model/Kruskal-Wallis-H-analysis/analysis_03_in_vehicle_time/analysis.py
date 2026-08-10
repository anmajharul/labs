#!/usr/bin/env python3
"""
analysis.py — In-Vehicle Time (min) Kruskal-Wallis Analysis
===================================================
Standalone Python execution module.
Author  : Majharul Islam (BUBT)
Date    : 2026-08-11
"""

import sys
from pathlib import Path
import pandas as pd

SCRIPT_DIR   = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from kruskal_wallis_utils import (
    load_raw_data, prepare_analysis_dataframe, kruskal_wallis_manual,
    kruskal_wallis_scipy, dunn_bonferroni, kw_effect_size
)

raw_df = load_raw_data(str(PROJECT_ROOT / "data" / "raw" / "Mode_shift_bubt.xlsx"))
df, _ = prepare_analysis_dataframe(raw_df)

outcome = "in_vehicle_time"
grouper = "primary_mode"

kw_manual = kruskal_wallis_manual(df, outcome, grouper)
kw_scipy  = kruskal_wallis_scipy(df, outcome, grouper)
k_val     = kw_manual.get("df", 3) + 1
es        = kw_effect_size(kw_manual["H_corrected"], kw_manual["N"], k_val)
eta_val   = es.get("eta2", 0.0)
dunn      = dunn_bonferroni(df, outcome, grouper)
group_stats = kw_manual.get("groups", {})

print(f"=== KRUSKAL-WALLIS: IN-VEHICLE TIME (MIN) ===")
print(f"  N = {kw_manual['N']}, k = {k_val}")
print(f"  H (uncorrected) = {kw_manual['H_uncorrected']:.4f}")
print(f"  Tie Correction C = {kw_manual['tie_correction']:.6f}")
print(f"  H (corrected)   = {kw_manual['H_corrected']:.4f} (scipy: {kw_scipy['H_scipy']:.4f})")
print(f"  df = {kw_manual['df']}, p = {kw_manual['p_value']:.6f}")
print(f"  Effect Size eta^2 = {eta_val:.4f} ({es['interpretation']})")

print("\nGroup Mean Ranks:")
for grp, gs in group_stats.items():
    print(f"  {grp}: n={gs['n']}, rank_sum={gs['rank_sum']:.2f}, mean_rank={gs['mean_rank']:.3f}")

out_df = pd.DataFrame([{
    "Outcome": "In-Vehicle Time (min)",
    "N": kw_manual["N"],
    "H_uncorrected": round(kw_manual["H_uncorrected"], 4),
    "Tie_Correction_C": round(kw_manual["tie_correction"], 6),
    "H_corrected": round(kw_manual["H_corrected"], 4),
    "df": kw_manual["df"],
    "p_value": round(kw_manual["p_value"], 6),
    "eta_squared": round(eta_val, 6),
    "interpretation": es["interpretation"]
}])
out_df.to_csv(SCRIPT_DIR / "results.csv", index=False)
out_df.to_csv(SCRIPT_DIR / "publication_table.csv", index=False)
dunn.to_csv(SCRIPT_DIR / "dunn_posthoc.csv", index=False)
