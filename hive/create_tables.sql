CREATE TABLE wine_quality (
    fixed_acidity DOUBLE,
    volatile_acidity DOUBLE,
    citric_acid DOUBLE,
    residual_sugar DOUBLE,
    chlorides DOUBLE,
    free_sulfur_dioxide DOUBLE,
    total_sulfur_dioxide DOUBLE,
    density DOUBLE,
    ph DOUBLE,
    sulphates DOUBLE,
    alcohol DOUBLE,
    quality INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");