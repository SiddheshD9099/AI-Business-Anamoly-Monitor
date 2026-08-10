def calculate_business_impact(
    metric,
    severity,
    percentage_change
):
    """
    Determine the potential business impact
    of an anomaly.
    """

    impact = "LOW"

    if metric == "Revenue":

        if severity == "CRITICAL":
            impact = "HIGH"

        elif severity == "WARNING":
            impact = "MEDIUM"

    elif metric == "Conversion_Rate":

        if percentage_change is not None:

            if percentage_change <= -20:
                impact = "HIGH"

            elif percentage_change <= -10:
                impact = "MEDIUM"

    elif metric == "Refunds":

        if percentage_change is not None:

            if percentage_change >= 50:
                impact = "HIGH"

            elif percentage_change >= 25:
                impact = "MEDIUM"

    elif metric == "Cost":

        if percentage_change is not None:

            if percentage_change >= 30:
                impact = "HIGH"

            elif percentage_change >= 15:
                impact = "MEDIUM"

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