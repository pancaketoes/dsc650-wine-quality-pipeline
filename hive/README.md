# Hive Managed Table

## Overview

Apache Hive was used to provide a structured SQL interface over the wine quality dataset after it was ingested into HDFS.

A managed Hive table named `wine_quality` was created with columns corresponding to the chemical characteristics of each wine sample and the final quality score.

## Table Design

The dataset contains the following variables:

- fixed_acidity
- volatile_acidity
- citric_acid
- residual_sugar
- chlorides
- free_sulfur_dioxide
- total_sulfur_dioxide
- density
- ph
- sulphates
- alcohol
- quality

Most measurement variables were stored as `DOUBLE`, while `quality` was stored as an `INT`.

The CSV contains a header row, so the Hive table was configured with:

```sql
TBLPROPERTIES ("skip.header.line.count"="1");
```

## Data Loading

The dataset was loaded from HDFS into the managed Hive table using:

```sql
LOAD DATA INPATH '/tmp/wine_quality/winequality_red_clean.csv'
INTO TABLE wine_quality;
```

## Queries

A sample query was used to verify that individual records were loaded correctly:

```sql
SELECT * FROM wine_quality LIMIT 10;
```

An aggregation query grouped the dataset by wine quality score:

```sql
SELECT quality, COUNT(*) AS wine_count
FROM wine_quality
GROUP BY quality
ORDER BY quality;
```

The aggregation confirmed that the data was correctly parsed and that multiple wine quality scores were represented in the dataset.

Supporting SQL files and screenshots are included in this directory.