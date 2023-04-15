import streamlit as st

st.set_page_config(page_title="Parameters")

st.markdown("# Parameters")
# st.sidebar.header("Parameters")

st.markdown(
    """
    MySQL Translator is an open-source application that lets you interact 
    with your MySQL database using natural language. Below are a
    few parameters to keep in mind:

    ### Capabilities:
    * Most SELECT requests
    * Up to regular-difficulty joins
    * Standard SQL calculations (AVG(), STDDEV(), VARIANCE(), MIN(), MAX())
    * Most conditions (e.g., "list all actors whose last name contain the letters 'GEN'")


    ### Limitations:
    * Works best when specific table names and columns are used in request (e.g., "film" instead of "movie" for "film" table)
    * Advanced joins have not been successful thus far
    
    ### Examples:
    * "list all actors by first name and last name alphabetically in descending order"
    * "calculate standard deviation of all films in sales_by_film_category"
    * "list the total paid by each customer, list the customers alphabetically by last name" (JOIN)
    * "Display the most frequently rented movies in descending order."

"""
)