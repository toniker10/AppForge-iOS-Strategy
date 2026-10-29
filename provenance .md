# Provenance – Apple Store Apps Dataset

- **Source**: Kaggle – Mobile App Store (7200 apps)
- **URL**: https://www.kaggle.com/datasets/ramamet4/app-store-apple-data-set-10k-apps
- **Author**: Ramanathan Perumal
- **Original data source**: iTunes Search API (Apple Inc.)
- **Collection date (per source)**: July 2017
- **License**: GPL 2
- **Download date**: 11 October 2026
- **Files**:
  - `AppleStore.csv` (837,657 bytes, about 818 KB)
  - `appleStore_description.csv` (12,965,917 bytes, about 12,662 KB or 12.4 MB)
- **Handling**: originals kept unmodified. All analysis is done on working copies.

## Initial inspection

| # | Check | Result |
|---|---|---|
| 1 | Files and exact names | 2 files: `AppleStore.csv`, `appleStore_description.csv` |
| 2 | Row containing the real headers | Row 1, no rows above it |
| 3 | Data rows (excluding header) | 7,197 in both files (matches the official 7,197) |
| 4 | Columns | `AppleStore.csv` has 17: an unnamed index column (values 1 to 7,197), then id, track_name, size_bytes, currency, price, rating_count_tot, rating_count_ver, user_rating, user_rating_ver, ver, cont_rating, prime_genre, sup_devices.num, ipadSc_urls.num, lang.num, vpp_lic. `appleStore_description.csv` has 4: id, track_name, size_bytes, app_desc |
| 5 | Unique ids | 7,197 in both files (same count) |

## Cleaning log

| Issue | Severity / count | Decision |
|---|---|---|
| Apps with `rating_count_tot = 0` (`user_rating` = 0, not a real rating) | 929 apps (12.9%) | Excluded from rating averages (6,268 rated apps remain). Kept for share of catalog |
| Unnamed index column in `AppleStore.csv` | 1 column | Ignored |
| `lang.num` contains a dot | 1 column | Quoted in SQL as `"lang.num"` |
| Description file | Single file, 7,197 rows | Imported as `appleStore_description_combined`, no recombination needed |

## Analysis decisions

| Decision | Reason |
|---|---|
| A genre needs at least 10 rated apps to be compared | Excludes *Catalogs* (10 apps, 5 rated); averages on tiny groups are unreliable |
| Benchmark apps need at least 100 ratings | Avoids 5.0 scores based on a single review |
| Medians are computed with `ROW_NUMBER()` | SQLite has no `MEDIAN()`; `analysis_stats.py` cross-checks them |
| p-value and correlation are computed in Python | SQLite has no statistical functions |

## Known quirks

- `user_rating` only takes values in 0.5 steps (1.0 to 5.0).
- Genre is the app's primary genre only (`prime_genre`).
- Average ratings per genre are not weighted by number of ratings.
