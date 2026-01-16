import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mumbai Housing Engine", layout="wide")
st.title("🦁 Mumbai Housing Value Engine")

# Database Connection
conn = sqlite3.connect('mumbai_housing.db')
df = pd.read_sql_query("SELECT * FROM properties", conn)

# 1. Sidebar Filters
st.sidebar.header("Filter Deals")
locs = sorted(df['locality'].unique())
selected_loc = st.sidebar.selectbox("Choose Locality", options=locs)

# 2. Logic: Neighborhood Comparison
# We calculate the neighborhood average to find the "Deals"
avg_price = df[df['locality'] == selected_loc]['price_per_sqft'].mean()
deals_df = df[(df['locality'] == selected_loc) & (
    df['price_per_sqft'] < avg_price * 0.85)]

# 3. Display Metrics
m1, m2 = st.columns(2)
m1.metric(f"Avg Price in {selected_loc}", f"₹{int(avg_price)} /sqft")
m2.metric("Hot Deals Found", len(deals_df))

# 4. Visualizing the Arbitrage
st.subheader(f"🔥 Best Value Properties in {selected_loc}")
st.dataframe(deals_df[['locality', 'sqft', 'price_cr', 'price_per_sqft']])

# 5. Aesthetic Price Distribution
st.subheader(f"📊 Market Temperature: {selected_loc}")

# Create a more refined histogram
fig = px.histogram(
    df[df['locality'] == selected_loc],
    x="price_per_sqft",
    nbins=50,  # More bins = smoother "hill"
    title=f"Price Concentration in {selected_loc}",
    color_discrete_sequence=['#1E88E5'],  # Professional Blue
    marginal="box",  # Adds a box plot on top to see outliers!
    opacity=0.7
)

# Add a vertical line for the average
fig.add_vline(x=avg_price, line_dash="dash", line_color="red",
              annotation_text=f"Average: ₹{int(avg_price)}",
              annotation_position="top right")

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Price per Sqft (INR)",
    yaxis_title="Number of Properties",
    bargap=0.05
)

st.plotly_chart(fig, use_container_width=True)

conn.close()
