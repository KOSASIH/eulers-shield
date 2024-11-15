import pandas as pd

def mask_data(dataframe, columns_to_mask):
    """Mask sensitive data in specified columns of a DataFrame."""
    masked_dataframe = dataframe.copy()
    for column in columns_to_mask:
        if column in masked_dataframe.columns:
            # Replace sensitive data with asterisks or a masking pattern
            masked_dataframe[column] = masked_dataframe[column].apply(lambda x: '*' * len(str(x)))
    return masked_dataframe

# Example Usage:
if __name__ == "__main__":
    # Sample DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Email': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
        'Phone': ['123-456-7890', '987-654-3210', '555-555-5555']
    }
    df = pd.DataFrame(data)

    # Columns to mask
    columns_to_mask = ['Email', 'Phone']

    # Mask the data
    masked_df = mask_data(df, columns_to_mask)
    print("Original DataFrame:\n", df)
    print("Masked DataFrame:\n", masked_df)
