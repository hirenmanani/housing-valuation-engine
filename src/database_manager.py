# database_manager.py logic
import pandas as pd
import sqlite3  # Built into Python, no admin rights needed!


def load_to_db():
    # 1. Read your transformed data
    df = pd.read_csv('mumbai_transformed_data.csv')

    # 2. Create a local SQLite database
    conn = sqlite3.connect('mumbai_housing.db')
    cursor = conn.cursor()

    # 2.i CREATE THE INDEX
    # This makes searches by locality near-instant
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_locality ON properties(locality);")

    # 3. Load the data into a table
    df.to_sql('properties', conn, if_exists='replace', index=False)

    print("✅ Data successfully loaded into SQL Database!")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    load_to_db()
