# Uber Eats Bangalore Restaurant Intelligence & Decision Support Systems

This project analyzes restaurant performance,location intelligence on Uber Eats using Python, SQL, and Streamlit.

The goal of this project is to identify:
- Top performing restaurants
- Pricing segment performance
- Location Intelligence
- Partner Onboarding Strategy
- Pricing Optimization
- Cuisine Performance Analysis
- Product Feature Impact Assessment
- Market Segmentation
- Customer Satisfaction Drivers
- Expansion & Premium Restaurant Planning

## Project Overview

This dashboard helps understand how different factors affect restaurant success such as:
- Pricing
- Location
- Cuisine
- Online ordering
- Table booking

## Technologies Used

- Python
- SQL (SQLite)
- Pandas
- Streamlit

## Project Structure

```
UberEatsAnalyticsSystem.py – Main Streamlit dashboard  
scripts/UberEatsDataSet.py - Data Extraction, Cleaning, DataBase creation
database/my_database.db – SQLite database  
pages/ – Dashboard analysis pages with filter criterias, Q&A and orders  
README.md – Project documentation
```

## Approach
- Data Extraction & Transformation (Python)
- Source data loaded from CSV
- Data cleaning using Pandas
- Database Layer (SQLite3)
- Cleaned data stored in Relational Database
- Cursor-based SQL queries executed
- Streamlit Application (No Visualization)
- Displaying DataFrame-based results
- Allowing business users to explore insights through structured tabular outputs


## How to Run the Project

1 Install dependencies

```
pip install -r requirements.txt
```

2 Run Streamlit app

```
streamlit run UberEatsAnalyticsSystem.py
```

```
database/my_database.db – this file is not checked in due to size constraints. Execute scripts/UberEatsDataSet.py for the dateset creation and database creation. 

```

## Key Business Functionalities Achieved
1. Dashboard Page
- Provides multiple filtering options for users
- Allows users to filter and retrieve data dynamically from the SQL database
- Displays the filtered results in DataFrame/table format
- All filtering logic is implemented strictly using SQL queries

2. Q&A Page
- Displays analysis for 10 predefined business questions
- Each answer is generated through SQL-based computation
- Results are presented in structured table format within Streamlit
      
3. Order Data Integration & Custom Analytical Q&A
- The generated order dataset (originally stored in JSON format) is imported and stored in the SQL database as a structured table.
- All order-related analysis done using SQL queries.
- A custom Q&A module implemented specifically for the order dataset
- The system supports answering as many meaningful business queries as possible, leveraging SQL-based computation for consistency and efficiency


## Dashboard Preview


## Author

Vidhy Sri Sri Ram
