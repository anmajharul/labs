#!/usr/bin/env python3
"""
Analysis 10: Primary Mode x Heavy Rain Behaviour
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
        row_keywords=["PRIMARY mode"],
        col_keywords=["raining heavily"],
        row_var_label="Primary Mode x Heavy Rain Behaviour (Row)",
        col_var_label="Primary Mode x Heavy Rain Behaviour (Col)",
        table_title="Table 4.X: Travel Behaviour During Heavy Rain by Primary Mode (n, row %)",
        output_dir=str(OUTPUT_DIR),
        row_order=['Public Bus', 'MRT (Metro Rail)', 'Personal Motorcycle', 'Ridesharing (Uber/Pathao)'],
        col_order=['No Change', 'Switch Mode', 'Wait', 'Cancel Trip'],
        use_monte_carlo_ffh=False,
        use_monte_carlo_permutation=True,
        row_recode=None,
    )
    print(f"Analysis 10 Complete: chi2 = {results['chi2_statistic']:.4f}, p = {results['p_value']:.4f}")


if __name__ == "__main__":
    main()
