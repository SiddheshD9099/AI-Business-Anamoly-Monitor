from ai_analyzer import (
    generate_business_summary
)

from data_reader import (
    read_business_data
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


def analyze_latest_day(file_path):
    """
    Read, clean, analyze, and detect anomalies
    for the latest available business day.
    """

    # --------------------------------------------------
    # 1. READ DATA
    # --------------------------------------------------

    df = read_business_data(
        file_path
    )

    # --------------------------------------------------
    # 2. VALIDATE DATA
    # --------------------------------------------------

    validate_columns(
        df
    )

    # --------------------------------------------------
    # 3. CLEAN DATA
    # --------------------------------------------------

    df = clean_data(
        df
    )

    # --------------------------------------------------
    # 4. GET CONFIGURED METRICS
    # --------------------------------------------------

    metrics = list(
        METRIC_CONFIG.keys()
    )

    # --------------------------------------------------
    # 5. CALCULATE DAY-OVER-DAY CHANGES
    # --------------------------------------------------

    df = add_percentage_changes(
        df,
        metrics
    )

    # --------------------------------------------------
    # 6. CALCULATE 7-DAY BASELINE
    # --------------------------------------------------

    df = add_moving_average(
        df,
        metrics,
        window=7
    )

    # --------------------------------------------------
    # 7. CALCULATE BASELINE DEVIATION
    # --------------------------------------------------

    df = add_baseline_deviation(
        df,
        metrics
    )

    # --------------------------------------------------
    # 8. CALCULATE Z-SCORES
    # --------------------------------------------------

    df = add_z_scores(
        df,
        metrics,
        window=7
    )

    # --------------------------------------------------
    # 9. GET LATEST DAY
    # --------------------------------------------------

    latest = df.iloc[-1]

    results = []

    # --------------------------------------------------
    # 10. ANALYZE EACH METRIC
    # --------------------------------------------------

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
# MAIN PROGRAM
# ======================================================

if __name__ == "__main__":

    # --------------------------------------------------
    # 1. INPUT FILE
    # --------------------------------------------------

    file_path = "data/business_metrics.xlsx"

    # --------------------------------------------------
    # 2. RUN STATISTICAL ANALYSIS
    # --------------------------------------------------

    results = analyze_latest_day(
        file_path
    )

    # --------------------------------------------------
    # 3. EVALUATE BUSINESS RELATIONSHIPS
    # --------------------------------------------------

    business_findings = (
        evaluate_business_relationships(
            results
        )
    )

    # ==================================================
    # 4. PRINT ANOMALY ANALYSIS
    # ==================================================

    print()

    print("=" * 70)
    print(
        "BUSINESS ANOMALY ANALYSIS"
    )
    print("=" * 70)

    for result in results:

        print()

        print(
            f"Metric: "
            f"{result['metric']}"
        )

        print(
            f"Current Value: "
            f"{result['current_value']}"
        )

        # ----------------------------------------------
        # Day-over-day change
        # ----------------------------------------------

        percentage_change = (
            result["percentage_change"]
        )

        if percentage_change is not None:

            print(
                f"Day Change: "
                f"{percentage_change:+.2f}%"
            )

        else:

            print(
                "Day Change: N/A"
            )

        # ----------------------------------------------
        # Baseline deviation
        # ----------------------------------------------

        baseline_deviation = (
            result["baseline_deviation"]
        )

        if baseline_deviation is not None:

            print(
                f"Baseline Deviation: "
                f"{baseline_deviation:+.2f}%"
            )

        else:

            print(
                "Baseline Deviation: N/A"
            )

        # ----------------------------------------------
        # Z-score
        # ----------------------------------------------

        z_score = (
            result["z_score"]
        )

        if z_score is not None:

            print(
                f"Z-score: "
                f"{z_score:.2f}"
            )

        else:

            print(
                "Z-score: N/A"
            )

        # ----------------------------------------------
        # Anomaly score
        # ----------------------------------------------

        print(
            f"Anomaly Score: "
            f"{result['score']}"
        )

        # ----------------------------------------------
        # Severity
        # ----------------------------------------------

        print(
            f"Severity: "
            f"{result['severity']}"
        )

        # ----------------------------------------------
        # Business impact
        # ----------------------------------------------

        print(
            f"Business Impact: "
            f"{result['business_impact']}"
        )

        # ----------------------------------------------
        # Priority
        # ----------------------------------------------

        print(
            f"Priority: "
            f"{result['priority']}"
        )

        print(
            "-" * 70
        )

    # ==================================================
    # 5. PRINT BUSINESS FINDINGS
    # ==================================================

    print()

    print("=" * 70)
    print(
        "BUSINESS FINDINGS"
    )
    print("=" * 70)

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
                f"{finding['type']}"
            )

            print(
                f"Severity: "
                f"{finding['severity']}"
            )

            print(
                f"Observation: "
                f"{finding['observation']}"
            )

            print(
                f"Possible Implication: "
                f"{finding['possible_implication']}"
            )

            print(
                "Recommended Checks:"
            )

            for check in finding[
                "recommended_checks"
            ]:

                print(
                    f"  • {check}"
                )

            print(
                "-" * 70
            )

    # ==================================================
    # 6. GENERATE BASIC BUSINESS REPORT
    # ==================================================

    # ==================================================
    # 7. CREATE REPORTS DIRECTORY
    # ==================================================

    BASE_DIR = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    reports_dir = (
        BASE_DIR / "reports"
    )

    reports_dir.mkdir(
        exist_ok=True
    )

    # ==================================================
    # 8. CREATE TIMESTAMP
    # ==================================================

    timestamp = (
        datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    # ==================================================
    # 9. CREATE REPORT PATH
    # ==================================================

    report_path = (
        reports_dir
        / f"anomaly_report_{timestamp}.txt"
    )


    # ==================================================
    # 11. RUN GEMINI AI ANALYSIS
    # ==================================================

    print()

    print("=" * 70)
    print(
        "AI BUSINESS ANALYSIS"
    )
    print("=" * 70)

    ai_summary = (
        generate_business_summary(
            results,
            business_findings
        )
    )

# ==================================================
# GENERATE FINAL REPORT
# ==================================================

    report = generate_report(
        results,
        business_findings,
        ai_summary
    )

# ==================================================
# SAVE FINAL REPORT
# ==================================================

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    # ==================================================
    # 12. PRINT AI EXECUTIVE SUMMARY
    # ==================================================

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

    # ==================================================
    # 13. PRINT AI KEY FINDINGS
    # ==================================================

    print()

    print(
        "Key Findings:"
    )

    key_findings = ai_summary.get(
        "key_findings",
        []
    )

    if key_findings:

        for finding in key_findings:

            print(
                f"  • {finding}"
            )

    else:

        print(
            "  No key findings generated."
        )

    # ==================================================
    # 14. PRINT POSSIBLE CAUSES
    # ==================================================

    print()

    print(
        "Possible Causes:"
    )

    possible_causes = ai_summary.get(
        "possible_causes",
        []
    )

    if possible_causes:

        for cause in possible_causes:

            print(
                f"  • {cause}"
            )

    else:

        print(
            "  No possible causes generated."
        )

    # ==================================================
    # 15. PRINT RECOMMENDED ACTIONS
    # ==================================================

    print()

    print(
        "Recommended Actions:"
    )

    recommended_actions = ai_summary.get(
        "recommended_actions",
        []
    )

    if recommended_actions:

        for action in recommended_actions:

            print(
                f"  • {action}"
            )

    else:

        print(
            "  No recommended actions generated."
        )

    # ==================================================
    # 16. PRINT PRIORITY MESSAGE
    # ==================================================

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

    # ==================================================
    # 17. SAVE AI ANALYSIS TO REPORT
    # ==================================================

    with open(
        report_path,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n\n"
        )

        file.write(
            "=" * 70
        )

        file.write(
            "\nAI BUSINESS ANALYSIS\n"
        )

        file.write(
            "=" * 70
        )

        file.write(
            "\n\nExecutive Summary:\n"
        )

        file.write(
            ai_summary.get(
                "executive_summary",
                "No executive summary generated."
            )
        )

        file.write(
            "\n\nKey Findings:\n"
        )

        for finding in key_findings:

            file.write(
                f"\n• {finding}"
            )

        file.write(
            "\n\nPossible Causes:\n"
        )

        for cause in possible_causes:

            file.write(
                f"\n• {cause}"
            )

        file.write(
            "\n\nRecommended Actions:\n"
        )

        for action in recommended_actions:

            file.write(
                f"\n• {action}"
            )

        file.write(
            "\n\nPriority Message:\n"
        )

        file.write(
            ai_summary.get(
                "priority_message",
                "No priority message generated."
            )
        )

    # ==================================================
    # 18. FINAL OUTPUT
    # ==================================================

    print()

    print("=" * 70)

    print(
        f"Report saved to: "
        f"{report_path}"
    )

    print("=" * 70)

