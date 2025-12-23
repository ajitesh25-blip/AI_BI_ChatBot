import pandas as pd
from db.db_connection import get_engine

def get_schema_description():
    """
    Reads all table names and columns from the database,
    and returns a string describing the schema.
    """

    engine = get_engine()

    
    query = """
    SELECT TABLE_NAME, COLUMN_NAME
    FROM information_schema.columns
    WHERE table_schema = 'ai_bi'
    ORDER BY TABLE_NAME;
    """

    df = pd.read_sql(query, engine)

    
    df.columns = [col.lower() for col in df.columns]

    
    schema_text = ""
    for table in df["table_name"].unique():
        cols = df[df["table_name"] == table]["column_name"].tolist()
        schema_text += f"{table}({', '.join(cols)})\n"

    return schema_text