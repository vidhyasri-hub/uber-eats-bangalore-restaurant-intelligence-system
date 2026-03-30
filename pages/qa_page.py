import streamlit as st # type: ignore
import sqlite3
import pandas as pd # type: ignore

#st.title("📊 QA page")
#st.title("Welcome! This page is for deep-dive business Q&A based on SQL data.")
st.markdown(
    """
    <h3 style='font-size:16px; text-align: justify; font-family:Open Sans, sans-serif; font-weight: normal; color: #00005554;'>
        Welcome! Let's explore some Business driven insights with the help of our system and data.
    </h3>
    """,
    unsafe_allow_html=True
)

def run_sql(query):
        with sqlite3.connect('database/my_database.db') as conn:
            return pd.read_sql_query(query, conn)

st.subheader("1. Which Bangalore locations have the highest average restaurant ratings?")
 #Business Value: Identifies premium-performing areas suitable for brand positioning and new partner onboarding.
query = "SELECT location,COUNT(name) AS total_restaurants,ROUND(AVG(rate), 2) AS avg_rating,ROUND(AVG(votes), 0) AS avg_votes FROM uber_eats_data WHERE rate IS NOT NULL GROUP BY location HAVING COUNT(name) >= 5 ORDER BY avg_rating DESC LIMIT 10";
results = run_sql(query)
st.dataframe(results, use_container_width=True, hide_index=True)

st.subheader("2. Does table booking correlate with higher customer ratings?")
 #Business Value: Measures the effectiveness of table booking as a premium feature.
query = "SELECT book_table_avail,COUNT(*) AS total_restaurants,ROUND(AVG(rate), 2) AS avg_rating,ROUND(AVG(votes), 0) AS avg_votes FROM uber_eats_data WHERE rate IS NOT NULL GROUP BY book_table_avail ORDER BY avg_rating DESC LIMIT 10";
results = run_sql(query)
st.dataframe(results, use_container_width=True, hide_index=True)

st.subheader("3. What price range delivers the best customer satisfaction?")
 #Business Value: Helps define the optimal pricing segment for partner success.
query = "SELECT pricing_segment,COUNT(*) AS total_restaurants,ROUND(AVG(rate), 2) AS avg_customer_rating,ROUND(AVG(votes), 0) AS avg_votes FROM uber_eats_data WHERE rate IS NOT NULL GROUP BY pricing_segment ORDER BY avg_customer_rating DESC LIMIT 10";
results = run_sql(query)
st.dataframe(results, use_container_width=True, hide_index=True)


st.subheader("4. How do low, mid, and premium-priced restaurants perform in terms of ratings?")
 #Business Value: Supports pricing-based market segmentation strategies.
query = """SELECT
    pricing_segment AS "Pricing Segment",
    rating_category AS "Rating Category",
    COUNT(*) AS "Number of Restaurants"
FROM uber_eats_data
WHERE rate_normalized IS NOT NULL
GROUP BY pricing_segment, rating_category
ORDER BY pricing_segment, COUNT(*) DESC""".replace("\n", " ");
results = run_sql(query)
st.dataframe(results, use_container_width=True, hide_index=True)


st.subheader("5. Which cuisines are most common in Bangalore?")
#Business Value: Reveals market demand and cuisine saturation levels.
query1= "SELECT cuisines, COUNT(*) AS total_restaurants,ROUND(AVG(rate), 2) AS avg_rating,ROUND(AVG(cost), 2) AS avg_cost FROM uber_eats_data GROUP BY cuisines ORDER BY total_restaurants DESC LIMIT 10";
results = run_sql(query1)
st.dataframe(results, use_container_width=True, hide_index=True)

st.subheader("6. Which cuisines receive the highest average ratings?")
 #Business Value: Identifies high-quality cuisine categories suitable for promotion.
query2= "SELECT  cuisines, ROUND(AVG(rate), 2) AS avg_rating, COUNT(*) AS restaurant_count,SUM(votes) AS total_votes, ROUND(AVG(cost), 2) AS avg_cost FROM uber_eats_data WHERE rate > 0 GROUP BY cuisines HAVING restaurant_count >= 5 ORDER BY avg_rating DESC LIMIT 10";
results = run_sql(query2)
st.dataframe(results, use_container_width=True, hide_index=True)

st.subheader("7. What is the relationship between restaurant cost and rating?")
 #Business Value: Determines whether higher pricing translates to better customer perception.
