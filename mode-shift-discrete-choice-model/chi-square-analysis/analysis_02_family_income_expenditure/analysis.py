#!/usr/bin/env python3
"""
Analysis 02: Family Income x Personal Expenditure
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
        col_keywords=["personal monthly expenditure"],
        row_var_label="Family Income x Personal Expenditure (Row)",
        col_var_label="Family Income x Personal Expenditure (Col)",
        table_title="Table 4.3: Personal Monthly Expenditure by Family Income (n, row %)",
        output_dir=str(OUTPUT_DIR),
        row_order=None,
        col_order=None,
        use_monte_carlo_ffh=False,
        use_monte_carlo_permutation=False,
        row_recode=None,
    )
    print(f"Analysis 02 Complete: chi2 = {results['chi2_statistic']:.4f}, p = {results['p_value']:.4f}")


if __name__ == "__main__":
    main()
