import pandas as pd
import re

def clean_price(price):

    if not price:
        return None

    match = re.search(r"(\d+)\s*元", price)

    if match:
        return int(match.group(1))

    return None

def normalize_date(date_str):
    if not date_str:
        return None

    return pd.to_datetime(date_str, errors="coerce").date()