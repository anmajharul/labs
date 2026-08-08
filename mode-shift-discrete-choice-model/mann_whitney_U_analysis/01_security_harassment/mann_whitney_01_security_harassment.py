#!/usr/bin/env python3
"""
mann_whitney_01_security_harassment.py
======================================
Standalone sub-analysis for Security/Harassment matching chi-square sub-folder structure.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np

# Add parent dir to sys.path to import mann_whitney_utils
CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
sys.path.insert(0, str(PARENT_DIR))

from mann_whitney_utils import (
    load_raw_data,
    detect_column,
    extract_gender,
    compute_mann_whitney_full,
    export_table_4_4_docx,
)

DATA_PATH = str(PARENT_DIR / "data" / "Mode_shift_bubt.xlsx")

def main():
    df = load_raw_data(DATA_PATH)
    gender_series = extract_gender(df)
    gender_clean = gender_series.astype(str).str.strip()
    
    col_name = detect_column(df, "security_harassment")
    mask_valid = gender_clean.isin(["Male", "Female"]) & df[col_name].notna()
    
    male_vals = pd.to_numeric(df.loc[mask_valid & (gender_clean == "Male"), col_name], errors="coerce").dropna().values.astype(float)
    female_vals = pd.to_numeric(df.loc[mask_valid & (gender_clean == "Female"), col_name], errors="coerce").dropna().values.astype(float)
    
    res = compute_mann_whitney_full(male_vals, female_vals, "Safety: Harassment/Security")
    
    results_df = pd.DataFrame([{
        "analysis": "Safety: Harassment/Security",
        "n1_male": res["n1_male"],
        "n2_female": res["n2_female"],
        "N": res["N"],
        "U1_male": res["U1_male"],
        "U2_female": res["U2_female"],
        "U_reported": res["U_min"],
        "Z_statistic": round(res["Z_no_CC"], 4),
        "p_value": round(res["p_no_CC_manual"], 6),
        "effect_size_r": res["effect_size_r"],
        "decision": res["decision"]
    }])
    
    results_df.to_csv(CURRENT_DIR / "results.csv", index=False)
    
    # Observed frequencies
    obs = pd.crosstab(gender_clean[mask_valid], df.loc[mask_valid, col_name])
    obs.to_csv(CURRENT_DIR / "observed_frequency.csv")
    
    # Export publication docx table for this sub-analysis
    export_table_4_4_docx(
        res,
        "Safety: Harassment/Security",
        str(CURRENT_DIR / "publication_table.docx")
    )
    
    print("01_security_harassment analysis completed successfully.")

if __name__ == "__main__":
    main()
