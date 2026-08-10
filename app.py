import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ======================================================
# PROJECT PATH
# ======================================================

BASE_DIR = Path(
    __file__
).resolve().parent

SRC_DIR = BASE_DIR / "src"

if str(SRC_DIR) not in sys.path:

    sys.path.insert(
        0,
        str(SRC_DIR)
    )


# ======================================================
# IMPORT ANALYSIS PIPELINE
# ======================================================

from daily_analysis import (
    run_full_analysis
)

from history_db import (
    get_metric_history,
    get_run_history,
    get_alert_history
)


# ======================================================
# STREAMLIT CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="AI Business Anomaly Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 650;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ======================================================
# HEADER
# ======================================================

st.markdown(
    '<div class="main-title">'
    'AI Business Anomaly Monitor'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Automated statistical monitoring and '
    'AI-powered business intelligence'
    '</div>',
    unsafe_allow_html=True
)


# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title(
    "Monitor Controls"
)

st.sidebar.info(
    "The dashboard analyzes the latest available "
    "business data from the Excel source."
)

st.sidebar.markdown(
    "---"
)

st.sidebar.caption(
    "System Status"
)

st.sidebar.success(
    "Database: Connected"
)

st.sidebar.success(
    "Analysis Engine: Ready"
)

st.sidebar.success(
    "AI Engine: Ready"
)

# ======================================================
# DATA FILE
# ======================================================

data_file = (
    BASE_DIR
    / "data"
    / "business_metrics.xlsx"
)


# ======================================================
# RUN ANALYSIS BUTTON
# ======================================================

run_analysis = st.sidebar.button(
    "Run Analysis",
    type="primary",
    use_container_width=True
)


# ======================================================
# LOAD ANALYSIS
# ======================================================

if (
    "analysis_data" not in st.session_state
    or run_analysis
):

    try:

        with st.spinner(
            "Analyzing business data..."
        ):

            (
                results,
                business_findings,
                ai_summary,
                report,
                run_id,
                email_sent
            ) = run_full_analysis(
                str(data_file)
            )

            st.session_state[
                "analysis_data"
            ] = {

                "results": results,

                "business_findings":
                    business_findings,

                "ai_summary":
                    ai_summary,

                "report":
                    report,

                "run_id":
                    run_id,

                "email_sent": 
                    email_sent,
            }

    except Exception as error:

        st.error(
            "Unable to run the analysis."
        )

        st.exception(
            error
        )

        st.stop()


# ======================================================
# GET RESULTS
# ======================================================

analysis = st.session_state[
    "analysis_data"
]

results = analysis[
    "results"
]

business_findings = analysis[
    "business_findings"
]

ai_summary = analysis[
    "ai_summary"
]

report = analysis[
    "report"
]

run_id = analysis.get(
    "run_id"
)

email_sent = analysis.get(
    "email_sent",
    False
)


# ======================================================
# SUMMARY COUNTS
# ======================================================

critical_count = sum(
    1
    for result in results
    if result.get("severity")
    == "CRITICAL"
)

warning_count = sum(
    1
    for result in results
    if result.get("severity")
    == "WARNING"
)

normal_count = sum(
    1
    for result in results
    if result.get("severity")
    == "NORMAL"
)

high_impact_count = sum(
    1
    for result in results
    if result.get("business_impact")
    == "HIGH"
)


# ======================================================
# MONITORING OVERVIEW
# ======================================================

st.markdown(
    '<div class="section-title">'
    'Monitoring Overview'
    '</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Metrics Analyzed",
        len(results)
    )


with col2:

    st.metric(
        "Critical Anomalies",
        critical_count
    )


with col3:

    st.metric(
        "Warnings",
        warning_count
    )


with col4:

    st.metric(
        "High Business Impact",
        high_impact_count
    )


# ======================================================
# ANOMALY TABLE
# ======================================================

st.markdown(
    '<div class="section-title">'
    'Metric Analysis'
    '</div>',
    unsafe_allow_html=True
)


table_data = []

for result in results:

    table_data.append({

        "Metric":
            result.get("metric"),

        "Current Value":
            result.get("current_value"),

        "Day Change":
            result.get("percentage_change"),

        "Baseline Deviation":
            result.get(
                "baseline_deviation"
            ),

        "Z-Score":
            result.get(
                "z_score"
            ),

        "Anomaly Score":
            result.get(
                "score"
            ),

        "Severity":
            result.get(
                "severity"
            ),

        "Business Impact":
            result.get(
                "business_impact"
            ),

        "Priority":
            result.get(
                "priority"
            ),
    })


st.dataframe(
    table_data,
    use_container_width=True,
    hide_index=True
)


# ======================================================
# HISTORICAL TRENDS
# ======================================================

st.markdown(
    '<div class="section-title">'
    'Historical Trends'
    '</div>',
    unsafe_allow_html=True
)


