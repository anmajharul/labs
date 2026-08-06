#!/usr/bin/env python3
"""
Analysis 07: Travel Cost x Premium Bus Acceptance
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
        row_keywords=["total one-way cost"],
        col_keywords=["premium bus"],
        row_var_label="Travel Cost x Premium Bus Acceptance (Row)",
        col_var_label="Travel Cost x Premium Bus Acceptance (Col)",
        table_title="Table 4.9: Acceptance of Double-Fare Premium Bus (n, row %)",
        output_dir=str(OUTPUT_DIR),
        row_order=['< 30 BDT', '30-50 BDT', '50-70 BDT', '> 70 BDT'],
        col_order=['Yes', 'No'],
        use_monte_carlo_ffh=False,
        use_monte_carlo_permutation=False,
        row_recode=None,
    )
    print(f"Analysis 07 Complete: chi2 = {results['chi2_statistic']:.4f}, p = {results['p_value']:.4f}")


if __name__ == "__main__":
    main()
