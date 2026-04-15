def merge_book_data(openlib, google, mandarin, isbn):
    
    # Merge metadata from multiple sources into one clean record.
    # Priority: Google Books > OpenLibrary > books.tw (price only)

    result = {
        "isbn": isbn,

        # core metadata
        "title": None,
        "author": None,
        "pages": None,
        "publisher": None,
        "publish_date": None,
        "description": None,
        "price": None
    }

    
    result["title"] = (
        google.get("title")
        or openlib.get("title")
    )

    
    result["author"] = google.get("author")

    
    result["pages"] = (
        google.get("pages")
        or openlib.get("pages")
    )


    result["publisher"] = (
        google.get("publisher")
        or openlib.get("publisher")
    )


    result["publish_date"] = (
        google.get("publish_date")
        or openlib.get("publish_date")
    )


    result["description"] = google.get("description")

    result["price"] = mandarin.get("price")

    return result