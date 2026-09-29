import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from business_rules import evaluate_business_relationships


def test_bfsi_relationship_rules_detect_all_risk_signals():
    results = [
        {
            "metric": "failed_transaction_rate",
            "percentage_change": 80,
            "baseline_deviation": 50,
            "severity": "CRITICAL",
        },
        {
            "metric": "chargeback_count",
            "percentage_change": 90,
            "baseline_deviation": 70,
            "severity": "CRITICAL",
        },
        {
            "metric": "loan_disbursal_amount",
            "percentage_change": 40,
            "baseline_deviation": 35,
            "severity": "CRITICAL",
        },
        {
            "metric": "npa_ratio",
            "percentage_change": 25,
            "baseline_deviation": 20,
            "severity": "CRITICAL",
        },
        {
            "metric": "avg_transaction_value",
            "percentage_change": 45,
            "baseline_deviation": 40,
            "severity": "CRITICAL",
        },
        {
            "metric": "daily_transaction_volume",
            "percentage_change": -30,
            "baseline_deviation": -25,
            "severity": "CRITICAL",
        },
    ]

    findings = evaluate_business_relationships(results)

    assert {
        finding["type"]
        for finding in findings
    } == {
        "TRANSACTION_FAILURE_CHARGEBACK_SPIKE",
        "DISBURSAL_NPA_RISK",
        "TRANSACTION_CONCENTRATION_RISK",
    }
    assert all(
        {
            "observation",
            "severity",
            "possible_implication",
            "recommended_checks",
        }.issubset(finding)
        for finding in findings
    )


def test_relationship_rules_require_both_related_metrics():
    findings = evaluate_business_relationships(
        [
            {
                "metric": "failed_transaction_rate",
                "baseline_deviation": 50,
                "percentage_change": 50,
                "severity": "CRITICAL",
            }
        ]
    )

    assert findings == []


def test_empty_results():
    assert evaluate_business_relationships([]) == []
