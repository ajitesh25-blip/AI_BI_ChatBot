import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import pandas as pd


def plot_chart(df):
    """
    Generates a chart for a given dataframe.
    Returns a buffer that can be displayed in Streamlit.
    """
    if df.empty:
        return None

    # If 2 columns, assume categorical vs numeric → bar chart
    if df.shape[1] == 2:
        x_col, y_col = df.columns
        plt.figure(figsize=(8,5))
        sns.barplot(data=df, x=x_col, y=y_col)
        plt.xticks(rotation=45)
        plt.tight_layout()

    # If first column is date/time, second is numeric → line chart
    elif df.shape[1] >= 2 and pd.api.types.is_datetime64_any_dtype(df[df.columns[0]]):
        x_col, y_col = df.columns[0], df.columns[1]
        plt.figure(figsize=(8,5))
        sns.lineplot(data=df, x=x_col, y=y_col, marker='o')
        plt.xticks(rotation=45)
        plt.tight_layout()

    # Fallback: first two numeric columns → bar chart
    else:
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) >= 2:
            x_col, y_col = numeric_cols[:2]
            plt.figure(figsize=(8,5))
            sns.barplot(data=df, x=x_col, y=y_col)
            plt.tight_layout()
        else:
            return None  # Not enough numeric data to plot

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf