import pandas as pd # type: ignore
import numpy as np # type: ignore
import sqlite3

dataset = pd.read_csv("data/Uber_Eats_data.csv")
#display(dataset)

# From requirement document 
"""
Data cleaning using Pandas:
Duplicate removal
Missing value handling
Rating normalization
Cost standardization
Feature engineering for pricing segments and rating categories
"""

# Before that Cleaning few column's values 
# 1. 'rate' column
def clean_rate(ratingValue):
    if pd.isna(ratingValue) or ratingValue == 'NEW' or ratingValue == '-':
        return np.nan
    else:
        ratingValue = str(ratingValue).split('/')[0]
        return float(ratingValue)

dataset['rate'] = dataset['rate'].apply(clean_rate)
#display(dataset)

# 2. 'approx_cost(for two people)' column to remove commas and replace blank values with NaN
dataset['approx_cost(for two people)'] = dataset['approx_cost(for two people)'].astype(str).str.replace(',', '')
dataset['approx_cost(for two people)'] = pd.to_numeric(dataset['approx_cost(for two people)'], errors='coerce')
#display(dataset)

# 3. Duplicate removal
dataset.drop_duplicates(inplace=True)

#4. Missing value handling
# The possible columns as per the dataset for missing value handling are integer based columns - rate, approx_cost(for two people) and votes
# We can use median based on the values 
dataset['rate'] = dataset['rate'].fillna(dataset['rate'].median())
dataset['approx_cost(for two people)'] = dataset['approx_cost(for two people)'].fillna(dataset['approx_cost(for two people)'].median())
dataset['votes'] = dataset['votes'].fillna(dataset['votes'].median())
#display(dataset)

#5. Rating normalization
min_r = dataset['rate'].min()
max_r = dataset['rate'].max()
dataset['rate_normalized'] = (dataset['rate'] - min_r) / (max_r - min_r)
#display(dataset)

#6. Cost standardization
cost_column = 'approx_cost(for two people)'
mean_cost = dataset[cost_column].mean()
std_cost = dataset[cost_column].std()
dataset['cost_standardized'] = (dataset[cost_column] - mean_cost) / std_cost
#display(dataset)

#7. Feature engineering for pricing segments and rating categories
# Pricing segments 
# cost_standardized column is taken for consideration for easy analytics
def pricing_segment(cost):  
    if cost < -1:  
        return 'Budget-Friendly'  
    elif -1 <= cost <= 2:  
        return 'Medium-Range'  
    else:  
        return 'Premium-Range'
dataset['pricing_segment'] = dataset['cost_standardized'].apply(pricing_segment)
#display(dataset)

# Rating categories
# rate column is taken as it can be used for ratig the restaurants 
def rating_category(rateValue):
    if rateValue < 2:
        return 'Poor'
    elif 2 <= rateValue < 3.5:
        return 'Average'
    elif 3.5 <= rateValue < 4.5:
        return 'Good'
    else:
        return 'Excellent'
dataset['rating_category'] = dataset['rate'].apply(rating_category)
#display(dataset)
#display(dataset[['name', 'rate', 'rate_normalized', 'approx_cost(for two people)', 'pricing_segment', 'rating_category']].head())

# Database creation using SQLite
conn = sqlite3.connect('database/my_database.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS uber_eats_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    online_order_avail VARCHAR(10),
    book_table_avail VARCHAR(10),
    rate FLOAT,
    rate_normalized FLOAT,
    votes INT,
    phone VARCHAR(20),
    location VARCHAR(255),
    rest_type VARCHAR(255),
    dish_liked TEXT,          
    cuisines TEXT,
    cost FLOAT,
    cost_standardized FLOAT,
listed_in_type VARCHAR(55),
listed_in_city VARCHAR(55),
pricing_segment VARCHAR(20),
rating_category VARCHAR(20)
)''')     

cursor.execute("SELECT sql FROM sqlite_master WHERE name='uber_eats_data'")
#print("print--> ",cursor.fetchone()[0])

for i, row in dataset.iterrows():
    sql = "INSERT INTO uber_eats_data (name, online_order_avail, book_table_avail, rate, rate_normalized, votes, phone, location, rest_type, dish_liked, cuisines, cost, cost_standardized, listed_in_type, listed_in_city, pricing_segment, rating_category) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, (row['name'], row['online_order'], row['book_table'], row['rate'], row['rate_normalized'], row['votes'], row['phone'], row['location'], row['rest_type'], row['dish_liked'], row['cuisines'], row['approx_cost(for two people)'], row['cost_standardized'], row['listed_in(type)'], row['listed_in(city)'], row['pricing_segment'], row['rating_category']))

conn.commit()
print("Data successfully loaded to SQLite!")

df_check = pd.read_sql_query("SELECT * FROM uber_eats_data", conn)
#print("print--->",df_check)