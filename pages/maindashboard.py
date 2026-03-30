import streamlit as st # type: ignore
import sqlite3
import pandas as pd # type: ignore

#st.title("Ubers Eats Dashboard")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F5F7FA;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <h2 style='font-size:20px; text-align: center; font-family:Arial, sans-serif; color: #291fb4;'>
        Ubers Eats Dashboard
    </h2>
    """,
    unsafe_allow_html=True
)

def run_sql(query, params=()):
        with sqlite3.connect('database/my_database.db') as conn:
            return pd.read_sql_query(query, conn, params=params)

# --- 1. GET FILTER OPTIONS FROM DATABASE ---
# We query the DB to get the actual values available in our data



locations = run_sql("SELECT DISTINCT location FROM uber_eats_data ORDER BY location")['location'].tolist()
rest_types = run_sql("SELECT DISTINCT rest_type FROM uber_eats_data ORDER BY rest_type")['rest_type'].tolist()
segments = run_sql("SELECT DISTINCT pricing_segment FROM uber_eats_data")['pricing_segment'].tolist()

# --- 2.  FILTERS ---
#st.header("Filter Criteria")
st.markdown(
    """
    <h3 style='font-size:18px; text-align: left; font-family:Arial, sans-serif; color: #00005554;'>
        Filter Criteria
    </h3>
    """,
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns(3)

with col1:
    restaurant_name = st.text_input("Restaurant Name", "")
    rate = st.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.5)
    online_order = st.checkbox("Online Order Available")
    book_table = st.checkbox("Table Booking Available")


with col2:
    location_name = st.selectbox("Location", ["All"] + locations)
    approx_cost_for_two = st.number_input("Approximate Cost for Two", min_value=0, step=200)

with col3:
    cuisines_type = st.text_input("Cuisines Type", "")
    restaurant_type = st.selectbox("Restaurant Type", ["All"] + rest_types)
    selected_segments = st.multiselect("Pricing Segments", segments)

# --- 3. SQL query formation ---
# We start with 1=1 so we can easily append "AND ..." conditions
base_query ="SELECT DISTINCT name as 'Restaurant Name', location as 'Location', cuisines as 'Cuisines Type',rate as 'Rating',cost as 'Cost',online_order_avail as 'Online Order Available',book_table_avail as 'Table Booking Available' FROM uber_eats_data WHERE 1=1"
params = []

if restaurant_name:
    base_query += " AND name LIKE ?"
    params.append(f"%{restaurant_name}%")

if location_name != "All":
    base_query += " AND location = ?"
    params.append(location_name)

if cuisines_type:
    base_query += " AND cuisines LIKE ?"
    params.append(f"%{cuisines_type}%")

if rate > 0:
    base_query += " AND rate >= ?"
    params.append(rate)

if approx_cost_for_two > 0:
    base_query += " AND cost <= ?"
    params.append(approx_cost_for_two)

if online_order:
    base_query += " AND online_order_avail = 'Yes'"

if book_table:
    base_query += " AND book_table_avail = 'Yes'"

if restaurant_type != "All":
    base_query += " AND rest_type = ?"
    params.append(restaurant_type)

# Add Multi-select Pricing Filter
if selected_segments:
    placeholders = ', '.join(['?'] * len(selected_segments))
    base_query += f" AND pricing_segment IN ({placeholders})"
    params.extend(selected_segments)

if st.button("Apply Filters"):
    results = run_sql(base_query, params)
    
    # Display Stats
    st.info(f"Showing **{len(results)}** restaurants found via SQL query.")
    
    # Display Table
    st.dataframe(results, use_container_width=True, hide_index=True)
else:
    # Initial view before button click
    initial_results = run_sql("SELECT DISTINCT name as 'Restaurant Name', location as 'Location', cuisines as 'Cuisines Type',rate as 'Rating',cost as 'Cost',online_order_avail as 'Online Order Available',book_table_avail as 'Table Booking Available' FROM uber_eats_data LIMIT 25")
    st.write("Previewing first 25 records. Use filters to search the full data set.")
    st.dataframe(initial_results, use_container_width=True, hide_index=True)
    
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/qa_page.py", label="Click here for Top 10 Q&A")

with col3:
    st.page_link("pages/order_integration_page.py", label="Click here for Orders page")