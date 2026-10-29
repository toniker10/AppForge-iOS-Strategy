"""Statistics that SQLite cannot compute (p-value, correlation), plus a
cross-check of the medians and shares used in the README.

Usage:  python analysis_stats.py
"""
from pathlib import Path

import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent
RAW = ROOT  # the two CSV files sit in the same folder as the scripts


def main() -> None:
    apps = pd.read_csv(RAW / "AppleStore.csv")
    desc = pd.read_csv(RAW / "appleStore_description.csv")

    print(f"Total apps: {len(apps)}, unique ids: {apps['id'].nunique()}")

    # Cleaning rule: user_rating = 0 with no ratings is not a real rating.
    rated = apps[apps["rating_count_tot"] > 0].copy()
    n_unrated = len(apps) - len(rated)
    print(f"Rated apps: {len(rated)} | unrated: {n_unrated} ({100 * n_unrated / len(apps):.1f}%)")

    # 1. Paid vs free (Welch t-test, rated apps only)
    rated["is_paid"] = rated["price"] > 0
    paid = rated.loc[rated["is_paid"], "user_rating"]
    free = rated.loc[~rated["is_paid"], "user_rating"]
    _, p = stats.ttest_ind(paid, free, equal_var=False)
    print(f"\nPaid avg {paid.mean():.2f} (n={len(paid)}) vs Free avg {free.mean():.2f} "
          f"(n={len(free)}), Welch p = {p:.2f}")
    print("Median rating count (False=free, True=paid):",
          rated.groupby("is_paid")["rating_count_tot"].median().to_dict())

    apps["is_paid"] = apps["price"] > 0
    print("Raw avg incl. unrated:", apps.groupby("is_paid")["user_rating"].mean().round(2).to_dict())
    print("Pct unrated:",
          apps.groupby("is_paid")["rating_count_tot"].apply(lambda s: (s == 0).mean() * 100).round(1).to_dict())

    # 2. Language buckets
    rated["lang_bucket"] = pd.cut(rated["lang.num"], bins=[-1, 9, 30, float("inf")],
                                  labels=["<10", "10-30", "31+"])
    print("\nLanguage buckets:")
    print(rated.groupby("lang_bucket", observed=True).agg(
        n=("id", "count"),
        avg_rating=("user_rating", "mean"),
        median_rating_count=("rating_count_tot", "median")).round(2))

    # 3. Description length vs rating
    merged = rated.merge(desc[["id", "app_desc"]], on="id")
    merged["desc_len"] = merged["app_desc"].str.strip().str.len()
    r, p_r = stats.pearsonr(merged["desc_len"], merged["user_rating"])
    rho, p_rho = stats.spearmanr(merged["desc_len"], merged["user_rating"])
    print(f"\nDescription length vs rating (n={len(merged)}):")
    print(f"  Pearson  r   = {r:.2f} (p = {p_r:.2g})")
    print(f"  Spearman rho = {rho:.2f} (p = {p_rho:.2g})")
    print(f"  r^2 = {r ** 2:.3f}  -> length explains about {100 * r ** 2:.1f}% of the variance in rating")


if __name__ == "__main__":
    main()
