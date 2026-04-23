import requests

def fetch_openlibrary(isbn):

    url = f"https://openlibrary.org/isbn/{isbn}.json"

    try:
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            return {}

        data = res.json()

        return {
            "title": data.get("title"),
            "pages": data.get("number_of_pages"),
            "publish_date": data.get("publish_date"),
            "publisher": data.get("publishers", [None])[0]
        }

    except requests.exceptions.RequestException as e:
        return {"error": "REQUEST_FAILED", "details": str(e)}