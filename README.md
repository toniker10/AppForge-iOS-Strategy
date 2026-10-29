# AppForge Labs – iOS App Store Strategy Analysis

**Recommendation:** enter the **Finance** category (with **Sports** as the validation candidate), localize into **10–30 languages**, and do not count on a paid price to lift ratings.

| | |
|---|---|
| **Role** | Data analyst (portfolio project) |
| **Tools** | SQL (SQLite), Python (pandas, SciPy, matplotlib) |
| **Data** | 7,197 iOS apps from Kaggle, collected July 2017 (apps table + descriptions table) |

> **Note:** AppForge Labs is a fictional company. The analysis is real, the business scenario is a framing device.

![Dashboard](dashboard.png)

---

## Business context

AppForge Labs is a hypothetical studio about to build its first iOS app. Leadership asked three questions, each with a metric:

| Question | Metric |
|---|---|
| Which category should we enter? | **Category opportunity**: a genre qualifies if it has ≥ 10 rated apps, an average rating below the overall average (4.05) **and** a share of the catalog below the median genre share (1.64%) |
| How should we price the app? | Average rating of paid vs free apps, **rated apps only** |
| What drives higher ratings? | Average rating by number of languages and by description length |

The report follows four steps: **What** happened, **Why** it happened, **So what** it means, **Now what** to do.

---

## 1. What (what the data shows)

| Topic | Finding |
|---|---|
| Category | 9 of 22 eligible genres qualify as opportunities. **Finance** averages **3.56** (overall 4.05) with only **1.4%** of the catalog. |
| Pricing | Paid and free apps both average **4.05** (Welch p = 0.89). The raw gap (3.72 paid vs 3.38 free) disappears once unrated apps are removed. |
| Localization | Apps with 10–30 languages average **4.21**, versus **4.00** for apps with fewer than 10. |
| Description | Apps with descriptions over 1,000 characters average **4.11**, versus **3.90** under 500 characters. The link is weak (Pearson r = 0.11). |
| Market | Games and Entertainment make up **61.1%** of all apps. Games rate well (4.19). |

**Category opportunities** (all three criteria met):

| Genre | Apps | Rated | Share of catalog | Avg rating | Avg ratings per app |
|---|---:|---:|---:|---:|---:|
| Sports | 114 | 101 | 1.6% | 3.37 | 15,832 |
| **Finance** | 104 | 71 | 1.4% | 3.56 | 16,182 |
| News | 75 | 60 | 1.0% | 3.73 | 16,269 |
| Travel | 81 | 71 | 1.1% | 3.85 | 16,120 |
| Food & Drink | 63 | 52 | 0.9% | 3.86 | 16,887 |
| Medical | 23 | 20 | 0.3% | 3.88 | **682** |
| Weather | 72 | 66 | 1.0% | 3.92 | 24,197 |
| Navigation | 46 | 31 | 0.6% | 3.98 | 17,590 |
| Business | 57 | 53 | 0.8% | 4.03 | **5,149** |

**Paid vs free:**

| | Free | Paid |
|---|---:|---:|
| Rated apps | 3,383 | 2,885 |
| **Avg rating (rated only)** | **4.05** | **4.05** |
| Raw avg rating (unrated counted as 0) | 3.38 | 3.72 |
| Share of apps with no ratings | 16.6% | 8.2% |
| Median ratings per app | 1,033 | 259 |

**Languages and description length:**

| Languages supported | Apps | Avg rating | Median ratings per app |
|---|---:|---:|---:|
| < 10 | 4,729 | 4.00 | 336 |
| **10–30** | 1,381 | **4.21** | 1,701 |
| 31+ | 158 | 4.09 | 3,497 |

| Description length | Apps | Avg rating |
|---|---:|---:|
| Short (< 500 chars) | 696 | 3.90 |
| Medium (500–1,000) | 1,253 | 3.94 |
| Long (> 1,000) | 4,319 | 4.11 |

---

## 2. Why (what explains it)

```
Is there room for a new app in a category?
├── Quality gap   genre avg rating below the overall 4.05
├── Crowding      genre share of catalog below the median 1.64%
└── Demand        enough ratings per app (this rules out Medical: 682 per app)

What drives the average rating?
├── Category            largest spread (Sports 3.37 ... Book 4.27)
├── Price model         no effect (4.05 vs 4.05)
├── Languages           association (4.21 for 10–30), likely app maturity
└── Description length  weak (r = 0.11)
```

