import sys
from pathlib import Path

import pandas as pd
import pytest


# ======================================================
# ADD SRC TO PYTHON PATH
# ======================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

SRC_DIR = BASE_DIR / "src"

sys.path.insert(
    0,
    str(SRC_DIR)
)


from metrics import (
    add_percentage_changes,
    add_moving_average,
    add_baseline_deviation,
    add_z_scores,
    METRIC_COLUMNS,
    validate_metric_schema,
)


# ======================================================
# TEST DATA
# ======================================================

def create_test_dataframe():

    return pd.DataFrame({

        "Date": pd.date_range(
            "2026-01-01",
            periods=10
        ),

        "daily_transaction_volume": [
            100,
            110,
            105,
            115,
            120,
            125,
            130,
            135,
            140,
            150,
        ],

        "avg_transaction_value": [
            10,
            11,
            10,
            12,
            12,
            13,
            13,
            14,
            14,
            15,
        ],

    })


def test_validate_bfsi_metric_schema():
    df = pd.DataFrame(
        {
            column: range(10)
            for column in METRIC_COLUMNS
        }
    )

    assert validate_metric_schema(df)


def test_metric_schema_reports_missing_column():
    df = pd.DataFrame(
        {
            column: range(10)
            for column in METRIC_COLUMNS
            if column != "npa_ratio"
        }
    )

    with pytest.raises(ValueError, match="npa_ratio"):
        validate_metric_schema(df)


# ======================================================
# TEST PERCENTAGE CHANGE
# ======================================================

def test_percentage_change():

    df = create_test_dataframe()

    result = add_percentage_changes(
        df,
        ["daily_transaction_volume"]
    )

    assert (
        "daily_transaction_volume_Change"
        in result.columns
    )

    # 110 compared with 100 = +10%
    assert round(
        result.iloc[1][
            "daily_transaction_volume_Change"
        ],
        2
    ) == 10.00


# ======================================================
# TEST MOVING AVERAGE
# ======================================================

def test_moving_average():

    df = create_test_dataframe()

    result = add_moving_average(
        df,
        ["daily_transaction_volume"],
        window=7
    )

    assert (
        "daily_transaction_volume_MA"
        in result.columns
    )


# ======================================================
# TEST BASELINE DEVIATION
# ======================================================

def test_baseline_deviation():

    df = create_test_dataframe()

    df = add_moving_average(
        df,
        ["daily_transaction_volume"],
        window=7
    )

    result = add_baseline_deviation(
        df,
        ["daily_transaction_volume"]
    )

    assert (
        "daily_transaction_volume_Baseline_Deviation"
        in result.columns
    )


# ======================================================
# TEST Z-SCORE
# ======================================================

def test_z_score():

    df = create_test_dataframe()

    result = add_z_scores(
        df,
        ["daily_transaction_volume"],
        window=7
    )

    assert (
        "daily_transaction_volume_ZScore"
        in result.columns
    )
