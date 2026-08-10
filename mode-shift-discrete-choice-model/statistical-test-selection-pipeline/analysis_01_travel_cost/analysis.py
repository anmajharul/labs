#!/usr/bin/env python3
"""
analysis.py — Travel Cost Statistical Test Selection Domain
======================================================
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

from pipeline_utils import (
    load_dataset, classify_all_columns, build_analysis_matrix,
    group_descriptives, shapiro_wilk_by_group, run_levene, select_test,
    kruskal_wallis_manual, effect_size_kw, fmt_p
)

df       = load_dataset(str(PROJECT_ROOT / "data" / "raw" / "Mode_shift_bubt.xlsx"))
at_c     = [c for c in df.columns if "access time" in c.lower()][0]
ivt_c    = [c for c in df.columns if "in-vehicle" in c.lower() or "vehicle time" in c.lower()][0]
df["total_travel_time"] = df[at_c].astype(float) + df[ivt_c].astype(float)

cls      = classify_all_columns(df)
matrix   = build_analysis_matrix(df, cls)

outcome  = [c for c in df.columns if "cost" in c.lower()][0] if "cost" in df.columns or any("cost" in c.lower() for c in df.columns) else "What is the TOTAL One-Way Cost of this trip?"
sub_matrix = matrix[(matrix["Outcome"] == outcome) & (matrix["Suitable"] == True)]
if len(sub_matrix) == 0:
    sub_matrix = matrix[matrix["Outcome"] == outcome]

results = []
for _, row in sub_matrix.iterrows():
    g = row["Grouping"]
    desc = group_descriptives(df, outcome, g)
    sw   = shapiro_wilk_by_group(df, outcome, g)
    lev  = run_levene(df, outcome, g, center="median")
    sel  = select_test(df, outcome, g, "continuous_numeric", sw, lev, desc)
    kw   = kruskal_wallis_manual(df, outcome, g)
    es   = effect_size_kw(kw["H_corrected"], kw["N"], kw["k"])

    results.append({
        "Outcome": outcome[:50],
        "Grouping": g[:40],
        "N": kw["N"],
        "k": kw["k"],
        "Levene_p": round(lev.get("p", 0.0), 4),
        "H_corrected": round(kw["H_corrected"], 4),
        "p_value": round(kw["p_value"], 6),
        "eta_squared": es["value"],
        "Primary_Test": sel["primary"],
        "Decision": sel["decision"]
    })

res_df = pd.DataFrame(results)
res_df.to_csv(SCRIPT_DIR / "results.csv", index=False)
res_df.to_csv(SCRIPT_DIR / "publication_table.csv", index=False)
print(f"=== TRAVEL COST ANALYSIS ({len(res_df)} groupings) ===")
if len(res_df) > 0:
    print(res_df[["Grouping", "H_corrected", "p_value", "eta_squared", "Decision"]].to_string(index=False))
