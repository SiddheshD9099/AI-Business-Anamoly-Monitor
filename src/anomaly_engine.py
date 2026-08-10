from anomaly_scoring import (
    calculate_anomaly_score,
    determine_severity,
)

from impact_engine import (
    calculate_business_impact,
    determine_priority,
)


def analyze_metric(
    metric,
    current_value,
    percentage_change,
    baseline_deviation,
    z_score,
):
    """
    Analyze one business metric using
    multiple statistical signals.
    """

    score = calculate_anomaly_score(
        percentage_change,
        baseline_deviation,
        z_score,
    )

    severity = determine_severity(score)

    impact = calculate_business_impact(
        metric,
        severity,
        percentage_change
    )

    priority = determine_priority(
        severity,
        impact
    )

    return {
        "metric": metric,
        "current_value": current_value,
        "percentage_change": percentage_change,
        "baseline_deviation": baseline_deviation,
        "z_score": z_score,
        "score": score,
        "severity": severity,
        "business_impact": impact,
        "priority": priority,
    }