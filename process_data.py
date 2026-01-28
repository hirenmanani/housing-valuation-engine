from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

# 1. Initialize Spark
spark = SparkSession.builder \
    .appName("MumbaiHousingEnrichment") \
    .config("spark.jars", "/app/jars/postgresql-42.7.1.jar") \
    .getOrCreate()

# 2. Load Raw Data (With explicit Schema Refresh)
db_url = "jdbc:postgresql://db:5432/mumbai_housing"

# Force Spark to forget old metadata
spark.catalog.clearCache()

properties_df = spark.read \
    .format("jdbc") \
    .option("url", db_url) \
    .option("dbtable", "properties") \
    .option("user", "admin") \
    .option("password", "mumbai_password") \
    .option("driver", "org.postgresql.Driver") \
    .load()

# DEBUG: Add this line to see what Spark REALLY sees before the join
print("Columns found in source:", properties_df.columns)

# 3. Calculate Locality Averages
locality_avgs = properties_df.groupBy("locality").agg(
    avg(col("price_cr") * 10000000 / col("sqft")).alias("avg_locality_rate")
)

# 4. Join & Calculate Luxury Index (Explicit Attribute Preservation)
# Using aliases 'p' and 'avg' makes the join cleaner
enriched_df = properties_df.alias("p").join(
    locality_avgs.alias("avg"),
    "locality"
).select(
    "p.*",  # This explicitly pulls bhk, id, sqft, and everything else from raw data
    "avg.avg_locality_rate"
).withColumn(
    "current_rate", (col("price_cr") * 10000000 / col("sqft"))
).withColumn(
    "luxury_index", col("current_rate") / col("avg_locality_rate")
)

# 5. Write to Postgres
enriched_df.write \
    .format("jdbc") \
    .option("url", db_url) \
    .option("dbtable", "enriched_final") \
    .option("user", "admin") \
    .option("password", "mumbai_password") \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()

print("✅ Data Enrichment Complete: 'enriched_properties' now includes ALL columns (including bhk)!")
spark.stop()
