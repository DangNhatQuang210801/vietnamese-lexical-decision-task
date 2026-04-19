"""Finalize manually selected Vietnamese real-word candidates and diagnostics."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


DEFAULT_INPUT = Path("data_sample") / "_processed" / "manual_selection_sheet.csv"
DEFAULT_OUTPUT = Path("data_sample") / "_processed" / "final_realword_candidates_v1.csv"
DEFAULT_SUMMARY = Path("data_sample") / "_processed" / "final_realword_summary.txt"
DEFAULT_BOXPLOT = Path("data_sample") / "_processed" / "final_realword_logfreq_boxplot.png"

EXPECTED_LENGTHS = [1, 2, 3, 4]
TARGET_TOTAL_RANGE = (120, 160)
TARGET_PER_GROUP_RANGE = (30, 40)
MAX_GROUP_COUNT_GAP = 5
STRONG_CORRELATION_THRESHOLD = 0.40


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create final real-word candidate file from a filled manual sheet."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Filled manual_selection_sheet.csv path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output final_realword_candidates_v1.csv path.",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=DEFAULT_SUMMARY,
        help="Output final_realword_summary.txt path.",
    )
    parser.add_argument(
        "--boxplot",
        type=Path,
        default=DEFAULT_BOXPLOT,
        help="Optional boxplot output path if matplotlib is available.",
    )
    return parser.parse_args()


def normalize_keep(value: object) -> bool:
    """Chỉ nhận keep == 1; các giá trị khác xem như chưa chọn/không chọn."""
    if pd.isna(value):
        return False
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.notna(numeric):
        return numeric == 1
    text = str(value).strip().lower()
    return text in {"1", "yes", "y", "true", "keep"}


def load_selected(input_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Đọc sheet đã điền và lọc các dòng người review chọn keep == 1."""
    if not input_path.exists():
        raise FileNotFoundError(f"Manual selection sheet not found: {input_path}")

    df = pd.read_csv(input_path, encoding="utf-8-sig")
    if "keep" not in df.columns:
        raise ValueError("Manual sheet must contain a 'keep' column.")

    selected = df[df["keep"].map(normalize_keep)].copy()
    selected["frequency"] = pd.to_numeric(selected["frequency"], errors="coerce")
    selected["log_frequency"] = pd.to_numeric(selected["log_frequency"], errors="coerce")
    selected["syllable_length"] = pd.to_numeric(
        selected["syllable_length"], errors="coerce"
    ).astype("Int64")
    return df, selected


def group_frequency_stats(selected: pd.DataFrame) -> pd.DataFrame:
    """Tóm tắt số lượng và range log_frequency theo độ dài âm tiết."""
    if selected.empty:
        return pd.DataFrame(
            columns=["count", "min_log_frequency", "median_log_frequency", "max_log_frequency"]
        )

    stats = selected.groupby("syllable_length")["log_frequency"].agg(
        count="count",
        min_log_frequency="min",
        median_log_frequency="median",
        max_log_frequency="max",
    )
    return stats.reindex(EXPECTED_LENGTHS)


def compute_correlation(selected: pd.DataFrame) -> float | None:
    """Tính tương quan length-frequency để phát hiện collinearity."""
    usable = selected.dropna(subset=["syllable_length", "log_frequency"])
    if len(usable) < 3:
        return None
    return float(usable["syllable_length"].astype(float).corr(usable["log_frequency"]))


def balance_warnings(selected: pd.DataFrame, stats: pd.DataFrame, corr: float | None) -> list[str]:
    """Sinh cảnh báo về balance, không thay người review quyết định item."""
    warnings: list[str] = []
    total = len(selected)
    min_total, max_total = TARGET_TOTAL_RANGE
    min_group, max_group = TARGET_PER_GROUP_RANGE

    if total == 0:
        return [
            "No rows have keep == 1 yet. Fill the manual sheet before finalizing the stimulus set."
        ]

    if total < min_total or total > max_total:
        warnings.append(
            f"Total selected items ({total}) is outside the target range {min_total}-{max_total}."
        )

    counts = stats["count"].fillna(0).astype(int)
    for length in EXPECTED_LENGTHS:
        count = int(counts.get(length, 0))
        if count < min_group or count > max_group:
            warnings.append(
                f"Syllable length {length} has {count} items; target is about {min_group}-{max_group}."
            )

    if counts.max() - counts.min() > MAX_GROUP_COUNT_GAP:
        warnings.append(
            f"Group counts differ by {int(counts.max() - counts.min())}; consider rebalancing."
        )

    if corr is not None and abs(corr) >= STRONG_CORRELATION_THRESHOLD:
        warnings.append(
            f"syllable_length and log_frequency correlation is r={corr:.3f}; consider adjusting "
            "items to reduce frequency-length imbalance."
        )

    for length in EXPECTED_LENGTHS:
        row = stats.loc[length] if length in stats.index else None
        if row is None or pd.isna(row["count"]) or row["count"] < 2:
            warnings.append(
                f"Syllable length {length} has too few selected items to inspect frequency range."
            )
            continue
        spread = row["max_log_frequency"] - row["min_log_frequency"]
        if pd.notna(spread) and spread < 1.0:
            warnings.append(
                f"Syllable length {length} has narrow log_frequency spread ({spread:.2f})."
            )

    return warnings


