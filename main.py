import os
import sys
import argparse
from datetime import datetime

# --- Add src to path ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "src"))
sys.path.append(SRC_PATH)

from src.pipeline.catalog_pipeline import run_pipeline


def build_output_path(output_arg: str | None) -> str:

    if output_arg:
        return output_arg

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(CURRENT_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)

    return os.path.join(output_dir, f"result_{timestamp}.xlsx")


def validate_input_path(path: str) -> None:
   
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Book Catalog Metadata Pipeline"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input CSV file (e.g. data/input.csv or full path)"
    )

    parser.add_argument(
        "--output",
        required=False,
        help="Path to output Excel file (optional)"
    )

    args = parser.parse_args()

    try:
        input_path = args.input
        output_path = build_output_path(args.output)

        # Validate input
        validate_input_path(input_path)

        print("\nStarting Book Catalog Pipeline")
        print(f"Input File : {input_path}")

        # Run pipeline
        run_pipeline(input_path, output_path)

        print("\nPipeline completed successfully!")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()