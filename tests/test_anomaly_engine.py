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


from anomaly_engine import (
    analyze_metric
)


# ======================================================
# TEST NORMAL METRIC
# ======================================================

def test_normal_metric():

    result = analyze_metric(

        metric="daily_transaction_volume",

        current_value=1000,

        percentage_change=1.0,

        baseline_deviation=1.5,

        z_score=0.5,
    )

    assert isinstance(
        result,
        dict
    )

    assert (
        result["metric"]
        == "daily_transaction_volume"
    )


# ======================================================
# TEST LARGE ANOMALY
# ======================================================

def test_large_anomaly():

    result = analyze_metric(

        metric="daily_transaction_volume",

        current_value=500,

        percentage_change=-40.0,

        baseline_deviation=-35.0,

        z_score=-4.0,
    )

    assert isinstance(
        result,
        dict
    )

    assert (
        result["metric"]
        == "daily_transaction_volume"
    )

    assert (
        result["score"]
        >= 0
    )


# ======================================================
# TEST REQUIRED FIELDS
# ======================================================

def test_required_fields():

    result = analyze_metric(

        metric="chargeback_count",

        current_value=100,

        percentage_change=5,

        baseline_deviation=4,

        z_score=1,
    )

    required_fields = [

        "metric",

        "current_value",

        "percentage_change",

        "baseline_deviation",

        "z_score",

        "score",

        "severity",

        "business_impact",

        "priority",
    ]

    for field in required_fields:

        assert field in result
