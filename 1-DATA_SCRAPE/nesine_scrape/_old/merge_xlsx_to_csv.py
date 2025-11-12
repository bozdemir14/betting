"""Merge fixture XLSX files into consolidated CSV and XLSX outputs with a season column."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover - guards against missing optional dependency
    raise SystemExit("pandas is required for this script. Install it with 'pip install pandas'.") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge XLSX files into CSV/XLSX outputs and add a season column derived from file names.",
    )
    parser.add_argument(
        "input_glob",
        nargs="?",
        default="fikstur_tum_ligler_*.xlsx",
        help="Glob pattern for input XLSX files (default: %(default)s)",
    )
    parser.add_argument(
        "--output",
        default="csv/fikstur_tum_ligler_all_seasons.csv",
        help="Path for the merged CSV output (default: %(default)s)",
    )
    return parser.parse_args()


def season_from_name(path: Path) -> str:
    match = re.search(r"(\d{4})-(\d{4})", path.stem)
    if not match:
        raise ValueError(f"Could not find season years in file name: {path.name}")
    start_year, end_year = match.groups()
    return f"{start_year}-{end_year[-2:]}"


def main() -> None:
    args = parse_args()
    base_dir = Path(__file__).resolve().parent
    xlsx_paths = sorted(base_dir.glob(args.input_glob))

    if not xlsx_paths:
        raise SystemExit("No XLSX files matched the given pattern.")

    frames = []
    for path in xlsx_paths:
        season = season_from_name(path)
        df = pd.read_excel(path)
        df.insert(0, "season_year", season)
        frames.append(df)

    merged = pd.concat(frames, ignore_index=True)

    output_path = (base_dir / args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(output_path, index=False)

    if output_path.suffix:
        excel_output_path = output_path.with_suffix(".xlsx")
    else:
        excel_output_path = output_path.parent / f"{output_path.name}.xlsx"

    merged.to_excel(excel_output_path, index=False)
    print(f"Merged {len(xlsx_paths)} files into {output_path} and {excel_output_path}")


if __name__ == "__main__":
    main()
