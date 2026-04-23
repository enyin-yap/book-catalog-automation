import sys
import os
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))

sys.path.append(SRC_PATH)

from pipeline.catalog_pipeline import run_pipeline

input_path = "data/test_catalog(mixed).csv"
output_path = f"output/test_result_{timestamp}.xlsx"

run_pipeline(input_path, output_path)