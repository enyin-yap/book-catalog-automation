import pandas as pd
from utils.excel_styles import get_formats

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
        row["title"] = metadata["title"]

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
        row["price (TWD)"] = metadata["price"]

    return row


def save_output_excel(df, path, insights_df=None):
    
    df = df.rename(columns={
    "price": "price (TWD)"
    })

    book_columns = [
        "isbn",
        "price (TWD)",
        "title",
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

    # df.to_excel(path, index=False)

    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:

        df.to_excel(writer, index=False, sheet_name="Books_Info")
        
        workbook = writer.book 
        books_ws = writer.sheets["Books_Info"]

        formats = get_formats(workbook)
        
        books_ws.set_row(0, 30)  

        for row in range(1, len(df) + 1):
            books_ws.set_row(row, 50) 

        for col_num, col_name in enumerate(df.columns): 
            books_ws.write(0, col_num, col_name, formats["header"]) # first row

        
        for i, col in enumerate(df.columns):

            if col in ["isbn", "conditions"]:
                cell_format = formats["center"]

            elif col in ["description"]:
                cell_format = formats["wrap_top"]

            elif col in ["title", "author", "manufacturer"]:
                cell_format = formats["wrap_middle"]

            elif col == "price (TWD)":
                cell_format = formats["price"]

            else:
                cell_format = formats["left"]

            if col in ["description"]:
                max_len = 25

            elif col in ["title", "author", "manufacturer"]:
                max_len = 15

            elif col == "price (TWD)":
                max_len = 12

            else:
                # text_len = df[col].apply(lambda x: len(str(x)) if pd.notna(x) else 0).max()
                text_len = df[col].fillna("").astype(str).map(len).max()
                max_len = min(max(text_len, len(str(col))) + 2, 15)

            books_ws.set_column(i, i, max_len, cell_format)

        books_ws.freeze_panes(1, 1) 

        books_ws.autofilter(0, 0, df.shape[0], df.shape[1] - 1)

        if insights_df is not None and not insights_df.empty:

            insights_df.to_excel(writer, sheet_name="Insights", index=False)

            insights_ws = writer.sheets["Insights"]

            insights_ws.set_column(0, 0, 25, formats["insight_metric"])
            insights_ws.set_column(1, 1, 15, formats["insight_value"])

            for col_num, col_name in enumerate(insights_df.columns):
                insights_ws.write(0, col_num, col_name, formats["header"])

            insights_ws.set_row(0, 25)
            
            for row in range(1, len(insights_df) + 1):
                insights_ws.set_row(row, 30)

            insights_ws.freeze_panes(1, 0) 