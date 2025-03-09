from pyspark.sql import SparkSession
import time

# Initialize Spark session
spark = SparkSession.builder.appName("MyApp").config("spark.executor.memory", "4g").config("spark.memory.fraction", "1.0") \
    .config("spark.storage.memoryFraction", "0.8").getOrCreate()

# Disable vectorized Parquet reader for fair comparison
spark.conf.set("spark.sql.parquet.enableVectorizedReader", "false")

# Load Parquet files
customerDF = spark.read.parquet("../../Downloads/nifi-2.2.0/parquets/DIM_CUSTOMER")
supplierDF = spark.read.parquet("../../Downloads/nifi-2.2.0/parquets/DIM_SUPPLIER")
lineorderDF = spark.read.parquet("../../Downloads/nifi-2.2.0/parquets/FCT_LINEORDER")

# Register DataFrames as temporary views
customerDF.createOrReplaceTempView("customer")
supplierDF.createOrReplaceTempView("supplier")
lineorderDF.createOrReplaceTempView("lineorder")

# SQL Query
query = """
  SELECT
    c.n_name,
    s_name,
    SUM(l_quantity) AS sum_qty,
    SUM(l_extendedprice) AS sum_base_price,
    SUM(l_extendedprice * (1 - l_discount)) AS sum_disc_price,
    SUM(l_extendedprice * (1 - l_discount) * (1 + l_tax)) AS sum_charge,
    AVG(l_quantity) AS avg_qty,
    AVG(l_extendedprice) AS avg_price,
    AVG(l_discount) AS avg_disc,
    COUNT(*) AS count_order
  FROM
    lineorder l,
    customer c,
    supplier s
  WHERE
    l.l_shipdate <= date '1998-12-01' - interval '90' day AND
    l.o_custkey = c.c_custkey AND
    l.l_suppkey = s.s_suppkey
  GROUP BY
    c.n_name,
    s_name
"""


# Function to measure execution time
def measure_execution_time(num_runs, use_cache=False):
    execution_times = []

    # Cache tables if required
    if use_cache:
        spark.sql("CACHE TABLE customer")
        spark.sql("CACHE TABLE supplier")
        spark.sql("CACHE TABLE lineorder")

    for _ in range(num_runs):
        start_time = time.time()
        spark.sql(query).show()
        end_time = time.time()

        execution_times.append((end_time - start_time) * 1000)  # Convert to milliseconds

    # Compute average execution time
    avg_time = sum(execution_times) / num_runs
    return avg_time, execution_times


# Number of repetitions
num_runs = 8

# Cold Run (No Cache)
cold_avg_time, cold_times = measure_execution_time(num_runs, use_cache=False)
print(f"Cold Run Execution Times: {cold_times}")
print(f"Average Execution Time (Cold Run - No Cache): {cold_avg_time:.2f} ms")

# Warm Run (With Cache)
warm_avg_time, warm_times = measure_execution_time(num_runs, use_cache=True)
print(f"Warm Run Execution Times: {warm_times}")
print(f"Average Execution Time (Warm Run - With Cache): {warm_avg_time:.2f} ms")

# Uncache tables to free memory
spark.sql("UNCACHE TABLE customer")
spark.sql("UNCACHE TABLE supplier")
spark.sql("UNCACHE TABLE lineorder")
