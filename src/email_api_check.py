from email_alert import send_alert_email


test_results = [

    {
        "metric": "failed_transaction_rate",

        "current_value": 150000,

        "percentage_change": -25.5,

        "baseline_deviation": -30.2,

        "z_score": -3.1,

        "score": 95,

        "severity": "CRITICAL",

        "business_impact": "HIGH",

        "priority": "P0",
    }
]


test_findings = [

    {
        "type": "FAILED_TRANSACTION_SPIKE",

        "severity": "CRITICAL",

        "observation": (
            "The failed transaction rate has increased significantly."
        ),

        "possible_implication": (
            "The increase may indicate a possible payment-fraud "
            "pattern or a payment-processing issue."
        ),

        "recommended_checks": [
            "Review affected transactions for fraud indicators",
            "Compare failed transactions by payment channel",
            "Check payment gateway and authentication health",
        ],
    }
]


test_ai_summary = {

    "executive_summary": (
        "The failed transaction rate increased significantly "
        "and requires immediate review."
    ),

    "key_findings": [
        "Failed transaction rate increased significantly."
    ],

    "possible_causes": [
        "Possible transaction fraud",
        "Payment-processing disruption",
    ],

    "recommended_actions": [
        "Review affected transactions",
        "Check payment channel and authentication performance",
    ],

    "priority_message": (
        "Immediate investigation recommended."
    ),
}


result = send_alert_email(
    test_results,
    test_findings,
    test_ai_summary
)

print(
    f"Email test result: {result}"
)
