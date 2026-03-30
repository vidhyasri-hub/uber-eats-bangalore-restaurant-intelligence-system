import streamlit as st # type: ignore
import pandas as pd # type: ignore
import sqlite3

#st.title("Order Data Integration & Custom Analytical Q&A")
st.markdown(
    """
    <h2 style='font-size:20px; text-align: center; font-family:Arial, sans-serif; color: #291fb4;'>
        Order Data Integration & Custom Analytical Q&A
    </h2>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <h3 style='font-size:16px; text-align: justify; font-family:Open Sans, sans-serif; font-weight: normal; color: #00008884;'>
        Hey There! Let's explore some order-related analysis with the help of our order data depicting consistency and efficiency of the restaurant partners on Uber Eats.
    </h3>
    """,
    unsafe_allow_html=True
)
#import json
    
dataset = pd.read_json("data/orders.json")
#display(dataset)

# Database creation using SQLite
conn = sqlite3.connect('database/my_database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS uber_eats_order_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id VARCHAR(255),
    restaurant_name VARCHAR(50),
    order_date DATE,
    order_value FLOAT,
    discount_used	VARCHAR(5),
    payment_method VARCHAR(15)
)''')     

cursor.execute("SELECT sql FROM sqlite_master WHERE name='uber_eats_order_data'")

for i, row in dataset.iterrows():
    sql = "INSERT INTO uber_eats_order_data (order_id, restaurant_name, order_date, order_value, discount_used, payment_method) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, (row['order_id'], row['restaurant_name'], row['order_date'], row['order_value'], row['discount_used'], row['payment_method']))

conn.commit()
print("Data successfully loaded to SQLite!")


df_check = pd.read_sql_query("SELECT * FROM uber_eats_order_data", conn)
print("print--->",df_check)


def run_sql(query, params=()):
        with sqlite3.connect('database/my_database.db') as conn:
            return pd.read_sql_query(query, conn, params=params)
   
st.write("1. Top Revenue-Generating Restaurants")
query = "SELECT restaurant_name,COUNT(order_id) AS total_orders, ROUND(SUM(order_value), 2) AS total_revenue, ROUND(AVG(order_value), 2) AS avg_order_value FROM uber_eats_order_data GROUP BY restaurant_name ORDER BY total_revenue DESC LIMIT 10";
params = []
results = run_sql(query, params)
st.dataframe(results, use_container_width=True, hide_index=True)

st.write("2. Impact of Discounts on Sales")
query = "SELECT discount_used,COUNT(order_id) AS total_orders, ROUND(SUM(order_value), 2) AS total_sales, ROUND(AVG(order_value), 2) AS avg_order_value FROM uber_eats_order_data GROUP BY discount_used LIMIT 10";
results = run_sql(query, params)
st.dataframe(results, use_container_width=True, hide_index=True)

st.write("3. Preferred Payment Methods")
query = "SELECT payment_method,COUNT(order_id) AS total_orders, ROUND(SUM(order_value), 2) AS total_revenue, ROUND(AVG(order_value), 2) AS avg_order_value FROM uber_eats_order_data GROUP BY payment_method ORDER BY total_orders DESC LIMIT 10";
results = run_sql(query, params)
st.dataframe(results, use_container_width=True, hide_index=True)

st.write("4. Monthly Sales Trends")
query = "SELECT strftime('%Y-%m', order_date) AS month, COUNT(order_id) AS total_orders, ROUND(SUM(order_value), 2) AS total_revenue,  ROUND(AVG(order_value), 2) AS avg_order_value FROM uber_eats_order_data GROUP BY month ORDER BY month DESC LIMIT 12";
results = run_sql(query, params)
st.dataframe(results, use_container_width=True, hide_index=True)

st.write("5. Customer Retention Analysis")
query = "SELECT restaurant_name, COUNT(DISTINCT order_id) AS unique_customers, COUNT(order_id) AS total_orders, ROUND(SUM(order_value), 2) AS total_revenue FROM uber_eats_order_data GROUP BY restaurant_name ORDER BY unique_customers DESC LIMIT 10";
results = run_sql(query, params)
st.dataframe(results, use_container_width=True, hide_index=True)

st.write("6. Daily Order Trends")
query = "SELECT order_date, COUNT(order_id) AS total_orders,ROUND(SUM(order_value),2) AS daily_revenue FROM uber_eats_order_data GROUP BY order_date ORDER BY order_date LIMIT 10";
results = run_sql(query, params)
st.dataframe(results, use_container_width=True, hide_index=True)


col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/maindashboard.py", label="Click here for Dashboard page")

with col3:
    st.page_link("pages/qa_page.py", label="Click here for Top 10 Q&A")

