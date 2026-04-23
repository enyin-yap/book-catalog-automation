import requests

def fetch_googlebooks(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

    try:
        res = requests.get(url, timeout=10)

        # Check http status 
        if res.status_code == 503:
            return {"error": "SERVICE_UNAVAILABLE", "status": 503}

        if res.status_code != 200:
            return {"error": "HTTP_ERROR", "status": res.status_code}

        data = res.json()

        if "items" not in data:
            return {"error": "NOT_FOUND"}

        info = data["items"][0]["volumeInfo"]

        return {
            "title": info.get("title"),
            "author": ", ".join(info.get("authors", [])),
            "pages": info.get("pageCount"),
            "publish_date": info.get("publishedDate"),
            "publisher": info.get("publisher"),
            "description": info.get("description"),
            "status": "success"
        }

    except requests.exceptions.RequestException as e:
        return {"error": "REQUEST_FAILED", "details": str(e)}