# import sys
# import os

# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))

# sys.path.append(SRC_PATH)

from src.pipeline.merge_metadata import merge_book_data

# Use mock data to test the function first
google = {
    "title": "Poor Charlie's Almanack: The Essential Wit and Wisdom of Charles T. Munger",
    "author": "Charlie Munger",
    "pages": 350,
    "publisher": "Stripe Press (US)",
    # "publish_date": "2024/04",
    "description": "From the legendary vice-chairman of Berkshire Hathaway, lessons in investment strategy, philanthropy, and living a rational and ethical life. A timeless classic that will change how you approach life. There is a billion-dollar education inside this book."

}

openlib = {
    "title": "Poor Charlie's Almanack: The Essential Wit and Wisdom of Charles T. Munger",
    "pages": 320,
    "publisher": "Stripe Press",
    "publish_date": "2005"
}

mandarin = {
    "price": 160.0
}

isbn = "9781953953230"

# Test function
merged = merge_book_data(openlib, google, mandarin, isbn)

print(merged)