query = "SELECT pricing_segment,COUNT(*) AS total_restaurants,ROUND(AVG(rate), 2) AS avg_rating,ROUND(AVG(votes), 0) AS avg_engagement,ROUND(AVG(cost), 2) AS avg_cost_in_segment FROM uber_eats_data WHERE rate IS NOT NULL AND cost > 0 GROUP BY pricing_segment ORDER BY avg_cost_in_segment ASC";
results = run_sql(query)
st.dataframe(results, use_container_width=True, hide_index=True)

st.subheader("8. Which locations are ideal for premium restaurant onboarding?")
 #Business Value: Combines cost, rating, and location insights to guide premium expansion.
query = "SELECT location, COUNT(*) AS total_restaurants,SUM(CASE WHEN pricing_segment = 'Premium-Range' THEN 1 ELSE 0 END) AS premium_count,ROUND(AVG(cost), 2) AS avg_cost_in_location,ROUND(AVG(rate), 2) AS avg_location_rating, SUM(votes) AS total_engagement FROM uber_eats_data GROUP BY location HAVING premium_count > 0 AND avg_location_rating >= 4.0 ORDER BY premium_count DESC, avg_cost_in_location DESC LIMIT 10";
results = run_sql(query)
st.dataframe(results, use_container_width=True, hide_index=True)

st.subheader("9. What combination of factors maximizes restaurant success on Uber Eats? \n (Pricing + Location + Cuisine + Platform Features)")
#Business Value: Supports strategic partner recommendations.
query="""SELECT
    ROUND((AVG(rate) * 0.6 + (AVG(votes) / 1000) * 0.4), 2) 
        AS "Success Score",
    pricing_segment AS "Pricing Segment",
    location AS "Location",
    cuisines AS "Cuisine",
    CASE 
        WHEN online_order_avail = 'Yes' AND book_table_avail = 'Yes' 
            THEN 'Online + Table Booking'
        WHEN online_order_avail = 'Yes' 
            THEN 'Online Only'
        WHEN book_table_avail = 'Yes' 
            THEN 'Table Booking Only'
        ELSE 'No Platform Features'
    END AS "Platform Feature Type",
    COUNT(*) AS "Total Restaurants",
    ROUND(AVG(rate), 2) AS "Average Rating",
    ROUND(AVG(votes), 0) AS "Average Votes",
    ROUND(AVG(cost), 2) AS "Average Cost"
FROM uber_eats_data
WHERE rate IS NOT NULL
AND votes > 30
AND cost > 0
GROUP BY
    pricing_segment,
    location,
    cuisines,
    "Platform Feature Type"
HAVING COUNT(*) >= 5
ORDER BY "Success Score" DESC
LIMIT 10;""".replace("\n", " "); 
results = run_sql(query)
st.dataframe(results, use_container_width=True, hide_index=True)

st.subheader("10. Which restaurants are top performers within each pricing segment?")
#Business Value: Helps identify benchmark partners and best practices.
query = """WITH restaurant_performance AS (
    SELECT
        pricing_segment,
        name,
        location,
        cuisines,
        ROUND((AVG(rate) * 0.7 + (AVG(votes) / 1000) * 0.3), 2)
            AS success_score,
        CASE
            WHEN AVG(rate) >= 4.5 AND AVG(votes) >= 500
                THEN 'Top Performer'
            WHEN AVG(rate) >= 4.2
                THEN 'High Performer'
            ELSE 'Moderate'
        END AS performance_category
    FROM uber_eats_data
    WHERE rate IS NOT NULL
    AND votes > 50
    AND cost > 0
    GROUP BY pricing_segment, name, location, cuisines
    HAVING COUNT(*) >= 1
),
ranked_restaurants AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY pricing_segment
               ORDER BY success_score DESC
           ) AS rank_in_segment
    FROM restaurant_performance
)
SELECT
    pricing_segment AS "Pricing Segment",
    name AS "Restaurant Name",
    location AS "Location",
    cuisines AS "Cuisine",
    success_score AS "Success Score",
    performance_category AS "Performance Category",
    rank_in_segment AS "Rank in Segment"
FROM ranked_restaurants
WHERE rank_in_segment <= 3
ORDER BY pricing_segment, rank_in_segment;
""".replace("\n", " "); 
results = run_sql(query)
st.dataframe(results, use_container_width=True, hide_index=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/maindashboard.py", label="Click here for Dashboard page")

with col3:
    st.page_link("pages/order_integration_page.py", label="Click here for Orders page")