- **Finance:** users are active (about 16,000 ratings per app, in line with the other opportunity genres) but dissatisfied, and few apps compete. A plausible reason is high expectations of trust and accuracy in money apps. This is a hypothesis; the data does not test it.
- **Finance vs Sports:** Sports has the lowest rating (3.37) but sits right at the saturation limit (1.58% vs a 1.64% median). Finance is slightly less crowded (1.4%), so it is the first choice and Sports the validation candidate.
- **Medical and Business** have a low rating but little engagement (682 and 5,149 ratings per app), so a low rating alone does not make them an opportunity.
- **Lifestyle** rates low (3.58) but holds 2.0% of the catalog, above the median, so it is too crowded to qualify.
- **The "paid premium" is an artifact.** 16.6% of free apps have no ratings against 8.2% of paid apps, and unrated apps count as 0 in the raw average. Without them, the difference is zero.
- **Languages:** apps with 10–30 languages have a median of 1,701 ratings versus 336 for the smallest group. The better ratings probably reflect mature, well-resourced apps rather than a pure localization effect.
- **Description length:** Pearson r = 0.11 (p < 0.001, n = 6,268) and Spearman ρ = 0.08. The link is significant only because the sample is large; length explains about 1% of the variation in ratings.

---

## 3. So what (what it means for AppForge)

- **Finance is the clearest opening:** an engaged audience, an average rating well below the market, and little competition. A clearly better product has room to stand out.
- **Price is not a quality lever.** Choose free or paid for revenue reasons. A paid model also collects feedback more slowly (median 259 ratings vs 1,033), which delays learning after launch.
- **Localization is a reach decision, not a rating fix.** Expect better ratings only if the product itself is good.
- **Description length is basic hygiene.** It costs little, but it will not move ratings much.
- **Games and Entertainment are crowded.** Games rate well (4.19), which makes them a hard place to stand out for a first app.
- **Inside Finance, paid apps rate higher** (4.16, n = 16) than free ones (3.39, n = 55). With only 16 paid apps, this is too small a group to support a pricing decision.

---

## 4. Now what (recommendations)

| # | Action | Owner | Success metric |
|---|---|---|---|
| 1 | Prioritize **Finance** for the first app. Validate against **Sports** and **News** with a short round of user interviews | Product | One category chosen by the end of discovery |
| 2 | Study the leading Finance app as a benchmark (Credit Karma: 5.0 stars, 101,679 ratings) and list what it does that average apps do not | Product / Design | Written gap analysis |
| 3 | Launch **free**. Treat paid pricing as a later experiment, not a quality signal | Product | Average rating ≥ 4.0 after the first 100 ratings |
| 4 | Plan localization for **10–30 languages**, phased by market, and measure the effect rather than assuming it | Growth | Rating by locale after launch |
| 5 | Write a complete store description (over 1,000 characters), without expecting a large rating effect | Marketing | Conversion rate on the listing page |

---

## Data and cleaning

- **Source:** Kaggle, *Mobile App Store (7200 apps)*, collected July 2017 from the iTunes Search API. Licence: GPL 2. Full details in [`provenance.md`](provenance.md).
- 7,197 apps, 7,197 unique ids, one description per app.
- **929 apps (12.9%) have no ratings.** For them `user_rating = 0` means "no data", not "terrible". They are excluded from every rating average (6,268 rated apps remain) but kept for share-of-catalog counts.
- A genre needs at least 10 rated apps to be compared (this excludes *Catalogs*: 10 apps, 5 rated).

## Limitations

- **Observational data, July 2017 snapshot.** The store has changed since. These are associations, not causal effects.
- **Ratings are rounded to 0.5 steps** in the source, and genre averages treat every app equally (not weighted by number of ratings).
- **Rated apps only.** Apps without ratings are excluded from rating averages, which can hide very new or unpopular apps.
- **Small groups:** Finance paid apps (16), 31+ languages (158) and several genres have limited samples.
- **Correlation is not strategy.** Localization and description length may be symptoms of well-funded teams.

## Repository files

| File | What it is |
|---|---|
| `README.md` | This report |
| `dashboard.png` | Summary dashboard |
| `analysis_queries.sql` | All SQL: paid vs free, languages, categories, descriptions, benchmarks |
| `build_db.py` | Loads the two Kaggle CSVs into a SQLite database |
| `analysis_stats.py` | p-value, correlations and median cross-checks |
| `make_dashboard.py` | Builds `dashboard.png` |
| `provenance.md` | Source, data checks and cleaning log |
| `requirements.txt` | Python packages needed |

## How to reproduce

1. Download the dataset from Kaggle and put `AppleStore.csv` and `appleStore_description.csv` in the same folder as these files.
2. Run:

```bash
pip install -r requirements.txt
python build_db.py            # creates appforge.db
python analysis_stats.py      # p-value and correlations
python make_dashboard.py      # regenerates dashboard.png
```

3. Open `appforge.db` in any SQLite tool (SQLite 3.25+ needed for window functions) and run the queries in `analysis_queries.sql` one at a time.

---

*Portfolio project. Not financial or business advice.*
