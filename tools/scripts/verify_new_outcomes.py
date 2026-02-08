import pandas as pd
import os

FILE_PATH = "/home/div/AAA_detection_personal/data/raw/new_outcomes.xlsx"


def check_outcomes():
    if not os.path.exists(FILE_PATH):
        print(f"Error: File not found at {FILE_PATH}")
        return

    try:
        df = pd.read_excel(FILE_PATH)
        print(f"Loaded {FILE_PATH}")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")

        # Look for death/outcome columns
        interesting = [
            c
            for c in df.columns
            if "death" in c.lower()
            or "outcome" in c.lower()
            or "cv" in c.lower()
            or "status" in c.lower()
            or "date" in c.lower()
        ]
        print(f"\nInteresting Columns: {interesting}")

        for col in interesting:
            print(f"\nValue Counts for '{col}':")
            print(df[col].value_counts(dropna=False).head(10))

    except Exception as e:
        print(f"Error reading Excel: {e}")


if __name__ == "__main__":
    check_outcomes()
