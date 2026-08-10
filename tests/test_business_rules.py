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


from business_rules import (
    evaluate_business_relationships
)


# ======================================================
# TEST BUSINESS RULE ENGINE
# ======================================================

def test_business_relationship_engine():

    results = [

        {
            "metric": "Revenue",

            "current_value": 800,

            "percentage_change": -20,

            "baseline_deviation": -18,

            "z_score": -2.5,

            "score": 80,

            "severity": "CRITICAL",

            "business_impact": "HIGH",

            "priority": "P0",
        },

        {
            "metric": "Orders",

            "current_value": 100,

            "percentage_change": -5,

            "baseline_deviation": -4,

            "z_score": -1.2,

            "score": 40,

            "severity": "WARNING",

            "business_impact": "MEDIUM",

            "priority": "P2",
        },

    ]

    findings = (
        evaluate_business_relationships(
            results
        )
    )

    assert isinstance(
        findings,
        list
    )


# ======================================================
# TEST EMPTY RESULTS
# ======================================================

def test_empty_results():

    findings = (
        evaluate_business_relationships(
            []
        )
    )

    assert isinstance(
        findings,
        list
    )

