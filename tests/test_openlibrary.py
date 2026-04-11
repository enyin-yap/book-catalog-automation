import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))

sys.path.append(SRC_PATH)

from openlibrary_fetcher import fetch_openlibrary

# TEST 1: valid ISBN
print("Test 1:", fetch_openlibrary("9780755331604"))

# TEST 2: Mandarin ISBN
print("Test 2:", fetch_openlibrary("9789863424352"))

# TEST 3: invalid ISBN (numeric)
print("Test 3:", fetch_openlibrary("0000000"))

# TEST 3: invalid ISBN (alphabetical)
print("Test 3:", fetch_openlibrary("abc"))