#!/usr/bin/env python3
"""
Analysis 03: Family Income x Primary Mode
Author : Majharul Islam
Date   : 2026-08-07
"""

import logging
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DATA_PATH = REPO_ROOT / "data" / "Mode_shift_bubt.xlsx"
OUTPUT_DIR = SCRIPT_DIR

sys.path.insert(0, str(REPO_ROOT))
from chi_square_utils import run_full_analysis

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s — %(message)s")


def main() -> None:
    results = run_full_analysis(
        data_path=str(DATA_PATH),
        row_keywords=["approximate total monthly income"],
        col_keywords=["PRIMARY mode"],
        row_var_label="Family Income x Primary Mode (Row)",
        col_var_label="Family Income x Primary Mode (Col)",
        table_title="Table 4.4: Primary Travel Mode by Family Income (n, row %)",
        output_dir=str(OUTPUT_DIR),
        row_order=None,
        col_order=['Public Bus', 'MRT (Metro Rail)', 'Personal Motorcycle', 'Ridesharing (Uber/Pathao)'],
        use_monte_carlo_ffh=False,
        use_monte_carlo_permutation=False,
        row_recode=None,
    )
    print(f"Analysis 03 Complete: chi2 = {results['chi2_statistic']:.4f}, p = {results['p_value']:.4f}")


if __name__ == "__main__":
    main()
