# database_manager.py logic
import pandas as pd
import sqlite3  # Built into Python, no admin rights needed!


def load_to_db():
    # 1. Read your transformed data
    df = pd.read_csv('mumbai_transformed_data.csv')

    # 2. Create a local SQLite database (doesn't need admin rights)
    conn = sqlite3.connect('mumbai_housing.db')

    # 3. Load the data into a table
    df.to_sql('properties', conn, if_exists='replace', index=False)

    print("✅ Data successfully loaded into SQL Database!")
    conn.close()


if __name__ == "__main__":
    load_to_db()
