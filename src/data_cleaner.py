import pandas as pd


NUMERIC_COLUMNS = [
    "daily_transaction_volume",
    "avg_transaction_value",
    "failed_transaction_rate",
    "chargeback_count",
    "loan_disbursal_amount",
    "npa_ratio",
]


def clean_data(df):
    """
    Clean and standardize BFSI transaction data.
    """

    df = df.copy()

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    # Convert numeric columns to numbers
    for column in NUMERIC_COLUMNS:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove rows where Date is invalid
    df = df.dropna(subset=["Date"])

    # Sort by date
    df = df.sort_values("Date")

    # Reset row numbers
    df = df.reset_index(drop=True)

    return df