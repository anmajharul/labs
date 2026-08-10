#!/usr/bin/env python3
"""
run_all_analyses.py
===================
Master script to run all 4 Kruskal-Wallis analyses sequentially.

Usage
-----
    python run_all_analyses.py

Author : Majharul Islam
Date   : 2026-08-11
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] -- %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("run_all")

ANALYSES = [
    "analysis_01_one_way_cost",
    "analysis_02_access_time",
    "analysis_03_in_vehicle_time",
    "analysis_04_total_travel_time",
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
        logger.error("[ERROR] %s -- %s", analysis_dir, exc)
        return False


def main() -> None:
    logger.info("=" * 70)
    logger.info("Mode_shift_bubt -- Running All 4 Kruskal-Wallis H Analyses")
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
