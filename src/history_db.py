import sqlite3

from datetime import datetime

from pathlib import Path

import pandas as pd


# ======================================================
# DATABASE LOCATION
# ======================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

DATABASE_DIR = (
    BASE_DIR / "database"
)

DATABASE_DIR.mkdir(
    exist_ok=True
)

DATABASE_PATH = (
    DATABASE_DIR
    / "anomaly_monitor.db"
)


# ======================================================
# DATABASE CONNECTION
# ======================================================

def get_connection():
    """
    Create and return a new SQLite connection.

    Every function gets its own connection.
    Connections are closed only after that function
    has finished using them.
    """

    return sqlite3.connect(
        str(DATABASE_PATH)
    )


# ======================================================
# DATE NORMALIZATION
# ======================================================

def normalize_analysis_date(
    analysis_date
):
    """
    Convert any valid date-like value into:

        YYYY-MM-DD

    Returns None when the input is None.
    """

    if analysis_date is None:

        return None

    try:

        return (
            pd.to_datetime(
                analysis_date
            ).strftime(
                "%Y-%m-%d"
            )
        )

    except Exception:

        return str(
            analysis_date
        )


# ======================================================
# INITIALIZE DATABASE
# ======================================================

def initialize_database():
    """
    Create all required database tables and indexes.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ==================================================
        # ANALYSIS RUNS
        # ==================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_runs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                analysis_time TEXT NOT NULL,

                analysis_date TEXT

            )
            """
        )

        # ==================================================
        # METRIC RESULTS
        # ==================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS metric_results (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                run_id INTEGER NOT NULL,

                metric TEXT NOT NULL,

                current_value REAL,

                percentage_change REAL,

                baseline_deviation REAL,

                z_score REAL,

                anomaly_score REAL,

                severity TEXT,

                business_impact TEXT,

                priority TEXT,

                FOREIGN KEY (run_id)
                    REFERENCES analysis_runs(id)

            )
            """
        )

        # ==================================================
        # BUSINESS FINDINGS
        # ==================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS business_findings (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                run_id INTEGER NOT NULL,

                finding_type TEXT,

                severity TEXT,

                observation TEXT,

                possible_implication TEXT,

                FOREIGN KEY (run_id)
                    REFERENCES analysis_runs(id)

            )
            """
        )

        # ==================================================
        # ALERTS
        # ==================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                run_id INTEGER NOT NULL,

                metric TEXT NOT NULL,

                priority TEXT,

                severity TEXT,

                percentage_change REAL,

                analysis_date TEXT,

                sent_at TEXT NOT NULL,

                FOREIGN KEY (run_id)
                    REFERENCES analysis_runs(id)

            )
            """
        )

        # ==================================================
        # CHECK ALERT TABLE SCHEMA
        # ==================================================

        cursor.execute(
            """
            PRAGMA table_info(alerts)
            """
        )

        alert_columns = [
            row[1]
            for row in cursor.fetchall()
        ]

        # --------------------------------------------------
        # Add analysis_date to old alerts table if missing
        # --------------------------------------------------

        if (
            "analysis_date"
            not in alert_columns
        ):

            cursor.execute(
                """
                ALTER TABLE alerts
                ADD COLUMN analysis_date TEXT
                """
            )

        # ==================================================
        # CREATE STANDARD INDEXES
        # ==================================================

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_metric_results_run_id

            ON metric_results(run_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_business_findings_run_id

            ON business_findings(run_id)
            """
        )

        # ==================================================
        # COMMIT TABLES / NORMAL INDEXES
        # ==================================================

        connection.commit()

    finally:

        connection.close()


# ======================================================
# REMOVE DUPLICATE ALERTS
# ======================================================

