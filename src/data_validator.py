REQUIRED_COLUMNS = [
    "Date",
    "daily_transaction_volume",
    "avg_transaction_value",
    "failed_transaction_rate",
    "chargeback_count",
    "loan_disbursal_amount",
    "npa_ratio",
]


def validate_columns(df):
    """
    Check whether the date and BFSI metric columns exist.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return True