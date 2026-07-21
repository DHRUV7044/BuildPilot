"""
Manual Build - Pull, build, and upload immediately
Use this when you want to force a build without waiting for the auto-checker
"""

import sys
import logging
from pathlib import Path

# Import shared settings
from settings import *

# Import the automation class from auto_updater
from auto_updater import BuildAutomation, setup_logging

sys.dont_write_bytecode = True

logger = setup_logging()


def main():
    logger.info("=" * 50)
    logger.info("Manual Build Started")
    logger.info(f"Project: {PROJECT_DIR}")
    logger.info("=" * 50)

    automation = BuildAutomation()

    # Get current commit info for release
    result = automation.run_command([automation.git_cmd, "rev-parse", "HEAD"])
    if result and result.returncode == 0:
        automation.last_commit_hash = result.stdout.strip()

    logger.info("Running full pipeline...")
    success = automation.run_full_pipeline()

    if success:
        logger.info("=" * 50)
        logger.info("Manual build completed successfully!")
        logger.info("=" * 50)
        return 0
    else:
        logger.error("=" * 50)
        logger.error("Manual build failed!")
        logger.error("=" * 50)
        return 1


if __name__ == "__main__":
    sys.exit(main())
