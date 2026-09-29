import sys
from pathlib import Path

import pandas as pd
import pytest


BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from data_validator import REQUIRED_COLUMNS, validate_columns


def test_validate_bfsi_metric_schema():
    dataframe = pd.DataFrame(
        columns=REQUIRED_COLUMNS
    )

    assert validate_columns(dataframe)


def test_validate_columns_reports_missing_bfsi_metric():
    dataframe = pd.DataFrame(
        columns=[
            column
            for column in REQUIRED_COLUMNS
            if column != "npa_ratio"
        ]
    )

    with pytest.raises(ValueError, match="npa_ratio"):
        validate_columns(dataframe)
