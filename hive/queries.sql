-- Load the CSV from HDFS into the managed Hive table
LOAD DATA INPATH '/tmp/wine_quality/winequality_red_clean.csv'
INTO TABLE wine_quality;

-- Preview the loaded data
SELECT * FROM wine_quality LIMIT 10;

-- Aggregate wines by quality score
SELECT quality, COUNT(*) AS wine_count
FROM wine_quality
GROUP BY quality
ORDER BY quality;