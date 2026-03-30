import streamlit as st # type: ignore
import sqlite3
import pandas as pd # type: ignore
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #eef2f3, #dfe9f3);
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <h1 style='font-size:25px; text-align: center; font-family:Arial, sans-serif; color: #1F77B4;'>
        Uber Eats Bangalore Restaurant Intelligence & Decision Support Systems
    </h1>
    """,
    unsafe_allow_html=True
)

#st.title("Uber Eats Bangalore Restaurant Intelligence & Decision Support Systems")
#st.write("Welcome to the Uber Eats Bangalore Restaurant Intelligence Dashboard! This platform provides data-driven insights to help restaurant partners optimize their performance and make informed business decisions. Explore key metrics, trends, and actionable recommendations based on comprehensive analysis of restaurant data in Bangalore. Whether you're looking to enhance your restaurant's visibility, improve customer satisfaction, or identify growth opportunities, this dashboard is your go-to resource for strategic guidance and operational excellence on Uber Eats.")

def load_data():
    conn = sqlite3.connect('database/my_database.db')
    query = "SELECT * FROM uber_eats_data"
    dataFrame = pd.read_sql(query, conn)
    conn.close()
    return dataFrame

data = load_data()

main_dashboard_page = st.Page("pages/maindashboard.py", title="Dashboard", icon="📊", default=True)
qa_page = st.Page("pages/qa_page.py", title="Business Q&A", icon="❓")
order_integration_page = st.Page("pages/order_integration_page.py", title="Order Integration", icon="🛒")

pg = st.navigation([main_dashboard_page, qa_page, order_integration_page])
pg.run()

#st.dataframe(data.head(),use_container_width=True)
