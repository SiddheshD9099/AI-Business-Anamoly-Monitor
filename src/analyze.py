import pandas as pd

from data_reader import read_business_data
from data_validator import validate_columns
from data_cleaner import clean_data
from metrics import (
    add_percentage_changes,
    add_moving_average,
    add_baseline_deviation,
    add_z_scores,
    validate_metric_schema,
)


METRICS = [
    "daily_transaction_volume",
    "avg_transaction_value",
    "failed_transaction_rate",
    "chargeback_count",
    "loan_disbursal_amount",
    "npa_ratio",
]


def analyze_business_data(file_path):

    # 1. Read
    df = read_business_data(file_path)

    # 2. Validate
    validate_columns(df)

    # 3. Clean
    df = clean_data(df)

    validate_metric_schema(df)

    # 4. Percentage changes
    df = add_percentage_changes(
        df,
        METRICS
    )

    # 5. Moving averages
    df = add_moving_average(
        df,
        METRICS,
        window=7
    )

    df = add_baseline_deviation(
        df,
        METRICS
    )

    df = add_z_scores(
        df,
        METRICS,
        window=7
    )

    return df


if __name__ == "__main__":

    file_path = "../data/business_metrics.xlsx"

    df = analyze_business_data(file_path)

    print(df.tail())