def remove_duplicate_alerts():
    """
    Remove duplicate alert records.

    For each combination of:

        metric
        + priority
        + analysis_date

    the oldest alert is kept.
    """

    initialize_database()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM alerts

            WHERE id NOT IN (

                SELECT MIN(id)

                FROM alerts

                WHERE analysis_date IS NOT NULL

                GROUP BY
                    metric,
                    priority,
                    analysis_date
            )

            AND analysis_date IS NOT NULL
            """
        )

        deleted_count = (
            cursor.rowcount
        )

        connection.commit()

        return deleted_count

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ======================================================
# CREATE UNIQUE ALERT INDEX
# ======================================================

def create_alert_unique_index():
    """
    Create a database-level unique index that prevents
    duplicate alerts for the same metric, priority,
    and analysis date.

    This function first removes old duplicates.
    """

    initialize_database()

    # --------------------------------------------------
    # Remove duplicates created before this protection
    # --------------------------------------------------

    remove_duplicate_alerts()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_alert_unique

            ON alerts (
                metric,
                priority,
                analysis_date
            )
            """
        )

        connection.commit()

    finally:

        connection.close()


# ======================================================
# SAVE ANALYSIS
# ======================================================

def save_analysis(
    results,
    business_findings,
    analysis_date=None
):
    """
    Save one complete analysis run.

    Returns:
        run_id
    """

    initialize_database()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ==================================================
        # CREATE ANALYSIS RUN
        # ==================================================

        analysis_time = (
            datetime.now().isoformat(
                timespec="seconds"
            )
        )

        analysis_date_value = (
            normalize_analysis_date(
                analysis_date
            )
        )

        cursor.execute(
            """
            INSERT INTO analysis_runs
            (
                analysis_time,
                analysis_date
            )

            VALUES (?, ?)
            """,
            (
                analysis_time,
                analysis_date_value
            )
        )

        run_id = cursor.lastrowid

        # ==================================================
        # SAVE METRIC RESULTS
        # ==================================================

        for result in results:

            cursor.execute(
                """
                INSERT INTO metric_results
                (
                    run_id,
                    metric,
                    current_value,
                    percentage_change,
                    baseline_deviation,
                    z_score,
                    anomaly_score,
                    severity,
                    business_impact,
                    priority
                )

                VALUES (
                    ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?
                )
                """,
                (

                    run_id,

                    result.get(
                        "metric"
                    ),

                    result.get(
                        "current_value"
                    ),

                    result.get(
                        "percentage_change"
                    ),

                    result.get(
                        "baseline_deviation"
                    ),

                    result.get(
                        "z_score"
                    ),

                    result.get(
                        "score"
                    ),

                    result.get(
                        "severity"
                    ),

                    result.get(
                        "business_impact"
                    ),

                    result.get(
                        "priority"
                    ),

                )
            )

        # ==================================================
        # SAVE BUSINESS FINDINGS
        # ==================================================

        for finding in business_findings:

            cursor.execute(
                """
                INSERT INTO business_findings
                (
                    run_id,
                    finding_type,
                    severity,
                    observation,
                    possible_implication
                )

                VALUES (?, ?, ?, ?, ?)
                """,
                (

                    run_id,

                    finding.get(
                        "type"
                    ),

                    finding.get(
                        "severity"
                    ),

                    finding.get(
                        "observation"
                    ),

                    finding.get(
                        "possible_implication"
                    ),

                )
            )

        # ==================================================
        # COMMIT
        # ==================================================

        connection.commit()

        return run_id

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ======================================================
# GET METRIC HISTORY
# ======================================================

def get_metric_history(
    metric=None
):
    """
    Return historical metric analysis.
    """

    initialize_database()

    connection = get_connection()

    try:

        query = """
            SELECT

                ar.analysis_date,

                ar.analysis_time,

                mr.metric,

                mr.current_value,

                mr.percentage_change,

                mr.baseline_deviation,

                mr.z_score,

                mr.anomaly_score,

                mr.severity,

                mr.business_impact,

                mr.priority

            FROM metric_results mr

            JOIN analysis_runs ar

                ON mr.run_id = ar.id
        """

        parameters = []

        if metric is not None:

            query += """
                WHERE mr.metric = ?
            """

            parameters.append(
                metric
            )

        query += """
            ORDER BY
                ar.analysis_time ASC
        """

        df = pd.read_sql_query(
            query,
            connection,
            params=parameters
        )

        return df

    finally:

        connection.close()


# ======================================================
# GET RUN HISTORY
# ======================================================

