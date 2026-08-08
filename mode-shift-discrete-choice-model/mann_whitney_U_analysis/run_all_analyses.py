#!/usr/bin/env python3
"""
run_all_analyses.py
===================
Master script to run all 5 Mann-Whitney U sub-analyses sequentially.

Usage
-----
    python run_all_analyses.py

Author : Majharul Islam
Date   : 2026-08-09
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
    "01_security_harassment",
    "02_reliability",
    "03_road_accidents",
    "04_comfort",
    "05_crowding",
]


def run_analysis(analysis_dir: str) -> bool:
    # Check for python script in subfolder
    script_path = Path(analysis_dir) / f"mann_whitney_{analysis_dir}.py"
    if not script_path.exists():
        script_path = Path(analysis_dir) / "analysis.py"

    if not script_path.exists():
        logger.error("Script not found in %s", analysis_dir)
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
    logger.info("Mode_shift_bubt — Running All 5 Mann-Whitney U Sub-Analyses")
    logger.info("=" * 70)

    # First run root main pipeline
    logger.info("Running Master Root Pipeline (analysis_python.py)...")
    try:
        res = subprocess.run(
            [sys.executable, "analysis_python.py"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=300,
        )
        if res.returncode == 0:
            logger.info("[OK] Master Root Pipeline Passed")
        else:
            logger.error("[FAILED] Master Root Pipeline\n%s", res.stderr[-500:])
    except Exception as exc:
        logger.error("[ERROR] Master Root Pipeline — %s", exc)

    logger.info("-" * 70)
    results = {}
    for analysis_dir in ANALYSES:
        logger.info("Running sub-analysis: %s ...", analysis_dir)
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
    logger.info("Total: %d/%d sub-analyses passed.", passed, len(ANALYSES))


if __name__ == "__main__":
    main()
