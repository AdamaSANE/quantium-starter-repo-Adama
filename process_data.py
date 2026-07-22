from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = DATA_DIR / "pink_morsel_sales.csv"


def load_and_format_sales() -> pd.DataFrame:
    # Read every daily sales file and combine them into one table.
    frames = []
    for csv_file in sorted(DATA_DIR.glob("daily_sales_data_*.csv")):
        frame = pd.read_csv(csv_file)

        # Keep only Pink Morsel rows, then calculate sales from quantity and price.
        frame = frame[frame["product"] == "pink morsel"].copy()
        frame["sales"] = frame["quantity"] * frame["price"].str.replace("$", "", regex=False).astype(float)

        # Keep the three requested output fields with the required names.
        frame = frame[["sales", "date", "region"]].rename(
            columns={"date": "Date", "region": "Region", "sales": "Sales"}
        )
        frames.append(frame)

    return pd.concat(frames, ignore_index=True)


def main() -> None:
    formatted_sales = load_and_format_sales()
    formatted_sales.to_csv(OUTPUT_FILE, index=False)
    print(f"Wrote {len(formatted_sales)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()