def get_run_history():
    """
    Return historical analysis runs.
    """

    initialize_database()

    connection = get_connection()

    try:

        query = """
            SELECT

                ar.id,

                ar.analysis_time,

                ar.analysis_date,

                COUNT(mr.id)
                    AS metrics_analyzed,

                SUM(
                    CASE

                        WHEN mr.severity = 'CRITICAL'

                        THEN 1

                        ELSE 0

                    END
                ) AS critical_count,

                SUM(
                    CASE

                        WHEN mr.severity = 'WARNING'

                        THEN 1

                        ELSE 0

                    END
                ) AS warning_count

            FROM analysis_runs ar

            LEFT JOIN metric_results mr

                ON ar.id = mr.run_id

            GROUP BY

                ar.id,

                ar.analysis_time,

                ar.analysis_date

            ORDER BY

                ar.analysis_time DESC
        """

        df = pd.read_sql_query(
            query,
            connection
        )

        return df

    finally:

        connection.close()


# ======================================================
# CHECK IF ALERT ALREADY EXISTS
# ======================================================

def alert_already_sent(
    metric,
    priority,
    analysis_date
):
    """
    Check whether an alert already exists for:

        metric
        + priority
        + analysis_date
    """

    if analysis_date is None:

        return False

    date_value = (
        normalize_analysis_date(
            analysis_date
        )
    )

    initialize_database()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1

            FROM alerts

            WHERE metric = ?

            AND priority = ?

            AND analysis_date = ?

            LIMIT 1
            """,
            (
                str(metric),
                str(priority),
                date_value,
            )
        )

        return (
            cursor.fetchone()
            is not None
        )

    finally:

        connection.close()


# ======================================================
# SAVE ALERT
# ======================================================

def save_alert(
    run_id,
    metric,
    priority,
    severity,
    percentage_change,
    analysis_date
):
    """
    Save an email alert.

    Database-level duplicate protection ensures that
    the same metric + priority + analysis_date cannot
    be stored twice.

    Returns:

        True  = new alert inserted
        False = alert already existed
    """

    if analysis_date is None:

        raise ValueError(
            "analysis_date cannot be None."
        )

    date_value = (
        normalize_analysis_date(
            analysis_date
        )
    )

    # --------------------------------------------------
    # Make sure unique index exists
    # --------------------------------------------------

    create_alert_unique_index()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        sent_at = (
            datetime.now().isoformat(
                timespec="seconds"
            )
        )

        cursor.execute(
            """
            INSERT OR IGNORE INTO alerts
            (
                run_id,
                metric,
                priority,
                severity,
                percentage_change,
                analysis_date,
                sent_at
            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (

                run_id,

                str(metric),

                str(priority),

                str(severity),

                percentage_change,

                date_value,

                sent_at,

            )
        )

        inserted = (
            cursor.rowcount == 1
        )

        connection.commit()

        return inserted

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ======================================================
# GET ALERT HISTORY
# ======================================================

def get_alert_history():
    """
    Return all previously sent email alerts.
    """

    initialize_database()

    connection = get_connection()

    try:

        query = """
            SELECT

                a.id,

                a.run_id,

                a.metric,

                a.priority,

                a.severity,

                a.percentage_change,

                a.analysis_date,

                a.sent_at

            FROM alerts a

            ORDER BY
                a.sent_at DESC
        """

        df = pd.read_sql_query(
            query,
            connection
        )

        return df

    finally:

        connection.close()


# ======================================================
# DATABASE HEALTH CHECK
# ======================================================

def database_health_check():
    """
    Verify that SQLite is accessible and operational.
    """

    try:

        initialize_database()

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                "SELECT 1"
            )

            result = cursor.fetchone()

            return (
                result is not None
                and result[0] == 1
            )

        finally:

            connection.close()

    except Exception:

        return False


# ======================================================
# MAIN DATABASE SETUP
# ======================================================

if __name__ == "__main__":

    print(
        "Initializing database..."
    )

    initialize_database()

    print(
        "Cleaning duplicate alerts..."
    )

    removed = (
        remove_duplicate_alerts()
    )

    print(
        f"Duplicate alerts removed: "
        f"{removed}"
    )

    print(
        "Creating unique alert index..."
    )

    create_alert_unique_index()

    print(
        "Database setup completed."
    )

    print(
        f"Database path: "
        f"{DATABASE_PATH}"
    )

