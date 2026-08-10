import pandas as pd


def calculate_percentage_change(current, previous):
    """
    Calculate percentage change between two values.
    """

    if previous == 0:
        return None

    return ((current - previous) / previous) * 100


def add_percentage_changes(df, columns):
    """
    Add day-over-day percentage change columns.
    """

    df = df.copy()

    for column in columns:

        change_column = f"{column}_Change"

        df[change_column] = (
            df[column].pct_change() * 100
        )

    return df


def add_moving_average(df, columns, window=7):
    """
    Calculate rolling average for each metric.
    """

    df = df.copy()

    for column in columns:

        average_column = f"{column}_MA"

        df[average_column] = (
            df[column]
            .rolling(window=window)
            .mean()
            .shift(1)  
        )

    return df


def add_baseline_deviation(df, columns):
    """
    Calculate percentage difference between
    current value and moving-average baseline.
    """

    df = df.copy()

    for column in columns:

        baseline_column = f"{column}_MA"
        deviation_column = f"{column}_Baseline_Deviation"

        df[deviation_column] = (
            (
                df[column] - df[baseline_column]
            )
            / df[baseline_column]
        ) * 100

    return df

def add_z_scores(df, columns, window=7):
    """
    Calculate rolling Z-score for each metric.
    """

    df = df.copy()

    for column in columns:

        rolling_mean = (
            df[column]
            .rolling(window=window)
            .mean()
            .shift(1)
        )

        rolling_std = (
            df[column]
            .rolling(window=window)
            .std()
            .shift(1)
        )

        z_column = f"{column}_ZScore"

        df[z_column] = (
            (df[column] - rolling_mean)
            / rolling_std
        )

    return df