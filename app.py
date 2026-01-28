import streamlit as st
import pandas as pd
import sqlalchemy
import plotly.express as px
import joblib
import os

# 1. Configuration & Path Management
DB_URL = "postgresql://admin:mumbai_password@db:5432/mumbai_housing"
MODEL_PATH = 'models/mumbai_price_model.pkl'
COLUMNS_PATH = 'models/model_columns.pkl'

st.set_page_config(page_title="Mumbai Housing Engine", layout="wide")

# 2. Connection Pooling


@st.cache_resource
def get_db_engine():
    return sqlalchemy.create_engine(DB_URL)


@st.cache_data
def get_processed_data():
    try:
        engine = get_db_engine()
        # Removed BHK from query - pulling from the successful enriched table
        query = "SELECT * FROM enriched_properties"
        df = pd.read_sql_query(query, engine)
        if not df.empty:
            df['price_per_sqft'] = df['current_rate']
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()


def get_market_steals(threshold_pct=10):
    try:
        engine = get_db_engine()
        threshold_val = (100 - threshold_pct) / 100

        # REMOVED BHK - Only selecting existing columns
        query = f"""
        SELECT locality, sqft, price_cr, current_rate, avg_locality_rate, luxury_index,
               ROUND(((1 - luxury_index) * 100)::numeric, 2) as discount_pct
        FROM enriched_properties
        WHERE luxury_index < {threshold_val}
        ORDER BY luxury_index ASC LIMIT 5;
        """
        return pd.read_sql_query(query, engine)
    except Exception as e:
        st.sidebar.error(f"Query Error: {e}")
        return pd.DataFrame()


# 3. Sidebar Navigation
st.sidebar.title("🦁 MHVE Control Center")
page = st.sidebar.radio(
    "Go to:", ["📈 Market Analytics", "🔮 Price Predictor", "🔥 Best Deals"])

# Load data from Postgres
df = get_processed_data()

# --- PAGE 1: MARKET ANALYTICS ---
if page == "📈 Market Analytics":
    st.title("📈 Mumbai Real Estate Intelligence")

    if not df.empty:
        localities = df['locality'].unique()
        selected_loc = st.selectbox("Select Neighborhood:", localities)

        filtered_df = df[df['locality'] == selected_loc]
        avg_price = filtered_df['price_per_sqft'].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Rate", f"₹{int(avg_price)} /sqft")
        col2.metric("Listings", len(filtered_df))
        col3.metric("Max Price", f"₹{filtered_df['price_cr'].max()} Cr")

        st.subheader(f"Price Distribution: {selected_loc}")
        fig = px.histogram(filtered_df, x="price_per_sqft", nbins=30, marginal="box",
                           color_discrete_sequence=['#1E88E5'], opacity=0.75)
        fig.add_vline(x=avg_price, line_dash="dash", line_color="#D32F2F")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No data found. Check your Postgres connection.")

# --- PAGE 2: PRICE PREDICTOR ---
elif page == "🔮 Price Predictor":
    st.title("🔮 AI-Powered Valuation Tool")

    if os.path.exists(MODEL_PATH) and os.path.exists(COLUMNS_PATH):
        model = joblib.load(MODEL_PATH)
        model_cols = joblib.load(COLUMNS_PATH)

        col_a, col_b = st.columns(2)
        with col_a:
            u_sqft = st.number_input(
                "Square Footage", 500, 10000, 1000, step=50)
            # Note: We keep the slider for prediction, but don't use it in DB queries
            u_bhk = st.slider("BHK (For Prediction Model)", 1, 10, 2)
        with col_b:
            u_loc = st.selectbox(
                "Neighborhood", ['Worli', 'Andheri West', 'Bandra East', 'Chembur', 'Powai'])

        if st.button("Calculate Fair Value", use_container_width=True):
            input_data = pd.DataFrame(0, index=[0], columns=model_cols)
            input_data['sqft'] = u_sqft
            # If your model specifically needs BHK, it uses the slider input here
            if 'bhk' in input_data.columns:
                input_data['bhk'] = u_bhk

            loc_col = f'locality_{u_loc}'
            if loc_col in input_data.columns:
                input_data[loc_col] = 1

            prediction = model.predict(input_data)[0]
            st.balloons()
            st.success(f"### Estimated Market Price: ₹{prediction:.2f} Cr")
    else:
        st.warning("ML Models not found in /models folder.")

# --- PAGE 3: BEST DEALS ---
elif page == "🔥 Best Deals":
    st.title("🔥 Market Arbitrage Opportunities")
    threshold = st.slider("Select Discount Threshold (%)", 1, 20, 10)

    steals = get_market_steals(threshold_pct=threshold)

    if not steals.empty:
        for _, row in steals.iterrows():
            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.subheader(f"📍 {row['locality']}")
                c2.metric(
                    "Price", f"₹{row['price_cr']:.2f} Cr", f"-{row['discount_pct']}%")
                # Removed BHK reference - focusing on SQFT
                c3.write(f"**{int(row['sqft'])} sqft**")
                st.caption(
                    f"Neighborhood Avg: ₹{int(row['avg_locality_rate'])}/sqft")
    else:
        st.info(f"No properties found at a {threshold}% discount.")
