import pandas as pd
import numpy as np
import os

DATA_PATH = "/home/div/AAA_detection_personal/data/Con Data.xlsx"


def analyze_columns():
    if not os.path.exists(DATA_PATH):
        return

    try:
        df = pd.read_excel(DATA_PATH)
    except:
        return

    print(f"File: {DATA_PATH}")
    print(f"Columns: {list(df.columns)}")

    cols_to_check = [
        "NameOfCardiacDisease",
        "CVrr",
        "heartDisease",
        "HeartFailure",
        "stroke",
    ]

    for col in cols_to_check:
        if col in df.columns:
            print(f"\nValue Counts for '{col}':")
            print(df[col].value_counts(dropna=False))

            # Print entries where NameOfCardiacDisease is not NaN
            if col == "NameOfCardiacDisease":
                print(f"\nEntries for {col}:")
                print(df[df[col].notna()][col].tolist())


if __name__ == "__main__":
    analyze_columns()
