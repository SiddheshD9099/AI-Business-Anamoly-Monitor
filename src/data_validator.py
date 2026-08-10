REQUIRED_COLUMNS = [
    "Date",
    "Revenue",
    "Orders",
    "Conversion_Rate",
    "Traffic",
    "Cost",
    "Refunds",
]


def validate_columns(df):
    """
    Check whether all required columns exist.
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