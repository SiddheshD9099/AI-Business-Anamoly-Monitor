import pandas as pd

from data_validator import validate_columns


def read_business_data(file_path):
    """Read and validate the required BFSI transaction workbook schema."""

    df = pd.read_excel(file_path)

    validate_columns(df)

    return df


if __name__ == "__main__":

    file_path = "data/business_metrics.xlsx"

    df = read_business_data(file_path)

    print("Data loaded and validated successfully.")
    print()
    print(df.head())