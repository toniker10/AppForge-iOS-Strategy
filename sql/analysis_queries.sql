-- AppForge Labs – iOS App Strategy Analysis
-- Dialect: SQLite 3.25+ (window functions required).
-- Tables: AppleStore, appleStore_description_combined (created by scripts/build_db.py).
-- Cleaning rule: apps with rating_count_tot = 0 have user_rating = 0 (not a real rating),
-- so they are excluded from rating averages but kept for share-of-catalog counts.
-- SQLite has no MEDIAN(), so medians are computed with ROW_NUMBER().

---------------------------------------------------------------
-- 0. DATA CHECKS (run first; results are recorded in docs/provenance.md)
---------------------------------------------------------------
SELECT COUNT(*)                         AS total_apps,
       COUNT(DISTINCT id)               AS unique_ids,
       SUM(rating_count_tot = 0)        AS apps_without_ratings,
       ROUND(100.0 * SUM(rating_count_tot = 0) / COUNT(*), 1) AS pct_without_ratings
FROM AppleStore;

SELECT COUNT(*) AS desc_rows, COUNT(DISTINCT id) AS desc_unique_ids
FROM appleStore_description_combined;

---------------------------------------------------------------
-- 1a. PAID vs FREE – rated apps only (the fair comparison)
-- Includes median rating count.
---------------------------------------------------------------
WITH rated AS (
    SELECT CASE WHEN price > 0 THEN 'Paid' ELSE 'Free' END AS app_type,
           user_rating, rating_count_tot
    FROM AppleStore
    WHERE rating_count_tot > 0
),
ranked AS (
    SELECT app_type, rating_count_tot,
           ROW_NUMBER() OVER (PARTITION BY app_type ORDER BY rating_count_tot) AS rn,
           COUNT(*)     OVER (PARTITION BY app_type)                           AS cnt
    FROM rated
),
medians AS (
    SELECT app_type, AVG(rating_count_tot) AS median_rating_count
    FROM ranked
    WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
    GROUP BY app_type
)
SELECT r.app_type,
       COUNT(*)                          AS n_apps,
       ROUND(AVG(r.user_rating), 2)      AS avg_rating,
       ROUND(AVG(r.rating_count_tot), 0) AS avg_rating_count,
       ROUND(m.median_rating_count, 0)   AS median_rating_count
FROM rated r
JOIN medians m ON m.app_type = r.app_type
GROUP BY r.app_type;

---------------------------------------------------------------
-- 1b. PAID vs FREE – raw gap vs unrated share
-- Shows why the raw "paid premium" is an artifact: free apps have far more
-- unrated apps, and unrated = 0 drags their average down.
---------------------------------------------------------------
SELECT CASE WHEN price > 0 THEN 'Paid' ELSE 'Free' END AS app_type,
       COUNT(*)                                          AS n_apps,
       ROUND(AVG(user_rating), 2)                        AS raw_avg_rating_incl_unrated,
       ROUND(100.0 * SUM(rating_count_tot = 0) / COUNT(*), 1) AS pct_unrated
FROM AppleStore
GROUP BY app_type;

---------------------------------------------------------------
-- 2. LANGUAGE BUCKETS
-- The column name contains a dot, so it must be quoted.
-- Median rating count supports the "maturity, not cause" hypothesis.
---------------------------------------------------------------
WITH rated AS (
    SELECT CASE
               WHEN "lang.num" < 10              THEN '1) <10'
               WHEN "lang.num" BETWEEN 10 AND 30 THEN '2) 10-30'
               ELSE                                   '3) 31+'
           END AS language_bucket,
           user_rating, rating_count_tot
    FROM AppleStore
    WHERE rating_count_tot > 0
),
ranked AS (
    SELECT language_bucket, rating_count_tot,
           ROW_NUMBER() OVER (PARTITION BY language_bucket ORDER BY rating_count_tot) AS rn,
           COUNT(*)     OVER (PARTITION BY language_bucket)                           AS cnt
    FROM rated
),
medians AS (
    SELECT language_bucket, AVG(rating_count_tot) AS median_rating_count
    FROM ranked
    WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
    GROUP BY language_bucket
)
SELECT r.language_bucket,
       COUNT(*)                        AS n_apps,
       ROUND(AVG(r.user_rating), 2)    AS avg_rating,
       ROUND(m.median_rating_count, 0) AS median_rating_count
FROM rated r
JOIN medians m ON m.language_bucket = r.language_bucket
GROUP BY r.language_bucket
ORDER BY avg_rating DESC;

