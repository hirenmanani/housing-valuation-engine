import pandas as pd

# 1. Load the data you generated earlier
df = pd.read_csv('mumbai_raw_data.csv', on_bad_lines='skip')

# 2. Add the 'Price per SqFt' column (Crucial for Data Engineering)
# Formula: (Price in Cr * 10,000,000) / SqFt
df['price_per_sqft'] = (df['price_cr'] * 10000000) / df['sqft']

# 3. Filter: Let's find the "Gains" (Properties under 25,000 per sqft)
affordable_df = df[df['price_per_sqft'] < 25000]

# 4. Sort by the best value
best_deals = affordable_df.sort_values(by='price_per_sqft')

# 5. Save the "Clean" data for SQL tomorrow
best_deals.to_csv('mumbai_transformed_data.csv', index=False)

print(f"✅ Transformation Complete!")
print(f"Found {len(best_deals)} potential 'Value' properties.")