try:

    history_df = get_metric_history()

except Exception as error:

    history_df = pd.DataFrame()

    st.warning(
        f"Could not load historical data: {error}"
    )


if history_df.empty:

    st.info(
        "Historical data will appear after "
        "analysis runs have been saved."
    )

else:

    # --------------------------------------------------
    # Make a copy so we never modify the DB dataframe
    # --------------------------------------------------

    history_df = history_df.copy()

    # --------------------------------------------------
    # Clean metric names
    # --------------------------------------------------

    history_df["metric"] = (
        history_df["metric"]
        .astype(str)
        .str.strip()
    )

    available_metrics = (
        history_df["metric"]
        .dropna()
        .unique()
        .tolist()
    )

    if available_metrics:

        selected_metric = st.selectbox(
            "Select metric",
            available_metrics
        )

        metric_history = (
            history_df[
                history_df["metric"]
                == selected_metric
            ]
            .copy()
        )

        # ==============================================
        # CRITICAL FIX
        #
        # Convert database values into JSON-safe types
        # before giving them to Plotly.
        # ==============================================

        metric_history[
            "analysis_date"
        ] = pd.to_datetime(
            metric_history[
                "analysis_date"
            ],
            errors="coerce"
        )

        metric_history[
            "current_value"
        ] = pd.to_numeric(
            metric_history[
                "current_value"
            ],
            errors="coerce"
        )

        metric_history[
            "anomaly_score"
        ] = pd.to_numeric(
            metric_history[
                "anomaly_score"
            ],
            errors="coerce"
        )

        metric_history[
            "percentage_change"
        ] = pd.to_numeric(
            metric_history[
                "percentage_change"
            ],
            errors="coerce"
        )

        metric_history[
            "baseline_deviation"
        ] = pd.to_numeric(
            metric_history[
                "baseline_deviation"
            ],
            errors="coerce"
        )

        metric_history[
            "z_score"
        ] = pd.to_numeric(
            metric_history[
                "z_score"
            ],
            errors="coerce"
        )

        # --------------------------------------------------
        # Remove invalid rows
        # --------------------------------------------------

        metric_history = (
            metric_history.dropna(
                subset=[
                    "analysis_date"
                ]
            )
        )

        # --------------------------------------------------
        # Sort chronologically
        # --------------------------------------------------

        metric_history = (
            metric_history.sort_values(
                "analysis_date"
            )
        )

        # ==============================================
        # CURRENT VALUE TREND
        # ==============================================

        if not metric_history.empty:

            fig = px.line(
                metric_history,
                x="analysis_date",
                y="current_value",
                markers=True,
                title=(
                    f"{selected_metric} Trend"
                )
            )

            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Current Value",
                hovermode="x unified"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Not enough valid historical "
                "data to display the trend."
            )

        # ==============================================
        # ANOMALY SCORE TREND
        # ==============================================

        anomaly_history = (
            metric_history.dropna(
                subset=[
                    "anomaly_score"
                ]
            )
        )

        if not anomaly_history.empty:

            anomaly_fig = px.line(
                anomaly_history,
                x="analysis_date",
                y="anomaly_score",
                markers=True,
                title=(
                    f"{selected_metric} "
                    "Anomaly Score"
                )
            )

            anomaly_fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Anomaly Score",
                hovermode="x unified"
            )

            st.plotly_chart(
                anomaly_fig,
                use_container_width=True
            )

        else:

            st.info(
                "No valid anomaly-score history "
                "is available for this metric."
            )

    else:

        st.info(
            "No metrics are available in "
            "historical data."
        )


# ======================================================
# CRITICAL ANOMALIES
# ======================================================

st.markdown(
    '<div class="section-title">'
    'Critical Anomalies'
    '</div>',
    unsafe_allow_html=True
)


critical_results = [
    result
    for result in results
    if result.get("severity")
    == "CRITICAL"
]


if not critical_results:

    st.success(
        "No critical anomalies detected."
    )

else:

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

        if change is not None:

            change_text = (
                f"{change:+.2f}%"
            )

        else:

            change_text = "N/A"

        st.error(
            f"🔴 **{metric}** | "
            f"Change: {change_text} | "
            f"Impact: {impact} | "
            f"Priority: {priority}"
        )


# ======================================================
# BUSINESS FINDINGS
# ======================================================

st.markdown(
    '<div class="section-title">'
    'Business Findings'
    '</div>',
    unsafe_allow_html=True
)


if not business_findings:

    st.info(
        "No significant business relationships "
        "were detected."
    )

