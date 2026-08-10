import sys

from pathlib import Path

from datetime import datetime


# ======================================================
# PROJECT PATH
# ======================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
)

SRC_DIR = (
    BASE_DIR / "src"
)

if str(SRC_DIR) not in sys.path:

    sys.path.insert(
        0,
        str(SRC_DIR)
    )


# ======================================================
# IMPORT ANALYSIS PIPELINE
# ======================================================

from daily_analysis import (
    run_full_analysis
)


# ======================================================
# DATA FILE
# ======================================================

DATA_FILE = (
    BASE_DIR
    / "data"
    / "business_metrics.xlsx"
)


# ======================================================
# LOG DIRECTORY
# ======================================================

LOG_DIR = (
    BASE_DIR
    / "logs"
)

LOG_DIR.mkdir(
    exist_ok=True
)


# ======================================================
# LOG FILE
# ======================================================

LOG_FILE = (
    LOG_DIR
    / "scheduled_analysis.log"
)


# ======================================================
# LOGGER
# ======================================================

def write_log(message):

    timestamp = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    log_line = (
        f"[{timestamp}] {message}\n"
    )

    print(
        log_line,
        end=""
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            log_line
        )


# ======================================================
# RUN ANALYSIS
# ======================================================

def main():

    write_log(
        "=" * 60
    )

    write_log(
        "Scheduled analysis started."
    )

    write_log(
        f"Data file: {DATA_FILE}"
    )

    # --------------------------------------------------
    # Check Excel file
    # --------------------------------------------------

    if not DATA_FILE.exists():

        write_log(
            "ERROR: Excel data file was not found."
        )

        return 1

    try:

        # --------------------------------------------------
        # Run complete pipeline
        # --------------------------------------------------

        (
            results,
            business_findings,
            ai_summary,
            report,
            run_id,
            email_sent
        ) = run_full_analysis(
            str(DATA_FILE)
        )

        # --------------------------------------------------
        # Count anomalies
        # --------------------------------------------------

        critical_count = sum(

            1

            for result in results

            if result.get(
                "severity"
            ) == "CRITICAL"
        )

        warning_count = sum(

            1

            for result in results

            if result.get(
                "severity"
            ) == "WARNING"
        )

        # --------------------------------------------------
        # Log results
        # --------------------------------------------------

        write_log(
            f"Analysis run ID: {run_id}"
        )

        write_log(
            f"Metrics analyzed: {len(results)}"
        )

        write_log(
            f"Critical anomalies: {critical_count}"
        )

        write_log(
            f"Warnings: {warning_count}"
        )

        write_log(
            f"Email sent: {email_sent}"
        )

        write_log(
            "Scheduled analysis completed successfully."
        )

        write_log(
            "=" * 60
        )

        return 0

    except Exception as error:

        write_log(
            "ERROR: Scheduled analysis failed."
        )

        write_log(
            f"Reason: {error}"
        )

        write_log(
            "=" * 60
        )

        return 1


# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == "__main__":

    exit_code = main()

    sys.exit(
        exit_code
    )
