# BFSI-transaction-AI-anomaly-monitor

An automated business intelligence monitoring system that analyzes operational metrics, detects unusual changes, identifies potential business-impact relationships, generates AI-assisted explanations, stores historical analysis, and sends deduplicated email alerts.

The system is designed to turn routine business metric monitoring into an automated process rather than requiring manual inspection of spreadsheets.

---

## Overview

Business teams often monitor metrics such as revenue, orders, conversion rate, traffic, cost, and refunds. The challenge is not simply calculating these metrics, but identifying when a change is unusual, understanding how multiple metrics relate to each other, and communicating the issue quickly.

The AI Business Anomaly Monitor addresses this workflow by combining statistical anomaly detection, business rules, generative AI, persistent history, and automated email notifications.

### Core workflow

```text
Excel Business Data
        ↓
Data Validation & Cleaning
        ↓
Metric Calculations
        ↓
Anomaly Detection
        ↓
Business Relationship Analysis
        ↓
Gemini AI Summary
        ↓
SQLite History
        ↓
 ┌───────────────┬────────────────┐
 │               │                │
 ▼               ▼                ▼
Dashboard      Email Alert      Report
```

The complete workflow can also be executed automatically through Windows Task Scheduler.

---

# Features

## 1. Business Data Ingestion

The system reads business metrics from an Excel workbook.

Example metrics:

- Date
- Revenue
- Orders
- Conversion Rate
- Traffic
- Cost
- Refunds

The data is validated and cleaned before analysis.

---

## 2. Statistical Anomaly Detection

The system evaluates business metrics using multiple statistical signals.

### Percentage Change

Measures how significantly the current value has changed relative to the previous period.

```text
Percentage Change =
(Current Value - Previous Value)
/
Previous Value × 100
```

### Moving Average

A rolling historical average is used as a baseline for recent business behavior.

The current implementation uses a 7-period window.

### Baseline Deviation

Measures how far the current metric is from its recent baseline.

### Z-Score

Measures how unusual the current value is relative to historical observations.

```text
Z = (Current Value - Mean) / Standard Deviation
```

These signals are combined by the anomaly engine to determine anomaly severity, business impact, and priority.

---

# 3. Priority-Based Alerting

Detected anomalies are classified by priority.

The email alert system focuses on high-priority anomalies:

```text
P0
P1
```

Lower-priority observations can still appear in the dashboard and analysis reports without triggering an email.

This prevents normal fluctuations from generating unnecessary alerts.

---

# 4. Business Relationship Detection

Individual metrics do not always tell the complete story.

The system also evaluates relationships between metrics.

For example:

```text
Traffic ↑
Conversion Rate ↓
```

may indicate that traffic volume increased while traffic quality or conversion performance deteriorated.

Another example:

```text
Revenue ↓
Refunds ↑
```

may indicate a potential deterioration in sales quality or an increase in post-purchase issues.

The business rules layer converts these relationships into:

- Observation
- Severity
- Possible implication
- Recommended checks

---

# 5. Gemini AI Business Summary

The system uses Gemini to convert analytical results into business-oriented explanations.

Instead of presenting only statistical output such as:

```text
Metric exceeded threshold by X%.
```

the AI layer generates information such as:

- Executive summary
- Key findings
- Possible causes
- Recommended actions
- Priority message

This makes the output more useful for a business stakeholder.

The AI layer does not replace the statistical anomaly detector. Statistical analysis determines what changed; Gemini helps explain what the change could mean.

---

# 6. SQLite Historical Storage

Analysis results are persisted in SQLite.

The database stores:

### Analysis runs

Records when an analysis was performed.

### Metric results

Stores metric-level analytical results including:

- Current value
- Percentage change
- Baseline deviation
- Z-score
- Anomaly score
- Severity
- Business impact
- Priority

### Business findings

Stores relationships detected by the business rules layer.

### Alerts

Stores successfully sent alerts.

This allows historical analysis and alert tracking without requiring an external database server.

---

# 7. Duplicate Email Protection

A major part of the alerting system is preventing repeated emails for the same anomaly.

Each alert is identified using:

```text
Metric
+
Priority
+
Analysis Date
```

For example:

```text
Revenue + P0 + 2026-08-10
```

can only generate one alert.

The system uses both application-level checking and a database-level unique constraint.

The resulting workflow is:

```text
P0/P1 anomaly detected
        ↓
Check alert history
        ↓
Already alerted?
     /        \
   Yes         No
    ↓           ↓
Skip email   Send email
                ↓
          Save alert record
```

This prevents the scheduler from repeatedly sending the same notification every time it executes.

---

# 8. Email Notifications

High-priority anomalies can trigger email notifications through SMTP.

The email contains:

