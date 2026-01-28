import sqlite3
import pandas as pd

conn = sqlite3.connect('mumbai_housing.db')

# Find the top 5 cheapest localities by average price_per_sqft
query = """
SELECT locality, AVG(price_per_sqft) as avg_rate
FROM properties
GROUP BY locality
ORDER BY avg_rate ASC
LIMIT 5;
"""

result = pd.read_sql_query(query, conn)
print("🏆 Top 5 Value Localities in Mumbai:")
print(result)

conn.close()
