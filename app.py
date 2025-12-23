import streamlit as st
import openai
from dotenv import load_dotenv
import os
from insights import generate_insight
import pandas as pd
from sqlalchemy import text
from db.db_connection import get_engine
from utils.sql_generator import generate_sql
from utils.chart_generator import plot_chart
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI BI Analyst")
st.title("AI-Powered Business Intelligence Analyst")
st.write("Ask questions about your business data in plain English")
st.sidebar.header("📂 Dataset Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file", type=["csv"]
)

table_name = st.sidebar.text_input(
    "Enter table name for dataset"
)

if uploaded_file and table_name:
    try:
        df_upload = pd.read_csv(uploaded_file)
        engine = get_engine()
        df_upload.to_sql(table_name, engine, if_exists="replace", index=False)
        st.sidebar.success(f"Dataset uploaded successfully as table '{table_name}'")
    except SQLAlchemyError as e:
        st.sidebar.error(f"Database error: {e}")

@st.cache_data
def get_sql(query):
    return generate_sql(query)

user_query = st.text_input("Type your question here:")

if user_query:
    try:
        sql = get_sql(user_query)
        if sql:
            st.subheader("Generated SQL Query")
            st.code(sql, language="sql")

            engine = get_engine()
            df_result = pd.read_sql(sql, engine)

            if df_result.empty:
                st.warning("Query returned no results.")
            else:
                st.subheader("Query Result")
                st.dataframe(df_result)

            buf = plot_chart(df_result)
            if buf:
                st.subheader("Chart")
                st.image(buf)
        else:
            st.error("Unable to generate a safe SQL query.")
    except Exception as e:
        st.error(f"Error: {e}")