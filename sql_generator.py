import os
import re
from utils.schema_reader import get_schema_description
from dotenv import load_dotenv
import openai

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sql(user_query):
    """
    Generate a safe SQL query using OpenAI.
    Returns a fallback query if OpenAI quota is exceeded.
    """
    schema = get_schema_description()
    prompt = f"""
You are an expert MySQL analyst.
Database schema:
{schema}

Write a SAFE SQL query to answer:
{user_query}

Rules:
- Only SELECT statements
- Do not modify data
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        sql = response.choices[0].message.content.strip()

        # Only allow SELECT statements
        if not re.match(r"^SELECT", sql, re.IGNORECASE):
            return None

        return sql

    except Exception:
        # Generic fallback if quota exceeded or any other error occurs
        return "SELECT * FROM sales_data LIMIT 5;"