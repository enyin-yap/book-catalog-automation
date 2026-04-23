import re

def clean_price(price):

    if not price:
        return None

    match = re.search(r"(\d+)\s*元", price)

    if match:
        return int(match.group(1))

    return None

def merge_book_data(openlib, google, mandarin, isbn):

    result = {
        "isbn": isbn,
        "title": google.get("title") or openlib.get("title"),
        "author": google.get("author") or openlib.get("author"),
        "pages": google.get("pages") or openlib.get("pages"),
        "publisher": google.get("publisher") or openlib.get("publisher"),
        "publish_date": google.get("publish_date") or openlib.get("publish_date"),
        "description": google.get("description") or openlib.get("description"),
        "price": clean_price(mandarin.get("price"))
    }

    return result