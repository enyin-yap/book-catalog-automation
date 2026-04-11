import requests

def fetch_googlebooks(isbn):

    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        if "items" not in data:
            return {}

        info = data["items"][0]["volumeInfo"]

        return {
            "title": info.get("title"),
            "author": ", ".join(info.get("authors", [])),
            "pages": info.get("pageCount"),
            "publish_date": info.get("publishedDate"),
            "publisher": info.get("publisher"),
            "description": info.get("description")
        }

    except:
        return {}