import pandas as pd
import random

# Localities in Mumbai
localities = ['Andheri West', 'Bandra East',
              'Worli', 'Powai', 'Borivali West', 'Chembur']

data = []
for i in range(1, 10001):
    loc = random.choice(localities)
    # Price in Crores (1.0 to 10.0)
    price = round(random.uniform(1.2, 8.5), 2)
    # Square footage (500 to 2000)
    sqft = random.randint(600, 1800)

    data.append([i, loc, price, sqft])

df = pd.DataFrame(data, columns=['id', 'locality', 'price_cr', 'sqft'])

# Save to GitHub folder
df.to_csv('mumbai_raw_data.csv', index=False)
print("✅ 10,000 rows of raw data generated!")
