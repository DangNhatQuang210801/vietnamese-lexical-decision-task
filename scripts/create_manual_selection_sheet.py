"""Create a manual review worksheet for Vietnamese LDT real-word selection."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_INPUT = Path("data_sample") / "_processed" / "candidate_shortlist_by_length.csv"
DEFAULT_OUTPUT = Path("data_sample") / "_processed" / "manual_selection_sheet.csv"

MANUAL_COLUMNS = ["keep", "confidence", "reason", "notes"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an editable manual selection sheet from the candidate shortlist."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Input candidate_shortlist_by_length.csv path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output manual_selection_sheet.csv path.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    return parser.parse_args()


def create_manual_sheet(input_path: Path, output_path: Path, force: bool = False) -> pd.DataFrame:
    """Tạo worksheet, giữ nguyên candidate và thêm cột cho người review."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input shortlist not found: {input_path}")

    if output_path.exists() and not force:
        raise FileExistsError(
            f"Output already exists: {output_path}. Use --force to overwrite intentionally."
        )

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    # Không quyết định tự động: các cột này để trống cho người đánh giá ngôn ngữ.
    for col in reversed(MANUAL_COLUMNS):
        if col in df.columns:
            df = df.drop(columns=[col])
        df.insert(0, col, "")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return df


def main() -> None:
    args = parse_args()
    df = create_manual_sheet(args.input, args.output, args.force)
    print("Manual selection sheet created.")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Rows: {len(df):,}")
    if "syllable_length" in df.columns:
        print("Rows by syllable_length:")
        print(df.groupby("syllable_length").size().to_string())
    print("Next step: fill keep with 1/0, confidence with high/mid/low, and add notes as needed.")


if __name__ == "__main__":
    main()
