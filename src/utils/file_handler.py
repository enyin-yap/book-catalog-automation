import pandas as pd


def read_input_csv(path):
    
    # Read input CSV and return dataframe
    df = pd.read_csv(path, dtype={"isbn": str})

    return df


def extract_isbn_list(df):
    
    # Extract ISBN list from dataframe
    return df["isbn"].dropna().astype(str).tolist()


def update_row_metadata(row, metadata):
    
    # Update dataframe row with fetched metadata
    if metadata.get("title"):
        row["name"] = metadata["title"]

    if metadata.get("author"):
        row["author"] = metadata["author"]

    if metadata.get("pages"):
        row["pages"] = metadata["pages"]

    if metadata.get("publisher"):
        row["manufacturer"] = metadata["publisher"]

    if metadata.get("publish_date"):
        row["publisher_date"] = metadata["publish_date"]

    if metadata.get("description"):
        row["description"] = metadata["description"]

    if metadata.get("price"):
        row["price"] = metadata["price"]

    return row


def save_output_excel(df, path):

    book_columns = [
        "isbn",
        "price",
        "name",
        "author",
        "pages",
        "publisher_date",
        "manufacturer",
        "description"
    ]

    other_columns = [col for col in df.columns if col not in book_columns]

    # combine
    column_order = other_columns + book_columns

    df = df[column_order]

    df.to_excel(path, index=False)