import psycopg2
import pandas as pd
from tabulate import tabulate
import pyperclip

conn = psycopg2.connect(
    dbname = "pushups_data",
    user = "postgres",
    password = "Pushharder100",
    host = "localhost",
    port = "5432"
)
# cursor = conn.cursor()

# Loop through rows and insert with ON CONFLICT
# cursor.execute("""
# SELECT 
# 	name,
# 	SUM(pushups) AS total,
# 	AVG(pushups) AS average
# FROM "Last 2 weeks"
# GROUP BY name
# ORDER BY average DESC
# """)

# rows = cursor.fetchall()

# for row in rows:
#     print(row)

df = pd.read_sql("""
    SELECT name,
            SUM(pushups) AS total,
            ROUND(AVG(pushups)::numeric, 2) AS average,
            MIN(pushups) AS min,
            MAX(pushups) AS max,
            COUNT(pushups) AS days,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pushups) AS median
    FROM "Last 2 weeks"
    WHERE date >= '2025-08-01'
    GROUP BY name
    ORDER BY total DESC
""", conn)

# print(df.to_string(index=False))

tab_beauty = tabulate(df, headers='keys', tablefmt='psql', showindex=False)
# print(tab_beauty)

df_streak = pd.read_sql("""
   WITH
-- 1) Get one row per user per day
	user_dates AS (
		SELECT
			name,
			date::date AS dt
		FROM "Last 2 weeks"
		GROUP BY name, dt
	),

-- 2) Keep only days *up through yesterday*, and assign a descending rank
	ranked AS (
		SELECT
			name,
			dt,
			ROW_NUMBER() OVER (PARTITION BY name ORDER BY dt DESC) AS rn
		FROM user_dates
		WHERE dt <= CURRENT_DATE - INTERVAL '1 day'
	),

-- 3) Keep only those rows that *line up* as a perfect run back from yesterday:
-- dt = (yesterday - (rn - 1) days)
	consecutive AS (
		SELECT
			name,
			dt
		FROM ranked
		WHERE dt = (CURRENT_DATE - INTERVAL '1 day')
					- (rn - 1) * INTERVAL '1 day'
	),

-- 4) Count how many days each user survived in step 3
	streaks AS (
		SELECT
			name,
			COUNT(*) as current_streak
		FROM consecutive
		GROUP BY name
		HAVING COUNT(*) > 0 	-- only keep those with at least one day streak
	)

-- 5) Left join back to everyone so those with no yesterday get 0
	SELECT
		u.name,
		COALESCE(s.current_streak, 0) AS current_streak
	FROM (
		SELECT DISTINCT name
		FROM "Last 2 weeks"
	) u
	LEFT JOIN streaks s USING(name)
	WHERE s.current_streak > 0
	ORDER BY current_streak DESC;                     
""", conn)

tab_streak = tabulate(df_streak, headers='keys', tablefmt='psql', showindex=False)

# %% Biggest gaps

df_gap = pd.read_sql("""
WITH tmp AS (
SELECT 
	name,
	date,
	LAG(date) OVER (PARTITION BY name ORDER BY date) AS prev_date,
	date - LAG(date) OVER (PARTITION BY name ORDER BY date) AS gap
FROM "Last 2 weeks"
),
current AS (
	SELECT DISTINCT name AS name FROM "Last 2 weeks" WHERE date >= '2025-01-01'
)
SELECT 
	current.name,
	tmp.date,
	tmp.prev_date,
	tmp.gap,
	ROUND(tmp.gap / 365 ::numeric, 1) AS gap_year
FROM tmp
JOIN current ON tmp.name = current.name
WHERE gap > 1 --AND tmp.name = 'Антон'
ORDER BY gap DESC
LIMIT 20
""", conn)

tab_gap = tabulate(df_gap, headers='keys', tablefmt='psql', showindex=False)

# %% Longest streak

df_longests_streak = pd.read_sql("""
WITH
-- 1) Get one row per user per day
	user_dates AS (
		SELECT DISTINCT
			name,
			date::date AS dt
		FROM "Last 2 weeks"

	),
-- 2) Assign row numbers to each user’s dates
	ranked AS (
		SELECT
			name,
			dt,
			ROW_NUMBER() OVER (PARTITION BY name ORDER BY dt) AS rn
		FROM user_dates 
	),
-- 3) Calculate streak group based on the "gap"
streaks AS (
	SELECT
		name,
		dt,
		dt - (rn || ' days')::interval AS streak_group,
		rn
	FROM ranked
)

-- 4) Group by streak
SELECT
	name,
	MIN(dt) AS start_date,
	MAX(dt) AS end_date,
	COUNT(*) AS streak_length
FROM streaks
WHERE name = 'Антон'
GROUP BY name, streak_group
ORDER BY streak_length DESC
LIMIT 20
""", conn)

tab_longest_streak = tabulate(df_longests_streak, headers='keys', tablefmt='psql', showindex=False)

pyperclip.copy(tab_longest_streak)
print(tab_longest_streak)

# pyperclip.copy(tab_gap)
# print(tab_gap)

# pyperclip.copy(tab_streak)
# print(tab_streak)

# pyperclip.copy(tab_beauty)
# print(tab_beauty)

conn.commit()
# cursor.close()
conn.close()