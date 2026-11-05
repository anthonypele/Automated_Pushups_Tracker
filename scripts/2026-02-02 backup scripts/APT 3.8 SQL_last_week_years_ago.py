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

df = pd.read_sql("""
WITH date_windows AS (
    SELECT 'lw_25' AS label,
           date_trunc('week', CURRENT_DATE) - INTERVAL '7 days' AS week_start,
           date_trunc('week', CURRENT_DATE) AS week_end
    UNION ALL
    SELECT 'lw_24', date_trunc('week', CURRENT_DATE) - INTERVAL '1 year' - INTERVAL '7 days', date_trunc('week', CURRENT_DATE) - INTERVAL '1 year'
    UNION ALL
    SELECT 'lw_23', date_trunc('week', CURRENT_DATE) - INTERVAL '2 years' - INTERVAL '7 days', date_trunc('week', CURRENT_DATE) - INTERVAL '2 years'
    UNION ALL
    SELECT 'lw_22', date_trunc('week', CURRENT_DATE) - INTERVAL '3 years' - INTERVAL '7 days', date_trunc('week', CURRENT_DATE) - INTERVAL '3 years'
    UNION ALL
    SELECT 'lw_21', date_trunc('week', CURRENT_DATE) - INTERVAL '4 years' - INTERVAL '7 days', date_trunc('week', CURRENT_DATE) - INTERVAL '4 years'
    UNION ALL
    SELECT 'lw_20', date_trunc('week', CURRENT_DATE) - INTERVAL '5 years' - INTERVAL '7 days', date_trunc('week', CURRENT_DATE) - INTERVAL '5 years'
    UNION ALL
    SELECT 'lw_19', date_trunc('week', CURRENT_DATE) - INTERVAL '6 years' - INTERVAL '7 days', date_trunc('week', CURRENT_DATE) - INTERVAL '6 years'
    UNION ALL
    SELECT 'lw_18', date_trunc('week', CURRENT_DATE) - INTERVAL '7 years' - INTERVAL '7 days', date_trunc('week', CURRENT_DATE) - INTERVAL '7 years'
),

-- Users who were active at all during any of the 8 weeks
active_users AS (
    SELECT DISTINCT name
    FROM "Last 2 weeks"
    WHERE date >= (SELECT MIN(week_start) FROM date_windows)
),

-- Users active in 2025 only
active_2025 AS (
    SELECT DISTINCT name
    FROM "Last 2 weeks"
    WHERE date >= '2025-01-01'
),

stats AS (
    SELECT
        l2w.name,
        SUM(CASE WHEN l2w.date >= dw.week_start AND l2w.date < dw.week_end AND dw.label = 'lw_25' THEN l2w.pushups END) AS lw_25,
        SUM(CASE WHEN l2w.date >= dw.week_start AND l2w.date < dw.week_end AND dw.label = 'lw_24' THEN l2w.pushups END) AS lw_24,
        SUM(CASE WHEN l2w.date >= dw.week_start AND l2w.date < dw.week_end AND dw.label = 'lw_23' THEN l2w.pushups END) AS lw_23,
        SUM(CASE WHEN l2w.date >= dw.week_start AND l2w.date < dw.week_end AND dw.label = 'lw_22' THEN l2w.pushups END) AS lw_22,
        SUM(CASE WHEN l2w.date >= dw.week_start AND l2w.date < dw.week_end AND dw.label = 'lw_21' THEN l2w.pushups END) AS lw_21,
        SUM(CASE WHEN l2w.date >= dw.week_start AND l2w.date < dw.week_end AND dw.label = 'lw_20' THEN l2w.pushups END) AS lw_20,
        SUM(CASE WHEN l2w.date >= dw.week_start AND l2w.date < dw.week_end AND dw.label = 'lw_19' THEN l2w.pushups END) AS lw_19,
        SUM(CASE WHEN l2w.date >= dw.week_start AND l2w.date < dw.week_end AND dw.label = 'lw_18' THEN l2w.pushups END) AS lw_18
    FROM "Last 2 weeks" l2w
    JOIN active_users au ON l2w.name = au.name
    JOIN active_2025 a25 ON l2w.name = a25.name
    CROSS JOIN date_windows dw
    GROUP BY l2w.name
)

SELECT *
FROM stats
ORDER BY lw_25 DESC NULLS LAST;

""", conn)

tab_weeks = tabulate(df, headers='keys', tablefmt='psql', showindex=False)

pyperclip.copy(tab_weeks)
print(tab_weeks)


conn.commit()
# cursor.close()
conn.close()