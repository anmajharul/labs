#!/usr/bin/env python3
"""
Analysis 06: Reliability x Switch Intent
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
        row_keywords=["how reliable"],
        col_keywords=["late"],
        row_var_label="Reliability x Switch Intent (Row)",
        col_var_label="Reliability x Switch Intent (Col)",
        table_title="Table 4.8: Willingness to Switch by Reliability Level (n, row %)",
        output_dir=str(OUTPUT_DIR),
        row_order=['Poor (1-2)', 'Moderate (3)', 'Good (4-5)'],
        col_order=['Yes', 'No'],
        use_monte_carlo_ffh=False,
        use_monte_carlo_permutation=False,
        row_recode={1: 'Poor (1-2)', 2: 'Poor (1-2)', 3: 'Moderate (3)', 4: 'Good (4-5)', 5: 'Good (4-5)'},
    )
    print(f"Analysis 06 Complete: chi2 = {results['chi2_statistic']:.4f}, p = {results['p_value']:.4f}")


if __name__ == "__main__":
    main()
