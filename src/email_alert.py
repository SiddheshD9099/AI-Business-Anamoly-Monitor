import os
import smtplib

from email.message import EmailMessage

from dotenv import load_dotenv

from history_db import (
    alert_already_sent,
    save_alert
)


# ======================================================
# LOAD ENVIRONMENT VARIABLES
# ======================================================

load_dotenv()


# ======================================================
# EMAIL CONFIGURATION
# ======================================================

SMTP_HOST = os.getenv(
    "SMTP_HOST",
    "smtp.gmail.com"
)

SMTP_PORT = int(
    os.getenv(
        "SMTP_PORT",
        "587"
    )
)

SMTP_USERNAME = os.getenv(
    "SMTP_USERNAME"
)

SMTP_PASSWORD = os.getenv(
    "SMTP_PASSWORD"
)

ALERT_RECIPIENT = os.getenv(
    "ALERT_RECIPIENT"
)


# ======================================================
# CHECK EMAIL CONFIGURATION
# ======================================================

def email_is_configured():
    """
    Check whether all required email settings
    are available.
    """

    return all([
        SMTP_HOST,
        SMTP_PORT,
        SMTP_USERNAME,
        SMTP_PASSWORD,
        ALERT_RECIPIENT,
    ])


# ======================================================
# BUILD EMAIL BODY
# ======================================================

