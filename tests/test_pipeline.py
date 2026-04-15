import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))

sys.path.append(SRC_PATH)

from pipeline.catalog_pipeline import run_pipeline

input_path = "data/test_catalog.csv"
output_path = "output/test_result.xlsx"

run_pipeline(input_path, output_path)