def write_summary(
    summary_path: Path,
    selected: pd.DataFrame,
    stats: pd.DataFrame,
    corr: float | None,
    warnings: list[str],
    plot_message: str,
) -> None:
    """Viết report ngắn cho final set."""
    lines = [
        "Final Vietnamese real-word candidate summary",
        "============================================",
        "",
        f"Total selected items: {len(selected):,}",
        "",
        "Distribution and log_frequency range by syllable_length:",
    ]

    if selected.empty:
        lines.append("- No selected rows yet.")
    else:
        for length in EXPECTED_LENGTHS:
            if length not in stats.index or pd.isna(stats.loc[length, "count"]):
                lines.append(f"- {length} syllable(s): 0 items")
                continue
            row = stats.loc[length]
            lines.append(
                "- "
                f"{length} syllable(s): {int(row['count'])} items; "
                f"min={row['min_log_frequency']:.3f}, "
                f"median={row['median_log_frequency']:.3f}, "
                f"max={row['max_log_frequency']:.3f}"
            )

    lines.extend(["", "Frequency-length association:"])
    if corr is None:
        lines.append("- Not enough selected rows to compute correlation.")
    else:
        lines.append(f"- Pearson r = {corr:.3f}")

    lines.extend(["", "Warnings:"])
    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- No major balance warnings detected.")

    lines.extend(
        [
            "",
            "Suggestion:",
            "Use this output as a statistical check after human linguistic selection. "
            "If a group is under-filled, over-filled, or has a narrow frequency range, adjust "
            "the manual sheet and rerun this script. Do not use these diagnostics as a substitute "
            "for native-speaker lexical validation.",
            "",
            f"Plot status: {plot_message}",
            "",
        ]
    )

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n".join(lines), encoding="utf-8-sig")


def save_boxplot(selected: pd.DataFrame, boxplot_path: Path) -> str:
    """Tạo boxplot nếu matplotlib có sẵn."""
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return "matplotlib not installed; skipped boxplot."

    plot_df = selected.dropna(subset=["syllable_length", "log_frequency"])
    if plot_df.empty:
        return "no selected rows available; skipped boxplot."

    box_data = [
        plot_df.loc[plot_df["syllable_length"] == length, "log_frequency"].to_numpy()
        for length in EXPECTED_LENGTHS
    ]

    boxplot_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 6))
    plt.boxplot(box_data, tick_labels=[str(length) for length in EXPECTED_LENGTHS])
    plt.xlabel("syllable_length")
    plt.ylabel("log_frequency")
    plt.title("Final real-word log_frequency by syllable length")
    plt.tight_layout()
    plt.savefig(boxplot_path, dpi=160)
    plt.close()
    return f"saved {boxplot_path}"


def finalize(input_path: Path, output_path: Path, summary_path: Path, boxplot_path: Path) -> None:
    """Chạy toàn bộ bước finalize sau khi người dùng đã điền keep."""
    _, selected = load_selected(input_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    selected.to_csv(output_path, index=False, encoding="utf-8-sig")

    stats = group_frequency_stats(selected)
    corr = compute_correlation(selected)
    warnings = balance_warnings(selected, stats, corr)
    plot_message = save_boxplot(selected, boxplot_path)
    write_summary(summary_path, selected, stats, corr, warnings, plot_message)

    encoding = sys.stdout.encoding or "utf-8"

    def safe_text(value: object) -> str:
        return str(value).encode(encoding, errors="backslashreplace").decode(encoding)

    print("Final real-word candidate diagnostics complete.")
    print(f"Input manual sheet: {safe_text(input_path)}")
    print(f"Selected output: {safe_text(output_path)}")
    print(f"Summary: {safe_text(summary_path)}")
    print(f"Total selected: {len(selected):,}")
    if selected.empty:
        print("No rows selected yet. Fill keep == 1 in the manual sheet and rerun.")
    else:
        print(stats.to_string())
        if corr is not None:
            print(f"Pearson r(syllable_length, log_frequency): {corr:.3f}")
    print(plot_message)


def main() -> None:
    args = parse_args()
    finalize(args.input, args.output, args.summary, args.boxplot)


if __name__ == "__main__":
    main()
