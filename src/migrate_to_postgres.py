import pandas as pd
from sqlalchemy import create_engine, text
import os

# 1. Source: The CSV file (The verified "Bricks")
CSV_PATH = "/app/mumbai_transformed_data.csv"

if not os.path.exists(CSV_PATH):
    print(f"❌ Error: {CSV_PATH} not found!")
    exit()

print(f"📂 Reading data from {CSV_PATH}...")
# Load the CSV into a Pandas DataFrame
df = pd.read_csv(CSV_PATH)

# 2. Destination: The Postgres Container
POSTGRES_URL = 'postgresql://admin:mumbai_password@db:5432/mumbai_housing'
engine = create_engine(POSTGRES_URL)

# 3. The Move
try:
    print("🚀 Connecting to Postgres Fortress...")
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    print(f"📦 Migrating {len(df)} rows to PostgreSQL table 'properties'...")
    # This will CREATE the table 'properties' for you automatically
    df.to_sql('properties', engine, if_exists='replace', index=False)
    print("✅ Success! Data is now in Production-grade PostgreSQL.")

except Exception as e:
    print(f"❌ Migration Failed: {e}")
