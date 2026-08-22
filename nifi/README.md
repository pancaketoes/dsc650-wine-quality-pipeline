# NiFi Data Ingestion

## Overview

Apache NiFi was used as the ingestion layer for the project. The source dataset was the cleaned Red Wine Quality dataset stored in the project GitHub repository as a CSV file.

The direct GitHub dataset URL used by NiFi was:

```text
https://raw.githubusercontent.com/pancaketoes/dsc650-wine-quality-pipeline/main/data/winequality_red_clean.csv
```

The NiFi flow downloaded the dataset from GitHub and wrote it into the Hadoop Distributed File System (HDFS).

## NiFi Flow

The flow contained three processors:

1. **Download File (InvokeHTTP)**  
   Downloads the CSV dataset from the raw GitHub URL.

2. **Update File Name (UpdateAttribute)**  
   Sets the FlowFile filename to `winequality_red_clean.csv`.

3. **Write File to HDFS (PutHDFS)**  
   Writes the completed FlowFile into the HDFS directory `/tmp/wine_quality`.

The resulting ingestion flow was:

```text
GitHub CSV
    ↓
InvokeHTTP
    ↓
UpdateAttribute
    ↓
PutHDFS
    ↓
HDFS
```

## Parameters

The NiFi process group used the following parameter values:

```text
DOWNLOAD FILE URL:
https://raw.githubusercontent.com/pancaketoes/dsc650-wine-quality-pipeline/main/data/winequality_red_clean.csv

FILENAME:
winequality_red_clean.csv

HDFS WRITE DIRECTORY:
/tmp/wine_quality

USER:
tyler
```

## HDFS Verification

After the NiFi flow completed, the dataset was verified in HDFS using:

```bash
hdfs dfs -ls /tmp/wine_quality
```

The command confirmed that the following file had been successfully written:

```text
/tmp/wine_quality/winequality_red_clean.csv
```

This verified that NiFi successfully ingested the project dataset from GitHub and transferred it into HDFS.

## Supporting Files

The exported NiFi flow is stored in:

```text
flow-definition.json
```

Supporting screenshots are stored in the `screenshots` directory:

```text
nifi-flow.png
nifi-running.png
hdfs-ingestion-verification.png
```