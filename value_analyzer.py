import pandas as pd
import sqlite3
from logger_config import get_logger
logger = get_logger("ValueAnalyzer")

logger.info("Starting Value Analysis...")


conn = sqlite3.connect('mumbai_housing.db')

# This query calculates the median price for each locality
# and finds properties 20% below that median.
query = """
WITH LocalityMedians AS (
    SELECT 
        locality,
        AVG(price_per_sqft) as locality_avg_rate
    FROM properties
    GROUP BY locality
)
SELECT DISTINCT 
    p.locality, p.sqft, p.price_cr, p.price_per_sqft, lm.locality_avg_rate
FROM properties p
JOIN LocalityMedians lm ON p.locality = lm.locality
WHERE p.price_per_sqft < (lm.locality_avg_rate * 0.7) -- Finding the 30% discount "Steals"
ORDER BY p.price_per_sqft ASC
LIMIT 10;
"""

deals = pd.read_sql_query(query, conn)
print("🎯 TOP 10 UNDERVALUED DEALS (20% below Neighborhood Average):")
print(deals[['locality', 'sqft', 'price_cr',
      'price_per_sqft', 'locality_avg_rate']])

conn.close()

logger.info("Successfully found undervalued properties.")
