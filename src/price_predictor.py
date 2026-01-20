import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# 1. Load the NEW columns (including BHK)
conn = sqlite3.connect('database/mumbai_housing.db')
df = pd.read_sql_query(
    "SELECT sqft, bhk, locality, price_cr FROM properties", conn)
conn.close()

# 2. One-Hot Encode (Convert text neighborhoods to numbers)
df_encoded = pd.get_dummies(df, columns=['locality'])

# 3. Features (X) and Target (y)
X = df_encoded.drop('price_cr', axis=1)
y = df_encoded['price_cr']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 4. Train the "Lion's Brain"
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Save Model AND Columns (Needed for Streamlit later)
joblib.dump(model, 'models/mumbai_price_model.pkl')
joblib.dump(X.columns.tolist(), 'models/model_columns.pkl')

print(f"📈 NEW Accuracy Score (R²): {model.score(X_test, y_test):.4f}")