---------------------------------------------------------------
-- 3. CATEGORY OPPORTUNITY
-- Criteria (identical to the README definition):
--   a) genre has >= 10 rated apps
--   b) genre avg rating < overall avg rating (rated apps only)
--   c) genre share of catalog < median share across eligible genres
-- Share uses ALL apps; rating averages use rated apps only.
---------------------------------------------------------------
WITH g AS (
    SELECT prime_genre,
           COUNT(*)                  AS n_apps,
           SUM(rating_count_tot > 0) AS n_rated,
           100.0 * COUNT(*) / (SELECT COUNT(*) FROM AppleStore) AS share_pct,
           AVG(CASE WHEN rating_count_tot > 0 THEN user_rating      END) AS avg_rating,
           AVG(CASE WHEN rating_count_tot > 0 THEN rating_count_tot END) AS avg_rating_count
    FROM AppleStore
    GROUP BY prime_genre
    HAVING SUM(rating_count_tot > 0) >= 10
),
overall AS (
    SELECT AVG(user_rating) AS avg_rating
    FROM AppleStore
    WHERE rating_count_tot > 0
),
ranked_share AS (
    SELECT share_pct,
           ROW_NUMBER() OVER (ORDER BY share_pct) AS rn,
           COUNT(*)     OVER ()                   AS cnt
    FROM g
),
median_share AS (
    SELECT AVG(share_pct) AS share_pct
    FROM ranked_share
    WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
)
SELECT g.prime_genre,
       g.n_apps,
       g.n_rated,
       ROUND(g.share_pct, 1)        AS share_of_catalog_pct,
       ROUND(g.avg_rating, 2)       AS avg_rating,
       ROUND(g.avg_rating_count, 0) AS avg_rating_count
FROM g, overall, median_share
WHERE g.avg_rating < overall.avg_rating
  AND g.share_pct  < median_share.share_pct
ORDER BY g.avg_rating ASC;

---------------------------------------------------------------
-- 3b. FINANCE: paid vs free (rated apps only)
---------------------------------------------------------------
SELECT CASE WHEN price > 0 THEN 'Paid' ELSE 'Free' END AS app_type,
       COUNT(*)                   AS n_apps,
       ROUND(AVG(user_rating), 2) AS avg_rating
FROM AppleStore
WHERE prime_genre = 'Finance' AND rating_count_tot > 0
GROUP BY app_type;

---------------------------------------------------------------
-- 3c. GAMES + ENTERTAINMENT: share of catalog and Games rating
---------------------------------------------------------------
SELECT ROUND(100.0 * SUM(prime_genre IN ('Games', 'Entertainment')) / COUNT(*), 1)
           AS games_entertainment_share_pct
FROM AppleStore;

SELECT ROUND(AVG(user_rating), 2) AS games_avg_rating
FROM AppleStore
WHERE prime_genre = 'Games' AND rating_count_tot > 0;

---------------------------------------------------------------
-- 4. DESCRIPTION LENGTH (characters)
-- The correlation and p-value are computed in scripts/analysis_stats.py,
-- because SQLite has no CORR().
---------------------------------------------------------------
SELECT
    CASE
        WHEN LENGTH(TRIM(b.app_desc)) < 500   THEN '1) Short (<500)'
        WHEN LENGTH(TRIM(b.app_desc)) <= 1000 THEN '2) Medium (500-1000)'
        ELSE                                       '3) Long (>1000)'
    END AS desc_length,
    COUNT(*)                     AS n_apps,
    ROUND(AVG(a.user_rating), 2) AS avg_rating
FROM AppleStore a
JOIN appleStore_description_combined b ON a.id = b.id
WHERE a.rating_count_tot > 0
GROUP BY desc_length
ORDER BY desc_length;

---------------------------------------------------------------
-- 5. TOP APP PER GENRE (min. 100 ratings to avoid 5.0 apps with a single review)
-- ROW_NUMBER guarantees exactly one app per genre. Used as a benchmark list.
---------------------------------------------------------------
SELECT track_name, prime_genre, user_rating, rating_count_tot
FROM (
    SELECT track_name, prime_genre, user_rating, rating_count_tot,
           ROW_NUMBER() OVER (
               PARTITION BY prime_genre
               ORDER BY user_rating DESC, rating_count_tot DESC
           ) AS rn
    FROM AppleStore
    WHERE rating_count_tot >= 100
) t
WHERE rn = 1
ORDER BY prime_genre;
