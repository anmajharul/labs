#!/usr/bin/env python3
"""
run_all_analyses.py
===================
Master script to run all 11 chi-square analyses sequentially.

Usage
-----
    python run_all_analyses.py

Author : Majharul Islam
Date   : 2026-08-07
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("run_all")

ANALYSES = [
    "analysis_01_gender_primary_mode",
    "analysis_02_family_income_expenditure",
    "analysis_03_family_income_primary_mode",
    "analysis_04_trip_purpose_primary_mode",
    "analysis_05_crowding_switch",
    "analysis_06_reliability_switch",
    "analysis_07_travel_cost_premium_bus",
    "analysis_08_primary_mode_fare_increase",
    "analysis_09_primary_mode_dedicated_bus",
    "analysis_10_primary_mode_heavy_rain",
    "analysis_11_primary_mode_hartal",
]


def run_analysis(analysis_dir: str) -> bool:
    script_path = Path(analysis_dir) / "analysis.py"
    if not script_path.exists():
        logger.error("Script not found: %s", script_path)
        return False

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            timeout=300,
        )
        if result.returncode == 0:
            logger.info("[OK] %s", analysis_dir)
            return True
        else:
            logger.error("[FAILED] %s\n%s", analysis_dir, result.stderr[-500:])
            return False
    except Exception as exc:
        logger.error("[ERROR] %s — %s", analysis_dir, exc)
        return False


def main() -> None:
    logger.info("=" * 70)
    logger.info("Mode_shift_bubt — Running All 11 Chi-square Analyses")
    logger.info("=" * 70)

    results = {}
    for analysis_dir in ANALYSES:
        logger.info("Running: %s ...", analysis_dir)
        success = run_analysis(analysis_dir)
        results[analysis_dir] = "PASS" if success else "FAIL"

    logger.info("=" * 70)
    logger.info("SUMMARY")
    logger.info("=" * 70)
    passed = sum(1 for v in results.values() if v == "PASS")
    for name, status in results.items():
        emoji = "[OK]  " if status == "PASS" else "[FAIL]"
        logger.info("%s %s", emoji, name)
    logger.info("-" * 70)
    logger.info("Total: %d/%d analyses passed.", passed, len(ANALYSES))


if __name__ == "__main__":
    main()
