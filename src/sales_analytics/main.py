from .db import create_in_memory_db
from .loaders import load_all_data
from .analytics import generate_reports
from .config import DEFAULT_REPORTS_DIR
from pathlib import Path
import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--from-date",
        help="Initial date for the report",
    )

    parser.add_argument(
        "--to-date",
        help="Final date for the report",
    )
    parser.add_argument(
        "--output-dir",

        help="Dir to save the reports",
    )

    return parser.parse_args()

def main() -> None:
    args = parse_args()
    conn = create_in_memory_db()
    load_all_data(conn)
    generate_reports(conn, output_dir=Path(args.output_dir), initial_date = args.from_date, final_date=args.to_date)

if __name__ == "__main__":
    main()
