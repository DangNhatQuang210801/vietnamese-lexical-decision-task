"""Build a filtered Vietnamese lexical candidate pool for LDT stimuli.

The pipeline reads corpus-derived n-gram frequency tables, applies transparent
rule-based filters, keeps uncertain cases for manual review, and samples a
frequency-balanced shortlist within each syllable-length group.
"""

from __future__ import annotations

import argparse
import math
import re
from collections import Counter
from pathlib import Path

import pandas as pd

# Editable filtering config

REQUIRED_FILES = {
    "all": "all_1to4gram_frequency.csv",
    1: "unigrams_frequency.csv",
    2: "bigrams_frequency.csv",
    3: "trigrams_frequency.csv",
    4: "fourgrams_frequency.csv",
}

OUTPUT_FILES = {
    "filtered": "candidate_pool_filtered.csv",
    "kept": "candidate_pool_kept_only.csv",
    "manual": "candidate_pool_manual_review.csv",
    "shortlist": "candidate_shortlist_by_length.csv",
    "summary": "candidate_summary.txt",
    "hist": "diagnostic_log_frequency_histogram_by_length.png",
    "box": "diagnostic_log_frequency_boxplot_by_length.png",
}

SHORTLIST_TARGET_PER_LENGTH = 80
SHORTLIST_MIN_PER_BIN = 4
SHORTLIST_BINS = 8
SHORTLIST_MIN_FREQUENCY_BY_LENGTH = {
    1: 30,
    2: 20,
    3: 10,
    4: 5,
}
RANDOM_SEED = 20260419

# Các từ chức năng không phù hợp làm stimulus lexical decision.
FUNCTION_WORDS = {
    "ai",
    "ấy",
    "bao",
    "bằng",
    "bởi",
    "cả",
    "các",
    "cái",
    "càng",
    "chỉ",
    "chưa",
    "cho",
    "chứ",
    "có",
    "còn",
    "cũng",
    "cùng",
    "của",
    "cứ",
    "do",
    "đã",
    "đang",
    "đâu",
    "đây",
    "đấy",
    "để",
    "đều",
    "đến",
    "đừng",
    "được",
    "gì",
    "giờ",
    "hay",
    "hãy",
    "hết",
    "hơn",
    "khi",
    "không",
    "là",
    "lại",
    "làm",
    "lên",
    "lúc",
    "mà",
    "mình",
    "một",
    "mỗi",
    "mọi",
    "này",
    "nên",
    "nếu",
    "ngay",
    "nhé",
    "như",
    "nhưng",
    "những",
    "nào",
    "nó",
    "nơi",
    "nữa",
    "ở",
    "phải",
    "qua",
    "ra",
    "rằng",
    "rất",
    "rồi",
    "quá",
    "sau",
    "sẽ",
    "sự",
    "ta",
    "tại",
    "theo",
    "thật",
    "thì",
    "tới",
    "trên",
    "trong",
    "từ",
    "và",
    "vài",
    "vào",
    "về",
    "vì",
    "vừa",
    "với",
    "ơi",
}

# Đại từ / deictic thường làm cụm phụ thuộc ngữ cảnh; không drop hết, nhưng flag.
CONTEXT_WORDS = {
    "anh",
    "bạn",
    "chị",
    "cháu",
    "cô",
    "con",
    "em",
    "họ",
    "mình",
    "nàng",
    "người",
    "nó",
    "ông",
    "tôi",
    "vợ",
}

# Các động từ/cấu trúc ở đầu cụm thường tạo phrase/clause hơn là danh từ.
VERB_LIKE_STARTS = {
    "ăn",
    "bảo",
    "biết",
    "bị",
    "bỏ",
    "cản",
    "chan",
    "chia",
    "chỉ",
    "chờ",
    "chọn",
    "coi",
    "có",
    "cố",
    "cưới",
    "cần",
    "đi",
    "đọc",
    "được",
    "gặp",
    "gây",
    "giữ",
    "giúp",
    "hiểu",
    "hỏi",
    "kể",
    "khuấy",
    "làm",
    "lấy",
    "luôn",
    "mang",
    "mua",
    "muốn",
    "nghĩ",
    "ngủ",
    "nói",
    "nhận",
    "sống",
    "thay",
    "thấy",
    "thăm",
    "thích",
    "thương",
    "trở",
    "về",
    "viết",
    "yêu",
}

