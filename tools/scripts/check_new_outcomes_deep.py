import pandas as pd
import os

FILE_PATH = "/home/div/AAA_detection_personal/data/raw/new_outcomes.xlsx"


def check_deep():
    if not os.path.exists(FILE_PATH):
        return

    try:
        xl = pd.ExcelFile(FILE_PATH)
        print(f"Sheets: {xl.sheet_names}")

        for sheet in xl.sheet_names:
            print(f"\n--- Sheet: {sheet} ---")
            df = xl.parse(sheet)
            print(f"Columns: {list(df.columns)}")
            if "MBSI Results" in df.columns:
                print("MBSI Results Sample:")
                print(df["MBSI Results"].head(10))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    check_deep()