- Alert summary
- Critical anomalies
- Business findings
- AI executive summary
- Recommended actions
- Priority information

SMTP credentials are loaded through environment variables and are not stored in source code.

---

# 9. Streamlit Dashboard

The project includes a Streamlit dashboard for interactive analysis.

The dashboard provides access to:

- Current analysis
- Metric-level anomaly results
- Charts
- Severity and priority information
- Business findings
- AI-generated analysis
- Historical analysis
- Alert information

The dashboard is intended for interactive investigation, while the scheduled pipeline provides automated monitoring.

---

# 10. Automated Monitoring

The project can be executed automatically using Windows Task Scheduler.

The automation flow is:

```text
Windows Task Scheduler
        ↓
run_monitor.bat
        ↓
scheduled_analysis.py
        ↓
daily_analysis.py
        ↓
Business Analysis Pipeline
        ↓
Database + Email + Report
```

This allows the system to operate as a scheduled monitoring service rather than requiring manual execution.

---

# Technology Stack

| Category             | Technology                                  |
| -------------------- | ------------------------------------------- |
| Programming Language | Python                                      |
| Data Processing      | Pandas, NumPy                               |
| Input                | Microsoft Excel / XLSX                      |
| Visualization        | Plotly                                      |
| Dashboard            | Streamlit                                   |
| Statistical Analysis | Moving Average, Baseline Deviation, Z-Score |
| AI                   | Google Gemini API                           |
| Database             | SQLite                                      |
| Email                | SMTP                                        |
| Configuration        | Python dotenv                               |
| Testing              | Pytest                                      |
| Automation           | Windows Task Scheduler                      |
| Version Control      | Git / GitHub                                |

---

# Project Structure

```text
AI Business Anomaly Monitor/
│
├── app.py
├── scheduled_analysis.py
├── run_monitor.bat
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── data/
│   └── business_metrics.xlsx
│
├── database/
│   └── anomaly_monitor.db
│
├── logs/
│
├── reports/
│
├── src/
│   ├── ai_analyzer.py
│   ├── anomaly_engine.py
│   ├── business_rules.py
│   ├── config.py
│   ├── daily_analysis.py
│   ├── data_cleaner.py
│   ├── data_reader.py
│   ├── data_validator.py
│   ├── email_alert.py
│   ├── gemini_api_check.py
│   ├── history_db.py
│   ├── logger.py
│   ├── metrics.py
│   └── report_generator.py
│
└── tests/
    ├── test_anomaly_engine.py
    ├── test_business_rules.py
    ├── test_history_db.py
    ├── test_metrics.py
    └── test_scheduler.py
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/SiddheshD9099/AI-Business-Anamoly-Monitor.git
cd "AI Bussiness Anamoly Monitor"
```

---

## 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

### Git Bash

```bash
source venv/Scripts/activate
```

### PowerShell

```powershell
venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file in the project root.

Do not commit this file to GitHub.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_RECIPIENT=recipient@example.com
```

Use an SMTP app password where required by your email provider.

The repository contains `.env.example` as a configuration template.

---

# Input Data

Place the business data file at:

```text
data/business_metrics.xlsx
```

The workbook should contain the business metrics expected by the configured analysis pipeline.

Example:

| Date       | Revenue | Orders | Conversion Rate | Traffic |  Cost | Refunds |
| ---------- | ------: | -----: | --------------: | ------: | ----: | ------: |
| 2026-08-05 |  145000 |   1580 |             3.1 |   61000 | 30000 |    1800 |
| 2026-08-06 |  148000 |   1605 |             3.0 |   62500 | 30500 |    1900 |
| 2026-08-07 |  152000 |   1640 |             2.9 |   64000 | 31000 |    2100 |

The system determines the latest valid business date after sorting the input data.

---

# Running the Dashboard

Start Streamlit with:

```bash
streamlit run app.py
```

The dashboard can then be used to inspect the current analysis and historical results.

---

# Running the Analysis Manually

Run:

```bash
python src/daily_analysis.py
```

The analysis pipeline performs:

```text
Read Excel
    ↓
Validate
    ↓
Clean
    ↓
Calculate metrics
    ↓
Detect anomalies
    ↓
Evaluate business relationships
    ↓
Generate Gemini summary
    ↓
Save to SQLite
    ↓
Send required alerts
    ↓
Generate report
```

---

# Running the Automated Monitor

The scheduled pipeline can be executed through:

```bash
python scheduled_analysis.py
```

The Windows automation uses:

```text
run_monitor.bat
```

which can be configured as the action executed by Windows Task Scheduler.

---

# Testing

The project uses Pytest.

Run:

```bash
pytest -v
```

The automated test suite covers core functionality such as:

- Anomaly detection
- Metric calculations
- Business rules
- Database persistence
- Scheduler behavior