# Những token cuối dễ là mảnh cụm hoặc chức năng chưa hoàn chỉnh.
FRAGMENT_ENDINGS = {
    "bằng",
    "bởi",
    "các",
    "chiếc",
    "của",
    "đàn",
    "đã",
    "đang",
    "để",
    "được",
    "hay",
    "giơ",
    "g",
    "gr",
    "b",
    "bảo",
    "chuyện",
    "khi",
    "linh",
    "mà",
    "mang",
    "mỗi",
    "nghiêm",
    "như",
    "nhưng",
    "những",
    "quan",
    "qua",
    "rằng",
    "sáng",
    "tháng",
    "theo",
    "thì",
    "trong",
    "tự",
    "tốt",
    "thư",
    "và",
    "va",
    "về",
    "vì",
    "với",
    "đối",
    "đưng",
}

# Danh sách nhỏ các named entities phổ biến trong corpus báo chí.
PROBABLE_NAMED_ENTITIES = {
    "anh",
    "hà nội",
    "hoa kỳ",
    "mỹ",
    "nhật",
    "châu á",
    "nghệ an",
    "pháp",
    "sài gòn",
    "tp hcm",
    "trung quốc",
    "việt nam",
}

# Một số n-gram xấu đã thấy từ kiểm tra thủ công ban đầu.
EXPLICIT_BAD_ITEMS = {
    "có thể",
    "cảm thấy",
    "cảm ơn",
    "đã được",
    "người đàn",
    "đọc những dòng tâm",
    "tình cảm của mình",
}

# Các cue này không đủ để drop, nhưng nên đưa vào manual review.
NON_NOUN_CUES = {
    "bao giờ",
    "bây giờ",
    "bao lâu",
    "như thế",
    "thế nào",
    "làm sao",
}

SUSPICIOUS_FOREIGN_TERMS = {
    "alvarez",
    "asin",
    "ceramic",
    "cocoa",
    "doggiedating",
    "gprs",
    "kaerntner",
    "lamy",
    "mouse",
    "nagakawa",
    "olive",
    "promotion",
    "skincare",
    "tailieuziliao",
    "tungsten",
    "valentine",
    "vienna",
}

UNIT_OR_CODE_TOKENS = {"b", "cm", "g", "gb", "kg", "kh", "ml"}

VIETNAMESE_ITEM_RE = re.compile(
    r"^[a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệ"
    r"ìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữự"
    r"ỳýỷỹỵđ]+(?: [a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệ"
    r"ìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữự"
    r"ỳýỷỹỵđ]+)*$"
)
VIETNAMESE_DIACRITIC_RE = re.compile(
    r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệ"
    r"ìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữự"
    r"ỳýỷỹỵđ]"
)
FOREIGN_LETTER_RE = re.compile(r"[fjwz]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Filter Vietnamese n-gram candidates for lexical decision stimuli."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data_sample") / "_processed",
        help="Folder containing the frequency CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Folder for output files. Defaults to --input-dir.",
    )
    parser.add_argument(
        "--shortlist-target",
        type=int,
        default=SHORTLIST_TARGET_PER_LENGTH,
        help="Target number of shortlist rows per syllable length.",
    )
    return parser.parse_args()


def read_csv_utf8(path: Path) -> pd.DataFrame:
    """Đọc CSV UTF-8/UTF-8-SIG và chuẩn hóa tên cột."""
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [col.strip() for col in df.columns]
    return df


