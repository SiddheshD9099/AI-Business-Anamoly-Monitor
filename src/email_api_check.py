from email_alert import send_alert_email


test_results = [

    {
        "metric": "Revenue",

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
        "type": "REVENUE_DECLINE",

        "severity": "CRITICAL",

        "observation": (
            "Revenue has declined significantly."
        ),

        "possible_implication": (
            "The decline may indicate a problem "
            "with demand, conversion, or sales."
        ),

        "recommended_checks": [
            "Review traffic sources",
            "Check conversion rate",
            "Review recent campaigns",
        ],
    }
]


test_ai_summary = {

    "executive_summary": (
        "Revenue has declined significantly "
        "and requires immediate investigation."
    ),

    "key_findings": [
        "Revenue decreased significantly."
    ],

    "possible_causes": [
        "Lower conversion",
        "Reduced traffic quality",
    ],

    "recommended_actions": [
        "Review acquisition channels",
        "Check conversion performance",
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

