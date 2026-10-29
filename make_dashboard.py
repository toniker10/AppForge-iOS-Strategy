"""Create dashboard.png from the raw CSVs.

Usage:  python make_dashboard.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT  # the two CSV files sit in the same folder as the scripts
OUT = ROOT / "dashboard.png"

INK, MUTED, GRID = "#1f2937", "#6b7280", "#e5e7eb"
ACCENT, ACCENT2, GREY = "#2563eb", "#f59e0b", "#cbd5e1"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "text.color": INK, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": GRID,
    "axes.spines.top": False, "axes.spines.right": False,
})


def load():
    apps = pd.read_csv(RAW / "AppleStore.csv")
    desc = pd.read_csv(RAW / "appleStore_description.csv")
    rated = apps[apps["rating_count_tot"] > 0].copy()
    return apps, desc, rated


def opportunity_table(apps, rated):
    g = apps.groupby("prime_genre").agg(
        n_apps=("id", "count"),
        n_rated=("rating_count_tot", lambda s: (s > 0).sum()))
    g["share"] = 100 * g["n_apps"] / len(apps)
    g["avg_rating"] = rated.groupby("prime_genre")["user_rating"].mean()
    g = g[g["n_rated"] >= 10]
    overall = rated["user_rating"].mean()
    median_share = g["share"].median()
    g["opportunity"] = (g["avg_rating"] < overall) & (g["share"] < median_share)
    return g, overall, median_share


def bar_panel(ax, labels, values, ns, title, color, ylim=(0, 5)):
    bars = ax.bar(labels, values, color=color, width=0.6)
    ax.set_ylim(*ylim)
    ax.set_title(title, loc="left", fontsize=11, fontweight="bold", pad=10)
    ax.set_ylabel("Average rating (rated apps)")
    ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)
    for b, v, n in zip(bars, values, ns):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.08, f"{v:.2f}", ha="center",
                fontsize=10, fontweight="bold")
        ax.text(b.get_x() + b.get_width() / 2, 0.15, f"n={n:,}", ha="center",
                fontsize=8.5, color="white")


def main() -> None:
    apps, desc, rated = load()
    g, overall, median_share = opportunity_table(apps, rated)

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("AppForge Labs – iOS App Store: what should a new app do?",
                 x=0.04, ha="left", fontsize=16, fontweight="bold")
    fig.text(0.04, 0.925, "7,197 apps (2017 snapshot) · ratings analysed on the 6,268 apps that have at least one rating",
             fontsize=10, color=MUTED)

    # ---- Panel 1: category opportunity ----
    ax = axes[0, 0]
    ax.axhline(overall, color=MUTED, lw=1, ls="--")
    ax.axvline(median_share, color=MUTED, lw=1, ls="--")
    ax.axvspan(0.2, median_share, ymin=0, ymax=(overall - 3.2) / (4.5 - 3.2), color=ACCENT, alpha=0.06)
    for name, row in g.iterrows():
        col = ACCENT if row["opportunity"] else GREY
        ax.scatter(row["share"], row["avg_rating"], s=60, color=col, zorder=3,
                   edgecolor="white", linewidth=0.8)
    offsets = {"Sports": (6, 2), "Finance": (-8, -13), "News": (-6, -14), "Travel": (-4, 7),
               "Food & Drink": (-70, -3), "Medical": (-2, 8), "Weather": (-8, 8),
               "Navigation": (-60, 6), "Business": (-4, 8), "Lifestyle": (6, 3)}
    for name, (dx, dy) in offsets.items():
        r = g.loc[name]
        ax.annotate(name, (r["share"], r["avg_rating"]), xytext=(dx, dy), textcoords="offset points",
                    fontsize=8.5, color=ACCENT if r["opportunity"] else MUTED,
                    fontweight="bold" if name in ("Finance", "Sports") else "normal")
    ax.set_xscale("log")
    ax.set_xticks([0.3, 1, 3, 10, 50]); ax.set_xticklabels(["0.3%", "1%", "3%", "10%", "50%"])
    ax.set_xlim(0.25, 70); ax.set_ylim(3.2, 4.5)
    ax.set_xlabel("Share of catalog (log scale)"); ax.set_ylabel("Average rating")
    ax.set_title("Finance and Sports: low ratings in uncrowded categories", loc="left",
                 fontsize=11, fontweight="bold", pad=10)
    ax.text(65, overall + 0.015, f"overall avg {overall:.2f}", fontsize=8, color=MUTED, ha="right")
    ax.text(median_share * 1.05, 4.46, f"median share {median_share:.2f}%", fontsize=8, color=MUTED, va="top")
    ax.text(0.27, 3.22, "opportunity zone", fontsize=8.5, color=ACCENT, style="italic")
    ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)

    # ---- Panel 2: paid vs free ----
    ax = axes[0, 1]
    apps["type"] = np.where(apps["price"] > 0, "Paid", "Free")
    rated["type"] = np.where(rated["price"] > 0, "Paid", "Free")
    raw = apps.groupby("type")["user_rating"].mean()
    fair = rated.groupby("type")["user_rating"].mean()
    unrated = apps.groupby("type")["rating_count_tot"].apply(lambda s: (s == 0).mean() * 100)
    x = np.arange(2); w = 0.36
    b1 = ax.bar(x - w / 2, [raw["Free"], raw["Paid"]], w, color=GREY, label="Raw (unrated counted as 0)")
    b2 = ax.bar(x + w / 2, [fair["Free"], fair["Paid"]], w, color=ACCENT, label="Rated apps only")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.08, f"{b.get_height():.2f}",
                    ha="center", fontsize=10, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([f"Free\n{unrated['Free']:.1f}% unrated", f"Paid\n{unrated['Paid']:.1f}% unrated"])
    ax.set_ylim(0, 5.8); ax.set_yticks(range(6)); ax.set_ylabel("Average rating")
    ax.set_title("No paid premium: the gap is an unrated-apps artifact", loc="left",
                 fontsize=11, fontweight="bold", pad=10)
    ax.legend(frameon=False, fontsize=9, loc="upper center", ncol=2)
    ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)

    # ---- Panel 3: language buckets ----
    rated["lang_bucket"] = pd.cut(rated["lang.num"], bins=[-1, 9, 30, float("inf")],
                                  labels=["<10", "10–30", "31+"])
    lb = rated.groupby("lang_bucket", observed=True)["user_rating"].agg(["mean", "count"])
    bar_panel(axes[1, 0], lb.index.astype(str), lb["mean"], lb["count"],
              "Localization: 10–30 languages is the sweet spot", ACCENT)
    axes[1, 0].set_xlabel("Languages supported")

    # ---- Panel 4: description length ----
    m = rated.merge(desc[["id", "app_desc"]], on="id")
    m["len"] = m["app_desc"].str.strip().str.len()
    m["bucket"] = pd.cut(m["len"], bins=[-1, 499, 1000, float("inf")],
                         labels=["Short\n(<500)", "Medium\n(500–1000)", "Long\n(>1000)"])
    db = m.groupby("bucket", observed=True)["user_rating"].agg(["mean", "count"])
    bar_panel(axes[1, 1], db.index.astype(str), db["mean"], db["count"],
              "Longer descriptions, slightly higher ratings (weak link)", ACCENT)
    axes[1, 1].set_xlabel("Description length (characters)")

    fig.tight_layout(rect=(0.02, 0.02, 0.98, 0.91), h_pad=3, w_pad=3)
    fig.savefig(OUT, dpi=130, facecolor="white")
    print(f"Saved {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
