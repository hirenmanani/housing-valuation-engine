import sqlite3
import pandas as pd
import random


def generate_pro_data():
    localities = ['Worli', 'Andheri West', 'Bandra East', 'Chembur', 'Powai']
    # Professional pricing logic: Rate per sqft + BHK premium
    rates = {
        'Worli': 45000,
        'Andheri West': 28000,
        'Bandra East': 35000,
        'Chembur': 22000,
        'Powai': 25000
    }

    data = []
    for _ in range(10000):
        loc = random.choice(localities)
        sqft = random.randint(500, 3000)
        bhk = random.randint(1, 5)

        # Logic: Price = (Base Rate * Sqft) + (BHK Value) + Random Noise
        # Converting to Crores
        base_price = (sqft * rates[loc])
        bhk_premium = (bhk * 2500000)  # 25 Lakhs per extra room
        price_cr = round((base_price + bhk_premium) / 10000000, 2)

        data.append([loc, sqft, bhk, price_cr])

    df = pd.DataFrame(data, columns=['locality', 'sqft', 'bhk', 'price_cr'])

    conn = sqlite3.connect('mumbai_housing.db')
    # Use if_exists='replace' to fix your schema error!
    df.to_sql('properties', conn, if_exists='replace', index=False)
    conn.close()
    print("✅ Database upgraded to PRO SCHEMA (Locality, Sqft, BHK).")


generate_pro_data()
