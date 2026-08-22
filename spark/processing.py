"""
Data preparation utilities for the DSC 650 Wine Quality
Big Data Final Project.

The primary executable Spark ML application is analysis.py.
This module contains the preprocessing logic used to prepare
the Hive wine quality data for Spark MLlib.
"""

from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler


FEATURE_COLUMNS = [
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol",
]


def prepare_ml_data(df):
    """
    Prepare the wine quality dataframe for Spark MLlib.

    Steps:
    1. Remove rows containing null values.
    2. Convert the quality column into a numeric label.
    3. Assemble the predictor columns into a single features vector.

    Parameters
    ----------
    df : pyspark.sql.DataFrame
        Spark DataFrame containing the wine quality dataset.

    Returns
    -------
    pyspark.sql.DataFrame
        DataFrame containing only the MLlib features and label columns.
    """

    cleaned_df = df.na.drop()

    labeled_df = cleaned_df.withColumn(
        "label",
        col("quality").cast("double")
    )

    assembler = VectorAssembler(
        inputCols=FEATURE_COLUMNS,
        outputCol="features"
    )

    ml_data = assembler.transform(labeled_df)

    return ml_data.select("features", "label")