else:

    for finding in business_findings:

        severity = finding.get(
            "severity",
            "WARNING"
        )

        finding_type = finding.get(
            "type",
            "Business Finding"
        )

        observation = finding.get(
            "observation",
            ""
        )

        implication = finding.get(
            "possible_implication",
            ""
        )

        if severity == "CRITICAL":

            st.error(
                f"**{finding_type}**\n\n"
                f"{observation}\n\n"
                f"**Possible implication:** "
                f"{implication}"
            )

        else:

            st.warning(
                f"**{finding_type}**\n\n"
                f"{observation}\n\n"
                f"**Possible implication:** "
                f"{implication}"
            )

        checks = finding.get(
            "recommended_checks",
            []
        )

        if checks:

            with st.expander(
                "Recommended checks"
            ):

                for check in checks:

                    st.write(
                        f"• {check}"
                    )


# ======================================================
# AI EXECUTIVE SUMMARY
# ======================================================

st.markdown(
    '<div class="section-title">'
    'AI Executive Summary'
    '</div>',
    unsafe_allow_html=True
)


executive_summary = ai_summary.get(
    "executive_summary",
    "No AI summary available."
)


st.info(
    executive_summary
)


# ======================================================
# AI KEY FINDINGS + POSSIBLE CAUSES
# ======================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader(
        "Key Findings"
    )

    key_findings = ai_summary.get(
        "key_findings",
        []
    )

    if key_findings:

        for finding in key_findings:

            st.write(
                f"• {finding}"
            )

    else:

        st.write(
            "No key findings available."
        )


with col2:

    st.subheader(
        "Possible Causes"
    )

    possible_causes = ai_summary.get(
        "possible_causes",
        []
    )

    if possible_causes:

        for cause in possible_causes:

            st.write(
                f"• {cause}"
            )

    else:

        st.write(
            "No possible causes available."
        )


# ======================================================
# RECOMMENDED ACTIONS
# ======================================================

st.markdown(
    '<div class="section-title">'
    'Recommended Actions'
    '</div>',
    unsafe_allow_html=True
)


recommended_actions = ai_summary.get(
    "recommended_actions",
    []
)


if recommended_actions:

    for index, action in enumerate(
        recommended_actions
    ):

        st.checkbox(
            action,
            value=False,
            key=f"action_{index}"
        )

else:

    st.success(
        "No immediate actions recommended."
    )


# ======================================================
# PRIORITY MESSAGE
# ======================================================

st.markdown(
    '<div class="section-title">'
    'Priority'
    '</div>',
    unsafe_allow_html=True
)


priority_message = ai_summary.get(
    "priority_message",
    "No priority message available."
)


st.warning(
    priority_message
)

# ======================================================
# EMAIL ALERT STATUS
# ======================================================

st.markdown(
    '<div class="section-title">'
    'Alert Status'
    '</div>',
    unsafe_allow_html=True
)

if email_sent:

    st.success(
        "📧 Email alert sent successfully."
    )

elif critical_count > 0:

    st.warning(
        "Critical anomalies were detected, "
        "but no email alert was sent."
    )

else:

    st.info(
        "No P0/P1 anomaly required an email alert."
    )

# ======================================================
# ALERT HISTORY
# ======================================================

st.markdown(
    '<div class="section-title">'
    'Alert History'
    '</div>',
    unsafe_allow_html=True
)


try:

    run_history = get_run_history()

except Exception as error:

    run_history = pd.DataFrame()

    st.warning(
        f"Could not load alert history: {error}"
    )


if run_history.empty:

    st.info(
        "No historical analysis runs yet."
    )

else:

    # Make database values display-safe
    run_history = run_history.copy()

    if "analysis_time" in run_history.columns:

        run_history[
            "analysis_time"
        ] = run_history[
            "analysis_time"
        ].astype(str)

    if "analysis_date" in run_history.columns:

        run_history[
            "analysis_date"
        ] = run_history[
            "analysis_date"
        ].astype(str)

    st.dataframe(
        run_history,
        use_container_width=True,
        hide_index=True
    )

# ======================================================
# EMAIL ALERT HISTORY
# ======================================================

st.markdown(
    '<div class="section-title">'
    'Email Alert History'
    '</div>',
    unsafe_allow_html=True
)

try:

    alert_history = (
        get_alert_history()
    )

except Exception as error:

    alert_history = pd.DataFrame()

    st.warning(
        f"Could not load email alert history: {error}"
    )


if alert_history.empty:

    st.info(
        "No email alerts have been sent yet."
    )

else:

    st.dataframe(
        alert_history,
        use_container_width=True,
        hide_index=True
    )

# ======================================================
# REPORT DOWNLOAD
# ======================================================

st.markdown(
    '<div class="section-title">'
    'Report'
    '</div>',
    unsafe_allow_html=True
)


st.download_button(
    label="Download Anomaly Report",
    data=report,
    file_name="business_anomaly_report.txt",
    mime="text/plain",
    use_container_width=True
)


# ======================================================
# FOOTER
# ======================================================

st.caption(
    f"Analysis Run ID: {run_id}"
)

