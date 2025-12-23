from sqlalchemy import create_engine
import pandas as pd

def get_engine():
    """
    Returns a SQLAlchemy engine connected to your MySQL database.
    Replace username/password with your MySQL credentials.
    """
    return create_engine(
        "mysql+mysqlconnector://root:root123@localhost/ai_bi"
    )