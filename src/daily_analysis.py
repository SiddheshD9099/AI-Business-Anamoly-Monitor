from history_db import (
    save_analysis
)

from email_alert import (
    send_alert_email
)

from data_reader import (
    read_business_data
)

from ai_analyzer import (
    generate_business_summary
)

from data_validator import (
    validate_columns
)

from data_cleaner import (
    clean_data
)

from metrics import (
    add_percentage_changes,
    add_moving_average,
    add_baseline_deviation,
    add_z_scores,
)

from config import (
    METRIC_CONFIG
)

from anomaly_engine import (
    analyze_metric
)

from business_rules import (
    evaluate_business_relationships
)

from report_generator import (
    generate_report
)

from datetime import datetime

from pathlib import Path


# ======================================================
# ANALYZE LATEST BUSINESS DAY
# ======================================================

def analyze_latest_day(file_path):
    """
    Read, clean, analyze, and detect anomalies
    for the latest available business day.
    """

    # ==================================================
    # 1. READ DATA
    # ==================================================

    df = read_business_data(
        file_path
    )

    # ==================================================
    # 2. VALIDATE DATA
    # ==================================================

    validate_columns(
        df
    )

    # ==================================================
    # 3. CLEAN DATA
    # ==================================================

    df = clean_data(
        df
    )

    # ==================================================
    # 4. SORT BY DATE
    # ==================================================

    if "Date" in df.columns:

        df["Date"] = (
            __import__("pandas")
            .to_datetime(
                df["Date"],
                errors="coerce"
            )
        )

        df = (
            df
            .dropna(
                subset=["Date"]
            )
            .sort_values(
                "Date"
            )
            .reset_index(
                drop=True
            )
        )

    if df.empty:

        raise ValueError(
            "No valid business data available "
            "after cleaning."
        )

    # ==================================================
    # 5. GET CONFIGURED METRICS
    # ==================================================

    metrics = list(
        METRIC_CONFIG.keys()
    )

    # ==================================================
    # 6. CALCULATE DAY-OVER-DAY CHANGES
    # ==================================================

    df = add_percentage_changes(
        df,
        metrics
    )

    # ==================================================
    # 7. CALCULATE 7-DAY MOVING AVERAGE
    # ==================================================

    df = add_moving_average(
        df,
        metrics,
        window=7
    )

    # ==================================================
    # 8. CALCULATE BASELINE DEVIATION
    # ==================================================

    df = add_baseline_deviation(
        df,
        metrics
    )

    # ==================================================
    # 9. CALCULATE Z-SCORES
    # ==================================================

    df = add_z_scores(
        df,
        metrics,
        window=7
    )

    # ==================================================
    # 10. GET LATEST BUSINESS DAY
    # ==================================================

    latest = df.iloc[-1]

    results = []

    # ==================================================
    # 11. ANALYZE EACH METRIC
    # ==================================================

    for metric in metrics:

        result = analyze_metric(

            metric=metric,

            current_value=latest[
                metric
            ],

            percentage_change=latest[
                f"{metric}_Change"
            ],

            baseline_deviation=latest[
                f"{metric}_Baseline_Deviation"
            ],

            z_score=latest[
                f"{metric}_ZScore"
            ],
        )

        results.append(
            result
        )

    return results


# ======================================================
# RUN COMPLETE ANALYSIS
# ======================================================

