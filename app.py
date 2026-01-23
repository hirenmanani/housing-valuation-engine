import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import joblib
import os

# 1. Configuration & Path Management
# Relative paths for the new Lead-Engineer folder structure
DB_PATH = 'database/mumbai_housing.db'
MODEL_PATH = 'models/mumbai_price_model.pkl'
COLUMNS_PATH = 'models/model_columns.pkl'

st.set_page_config(page_title="Mumbai Housing Engine", layout="wide")

# 2. Connection & Transformation Logic

@st.cache_data  # Senior Move: Cache data to improve dashboard speed
def get_processed_data():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        # We calculate price_per_sqft on the fly in SQL
        query = """
        SELECT *, (price_cr * 10000000 / sqft) as price_per_sqft 
        FROM properties
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    return pd.DataFrame()


df = get_processed_data()

st.title("🦁 Mumbai Housing Valuation Engine")

# 3. The Predictor UI (Phase 4 Logic)
st.sidebar.header("🔮 Price Predictor")
if os.path.exists(MODEL_PATH) and os.path.exists(COLUMNS_PATH):
    model = joblib.load(MODEL_PATH)
    model_cols = joblib.load(COLUMNS_PATH)

    u_sqft = st.sidebar.number_input("Square Footage", 500, 5000, 1000)
    u_bhk = st.sidebar.slider("BHK", 1, 5, 2)
    u_loc = st.sidebar.selectbox("Select Neighborhood", [
                                 'Worli', 'Andheri West', 'Bandra East', 'Chembur', 'Powai'])

    if st.sidebar.button("Predict Fair Market Value"):
        input_data = pd.DataFrame(0, index=[0], columns=model_cols)
        input_data['sqft'] = u_sqft
        input_data['bhk'] = u_bhk
        loc_col = f'locality_{u_loc}'
        if loc_col in input_data.columns:
            input_data[loc_col] = 1

        prediction = model.predict(input_data)[0]
        st.sidebar.success(f"Estimated Value: ₹{prediction:.2f} Cr")
else:
    st.sidebar.warning("ML Models not found in /models folder.")

# 4. Analytics & Visualizations
if not df.empty:
    # Neighborhood Filter for the Charts
    localities = df['locality'].unique()
    selected_loc = st.selectbox("Analyze Market Trends for:", localities)

    # Filter data for charts
    filtered_df = df[df['locality'] == selected_loc]
    avg_price = filtered_df['price_per_sqft'].mean()

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Rate", f"₹{int(avg_price)} /sqft")
    col2.metric("Property Count", len(filtered_df))
    col3.metric("Max Price", f"₹{filtered_df['price_cr'].max()} Cr")

    # 5. Aesthetic Market Temperature Chart
    st.subheader(f"📊 Price Distribution: {selected_loc}")

    fig = px.histogram(
        filtered_df,
        x="price_per_sqft",
        nbins=30,
        marginal="box",
        title=f"Price Concentration in {selected_loc}",
        color_discrete_sequence=['#1E88E5'],
        opacity=0.75
    )

    fig.add_vline(x=avg_price, line_dash="dash", line_color="#D32F2F",
                  annotation_text=f"Mean: ₹{int(avg_price)}",
                  annotation_position="top right")

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Price per Sqft (INR)",
        yaxis_title="Frequency"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Database not found. Please run src/data_generator.py first.")
