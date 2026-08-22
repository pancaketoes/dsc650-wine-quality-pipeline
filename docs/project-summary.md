# DSC 650 Big Data Final Project Summary

## Project Overview

This project implemented an end-to-end big data pipeline using Apache NiFi, HDFS, Hive, Spark MLlib, YARN, HBase, and Python. The goal was to demonstrate how these technologies can be integrated to ingest, store, query, analyze, and persist machine-learning results within a distributed data environment.

The project used a cleaned version of the Red Wine Quality dataset. The dataset contains chemical measurements for red wine samples and a numeric wine quality score.

The complete pipeline was:

```text
GitHub Dataset
      ↓
Apache NiFi
      ↓
HDFS
      ↓
Hive Managed Table
      ↓
Spark MLlib
      ↓
YARN
      ↓
HBase
```

Spark generated machine-learning performance metrics, which were written to HBase through the HBase Thrift server using the HappyBase Python library.

## Dataset

The project dataset is stored in the GitHub repository at:

```text
data/winequality_red_clean.csv
```

The direct raw GitHub URL used by NiFi was:

```text
https://raw.githubusercontent.com/pancaketoes/dsc650-wine-quality-pipeline/main/data/winequality_red_clean.csv
```

The dataset contains 1,599 wine samples with 11 chemical predictor variables and one target variable, `quality`.

The predictor variables include acidity measurements, residual sugar, chlorides, sulfur dioxide measurements, density, pH, sulphates, and alcohol content.

## NiFi Data Ingestion

Apache NiFi was used to retrieve the dataset from GitHub and write it into HDFS.

The NiFi flow used three processors:

1. `InvokeHTTP` to download the CSV file from GitHub.
2. `UpdateAttribute` to set the correct filename.
3. `PutHDFS` to write the file into HDFS.

The HDFS destination directory was:

```text
/tmp/wine_quality
```

Successful ingestion was verified using:

```bash
hdfs dfs -ls /tmp/wine_quality
```

The output confirmed that `winequality_red_clean.csv` had been written successfully.

## Hive Managed Table

A managed Hive table named `wine_quality` was created to provide a structured SQL representation of the CSV dataset.

The numeric measurement columns were stored primarily as `DOUBLE`, while the `quality` target was stored as an `INT`.

The data was loaded from HDFS into Hive using:

```sql
LOAD DATA INPATH '/tmp/wine_quality/winequality_red_clean.csv'
INTO TABLE wine_quality;
```

The dataset was verified using sample queries and an aggregation query that counted the number of wines associated with each quality score.

The aggregation demonstrated that the data had been correctly loaded and parsed into the Hive schema.

## Environment Setup

The Python packages required for the Spark-to-HBase integration were installed on the master and worker nodes.

The primary packages included:

```text
numpy
happybase
```

HappyBase was required so the Python Spark application could communicate with HBase through the HBase Thrift API.

The HBase Thrift server was started on the master node and verified before running the Spark application.

## HBase Table Design

An HBase table named `wine_quality_metrics` was created to store the machine-learning evaluation results.

The table used the column family:

```text
metrics
```

The table was scanned before the Spark application executed to confirm that it initially contained zero rows.

The Spark application later used the row key:

```text
linear_regression
```

to store the model results.

## Spark MLlib Workflow

Spark read the dataset directly from the Hive managed table:

```text
default.wine_quality
```

The 11 chemical measurement columns were combined into a feature vector using Spark MLlib's `VectorAssembler`.

The target variable was the numeric `quality` score.

The data was divided into:

```text
80% training data
20% testing data
```

A random seed of `42` was used to make the split reproducible.

A Spark MLlib Linear Regression model was trained to predict wine quality from the chemical measurements.

## Model Evaluation

The completed Linear Regression model produced the following results:

```text
RMSE: 0.6846
MAE:  0.5375
R2:   0.4154
```

The RMSE indicates that the model's predictions differed from the actual wine quality score by approximately 0.68 points when larger prediction errors were weighted more heavily.

The MAE indicates an average absolute prediction error of approximately 0.54 quality points.

The R2 score indicates that approximately 41.5% of the variation in wine quality in the testing data was explained by the Linear Regression model.

These results demonstrate that the chemical measurements contain useful predictive information, although a substantial amount of wine-quality variation remains unexplained by the linear model.

## YARN Execution

The Spark ML application was submitted to the YARN cluster using:

```bash
spark-submit --master yarn /root/analysis.py
```

YARN managed the Spark workload and successfully completed the training and evaluation process.

The Spark execution produced model predictions and evaluation metrics before writing the metrics to HBase.

## HBase Results

After model evaluation, the Spark application connected to the HBase Thrift server using HappyBase.

The following values were written to the `metrics` column family:

```text
metrics:rmse
metrics:mae
metrics:r2
metrics:model
metrics:timestamp
```

A final HBase scan showed the populated `linear_regression` row and verified that the model-performance metrics had been successfully written.

This confirmed that the complete pipeline operated successfully from the original GitHub dataset through the final HBase storage layer.

## Challenges Encountered

Several technical issues occurred during implementation.

One challenge involved identifying the correct Docker container names. The environment used generated container names such as:

```text
hadoop-hive-spark-hbase-master-1
hadoop-hive-spark-hbase-worker1-1
hadoop-hive-spark-hbase-worker2-1
```

rather than shorter names such as `master` or `namenode`. Running `docker ps` was used to identify the correct containers.

Another issue occurred when HappyBase initially returned a connection-refused error on port `9090`. This indicated that the HBase Thrift server was not available at that time. Restarting and verifying the Thrift server resolved the connectivity issue before the Spark application was executed.

The NiFi workflow also required careful control of processor execution so duplicate copies of the dataset were not unintentionally processed.

These challenges emphasized the importance of verifying each service and pipeline stage before moving to the next component.

## Lessons Learned

This project demonstrated how individual big data technologies perform specialized roles within a larger pipeline.

NiFi provides ingestion and flow management, HDFS provides distributed storage, Hive provides structured SQL access, Spark performs distributed processing and machine learning, YARN manages distributed workloads, and HBase provides persistent low-latency storage for generated results.

The project also demonstrated the importance of validating each stage independently. Checking HDFS before moving to Hive, verifying the Hive table before running Spark, and testing the HBase Thrift connection before executing the ML application made troubleshooting easier.

## Production Considerations

A production implementation would require several improvements beyond this academic environment.

Services would run across larger clusters with greater memory and CPU resources rather than sharing a resource-constrained instructional virtual machine.

Security controls such as authentication, encrypted network communication, secrets management, and role-based permissions would also be required.

The data pipeline could be automated so new datasets were ingested and processed without manually starting each stage.

Additional machine-learning algorithms could also be compared with Linear Regression, including Random Forest Regression or Gradient-Boosted Trees, to determine whether nonlinear relationships improve wine-quality prediction.

Model tracking, monitoring, scheduled retraining, and additional validation data would also be useful in a production machine-learning system.

## Conclusion

The project successfully implemented a complete big data and machine-learning pipeline using the primary technologies covered in DSC 650.

The workflow successfully:

* Ingested a GitHub-hosted dataset using NiFi.
* Stored the dataset in HDFS.
* Created and populated a Hive managed table.
* Read Hive data using Spark.
* Trained and evaluated a Spark MLlib Linear Regression model.
* Submitted the Spark application through YARN.
* Connected Spark to HBase using HappyBase and the HBase Thrift server.
* Stored and verified machine-learning metrics in HBase.

The completed project demonstrates successful integration of NiFi, HDFS, Hive, Spark MLlib, YARN, and HBase in a single end-to-end data pipeline.
