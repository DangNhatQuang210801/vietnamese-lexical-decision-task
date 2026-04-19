"""Extract manually selected rows from manual_selection_sheet.csv."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


DEFAULT_INPUT = Path("data_sample") / "_processed" / "manual_selection_sheet.csv"
DEFAULT_OUTPUT = Path("data_sample") / "_processed" / "final_selected_items (kiểm tra).csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract rows where keep == 1 from a manual selection sheet."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Path to manual_selection_sheet.csv.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path for selected output CSV.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Đọc sheet đã review thủ công.
    df = pd.read_csv(args.input, encoding="utf-8-sig")

    if "keep" not in df.columns:
        raise ValueError("Input file must contain a 'keep' column.")

    # Chỉ giữ các dòng người review đánh dấu keep == 1.
    keep_numeric = pd.to_numeric(df["keep"], errors="coerce")
    df_selected = df[keep_numeric == 1].copy()

    # Giữ nguyên toàn bộ cột gốc và lưu file kết quả.
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df_selected.to_csv(args.output, index=False, encoding="utf-8-sig")

    print(f"Total selected rows: {len(df_selected)}")
    print("Rows per syllable_length:")
    if "syllable_length" in df_selected.columns and not df_selected.empty:
        print(df_selected.groupby("syllable_length").size().to_string())
    else:
        print("(none)")
    safe_output = str(args.output).encode(sys.stdout.encoding or "utf-8", errors="backslashreplace")
    print(f"Saved to: {safe_output.decode(sys.stdout.encoding or 'utf-8')}")


if __name__ == "__main__":
    main()