def run_full_analysis(file_path):
    """
    Run the complete business anomaly monitoring pipeline.

    Pipeline:

        Excel
        ↓
        Validation
        ↓
        Cleaning
        ↓
        Statistical analysis
        ↓
        Business relationship analysis
        ↓
        Gemini AI analysis
        ↓
        Report generation
        ↓
        SQLite persistence
        ↓
        Email alert
    """

    # ==================================================
    # 1. READ SOURCE DATA
    # ==================================================

    source_df = read_business_data(
        file_path
    )

    # ==================================================
    # 2. VALIDATE SOURCE DATA
    # ==================================================

    validate_columns(
        source_df
    )

    # ==================================================
    # 3. DETERMINE LATEST BUSINESS DATE
    # ==================================================

    if "Date" not in source_df.columns:

        raise ValueError(
            "The business data must contain "
            "a 'Date' column."
        )

    import pandas as pd

    source_df["Date"] = pd.to_datetime(
        source_df["Date"],
        errors="coerce"
    )

    source_df = (
        source_df
        .dropna(
            subset=["Date"]
        )
        .sort_values(
            "Date"
        )
        .reset_index(
            drop=True
        )
    )

    if source_df.empty:

        raise ValueError(
            "No valid business dates were found."
        )

    latest_date = (
        source_df["Date"]
        .iloc[-1]
    )

    latest_date = (
        latest_date.strftime(
            "%Y-%m-%d"
        )
    )

    print()
    print(
        "=" * 70
    )

    print(
        "BUSINESS ANOMALY MONITOR"
    )

    print(
        "=" * 70
    )

    print(
        f"Business date being analyzed: "
        f"{latest_date}"
    )

    # ==================================================
    # 4. STATISTICAL ANALYSIS
    # ==================================================

    results = analyze_latest_day(
        file_path
    )

    # ==================================================
    # 5. BUSINESS RELATIONSHIP ANALYSIS
    # ==================================================

    business_findings = (
        evaluate_business_relationships(
            results
        )
    )

    # ==================================================
    # 6. AI ANALYSIS
    # ==================================================

    ai_summary = (
        generate_business_summary(
            results,
            business_findings
        )
    )

    # ==================================================
    # 7. GENERATE REPORT
    # ==================================================

    report = generate_report(
        results,
        business_findings,
        ai_summary
    )

    # ==================================================
    # 8. SAVE ANALYSIS TO DATABASE
    # ==================================================

    run_id = save_analysis(

        results,

        business_findings,

        analysis_date=latest_date
    )

    print()
    print(
        f"Analysis saved to database. "
        f"Run ID: {run_id}"
    )

    # ==================================================
    # 9. SEND EMAIL ALERT
    # ==================================================

    email_sent = send_alert_email(

        results,

        business_findings,

        ai_summary,

        run_id=run_id,

        analysis_date=latest_date
    )

    # ==================================================
    # 10. SAVE REPORT TO FILE
    # ==================================================

    base_dir = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    reports_dir = (
        base_dir / "reports"
    )

    reports_dir.mkdir(
        exist_ok=True
    )

    timestamp = (
        datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    report_path = (
        reports_dir
        / f"anomaly_report_{timestamp}.txt"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            report
        )

    print()
    print(
        f"Report saved to: "
        f"{report_path}"
    )

    # ==================================================
    # 11. RETURN COMPLETE RESULT
    # ==================================================

    return (

        results,

        business_findings,

        ai_summary,

        report,

        run_id,

        email_sent
    )


# ======================================================
# MAIN PROGRAM
# ======================================================

if __name__ == "__main__":

    file_path = (
        "data/business_metrics.xlsx"
    )

    try:

        (
            results,
            business_findings,
            ai_summary,
            report,
            run_id,
            email_sent
        ) = run_full_analysis(
            file_path
        )

        # ==================================================
        # PRINT RESULTS
        # ==================================================

        print()
        print(
            "=" * 70
        )

        print(
            "BUSINESS ANOMALY ANALYSIS"
        )

        print(
            "=" * 70
        )

        for result in results:

            print()

            print(
                f"Metric: "
                f"{result.get('metric')}"
            )

            print(
                f"Current Value: "
                f"{result.get('current_value')}"
            )

            percentage_change = (
                result.get(
                    "percentage_change"
                )
            )

            if percentage_change is not None:

                try:

                    print(
                        f"Day Change: "
                        f"{float(percentage_change):+.2f}%"
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    print(
                        f"Day Change: "
                        f"{percentage_change}"
                    )

            else:

                print(
                    "Day Change: N/A"
                )

            baseline_deviation = (
                result.get(
                    "baseline_deviation"
                )
            )

            if baseline_deviation is not None:

                try:

                    print(
                        f"Baseline Deviation: "
                        f"{float(baseline_deviation):+.2f}%"
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    print(
                        f"Baseline Deviation: "
                        f"{baseline_deviation}"
                    )

            else:

                print(
                    "Baseline Deviation: N/A"
                )

            z_score = (
                result.get(
                    "z_score"
                )
            )

            if z_score is not None:

                try:

                    print(
                        f"Z-score: "
                        f"{float(z_score):.2f}"
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    print(
                        f"Z-score: "
                        f"{z_score}"
                    )

            else:

                print(
                    "Z-score: N/A"
                )

            print(
                f"Anomaly Score: "
                f"{result.get('score')}"
            )

            print(
                f"Severity: "
                f"{result.get('severity')}"
            )

            print(
                f"Business Impact: "
                f"{result.get('business_impact')}"
            )

            print(
                f"Priority: "
                f"{result.get('priority')}"
            )

            print(
                "-" * 70
            )

        # ==================================================
        # BUSINESS FINDINGS
        # ==================================================

        print()
        print(
            "=" * 70
        )

        print(
            "BUSINESS FINDINGS"
        )

        print(
            "=" * 70
        )

        if not business_findings:

            print()
            print(
                "No significant business "
                "relationships were detected."
            )

        else:

            for finding in business_findings:

                print()

                print(
                    f"Type: "
                    f"{finding.get('type')}"
                )

                print(
                    f"Severity: "
                    f"{finding.get('severity')}"
                )

                print(
                    f"Observation: "
                    f"{finding.get('observation')}"
                )

                print(
                    f"Possible Implication: "
                    f"{finding.get('possible_implication')}"
                )

                print(
                    "Recommended Checks:"
                )

                for check in finding.get(
                    "recommended_checks",
                    []
                ):

                    print(
                        f"  • {check}"
                    )

                print(
                    "-" * 70
                )

        # ==================================================
        # AI SUMMARY
        # ==================================================

        print()
        print(
            "=" * 70
        )

        print(
            "AI BUSINESS ANALYSIS"
        )

        print(
            "=" * 70
        )

        if isinstance(
            ai_summary,
            dict
        ):

            print()
            print(
                "Executive Summary:"
            )

            print(
                ai_summary.get(
                    "executive_summary",
                    "No executive summary generated."
                )
            )

            print()
            print(
                "Key Findings:"
            )

            for finding in ai_summary.get(
                "key_findings",
                []
            ):

                print(
                    f"  • {finding}"
                )

            print()
            print(
                "Possible Causes:"
            )

            for cause in ai_summary.get(
                "possible_causes",
                []
            ):

                print(
                    f"  • {cause}"
                )

            print()
            print(
                "Recommended Actions:"
            )

            for action in ai_summary.get(
                "recommended_actions",
                []
            ):

                print(
                    f"  • {action}"
                )

            print()
            print(
                "Priority Message:"
            )

            print(
                ai_summary.get(
                    "priority_message",
                    "No priority message generated."
                )
            )

        else:

            print(
                ai_summary
            )

        # ==================================================
        # EMAIL STATUS
        # ==================================================

        print()
        print(
            "=" * 70
        )

        print(
            "EMAIL STATUS"
        )

        print(
            "=" * 70
        )

        if email_sent:

            print(
                "Email alert: SENT"
            )

        else:

            print(
                "Email alert: NOT SENT"
            )

        print(
            "=" * 70
        )

    except Exception as error:

        print()
        print(
            "=" * 70
        )

        print(
            "ANALYSIS FAILED"
        )

        print(
            "=" * 70
        )

        print(
            f"Reason: {error}"
        )

        raise
