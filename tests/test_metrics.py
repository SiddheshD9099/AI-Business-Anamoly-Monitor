import sys
from pathlib import Path

import pandas as pd


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

        "Revenue": [
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

        "Orders": [
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


# ======================================================
# TEST PERCENTAGE CHANGE
# ======================================================

def test_percentage_change():

    df = create_test_dataframe()

    result = add_percentage_changes(
        df,
        ["Revenue"]
    )

    assert (
        "Revenue_Change"
        in result.columns
    )

    # 110 compared with 100 = +10%
    assert round(
        result.iloc[1][
            "Revenue_Change"
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
        ["Revenue"],
        window=7
    )

    assert (
        "Revenue_MA"
        in result.columns
    )


# ======================================================
# TEST BASELINE DEVIATION
# ======================================================

def test_baseline_deviation():

    df = create_test_dataframe()

    df = add_moving_average(
        df,
        ["Revenue"],
        window=7
    )

    result = add_baseline_deviation(
        df,
        ["Revenue"]
    )

    assert (
        "Revenue_Baseline_Deviation"
        in result.columns
    )


# ======================================================
# TEST Z-SCORE
# ======================================================

def test_z_score():

    df = create_test_dataframe()

    result = add_z_scores(
        df,
        ["Revenue"],
        window=7
    )

    assert (
        "Revenue_ZScore"
        in result.columns
    )

