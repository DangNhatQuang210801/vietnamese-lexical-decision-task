"""Export selected manual items with Vietnamese-friendly column names."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


INPUT_PATH = Path("data_sample") / "_processed" / "manual_selection_sheet (chọn tay).csv"
OUTPUT_PATH = Path("data_sample") / "_processed" / "danh_sach_da_chon_tieng_viet.csv"

COLUMN_RENAME = {
    "lexical_item": "muc_tu",
    "frequency": "tan_so",
    "log_frequency": "log_tan_so",
    "syllable_length": "so_am_tiet",
    "confidence": "do_tin_cay",
    "reason": "ly_do",
    "notes": "ghi_chu",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Filter keep == 1 and export selected items with Vietnamese column names."
    )
    parser.add_argument("--input", type=Path, default=INPUT_PATH, help="Manual selection CSV.")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH, help="Output CSV path.")
    return parser.parse_args()


def safe_print(text: str) -> None:
    """In an toàn khi terminal Windows không hỗ trợ đầy đủ Unicode."""
    encoding = sys.stdout.encoding or "utf-8"
    print(text.encode(encoding, errors="backslashreplace").decode(encoding))


def main() -> None:
    args = parse_args()

    # Đọc sheet chọn tay.
    df = pd.read_csv(args.input, encoding="utf-8-sig")

    if "keep" not in df.columns:
        raise ValueError("File input cần có cột 'keep'.")

    # Lọc các dòng được đánh dấu keep == 1.
    keep_numeric = pd.to_numeric(df["keep"], errors="coerce")
    selected = df[keep_numeric == 1].copy()

    # Chỉ giữ cột cần thiết nếu cột đó tồn tại.
    available_columns = [col for col in COLUMN_RENAME if col in selected.columns]
    selected = selected[available_columns].rename(columns=COLUMN_RENAME)

    # Sắp xếp để dễ kiểm tra thủ công.
    sort_columns = [col for col in ["so_am_tiet", "log_tan_so"] if col in selected.columns]
    if sort_columns:
        ascending = [True if col == "so_am_tiet" else False for col in sort_columns]
        selected = selected.sort_values(sort_columns, ascending=ascending)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    selected.to_csv(args.output, index=False, encoding="utf-8-sig")

    safe_print(f"Tổng số dòng đã chọn: {len(selected)}")
    safe_print("Số item theo từng so_am_tiet:")
    if "so_am_tiet" in selected.columns and not selected.empty:
        print(selected.groupby("so_am_tiet").size().to_string())
    else:
        safe_print("(không có item nào)")
    safe_print(f"Đã lưu: {args.output}")


if __name__ == "__main__":
    main()
