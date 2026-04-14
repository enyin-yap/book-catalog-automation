import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))

sys.path.append(SRC_PATH)

from collectors.mandarin_scraper import scrape_books_tw

# Test 1: Mandarin ISBN (should work)
print("Test 1:", scrape_books_tw("9789863424352"))

# Test 2: Invalid ISBN
print("Test 2:", scrape_books_tw("0000000000"))

