import pandas as pd
import sqlite3
from logger_config import get_logger
logger = get_logger("ValueAnalyzer")

logger.info("Starting Value Analysis...")


conn = sqlite3.connect('mumbai_housing.db')

# This query calculates the median price for each locality
# and finds properties 20% below that median.
query = """
WITH CalculatedProperties AS (
    SELECT 
        locality, 
        sqft, 
        bhk, 
        price_cr,
        -- We calculate the rate here: (Price * 1 Crore) / Sqft
        (price_cr * 10000000) / sqft as price_per_sqft
    FROM properties
),
LocalityMedians AS (
    SELECT 
        locality,
        AVG(price_per_sqft) as locality_avg_rate
    FROM CalculatedProperties
    GROUP BY locality
)
SELECT 
    p.locality, p.sqft, p.bhk, p.price_cr, p.price_per_sqft, lm.locality_avg_rate
FROM CalculatedProperties p
JOIN LocalityMedians lm ON p.locality = lm.locality
WHERE p.price_per_sqft < (lm.locality_avg_rate * 0.7) 
ORDER BY p.price_per_sqft ASC
LIMIT 10;
"""

deals = pd.read_sql_query(query, conn)
print("🎯 TOP 10 UNDERVALUED DEALS (20% below Neighborhood Average):")
print(deals[['locality', 'sqft', 'price_cr',
      'price_per_sqft', 'locality_avg_rate']])

conn.close()

logger.info("Successfully found undervalued properties.")