def build_alert_body(
    results,
    business_findings,
    ai_summary
):
    """
    Build a BFSI transaction-monitoring email body.
    """

    lines = []

    lines.append(
        "AI BFSI TRANSACTION RISK ALERT"
    )

    lines.append(
        "=" * 60
    )

    lines.append("")

    # ==================================================
    # ALERT SUMMARY
    # ==================================================

    critical_results = [

        result

        for result in results

        if result.get("severity")
        == "CRITICAL"
    ]

    high_impact_results = [

        result

        for result in results

        if result.get("business_impact")
        == "HIGH"
    ]

    lines.append(
        "ALERT SUMMARY"
    )

    lines.append(
        "-" * 60
    )

    lines.append(
        f"Critical anomalies: "
        f"{len(critical_results)}"
    )

    lines.append(
        "High-risk-impact metrics: "
        f"{len(high_impact_results)}"
    )

    lines.append("")

    # ==================================================
    # CRITICAL METRICS
    # ==================================================

    if critical_results:

        lines.append(
            "CRITICAL ANOMALIES"
        )

        lines.append(
            "-" * 60
        )

        for result in critical_results:

            metric = result.get(
                "metric",
                "Unknown"
            )

            change = result.get(
                "percentage_change"
            )

            impact = result.get(
                "business_impact",
                "UNKNOWN"
            )

            priority = result.get(
                "priority",
                "UNKNOWN"
            )

            lines.append(
                f"Metric: {metric}"
            )

            if change is not None:

                try:

                    lines.append(
                        f"Change: {float(change):+.2f}%"
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    lines.append(
                        f"Change: {change}"
                    )

            else:

                lines.append(
                    "Change: N/A"
                )

            lines.append(
                f"Risk Impact: {impact}"
            )

            lines.append(
                f"Priority: {priority}"
            )

            lines.append("")

    # ==================================================
    # BUSINESS FINDINGS
    # ==================================================

    if business_findings:

        lines.append(
            "BFSI RISK FINDINGS"
        )

        lines.append(
            "-" * 60
        )

        for finding in business_findings:

            lines.append(
                f"Type: "
                f"{finding.get('type')}"
            )

            lines.append(
                f"Severity: "
                f"{finding.get('severity')}"
            )

            lines.append(
                f"Observation: "
                f"{finding.get('observation')}"
            )

            lines.append(
                f"Possible implication: "
                f"{finding.get('possible_implication')}"
            )

            lines.append("")

    # ==================================================
    # AI SUMMARY
    # ==================================================

    lines.append(
        "AI EXECUTIVE SUMMARY"
    )

    lines.append(
        "-" * 60
    )

    if isinstance(
        ai_summary,
        dict
    ):

        lines.append(
            ai_summary.get(
                "executive_summary",
                "No AI summary available."
            )
        )

    else:

        lines.append(
            str(ai_summary)
            if ai_summary
            else "No AI summary available."
        )

    lines.append("")

    # ==================================================
    # RECOMMENDED ACTIONS
    # ==================================================

    lines.append(
        "RECOMMENDED ACTIONS"
    )

    lines.append(
        "-" * 60
    )

    if isinstance(
        ai_summary,
        dict
    ):

        actions = ai_summary.get(
            "recommended_actions",
            []
        )

    else:

        actions = []

    if actions:

        for action in actions:

            lines.append(
                f"• {action}"
            )

    else:

        lines.append(
            "No specific actions generated."
        )

    lines.append("")

    # ==================================================
    # PRIORITY
    # ==================================================

    lines.append(
        "PRIORITY"
    )

    lines.append(
        "-" * 60
    )

    if isinstance(
        ai_summary,
        dict
    ):

        lines.append(
            ai_summary.get(
                "priority_message",
                "No priority message available."
            )
        )

    else:

        lines.append(
            "No priority message available."
        )

    lines.append("")

    lines.append(
        "=" * 60
    )

    lines.append(
        "Generated by AI BFSI Transaction Monitor"
    )

    return "\n".join(lines)


# ======================================================
# SEND EMAIL
# ======================================================

def send_alert_email(
    results,
    business_findings,
    ai_summary,
    run_id=None,
    analysis_date=None
):
    """
    Send an anomaly alert email only for NEW P0/P1
    anomalies.

    Duplicate identity:

        metric
        + priority
        + analysis_date

    Returns:

        True  = email sent
        False = no email sent
    """

    # ==================================================
    # CONFIGURATION CHECK
    # ==================================================

    if not email_is_configured():

        print(
            "Email alert skipped: "
            "email configuration is incomplete."
        )

        return False

    # ==================================================
    # ANALYSIS DATE CHECK
    # ==================================================

    if analysis_date is None:

        print(
            "Email alert skipped: "
            "analysis_date is missing."
        )

        return False

    # ==================================================
    # NORMALIZE DATE
    # ==================================================

    try:

        import pandas as pd

        normalized_date = (
            pd.to_datetime(
                analysis_date
            ).strftime(
                "%Y-%m-%d"
            )
        )

    except Exception as error:

        print(
            "Email alert skipped: "
            f"invalid analysis_date: {error}"
        )

        return False

    print(
        f"Alert analysis date: "
        f"{normalized_date}"
    )

    # ==================================================
    # FIND P0/P1 ANOMALIES
    # ==================================================

    alert_results = [

        result

        for result in results

        if result.get("priority")
        in ["P0", "P1"]

    ]

    if not alert_results:

        print(
            "No P0/P1 anomalies detected. "
            "Email alert not required."
        )

        return False

    print(
        f"P0/P1 anomalies detected: "
        f"{len(alert_results)}"
    )

    # ==================================================
    # FIND NEW ALERTS
    # ==================================================

    new_alerts = []

    for result in alert_results:

        metric = result.get(
            "metric",
            "Unknown"
        )

        priority = result.get(
            "priority",
            "P1"
        )

        print(
            f"Checking alert history: "
            f"metric={metric}, "
            f"priority={priority}, "
            f"date={normalized_date}"
        )

        already_sent = (
            alert_already_sent(
                metric=metric,
                priority=priority,
                analysis_date=normalized_date
            )
        )

        print(
            f"Already alerted: "
            f"{already_sent}"
        )

        if not already_sent:

            new_alerts.append(
                result
            )

    # ==================================================
    # NO NEW ALERTS
    # ==================================================

    if not new_alerts:

        print(
            "P0/P1 anomalies detected, but "
            "all matching alerts have already "
            "been sent for this analysis date."
        )

        return False

    # ==================================================
    # EMAIL SUBJECT
    # ==================================================

    has_p0 = any(

        result.get("priority")
        == "P0"

        for result in new_alerts
    )

    if has_p0:

        subject = (
            "🚨 CRITICAL BFSI Risk Anomaly Detected"
        )

    else:

        subject = (
            "⚠️ BFSI Transaction Risk Alert"
        )

    # ==================================================
    # BUILD EMAIL BODY
    # ==================================================

    # Only NEW anomalies are included.

    body = build_alert_body(
        new_alerts,
        business_findings,
        ai_summary
    )

    # ==================================================
    # CREATE EMAIL MESSAGE
    # ==================================================

    message = EmailMessage()

    message["From"] = SMTP_USERNAME

    message["To"] = ALERT_RECIPIENT

    message["Subject"] = subject

    message.set_content(
        body
    )

    # ==================================================
    # SEND EMAIL
    # ==================================================

    try:

        print(
            "Connecting to SMTP server..."
        )

        with smtplib.SMTP(
            SMTP_HOST,
            SMTP_PORT,
            timeout=30
        ) as server:

            server.starttls()

            server.login(
                SMTP_USERNAME,
                SMTP_PASSWORD
            )

            server.send_message(
                message
            )

        print(
            "Email sent successfully."
        )

    except Exception as error:

        print(
            "Email alert failed."
        )

        print(
            f"Reason: {error}"
        )

        return False

    # ==================================================
    # RECORD ALERTS AFTER SUCCESSFUL EMAIL
    # ==================================================

    saved_count = 0

    for result in new_alerts:

        try:

            saved = save_alert(

                run_id=run_id,

                metric=result.get(
                    "metric",
                    "Unknown"
                ),

                priority=result.get(
                    "priority",
                    "P1"
                ),

                severity=result.get(
                    "severity"
                ),

                percentage_change=result.get(
                    "percentage_change"
                ),

                analysis_date=normalized_date
            )

            if saved:

                saved_count += 1

        except Exception as error:

            print(
                "WARNING: Email was sent but "
                f"alert history could not be saved "
                f"for metric "
                f"{result.get('metric', 'Unknown')}: "
                f"{error}"
            )

    # ==================================================
    # FINAL STATUS
    # ==================================================

    print(
        f"Alert history updated: "
        f"{saved_count}/{len(new_alerts)}"
    )

    if (
        saved_count
        == len(new_alerts)
    ):

        print(
            "Email alert completed successfully "
            "and all alerts were recorded."
        )

    else:

        print(
            "WARNING: Email was sent, but "
            "not all alerts were recorded "
            "in the database."
        )

    return True
