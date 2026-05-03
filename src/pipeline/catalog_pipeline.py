from collectors.openlibrary_fetcher import fetch_openlibrary
from collectors.googlebooks_fetcher import fetch_googlebooks
from collectors.mandarin_scraper import scrape_books_tw

from pipeline.merge_metadata import merge_book_data
from pipeline.insights import generate_insights
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
            print(f"[WARN] Google Books error 503 for {isbn}, retrying...")
            time.sleep(1)
            google_data = fetch_googlebooks(isbn)

        if is_success(google_data):
            google_status = "success"
        else:
            google_status = "fail"
            google_data = {}
        
        df.at[index, "google_status"] = google_status

 
        try:
            openlib_data = fetch_openlibrary(isbn)
            openlib_status = "success" if is_success(openlib_data) else "fail"
        except Exception as e:
            print(f"[ERROR] OpenLibrary failed for {isbn}: {e}")
            openlib_data = {}
            openlib_status = "fail"
        
        df.at[index, "openlibrary_status"] = openlib_status


        try:
            scraper_data = scrape_books_tw(isbn)
        except Exception as e:
            print(f"[ERROR] Scraper failed for {isbn}: {e}")
            scraper_data = {}

        
        if google_status == "success":
            df.at[index, "primary_source"] = "google"

        elif openlib_status == "success":
            df.at[index, "primary_source"] = "openlibrary"

        else:
            df.at[index, "primary_source"] = "none"


        merged = merge_book_data(
            openlib_data,
            google_data,
            scraper_data,
            isbn
        )

       
        # Update CSV field
        field_mapping = {
            "title": "title",
            "author": "author",
            "pages": "pages",
            "publisher_date": "publish_date",
            "manufacturer": "publisher",
            "description": "description",
            "price (TWD)": "price"
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

    insights_df = generate_insights(df)

    save_output_excel(df, output_path, insights_df)

    print(f"\nPipeline completed. Output saved to: {output_path}")

    return results