def load_sources(input_dir: Path) -> tuple[pd.DataFrame, dict[int, pd.DataFrame]]:
    """Đọc tất cả file, nhưng dùng all_1to4gram làm nguồn chính."""
    all_path = input_dir / REQUIRED_FILES["all"]
    if not all_path.exists():
        raise FileNotFoundError(f"Missing main combined source: {all_path}")

    by_length: dict[int, pd.DataFrame] = {}
    for length in (1, 2, 3, 4):
        path = input_dir / REQUIRED_FILES[length]
        if not path.exists():
            raise FileNotFoundError(f"Missing length-specific source: {path}")
        by_length[length] = read_csv_utf8(path)

    combined = read_csv_utf8(all_path)
    combined["source_file"] = REQUIRED_FILES["all"]
    return combined, by_length


def normalize_item(value: object) -> str:
    """Chuẩn hóa khoảng trắng và chữ thường để so khớp ổn định."""
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    return re.sub(r"\s+", " ", text)


def source_membership(by_length: dict[int, pd.DataFrame]) -> dict[tuple[str, int], str]:
    """Ghi nhận item cũng xuất hiện trong file theo từng độ dài."""
    mapping: dict[tuple[str, int], str] = {}
    for length, df in by_length.items():
        for item in df["lexical_item"].map(normalize_item):
            mapping[(item, length)] = REQUIRED_FILES[length]
    return mapping


