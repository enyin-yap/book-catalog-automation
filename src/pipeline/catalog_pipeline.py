from collectors.openlibrary_fetcher import fetch_openlibrary
from collectors.googlebooks_fetcher import fetch_googlebooks
from collectors.mandarin_scraper import scrape_books_tw

from pipeline.merge_metadata import merge_book_data
from utils.file_handler import read_input_csv, save_output_excel


def run_pipeline(input_path, output_path):

    # Load CSV
    df = read_input_csv(input_path)

    results = []

    # Loop through each row
    for index, row in df.iterrows():

        isbn = str(row.get("isbn"))

        if not isbn or isbn == "nan":
            continue

        print(f"Processing ISBN: {isbn}")


        openlib_data = fetch_openlibrary(isbn)
        google_data = fetch_googlebooks(isbn)
        scraper_data = scrape_books_tw(isbn)

        # Merge metadata
        merged = merge_book_data(
            openlib_data,
            google_data,
            scraper_data,
            isbn
        )

       # Fill CSV
        df.at[index, "name"] = merged.get("title")
        df.at[index, "author"] = merged.get("author")
        df.at[index, "pages"] = merged.get("pages")
        df.at[index, "publisher_date"] = merged.get("publish_date")
        df.at[index, "manufacturer"] = merged.get("publisher")
        df.at[index, "description"] = merged.get("description")
        df.at[index, "original_price"] = merged.get("price")

        results.append(merged)

    # Excel output
    save_output_excel(df, output_path)

    print(f"\nPipeline completed. Output saved to: {output_path}")

    return results