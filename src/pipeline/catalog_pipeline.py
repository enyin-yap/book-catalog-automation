from collectors.openlibrary_fetcher import fetch_openlibrary
from collectors.googlebooks_fetcher import fetch_googlebooks
from collectors.mandarin_scraper import scrape_books_tw

from pipeline.merge_metadata import merge_book_data
from utils.file_handler import read_input_csv, save_output_excel

import pandas as pd
import time


def is_success(result):
    return isinstance(result, dict) and result.get("status") == "success"


def is_retryable_error(result):
    return isinstance(result, dict) and result.get("error") in [
        "SERVICE_UNAVAILABLE"
    ]


def run_pipeline(input_path, output_path):

    df = read_input_csv(input_path)
    results = []

    for index, row in df.iterrows():

        isbn = str(row.get("isbn"))

        if not isbn or isbn == "nan":
            continue

        print(f"\nProcessing ISBN: {isbn}")


        google_data = fetch_googlebooks(isbn)

        # simple retry for error 503 
        if is_retryable_error(google_data):
            print(f"[WARN] Google Books 503 for {isbn}, retrying...")
            time.sleep(1)
            google_data = fetch_googlebooks(isbn)

        if not is_success(google_data):
            google_data = {}

 
        try:
            openlib_data = fetch_openlibrary(isbn)
        except Exception as e:
            print(f"[ERROR] OpenLibrary failed for {isbn}: {e}")
            openlib_data = {}


        try:
            scraper_data = scrape_books_tw(isbn)
        except Exception as e:
            print(f"[ERROR] Scraper failed for {isbn}: {e}")
            scraper_data = {}


        merged = merge_book_data(
            openlib_data,
            google_data,
            scraper_data,
            isbn
        )

       
        # Update CSV field
        field_mapping = {
            "name": "title",
            "author": "author",
            "pages": "pages",
            "publisher_date": "publish_date",
            "manufacturer": "publisher",
            "description": "description",
            "price": "price"
        }

        for df_col, merged_key in field_mapping.items():

            current_value = row.get(df_col)

            if pd.isna(current_value) or current_value == "":
                value = merged.get(merged_key)

                if value:
                    df.at[index, df_col] = value

        results.append({
            "isbn": isbn,
            "status": "processed",
            "google_status": google_data.get("status", "unknown"),
        })

        # simple rate limiting 
        time.sleep(0.2)


    save_output_excel(df, output_path)

    print(f"\nPipeline completed. Output saved to: {output_path}")

    return results