def validate_and_prepare(combined: pd.DataFrame, by_length: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """Chuẩn hóa kiểu dữ liệu và gắn source file đối chiếu."""
    expected = {"lexical_item", "frequency", "syllable_length", "log_frequency"}
    missing = expected - set(combined.columns)
    if missing:
        raise ValueError(f"Combined CSV is missing columns: {sorted(missing)}")

    df = combined.copy()
    df["lexical_item"] = df["lexical_item"].map(normalize_item)
    df["frequency"] = pd.to_numeric(df["frequency"], errors="coerce")
    df["syllable_length"] = pd.to_numeric(df["syllable_length"], errors="coerce").astype("Int64")
    df["log_frequency"] = pd.to_numeric(df["log_frequency"], errors="coerce")

    membership = source_membership(by_length)
    df["source_file"] = [
        membership.get((item, int(length)), REQUIRED_FILES["all"])
        if not pd.isna(length)
        else REQUIRED_FILES["all"]
        for item, length in zip(df["lexical_item"], df["syllable_length"], strict=False)
    ]
    return df


def is_probable_named_entity(item: str) -> bool:
    """Heuristic đơn giản cho địa danh/quốc danh phổ biến."""
    if item in PROBABLE_NAMED_ENTITIES:
        return True
    words = item.split()
    return len(words) >= 2 and item.endswith((" việt nam", " hà nội", " trung quốc"))


def evaluate_row(item: str, syllable_length: int | None, duplicate: bool) -> tuple[str, str, str]:
    """Áp luật lọc, trả về keep/drop + reason + warning."""
    reasons: list[str] = []
    warnings: list[str] = []

    words = item.split()
    observed_length = len(words)

    if not item:
        reasons.append("malformed_empty_item")
    elif not VIETNAMESE_ITEM_RE.match(item):
        reasons.append("malformed_non_vietnamese_or_punctuation")
    elif FOREIGN_LETTER_RE.search(item):
        reasons.append("malformed_foreign_letter")

    if syllable_length not in {1, 2, 3, 4}:
        reasons.append("invalid_syllable_length")
    elif observed_length != syllable_length:
        reasons.append("length_mismatch")

    if duplicate:
        reasons.append("duplicate_item")

    if item in EXPLICIT_BAD_ITEMS:
        reasons.append("explicit_bad_ngram")

    if item in SUSPICIOUS_FOREIGN_TERMS:
        reasons.append("probable_foreign_or_brand_term")

    if any(word in SUSPICIOUS_FOREIGN_TERMS for word in words):
        reasons.append("probable_foreign_or_brand_term")

    if any(word in UNIT_OR_CODE_TOKENS for word in words):
        reasons.append("unit_or_code_token")

    if observed_length == 1 and item in FUNCTION_WORDS:
        reasons.append("whole_item_function_word")

    if observed_length > 1:
        if words[0] in FUNCTION_WORDS or words[-1] in FUNCTION_WORDS:
            reasons.append("function_word_boundary")
        if words[-1] in FRAGMENT_ENDINGS:
            reasons.append("fragment_like_ending")
        if words[0] in VERB_LIKE_STARTS:
            reasons.append("clause_or_verb_like_start")
        if any(word in FUNCTION_WORDS for word in words[1:-1]):
            warnings.append("possible_function_phrase")
        if any(word in CONTEXT_WORDS for word in words):
            warnings.append("needs_manual_check")

    if is_probable_named_entity(item):
        reasons.append("probable_named_entity")

    # Không drop quá mạnh các trường hợp có thể không phải danh từ; chỉ flag cue rõ.
    if item in NON_NOUN_CUES:
        warnings.append("possible_non_noun")

    if (
        observed_length == 1
        and len(item) >= 4
        and not VIETNAMESE_DIACRITIC_RE.search(item)
        and item not in PROBABLE_NAMED_ENTITIES
    ):
        warnings.append("possible_named_entity_or_foreign")

    if observed_length >= 3 and words[-1] in {"tâm", "dòng", "người", "nỗi", "niềm"}:
        warnings.append("possible_fragment")

    if observed_length >= 2 and len(set(words)) < observed_length:
        warnings.append("repeated_syllable")

    keep_status = "drop" if reasons else "keep"
    reason_text = ";".join(reasons) if reasons else "kept_after_rule_filter"
    warning_text = ";".join(dict.fromkeys(warnings))
    return keep_status, reason_text, warning_text


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Áp toàn bộ filter và giữ audit trail cho từng item."""
    out = df.copy()
    duplicated = out.duplicated(subset=["lexical_item"], keep="first")

    decisions = [
        evaluate_row(
            item=row.lexical_item,
            syllable_length=None if pd.isna(row.syllable_length) else int(row.syllable_length),
            duplicate=bool(is_dup),
        )
        for row, is_dup in zip(out.itertuples(index=False), duplicated, strict=False)
    ]

    out[["keep_status", "filter_reason", "warning_flag"]] = pd.DataFrame(
        decisions, index=out.index
    )
    return out


def sample_shortlist(kept: pd.DataFrame, target_per_length: int) -> pd.DataFrame:
    """Lấy mẫu theo quantile log_frequency để tránh chỉ chọn item tần suất cao."""
    sampled_frames: list[pd.DataFrame] = []

    for length in (1, 2, 3, 4):
        group = kept[kept["syllable_length"] == length].copy()
        group = group.dropna(subset=["log_frequency", "frequency"])
        if group.empty:
            continue

        # Shortlist ưu tiên item sạch hơn: không warning và không quá hiếm.
        min_frequency = SHORTLIST_MIN_FREQUENCY_BY_LENGTH.get(length, 3)
        preferred = group[
            group["warning_flag"].fillna("").eq("")
            & (group["frequency"] >= min_frequency)
        ].copy()
        if len(preferred) >= min(target_per_length, len(group)):
            group = preferred

        bins = min(SHORTLIST_BINS, max(1, group["log_frequency"].nunique()))
        group["frequency_bin"] = pd.qcut(
            group["log_frequency"].rank(method="first"),
            q=bins,
            labels=False,
            duplicates="drop",
        )

        bin_count = max(1, group["frequency_bin"].nunique())
        per_bin = max(SHORTLIST_MIN_PER_BIN, math.ceil(target_per_length / bin_count))

        pieces = []
        for _, bin_df in group.groupby("frequency_bin", observed=True):
            sample_n = min(per_bin, len(bin_df))
            pieces.append(bin_df.sample(n=sample_n, random_state=RANDOM_SEED))

        sampled = pd.concat(pieces, ignore_index=True)
        if len(sampled) > target_per_length:
            sampled = sampled.sample(n=target_per_length, random_state=RANDOM_SEED)

        sampled = sampled.sort_values(["syllable_length", "log_frequency", "lexical_item"])
        sampled_frames.append(sampled)

    if not sampled_frames:
        return kept.iloc[0:0].copy()

    shortlist = pd.concat(sampled_frames, ignore_index=True)
    return shortlist.drop(columns=["frequency_bin"], errors="ignore")


def correlation_note(kept: pd.DataFrame) -> tuple[float | None, str]:
    """Tính tương quan syllable_length-log_frequency cho cảnh báo collinearity."""
    usable = kept.dropna(subset=["syllable_length", "log_frequency"])
    if len(usable) < 3:
        return None, "Not enough kept items to estimate correlation."

    corr = float(usable["syllable_length"].astype(float).corr(usable["log_frequency"]))
    strength = "weak"
    if abs(corr) >= 0.70:
        strength = "strong"
    elif abs(corr) >= 0.40:
        strength = "moderate"
    return corr, f"Pearson r = {corr:.3f}; association appears {strength}."


def examples(series: pd.Series, n: int = 12) -> str:
    values = [str(value) for value in series.dropna().head(n)]
    return ", ".join(values) if values else "(none)"


def write_summary(
    output_path: Path,
    audited: pd.DataFrame,
    kept: pd.DataFrame,
    manual: pd.DataFrame,
    shortlist: pd.DataFrame,
) -> None:
    """Viết báo cáo ngắn để phục vụ review thủ công."""
    removed = audited[audited["keep_status"] == "drop"]
    reason_counts = Counter()
    for reason_text in removed["filter_reason"].fillna(""):
        for reason in reason_text.split(";"):
            if reason:
                reason_counts[reason] += 1

    kept_by_length = kept["syllable_length"].value_counts().sort_index()
    shortlist_by_length = shortlist["syllable_length"].value_counts().sort_index()
    corr, corr_text = correlation_note(kept)

    lines = [
        "Vietnamese LDT candidate-pool filtering summary",
        "================================================",
        "",
        f"Total items read from combined source: {len(audited):,}",
        f"Items kept after automatic filtering: {len(kept):,}",
        f"Items dropped by automatic filtering: {len(removed):,}",
        f"Items flagged for manual review: {len(manual):,}",
        "",
        "Items removed by filter:",
    ]

    if reason_counts:
        for reason, count in reason_counts.most_common():
            lines.append(f"- {reason}: {count:,}")
    else:
        lines.append("- (none)")

    lines.extend(["", "Number kept by syllable length:"])
    for length in (1, 2, 3, 4):
        lines.append(f"- {length} syllable(s): {int(kept_by_length.get(length, 0)):,}")

    lines.extend(["", "Shortlist size by syllable length:"])
    for length in (1, 2, 3, 4):
        lines.append(f"- {length} syllable(s): {int(shortlist_by_length.get(length, 0)):,}")

    lines.extend(
        [
            "",
            "Examples of removed items:",
            examples(removed["lexical_item"]),
            "",
            "Examples of uncertain kept items:",
            examples(manual["lexical_item"]),
            "",
            "Frequency-length association in filtered pool:",
            corr_text,
        ]
    )

    if corr is not None and abs(corr) >= 0.40:
        lines.append(
            "Note: frequency and syllable length are still meaningfully associated; "
            "final stimulus selection should explicitly match or model frequency within length."
        )
    else:
        lines.append(
            "Note: no severe global collinearity is apparent in the filtered pool, "
            "but final hand selection should still balance log_frequency within each length."
        )

    min_shortlist = shortlist_by_length.min() if not shortlist_by_length.empty else 0
    usable_note = (
        "The filtered pool looks usable for manual lexical selection toward a 120-160 "
        "real-word stimulus set, because each syllable-length group has enough candidates "
        "and the shortlist samples across log-frequency ranges."
        if min_shortlist >= 60 and kept_by_length.reindex([1, 2, 3, 4], fill_value=0).min() >= 60
        else "The pool may be thin for at least one syllable length; manual review should check "
        "whether enough true lexical nouns remain before pseudoword construction."
    )

    lines.extend(
        [
            "",
            "Interpretation:",
            usable_note,
            "Automatic filtering is intentionally conservative: warning flags are not final "
            "linguistic judgments, and all shortlisted items still need native-speaker/manual review.",
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8-sig")


def save_plots(kept: pd.DataFrame, output_dir: Path) -> list[str]:
    """Xuất diagnostic plots nếu matplotlib có sẵn."""
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return ["matplotlib not installed; skipped diagnostic plots."]

    messages: list[str] = []
    plot_df = kept.dropna(subset=["log_frequency", "syllable_length"]).copy()
    if plot_df.empty:
        return ["no kept rows available; skipped diagnostic plots."]

    plt.figure(figsize=(10, 6))
    for length in (1, 2, 3, 4):
        vals = plot_df.loc[plot_df["syllable_length"] == length, "log_frequency"]
        if not vals.empty:
            plt.hist(vals, bins=30, alpha=0.45, label=f"{length} syllable(s)")
    plt.xlabel("log_frequency")
    plt.ylabel("candidate count")
    plt.title("Log-frequency distribution by syllable length")
    plt.legend()
    plt.tight_layout()
    hist_path = output_dir / OUTPUT_FILES["hist"]
    plt.savefig(hist_path, dpi=160)
    plt.close()
    messages.append(f"saved {hist_path}")

    box_data = [
        plot_df.loc[plot_df["syllable_length"] == length, "log_frequency"].to_numpy()
        for length in (1, 2, 3, 4)
    ]
    plt.figure(figsize=(8, 6))
    plt.boxplot(box_data, labels=["1", "2", "3", "4"])
    plt.xlabel("syllable_length")
    plt.ylabel("log_frequency")
    plt.title("Log-frequency by syllable length")
    plt.tight_layout()
    box_path = output_dir / OUTPUT_FILES["box"]
    plt.savefig(box_path, dpi=160)
    plt.close()
    messages.append(f"saved {box_path}")

    return messages


def main() -> None:
    args = parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir or input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    combined, by_length = load_sources(input_dir)
    prepared = validate_and_prepare(combined, by_length)
    audited = apply_filters(prepared)

    ordered_cols = [
        "lexical_item",
        "frequency",
        "log_frequency",
        "syllable_length",
        "source_file",
        "keep_status",
        "filter_reason",
        "warning_flag",
    ]
    audited = audited[ordered_cols]
    kept = audited[audited["keep_status"] == "keep"].copy()
    manual = kept[kept["warning_flag"].fillna("").ne("")].copy()
    shortlist = sample_shortlist(kept, args.shortlist_target)

    audited.to_csv(output_dir / OUTPUT_FILES["filtered"], index=False, encoding="utf-8-sig")
    kept.to_csv(output_dir / OUTPUT_FILES["kept"], index=False, encoding="utf-8-sig")
    manual.to_csv(output_dir / OUTPUT_FILES["manual"], index=False, encoding="utf-8-sig")
    shortlist.to_csv(output_dir / OUTPUT_FILES["shortlist"], index=False, encoding="utf-8-sig")
    write_summary(output_dir / OUTPUT_FILES["summary"], audited, kept, manual, shortlist)
    plot_messages = save_plots(kept, output_dir)

    corr, corr_text = correlation_note(kept)
    print("Candidate filtering complete.")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Total read: {len(audited):,}")
    print(f"Kept: {len(kept):,}")
    print(f"Manual-review flagged: {len(manual):,}")
    print(f"Shortlist size: {len(shortlist):,}")
    print(corr_text)
    for message in plot_messages:
        print(message)
    print(
        "Interpretation: the current corpus outputs are suitable for moving to manual "
        "lexical selection, provided the shortlist is checked for true lexical validity, "
        "noun-likeness, and frequency balance before pseudoword construction."
    )


if __name__ == "__main__":
    main()
