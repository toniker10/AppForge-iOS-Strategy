# Data provenance and cleaning log

## Source
- Kaggle dataset of iOS App Store apps (2017 snapshot), two files:
  - `AppleStore.csv`: one row per app (price, ratings, genre, languages, etc.)
  - `appleStore_description.csv`: one row per app with its store description
- Raw files are never modified. `build_db.py` loads copies into SQLite (`appforge.db`).
- Add the dataset URL and licence here before publishing.

## Data checks (query 0 in `analysis_queries.sql`)
| Check | Result |
|---|---|
| Rows in `AppleStore` | 7,197 |
| Unique `id` | 7,197 (no duplicates) |
| Rows in descriptions table | 7,197, all ids unique |
| Apps with `rating_count_tot = 0` | 929 (12.9%) |
| Rated apps used for rating analysis | 6,268 |

## Cleaning decisions
1. **Unrated apps:** `user_rating = 0` where `rating_count_tot = 0` is a placeholder, not a score. These apps are excluded from every rating average but kept when computing share of catalog.
2. **Unnamed index column:** the first column of `AppleStore.csv` is an index and is dropped when loading.
3. **Minimum sample for genres:** a genre needs at least 10 rated apps to be compared (excludes *Catalogs*: 10 apps, 5 rated).
4. **Minimum ratings for benchmark apps:** at least 100 ratings, to avoid 5.0 scores from a single review.
5. **Column name with a dot** (`lang.num`) is quoted in SQL.
6. **Medians:** SQLite has no `MEDIAN()`, so medians use `ROW_NUMBER()`; the Python script cross-checks them.

## Known quirks
- `user_rating` only takes values in 0.5 steps (1.0 to 5.0).
- Genre is the app's primary genre only (`prime_genre`).
- Average ratings per genre are unweighted by number of ratings.
