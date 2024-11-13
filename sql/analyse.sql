USE summer_olympics;
ALTER TABLE clean_events RENAME TO olympics;
ALTER TABLE event_table RENAME TO events;

DROP TABLE medalists;

SELECT * FROM events;
SELECT * FROM olympics;
SELECT * FROM country;


-- HOST COUNTRY percentage per medal 
SELECT 
    host_country,
    game_year,
    medal_type,
    COUNT(*) AS medals_won,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) 
                               FROM olympics AS total 
                               WHERE total.game_year = olympics.game_year 
                               AND total.medal_type = olympics.medal_type)), 2) AS percentage_of_total
FROM 
    olympics
WHERE 
    athlete_country = host_country
GROUP BY 
    host_country, 
    game_year, 
    medal_type
ORDER BY 
    game_year, 
    host_country, 
    medal_type;

-- HOST COUNTRY percentage in total

SELECT
    host_country,
    game_year,
    COUNT(*) AS medals_won,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*)
                               FROM olympics AS total
                               WHERE total.game_year = olympics.game_year)), 2) AS percentage_of_total
FROM
    olympics
WHERE
    athlete_country = host_country
GROUP BY
    host_country,
    game_year
ORDER BY
    game_year,
    host_country;
    
-- HOST compared to four previous/next olympics
    
    WITH medal_data AS (
    SELECT 
        host_country,
        game_year,
        medal_type,
        COUNT(*) AS medals_won,
        ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) 
                                   FROM olympics AS total 
                                   WHERE total.game_year = olympics.game_year 
                                   AND total.medal_type = olympics.medal_type)), 2) AS percentage_of_total
    FROM 
        olympics
    WHERE 
        athlete_country = host_country
    GROUP BY 
        host_country, 
        game_year, 
        medal_type
),
year_comparison AS (
    SELECT
        md.*,
        LAG(medals_won, 1) OVER (PARTITION BY md.host_country, md.medal_type ORDER BY md.game_year) AS prev_medals_won_1,
        LAG(medals_won, 2) OVER (PARTITION BY md.host_country, md.medal_type ORDER BY md.game_year) AS prev_medals_won_2,
        LAG(medals_won, 3) OVER (PARTITION BY md.host_country, md.medal_type ORDER BY md.game_year) AS prev_medals_won_3,
        LAG(medals_won, 4) OVER (PARTITION BY md.host_country, md.medal_type ORDER BY md.game_year) AS prev_medals_won_4,
        LEAD(medals_won, 1) OVER (PARTITION BY md.host_country, md.medal_type ORDER BY md.game_year) AS next_medals_won_1,
        LEAD(medals_won, 2) OVER (PARTITION BY md.host_country, md.medal_type ORDER BY md.game_year) AS next_medals_won_2,
        LEAD(medals_won, 3) OVER (PARTITION BY md.host_country, md.medal_type ORDER BY md.game_year) AS next_medals_won_3,
        LEAD(medals_won, 4) OVER (PARTITION BY md.host_country, md.medal_type ORDER BY md.game_year) AS next_medals_won_4
    FROM medal_data md
)
SELECT
    host_country,
    game_year,
    medal_type,
    medals_won,
    percentage_of_total,
    prev_medals_won_1,
    prev_medals_won_2,
    prev_medals_won_3,
    prev_medals_won_4,
    next_medals_won_1,
    next_medals_won_2,
    next_medals_won_3,
    next_medals_won_4,
    -- You can calculate differences between the current year's medals and previous/next Olympics as needed
    medals_won - COALESCE(prev_medals_won_1, 0) AS diff_from_prev_1,
    medals_won - COALESCE(prev_medals_won_2, 0) AS diff_from_prev_2,
    medals_won - COALESCE(prev_medals_won_3, 0) AS diff_from_prev_3,
    medals_won - COALESCE(prev_medals_won_4, 0) AS diff_from_prev_4,
    medals_won - COALESCE(next_medals_won_1, 0) AS diff_from_next_1,
    medals_won - COALESCE(next_medals_won_2, 0) AS diff_from_next_2,
    medals_won - COALESCE(next_medals_won_3, 0) AS diff_from_next_3,
    medals_won - COALESCE(next_medals_won_4, 0) AS diff_from_next_4
FROM year_comparison
ORDER BY game_year, host_country, medal_type;

