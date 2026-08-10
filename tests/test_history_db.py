import sys
from pathlib import Path


# ======================================================
# ADD SRC TO PATH
# ======================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

SRC_DIR = BASE_DIR / "src"

sys.path.insert(
    0,
    str(SRC_DIR)
)


from history_db import (
    initialize_database,
    save_analysis,
    get_run_history,
    get_metric_history,
    get_alert_history,
)


# ======================================================
# TEST DATABASE INITIALIZATION
# ======================================================

def test_database_initialization():

    initialize_database()

    assert True


# ======================================================
# TEST SAVE ANALYSIS
# ======================================================

def test_save_analysis():

    results = [

        {
            "metric": "Revenue",

            "current_value": 1000,

            "percentage_change": 5,

            "baseline_deviation": 4,

            "z_score": 1.2,

            "score": 20,

            "severity": "NORMAL",

            "business_impact": "LOW",

            "priority": "P3",
        }
    ]

    business_findings = []

    run_id = save_analysis(

        results,

        business_findings,

        analysis_date="2026-08-10"
    )

    assert run_id is not None


# ======================================================
# TEST RUN HISTORY
# ======================================================

def test_run_history():

    df = get_run_history()

    assert df is not None

    assert hasattr(
        df,
        "columns"
    )


# ======================================================
# TEST METRIC HISTORY
# ======================================================

def test_metric_history():

    df = get_metric_history()

    assert df is not None

    assert hasattr(
        df,
        "columns"
    )


# ======================================================
# TEST ALERT HISTORY
# ======================================================

def test_alert_history():

    df = get_alert_history()

    assert df is not None

    assert hasattr(
        df,
        "columns"
    )

