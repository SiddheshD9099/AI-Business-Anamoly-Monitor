def calculate_business_impact(
    metric,
    severity,
    percentage_change
):
    """
    Determine the potential business impact
    of an anomaly.
    """

    impact = {
        "CRITICAL": "HIGH",
        "WARNING": "MEDIUM",
    }.get(severity, "LOW")

    if percentage_change is None:
        return impact

    if metric == "failed_transaction_rate":
        if percentage_change >= 50:
            return "HIGH"
        if percentage_change >= 20:
            return "MEDIUM"

    elif metric == "chargeback_count":
        if percentage_change >= 50:
            return "HIGH"
        if percentage_change >= 25:
            return "MEDIUM"

    elif metric == "npa_ratio":
        if percentage_change >= 25:
            return "HIGH"
        if percentage_change >= 10:
            return "MEDIUM"

    elif metric in {
        "loan_disbursal_amount",
        "avg_transaction_value"
    }:
        if percentage_change >= 50:
            return "HIGH"
        if percentage_change >= 25:
            return "MEDIUM"

    return impact


def determine_priority(
    severity,
    business_impact
):
    """
    Determine business priority based on
    anomaly severity and business impact.
    """

    if (
        severity == "CRITICAL"
        and business_impact == "HIGH"
    ):
        return "P0"

    if (
        severity == "CRITICAL"
        or business_impact == "HIGH"
    ):
        return "P1"

    if (
        severity == "WARNING"
        or business_impact == "MEDIUM"
    ):
        return "P2"

    return "P3"