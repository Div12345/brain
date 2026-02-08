import pandas as pd
import os

DATA_PATH = "/home/div/AAA_detection_personal/data/Con Data.xlsx"


def check_sheets():
    if not os.path.exists(DATA_PATH):
        return

    try:
        xl = pd.ExcelFile(DATA_PATH)
        print(f"Sheet names: {xl.sheet_names}")

        for sheet in xl.sheet_names:
            print(f"\nSheet: {sheet}")
            df = xl.parse(sheet)
            print(f"Columns: {list(df.columns)}")

            # Check for death keywords in THIS sheet
            matches = [
                c for c in df.columns if "death" in c.lower() or "outcome" in c.lower()
            ]
            if matches:
                print(f"  FOUND KEYWORDS: {matches}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    check_sheets()
