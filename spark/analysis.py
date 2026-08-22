from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
import happybase
from datetime import datetime

# ---------------------------------------------------------
# Create Spark session with Hive support
# ---------------------------------------------------------
spark = (
    SparkSession.builder
    .appName("WineQualityLinearRegression")
    .enableHiveSupport()
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("\n=== DSC650 Wine Quality ML Project ===")

# ---------------------------------------------------------
# Read data from Hive
# ---------------------------------------------------------
df = spark.table("default.wine_quality")

print("\nHive table loaded successfully.")
print(f"Total rows: {df.count()}")

df.printSchema()

# Remove rows containing null values
df = df.na.drop()

# Convert quality to double for MLlib
df = df.withColumn("label", col("quality").cast("double"))

# ---------------------------------------------------------
# Feature columns
# ---------------------------------------------------------
feature_columns = [
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
    "alcohol"
]

assembler = VectorAssembler(
    inputCols=feature_columns,
    outputCol="features"
)

ml_data = assembler.transform(df).select("features", "label")

# ---------------------------------------------------------
# Train/test split
# ---------------------------------------------------------
train_data, test_data = ml_data.randomSplit(
    [0.8, 0.2],
    seed=42
)

print(f"\nTraining rows: {train_data.count()}")
print(f"Testing rows: {test_data.count()}")

# ---------------------------------------------------------
# Linear Regression model
# ---------------------------------------------------------
lr = LinearRegression(
    featuresCol="features",
    labelCol="label",
    maxIter=100
)

model = lr.fit(train_data)

print("\nModel training completed successfully.")

# ---------------------------------------------------------
# Predictions
# ---------------------------------------------------------
predictions = model.transform(test_data)

print("\nSample predictions:")
predictions.select("label", "prediction").show(10)

# ---------------------------------------------------------
# Evaluation
# ---------------------------------------------------------
rmse_evaluator = RegressionEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="rmse"
)

mae_evaluator = RegressionEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="mae"
)

r2_evaluator = RegressionEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="r2"
)

rmse = rmse_evaluator.evaluate(predictions)
mae = mae_evaluator.evaluate(predictions)
r2 = r2_evaluator.evaluate(predictions)

print("\n=== MODEL EVALUATION ===")
print(f"RMSE: {rmse:.4f}")
print(f"MAE:  {mae:.4f}")
print(f"R2:   {r2:.4f}")

# ---------------------------------------------------------
# Write metrics to HBase using HappyBase
# ---------------------------------------------------------
print("\nConnecting to HBase Thrift server...")

connection = happybase.Connection(
    host="localhost",
    port=9090
)

connection.open()

table = connection.table("wine_quality_metrics")

row_key = b"linear_regression"

table.put(
    row_key,
    {
        b"metrics:rmse": str(rmse).encode("utf-8"),
        b"metrics:mae": str(mae).encode("utf-8"),
        b"metrics:r2": str(r2).encode("utf-8"),
        b"metrics:model": b"LinearRegression",
        b"metrics:timestamp": datetime.now().isoformat().encode("utf-8")
    }
)

connection.close()

print("\nModel metrics successfully written to HBase.")
print("=== PROJECT COMPLETE ===\n")

spark.stop()