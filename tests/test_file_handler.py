import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))

sys.path.append(SRC_PATH)

import utils.file_handler as fh

# Test Load CSV Function
df = fh.read_input_csv("data/catalog1.csv")

print("DATAFRAME:")
print(df.head())
print(df.columns)

# Test Extract ISBN list Function
isbn_list = fh.extract_isbn_list(df)

print("\nISBN LIST:")
print(isbn_list) 