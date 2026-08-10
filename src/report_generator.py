from datetime import datetime


def format_value(value):
    """
    Safely format numeric values.
    """

    if value is None:
        return "N/A"

    try:
        return f"{value:.2f}"

    except (TypeError, ValueError):

        return str(value)


def format_percentage(value):
    """
    Format percentage values.
    """

    if value is None:
        return "N/A"

    try:
        return f"{value:+.2f}%"

    except (TypeError, ValueError):

        return str(value)


def generate_report(
    results,
    business_findings=None,
    ai_summary=None
):
    """
    Generate a complete business anomaly report.
    """

    if business_findings is None:

        business_findings = []

    if ai_summary is None:

        ai_summary = {}

    lines = []

    # ==================================================
    # HEADER
    # ==================================================

    lines.append(
        "=" * 70
    )

    lines.append(
        "BUSINESS ANOMALY REPORT"
    )

    lines.append(
        "=" * 70
    )

    lines.append(
        f"Generated: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    lines.append("")

    # ==================================================
    # ANOMALY SUMMARY
    # ==================================================

    critical = [
        result
        for result in results
        if result.get("severity") == "CRITICAL"
    ]

    warnings = [
        result
        for result in results
        if result.get("severity") == "WARNING"
    ]

    high_impact = [
        result
        for result in results
        if result.get("business_impact") == "HIGH"
    ]

    lines.append(
        "ANOMALY SUMMARY"
    )

    lines.append(
        "-" * 70
    )

    lines.append(
        f"Total metrics analyzed: {len(results)}"
    )

    lines.append(
        f"Critical anomalies: {len(critical)}"
    )

    lines.append(
        f"Warnings: {len(warnings)}"
    )

    lines.append(
        f"High-impact metrics: {len(high_impact)}"
    )

    lines.append("")

    # ==================================================
    # METRIC DETAILS
    # ==================================================

    lines.append(
        "METRIC DETAILS"
    )

    lines.append(
        "-" * 70
    )

    for result in results:

        lines.append("")

        lines.append(
            f"Metric: {result.get('metric')}"
        )

        lines.append(
            f"Current value: "
            f"{format_value(result.get('current_value'))}"
        )

        lines.append(
            f"Day change: "
            f"{format_percentage(result.get('percentage_change'))}"
        )

        lines.append(
            f"Baseline deviation: "
            f"{format_percentage(result.get('baseline_deviation'))}"
        )

        lines.append(
            f"Z-score: "
            f"{format_value(result.get('z_score'))}"
        )

        lines.append(
            f"Anomaly score: "
            f"{result.get('score', 'N/A')}"
        )

        lines.append(
            f"Severity: "
            f"{result.get('severity', 'N/A')}"
        )

        lines.append(
            f"Business impact: "
            f"{result.get('business_impact', 'N/A')}"
        )

        lines.append(
            f"Priority: "
            f"{result.get('priority', 'N/A')}"
        )

    # ==================================================
    # BUSINESS FINDINGS
    # ==================================================

    lines.append("")
    lines.append(
        "BUSINESS FINDINGS"
    )
    lines.append(
        "-" * 70
    )

    if not business_findings:

        lines.append(
            "No significant business relationships detected."
        )

    else:

        for finding in business_findings:

            lines.append("")

            lines.append(
                f"Type: {finding.get('type')}"
            )

            lines.append(
                f"Severity: {finding.get('severity')}"
            )

            lines.append(
                f"Observation: "
                f"{finding.get('observation')}"
            )

            lines.append(
                f"Possible implication: "
                f"{finding.get('possible_implication')}"
            )

            lines.append(
                "Recommended checks:"
            )

            for check in finding.get(
                "recommended_checks",
                []
            ):

                lines.append(
                    f"  • {check}"
                )

    # ==================================================
    # AI EXECUTIVE SUMMARY
    # ==================================================

    lines.append("")
    lines.append(
        "AI BUSINESS SUMMARY"
    )
    lines.append(
        "-" * 70
    )

    executive_summary = ai_summary.get(
        "executive_summary"
    )

    if executive_summary:

        lines.append(
            executive_summary
        )

    else:

        lines.append(
            "AI summary unavailable."
        )

    # ==================================================
    # KEY FINDINGS
    # ==================================================

    lines.append("")

    lines.append(
        "Key Findings:"
    )

    for finding in ai_summary.get(
        "key_findings",
        []
    ):

        lines.append(
            f"  • {finding}"
        )

    # ==================================================
    # POSSIBLE CAUSES
    # ==================================================

    lines.append("")

    lines.append(
        "Possible Causes:"
    )

    for cause in ai_summary.get(
        "possible_causes",
        []
    ):

        lines.append(
            f"  • {cause}"
        )

    # ==================================================
    # RECOMMENDED ACTIONS
    # ==================================================

    lines.append("")

    lines.append(
        "Recommended Actions:"
    )

    for action in ai_summary.get(
        "recommended_actions",
        []
    ):

        lines.append(
            f"  • {action}"
        )

    # ==================================================
    # PRIORITY
    # ==================================================

    lines.append("")

    lines.append(
        "Priority Message:"
    )

    lines.append(
        ai_summary.get(
            "priority_message",
            "No priority message available."
        )
    )

    lines.append("")

    lines.append(
        "=" * 70
    )

    return "\n".join(lines)