External Gemini API experiments are kept separate from the normal automated test suite so that running Pytest does not consume API quota.

---

# Reports

Generated reports are stored in:

```text
reports/
```

Reports contain the analytical findings and business interpretation produced during an analysis run.

---

# Alert History

Alert records are stored in SQLite.

The system tracks:

```text
Run ID
Metric
Priority
Severity
Percentage Change
Analysis Date
Sent Time
```

This history is used to prevent duplicate notifications.

---

# Design Decisions

## Why statistical anomaly detection?

The project uses interpretable statistical methods instead of immediately applying a machine learning model.

For a relatively small business dataset, techniques such as:

- Moving averages
- Baseline deviation
- Z-scores
- Percentage changes

provide transparent and explainable anomaly signals.

This also makes the system easier for business users to understand.

---

## Why Gemini?

Statistical methods are useful for detecting unusual behavior, but they do not inherently provide a business explanation.

Gemini is used as an interpretation layer.

The system first determines:

```text
What changed?
```

and then asks the AI layer to help answer:

```text
What could this mean?
What could cause it?
What should the business investigate?
```

This separates deterministic analysis from generative interpretation.

---

## Why SQLite?

SQLite was selected because the project is designed as a lightweight monitoring application.

It provides:

- Persistent history
- Zero database-server setup
- SQL querying
- Reliable local storage
- Easy deployment for a single-machine monitoring workflow

A production multi-user deployment could migrate the persistence layer to PostgreSQL.

---

## Why separate business rules from AI?

Business relationships that are deterministic should not depend entirely on an LLM.

For example:

```text
Traffic increases
+
Conversion rate decreases
```

can be evaluated using explicit business rules.

The AI layer then adds natural-language interpretation.

This produces a more predictable architecture:

```text
Deterministic Detection
        +
Deterministic Business Rules
        +
Generative AI Explanation
```

---

# Limitations

The current version is designed as a focused MVP.

Current limitations include:

- Excel is the primary data source.
- SQLite is intended for lightweight local persistence.
- Statistical thresholds depend on available historical data.
- Gemini output depends on API availability and quota.
- Business rules are currently explicitly defined rather than learned automatically.
- Windows Task Scheduler is used for local automation.
- The system does not yet provide multi-user cloud deployment.

---

# Future Improvements

Potential future versions could include:

### Data Sources

- PostgreSQL
- MySQL
- REST APIs
- Cloud warehouses
- Direct database connectors

### Anomaly Detection

- Isolation Forest
- One-Class SVM
- Seasonal decomposition
- Prophet
- Robust statistical methods
- Multivariate anomaly detection

### Monitoring

- Cloud deployment
- Docker
- Scheduled cloud jobs
- Webhook notifications
- Slack / Teams alerts

### Intelligence

- Historical root-cause analysis
- Anomaly trend tracking
- Adaptive thresholds
- Metric correlation analysis
- Feedback-based alert tuning

### Scalability

```text
Excel
  ↓
Cloud Data Warehouse
  ↓
Scheduled Processing
  ↓
Anomaly Detection Service
  ↓
AI Explanation Layer
  ↓
PostgreSQL
  ↓
Dashboard + Notification Services
```

---

# Example Business Scenario

Suppose the system observes:

```text
Traffic       ↑ 25%
Conversion    ↓ 32%
Revenue       ↓ 10%
```

A basic monitoring script might report:

```text
Conversion Rate changed by -32%.
```

This project goes further.

The anomaly engine identifies the unusual metric movement, the business rules layer recognizes the relationship between traffic and conversion, and Gemini generates a business-oriented explanation and recommended investigation areas.

The resulting alert can communicate the issue as:

```text
Traffic increased significantly while conversion rate
declined. Revenue also deteriorated, suggesting that
the additional traffic may not be converting effectively.
Investigate traffic source quality, campaign targeting,
landing-page performance, and conversion funnel changes.
```

The exact AI output depends on the analyzed data.

---

# Engineering Highlights

This project demonstrates practical experience with:

- Python application development
- Data cleaning and validation
- Statistical analysis
- Anomaly detection
- Business rule engines
- Generative AI integration
- SQLite database design
- Database constraints
- Email automation
- Streamlit dashboards
- Automated testing
- Environment-based configuration
- Windows task scheduling
- Logging and reporting
- Git/GitHub workflow

---

# Project Goal

The goal of the project is not simply to detect statistical outliers.

The goal is to build a complete monitoring workflow:

```text
Detect
  ↓
Prioritize
  ↓
Understand
  ↓
Explain
  ↓
Alert
  ↓
Persist
  ↓
Monitor Again
```

This turns raw business metrics into an automated decision-support workflow.

---
