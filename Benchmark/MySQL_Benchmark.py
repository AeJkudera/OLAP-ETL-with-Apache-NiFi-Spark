import subprocess
import mysql.connector
import time

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="mostafa-galal",
    password="fight club",
    database="tpch1g"
)
cursor = conn.cursor()

# Define the SQL query
sql_query = """
SELECT
    n_name,
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
    lineitem,
    orders,
    customer,
    nation,
    supplier
WHERE
    l_shipdate <= DATE '1998-12-01' - INTERVAL 90 DAY
    AND l_orderkey = o_orderkey
    AND o_custkey = c_custkey
    AND c_nationkey = n_nationkey
    AND l_suppkey = s_suppkey
GROUP BY
    n_name,
    s_name;
"""


# Function to execute and time the query
def run_query(label, iterations, clear_cache=False):
    execution_times = []
    for i in range(iterations):
        if clear_cache:
            cursor.execute("FLUSH TABLES;")  # Clear MySQL query cache (MySQL ≤ 5.7)
            subprocess.run("sync; echo 3 | sudo tee /proc/sys/vm/drop_caches", shell=True)  # Linux: Clear OS disk cache

        start_time = time.time()
        cursor.execute(sql_query)
        cursor.fetchall()
        end_time = time.time()

        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        execution_times.append(execution_time)

    return execution_times


### **Cold Runs (8 Iterations - No Cache)** ###
print("Running COLD RUNS (Clearing Cache before each run)...")
cold_times = run_query("Cold Run", 8, clear_cache=True)

### **Warm Runs (8 Iterations - Cached Data)** ###
print("\nRunning WARM RUNS (Using Cached Data)...")
warm_times = run_query("Warm Run", 8, clear_cache=False)

# Print results in the required format
print("\nCold Run Execution Times:", cold_times)
print(f"Average Execution Time (Cold Run - No Cache): {sum(cold_times) / 8:.2f} ms")

print("\nWarm Run Execution Times:", warm_times)
print(f"Average Execution Time (Warm Run - Cached Data): {sum(warm_times) / 8:.2f} ms")

# Close connection
cursor.close()
conn.close()