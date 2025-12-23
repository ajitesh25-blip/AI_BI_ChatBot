
def generate_insight(df):
    """
    Generates simple business insights from a pandas DataFrame.

    Parameters:
        df (pandas.DataFrame): Query result.

    Returns:
        str: Human-readable insight.
    """
    if df.empty:
        return "No data available for this query."

    
    if "total_sales" in df.columns:
        total = df.iloc[0, 0]
        return f" Total sales are ${total:,.2f}."

    
    if df.shape[1] >= 2:
        col_name = df.columns[0]
        value_col = df.columns[1]

      
        max_row = df.loc[df[value_col].idxmax()]
        max_label = max_row[col_name]
        max_value = max_row[value_col]

        return f" {max_label} has the highest {value_col} with ${max_value:,.2f}."

    
    return "Data loaded, but no clear insight generated."