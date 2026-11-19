#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def validate_date(date_str: str | None) -> str:
    """Validate YYYY-MM-DD format or return today's date."""
    if not date_str:
        return datetime.now().strftime("%Y-%m-%d")
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date '{date_str}'. Use YYYY-MM-DD format.")


def prepare_path(path_str: str) -> Path:
    """Return expanded Path and create parent directory if needed."""
    file_path = Path(path_str).expanduser()
    if file_path.parent and str(file_path.parent) not in ("", "."):
        file_path.parent.mkdir(parents=True, exist_ok=True)
    return file_path


def add_entry(file_str: str, hours_val: float, date_str: str | None = None) -> None:
    """Append a {date: hours} JSON line to the target file."""
    file_path = prepare_path(file_str)
    date_key = validate_date(date_str)
    hours = round(float(hours_val), 1)

    if hours < 0:
        print("Error: hours cannot be negative.", file=sys.stderr)
        sys.exit(1)

    entry = {date_key: hours}
    with file_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def get_total_hours(file_str: str) -> float:
    """Sum all numeric hour values across all lines in the target file."""
    file_path = Path(file_str).expanduser()
    if not file_path.exists():
        print(f"Error: file not found: '{file_path}'.", file=sys.stderr)
        sys.exit(1)

    total = 0.0
    with file_path.open("r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"Warning: malformed JSON at line {line_num}: {exc}", file=sys.stderr)
                continue

            if isinstance(obj, dict):
                for val in obj.values():
                    if isinstance(val, (int, float)) and not isinstance(val, bool):
                        total = round(total + round(float(val), 1), 1)

    return total


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="CLI hours tracker using JSONL files (one JSON object per line)."
    )
    parser.add_argument(
        "--add",
        type=float,
        default=None,
        metavar="TIME",
        help="Time in hours to log (rounded to 1 decimal place)",
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to the target JSON file (required with --add)",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        metavar="YYYY-MM-DD",
        help="Optional date for --add (default: today)",
    )
    parser.add_argument(
        "--view-total-time",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to the JSON file to sum total hours",
    )
    return parser


def main() -> None:
    """Entry point for CLI execution."""
    parser = build_parser()
    args = parser.parse_args()

    if args.view_total_time:
        total = get_total_hours(args.view_total_time)
        print(f"Total hrs: {total:.1f}")
        return

    if args.add is not None:
        if not args.file:
            parser.error("--file is required when using --add.")
        add_entry(args.file, args.add, args.date)
        return

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
