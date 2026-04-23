import requests
from bs4 import BeautifulSoup

def scrape_books_tw(isbn):

    url = f"https://search.books.com.tw/search/query/key/{isbn}"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(res.text, "html.parser")

        price = None

        price_tag = soup.select_one(".price")

        if price_tag:
            price = price_tag.text.strip()

        return {
            "price": price
        }

    except requests.exceptions.RequestException as e:
        return {"error": "REQUEST_FAILED", "details": str(e)}