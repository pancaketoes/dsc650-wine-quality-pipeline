# Spark MLlib Wine Quality Analysis

## Overview

Apache Spark MLlib was used to train and evaluate a machine-learning model using the wine quality dataset stored in Hive.

The Spark application reads the managed Hive table `wine_quality`, prepares the feature columns, trains a Linear Regression model, evaluates the model, and writes the resulting performance metrics into HBase.

## Data Source

Spark reads the project data directly from the Hive managed table:

```text
default.wine_quality
```

The dataset contains 11 chemical measurements used as predictor variables and the wine `quality` score as the target variable.

## Machine Learning Algorithm

The model used for this project is:

```text
Linear Regression
```

Linear Regression was selected because the target variable, `quality`, is numeric. The purpose of the model is to predict wine quality from the chemical characteristics of each wine sample.

## Input Features

The following columns were used as predictors:

* `fixed_acidity`
* `volatile_acidity`
* `citric_acid`
* `residual_sugar`
* `chlorides`
* `free_sulfur_dioxide`
* `total_sulfur_dioxide`
* `density`
* `ph`
* `sulphates`
* `alcohol`

The `quality` column was converted to a double and used as the model label.

Spark MLlib's `VectorAssembler` was used to combine the predictor columns into a single feature vector required by the Linear Regression algorithm.

## Data Preparation

Rows containing null values were removed before model training.

The dataset was divided into:

```text
80% training data
20% testing data
```

A random seed of `42` was used to make the train/test split reproducible.

## Model Training

The Linear Regression model was trained using Spark MLlib with the assembled feature vector and the wine quality label.

After training, the model generated predictions for the testing dataset.

## Model Evaluation

Three regression metrics were calculated:

* **RMSE** - Root Mean Squared Error
* **MAE** - Mean Absolute Error
* **R2** - R-squared

The values produced during the final Spark execution were:

```text
RMSE: 0.6846
MAE:  0.5375
R2:   0.4154
```

The RMSE indicates that the model's predictions differed from the actual wine quality score by approximately 0.68 quality points on average when larger errors were given additional weight.

The MAE of approximately 0.54 indicates that the average absolute prediction error was slightly more than half of one quality point.

The R2 value of 0.4154 indicates that the Linear Regression model explained approximately 41.5% of the variation in wine quality within the testing dataset.

## HBase Integration

After model evaluation, Spark connected to the HBase Thrift server using the Python HappyBase library.

The model-performance metrics were written to the HBase table:

```text
wine_quality_metrics
```

using the row key:

```text
linear_regression
```

The following columns were written to the `metrics` column family:

```text
metrics:rmse
metrics:mae
metrics:r2
metrics:model
metrics:timestamp
```

The populated HBase scan after the Spark job verified that the metrics were successfully stored.

## YARN Execution

The Spark application was submitted through YARN using:

```bash
spark-submit --master yarn /root/analysis.py
```

YARN managed the Spark workload while the application read the Hive table, trained the Linear Regression model, evaluated its performance, and wrote the resulting metrics into HBase.

## Supporting Files

The PySpark source code is stored in:

```text
analysis.py
```

Supporting screenshots are stored in the `screenshots` directory:

```text
spark-training-output.png
spark-ml-evaluation.png
spark-submit-output.png
```

The successful Spark execution and subsequent populated HBase scan demonstrate that Spark MLlib, YARN, Hive, HappyBase, and HBase were successfully integrated as part of the complete project pipeline.
