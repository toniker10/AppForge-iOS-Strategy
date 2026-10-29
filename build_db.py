"""Load the raw Kaggle CSVs into a local SQLite database (appforge.db).

Raw files are never modified; the database is a copy.
Usage:  python build_db.py
"""
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT  # the two CSV files sit in the same folder as the scripts
DB = ROOT / "appforge.db"


def main() -> None:
    apps = pd.read_csv(RAW / "AppleStore.csv")
    desc = pd.read_csv(RAW / "appleStore_description.csv")

    # The first column is an unnamed index column: ignore it.
    apps = apps.drop(columns=[apps.columns[0]])

    with sqlite3.connect(DB) as con:
        apps.to_sql("AppleStore", con, if_exists="replace", index=False)
        desc.to_sql("appleStore_description_combined", con, if_exists="replace", index=False)

    print(f"Built {DB.relative_to(ROOT)}: {len(apps)} apps, {len(desc)} descriptions")


if __name__ == "__main__":
    main()
