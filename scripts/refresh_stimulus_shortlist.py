"""Refresh the Vietnamese LDT shortlist from the larger kept candidate pool."""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

import pandas as pd


DEFAULT_INPUT_DIR = Path("data_sample") / "_processed"
DEFAULT_KEPT = "candidate_pool_kept_only.csv"
DEFAULT_MANUAL_REVIEW = "candidate_pool_manual_review.csv"
DEFAULT_SHORTLIST = "candidate_shortlist_by_length.csv"
DEFAULT_MANUAL_SHEET = "manual_selection_sheet (chọn tay).csv"
DEFAULT_REPORT = "candidate_shortlist_refresh_summary.txt"

TARGET_PER_LENGTH = 60
FREQUENCY_BINS = 8
RANDOM_SEED = 20260419
MIN_FREQUENCY_BY_LENGTH = {
    1: 10,
    2: 10,
    3: 5,
    4: 3,
}

BASE_COLUMNS = [
    "lexical_item",
    "frequency",
    "log_frequency",
    "syllable_length",
    "source_file",
    "keep_status",
    "filter_reason",
    "warning_flag",
]
MANUAL_COLUMNS = ["keep", "confidence", "reason", "notes"]


# =====================
# Editable lexical rules
# =====================

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
    "cho",
    "chưa",
    "chứ",
    "có",
    "còn",
    "cùng",
    "cũng",
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
    "nào",
    "này",
    "nên",
    "nếu",
    "ngay",
    "nhé",
    "như",
    "nhưng",
    "những",
    "nó",
    "nơi",
    "nữa",
    "ở",
    "phải",
    "qua",
    "quá",
    "ra",
    "rằng",
    "rất",
    "rồi",
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
    "tuy",
    "và",
    "vài",
    "vào",
    "về",
    "vì",
    "vừa",
    "với",
    "ơi",
    "nay",
    "nhiên",
}

CONTEXT_WORDS = {
    "anh",
    "bạn",
    "cháu",
    "chị",
    "cô",
    "con",
    "em",
    "họ",
    "mình",
    "nàng",
    "nó",
    "ông",
    "tôi",
    "vợ",
}

VERB_LIKE_WORDS = {
    "ăn",
    "bảo",
    "biết",
    "bị",
    "bỏ",
    "cảm",
    "chia",
    "chiếm",
    "chờ",
    "chọn",
    "coi",
    "cưới",
    "đi",
    "đọc",
    "gặp",
    "gây",
    "giữ",
    "giúp",
    "hiểu",
    "hỏi",
    "khám",
    "kể",
    "lấy",
    "mang",
    "mua",
    "muốn",
    "nấu",
    "nghĩ",
    "ngủ",
    "nói",
    "nhận",
    "sửa",
    "sống",
    "thấy",
    "thích",
    "thương",
    "tìm",
    "trở",
    "viết",
    "yêu",
}

QUANTITY_WORDS = {
    "bát",
    "bộ",
    "cái",
    "chiếc",
    "chục",
    "gam",
    "gói",
    "kg",
    "khoảng",
    "lần",
    "lít",
    "muỗng",
    "nghìn",
    "nhiều",
    "phần",
    "số",
    "tách",
    "thìa",
    "triệu",
    "vài",
}

FOREIGN_OR_CODE_WORDS = {
    "alert",
    "baby",
    "blog",
    "cm",
    "c",
    "contactus",
    "cookie",
    "download",
    "email",
    "g",
    "gb",
    "gr",
    "h",
    "html",
    "internet",
    "kh",
    "login",
    "ml",
    "online",
    "password",
    "sex",
    "shop",
    "url",
    "usd",
    "valentine",
    "web",
}

RELATIONSHIP_DRAMA_WORDS = {
    "bạn gái",
    "bạn trai",
    "chia tay",
    "chồng",
    "gia đình",
    "ghen",
    "hạnh phúc",
    "hôn nhân",
    "ly hôn",
    "ngoại tình",
    "người yêu",
    "tâm sự",
    "tình cảm",
    "tình yêu",
    "trai",
    "gái",
    "vợ",
}

FRAGMENT_EDGE_WORDS = {
    "ban",
    "bán",
    "bắt",
    "cao",
    "can",
    "chấn",
    "chính",
    "đại",
    "gắn",
    "gần",
    "gia",
    "gọn",
    "góp",
    "giống",
    "khám",
    "khuyến",
    "lớn",
    "mặc",
    "nấu",
    "nội",
    "nguyên",
    "sản",
    "sinh",
    "thông",
    "thấy",
    "thế",
    "thiết",
    "tiếp",
    "tim",
    "tuần",
    "trẻ",
    "trứng",
    "xong",
    "vàng",
    "vấn",
    "xã",
    "cà",
}

SECTION_OR_WEB_WORDS = {
    "ban",
    "biên",
    "mục",
    "trang",
    "visitor",
}

PREFERRED_NOUN_CUES = {
    "an ninh",
    "bảo hiểm",
    "bệnh viện",
    "chính phủ",
    "chính sách",
    "công nghệ",
    "công nghiệp",
    "công ty",
    "cơ quan",
    "dân số",
    "dịch vụ",
    "doanh nghiệp",
    "giáo dục",
    "giao thông",
    "hệ thống",
    "khoa học",
    "kinh tế",
    "lao động",
    "luật pháp",
    "môi trường",
    "ngân hàng",
    "nghệ thuật",
    "nhà nước",
    "pháp luật",
    "sản phẩm",
    "sản xuất",
    "thị trường",
    "thông tin",
    "thương mại",
    "truyền thông",
    "trường học",
    "văn hóa",
    "xã hội",
    "y tế",
}

NOUNISH_TOKENS = {
    "án",
    "báo",
    "bệnh",
    "biển",
    "cầu",
    "cây",
    "cửa",
    "dân",
    "dịch",
    "đất",
    "đời",
    "giá",
    "hàng",
    "học",
    "hội",
    "hợp",
    "khoa",
    "liệu",
    "luật",
    "lực",
    "máy",
    "môi",
    "ngành",
    "ngân",
    "nghệ",
    "nghiệp",
    "nhà",
    "nước",
    "pháp",
    "phẩm",
    "quyền",
    "rừng",
    "sách",
    "sản",
    "sinh",
    "tế",
    "thống",
    "tin",
    "trị",
    "trường",
    "tuyến",
    "viện",
    "vật",
    "xã",
    "xe",
}

ONE_SYLLABLE_NOUNISH = {
    "áo",
    "bàn",
    "báo",
    "bệnh",
    "biển",
    "bút",
    "cá",
    "cầu",
    "cây",
    "chợ",
    "cỏ",
    "cốc",
    "cửa",
    "đá",
    "đất",
    "đèn",
    "đường",
    "ghế",
    "gió",
    "hoa",
    "lá",
    "lớp",
    "luật",
    "máy",
    "mắt",
    "mũ",
    "núi",
    "nước",
    "rừng",
    "sách",
    "sông",
    "tay",
    "thuốc",
    "tiền",
    "trường",
    "vải",
    "viện",
    "xe",
}

DOMAIN_KEYWORDS = {
    "institution": {"chính", "pháp", "luật", "quyền", "nhà", "nước", "cơ", "quan"},
    "education": {"giáo", "dục", "học", "sinh", "trường", "khoa"},
    "health": {"bệnh", "viện", "thuốc", "y", "tế", "sức", "khỏe"},
    "economy": {"kinh", "tế", "thị", "trường", "ngân", "hàng", "doanh", "nghiệp"},
    "technology": {"công", "nghệ", "thông", "tin", "máy", "điện", "hệ", "thống"},
    "nature": {"đất", "nước", "rừng", "biển", "sông", "núi", "cây", "hoa"},
    "object": {"áo", "bàn", "ghế", "sách", "xe", "cửa", "đèn", "máy"},
    "abstract": {"văn", "hóa", "nghệ", "thuật", "tư", "tưởng", "giá", "trị"},
}

VIETNAMESE_RE = re.compile(
    r"^[a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệ"
    r"ìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữự"
    r"ỳýỷỹỵđ]+(?: [a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệ"
    r"ìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữự"
    r"ỳýỷỹỵđ]+)*$"
)
FOREIGN_LETTER_RE = re.compile(r"[fjwz]")
VIETNAMESE_DIACRITIC_RE = re.compile(
    r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệ"
    r"ìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữự"
    r"ỳýỷỹỵđ]"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild a cleaner stimulus shortlist.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help="Folder containing candidate_pool_kept_only.csv.",
    )
    parser.add_argument(
        "--target-per-length",
        type=int,
        default=TARGET_PER_LENGTH,
        help="Number of shortlist items per syllable length.",
    )
    return parser.parse_args()


def normalize_item(value: object) -> str:
    """Chuẩn hóa chữ thường và khoảng trắng."""
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip().lower())


def contains_phrase(item: str, phrases: set[str]) -> bool:
    return any(phrase in item for phrase in phrases)


def lexical_domain(words: list[str]) -> str:
    """Gán domain thô để tăng đa dạng ngữ nghĩa khi lấy mẫu."""
    word_set = set(words)
    best_domain = "other"
    best_count = 0
    for domain, keywords in DOMAIN_KEYWORDS.items():
        count = len(word_set & keywords)
        if count > best_count:
            best_domain = domain
            best_count = count
    return best_domain


def passes_strict_rules(row: pd.Series) -> tuple[bool, str]:
    """Loại mạnh các n-gram giống mảnh câu/cụm thiếu ổn định."""
    item = normalize_item(row["lexical_item"])
    words = item.split()
    length = int(row["syllable_length"])
    warning = "" if pd.isna(row.get("warning_flag")) else str(row.get("warning_flag")).strip()
    min_frequency = MIN_FREQUENCY_BY_LENGTH.get(length, 5)

    if not item:
        return False, "empty_item"
    if len(words) != length:
        return False, "length_mismatch"
    if not VIETNAMESE_RE.match(item):
        return False, "malformed_or_punctuation"
    if FOREIGN_LETTER_RE.search(item):
        return False, "foreign_letter"
    if any(word in FOREIGN_OR_CODE_WORDS for word in words):
        return False, "foreign_or_code_token"
    if any(word in SECTION_OR_WEB_WORDS for word in words):
        return False, "section_or_web_fragment"
    if any(len(word) == 1 for word in words):
        return False, "single_letter_token"
    if float(row["frequency"]) < min_frequency:
        return False, "too_rare_for_refresh_shortlist"
    if length == 1 and len(item) >= 5 and not VIETNAMESE_DIACRITIC_RE.search(item):
        return False, "possible_foreign_or_name"

    # Ưu tiên item không bị flag ở pipeline cũ.
    if warning:
        return False, "old_warning_flag"

    if item in FUNCTION_WORDS:
        return False, "function_word"
    if any(word in FUNCTION_WORDS for word in words):
        return False, "contains_function_word"
    if any(word in CONTEXT_WORDS for word in words):
        return False, "context_dependent_word"
    if any(word in QUANTITY_WORDS for word in words):
        return False, "quantity_phrase"
    if contains_phrase(item, RELATIONSHIP_DRAMA_WORDS):
        return False, "relationship_drama_theme"
    if words[0] in FRAGMENT_EDGE_WORDS or words[-1] in FRAGMENT_EDGE_WORDS:
        return False, "fragment_edge_word"

    # Drop nhiều verb phrase, nhưng giữ vài compound lexicalized qua cue danh từ.
    item_has_preferred_cue = contains_phrase(item, PREFERRED_NOUN_CUES)
    if length >= 2 and any(word in VERB_LIKE_WORDS for word in words):
        return False, "verb_like_expression"

    if length >= 2:
        nounish = item_has_preferred_cue or words[0] in NOUNISH_TOKENS or words[-1] in NOUNISH_TOKENS
        if not nounish:
            return False, "weak_noun_likeness"
        if words[-1] in {"cách", "chuyện", "điều", "kiểu", "lúc", "nỗi", "phần", "việc"}:
            return False, "fragment_like_ending"
    else:
        if item not in ONE_SYLLABLE_NOUNISH and item not in NOUNISH_TOKENS:
            return False, "weak_one_syllable_noun_likeness"

    if len(set(words)) < len(words):
        return False, "repeated_syllable"

    return True, "strict_keep"


def score_candidate(row: pd.Series) -> float:
    """Chấm điểm ưu tiên noun-like, domain đa dạng, và frequency không quá cực đoan."""
    item = normalize_item(row["lexical_item"])
    words = item.split()
    length = int(row["syllable_length"])
    freq = float(row["frequency"])
    score = 0.0

    if contains_phrase(item, PREFERRED_NOUN_CUES):
        score += 4.0
    if words[0] in NOUNISH_TOKENS:
        score += 1.5
    if words[-1] in NOUNISH_TOKENS:
        score += 1.5
    if length == 1 and item in ONE_SYLLABLE_NOUNISH:
        score += 3.0
    if lexical_domain(words) != "other":
        score += 2.0

    # Ưu tiên tần suất vừa/khá, không chỉ top.
    if freq >= 10:
        score += 1.0
    if freq >= 30:
        score += 0.5
    if length >= 3 and freq >= 5:
        score += 0.5

    # Hạn chế everyday relationship/life-talk còn sót lại.
    if any(word in {"đời", "nhà"} for word in words) and lexical_domain(words) == "other":
        score -= 1.0

    return score


def load_candidates(input_dir: Path) -> pd.DataFrame:
    """Đọc pool chính; secondary source chỉ để kiểm tra tồn tại nếu cần mở rộng sau."""
    kept_path = input_dir / DEFAULT_KEPT
    if not kept_path.exists():
        raise FileNotFoundError(f"Missing main source: {kept_path}")

    df = pd.read_csv(kept_path, encoding="utf-8-sig")
    missing = set(BASE_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in {kept_path}: {sorted(missing)}")

    # Chuẩn hóa kiểu dữ liệu.
    df = df[BASE_COLUMNS].copy()
    df["lexical_item"] = df["lexical_item"].map(normalize_item)
    df["frequency"] = pd.to_numeric(df["frequency"], errors="coerce")
    df["log_frequency"] = pd.to_numeric(df["log_frequency"], errors="coerce")
    df["syllable_length"] = pd.to_numeric(df["syllable_length"], errors="coerce").astype("Int64")
    return df.dropna(subset=["frequency", "log_frequency", "syllable_length"])


def strict_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Áp strict filter và giữ lý do nội bộ để viết report."""
    decisions = df.apply(passes_strict_rules, axis=1, result_type="expand")
    decisions.columns = ["strict_keep", "strict_reason"]
    out = pd.concat([df.reset_index(drop=True), decisions.reset_index(drop=True)], axis=1)
    out = out[out["strict_keep"]].copy()
    out["domain"] = out["lexical_item"].map(lambda item: lexical_domain(item.split()))
    out["quality_score"] = out.apply(score_candidate, axis=1)
    return out


def take_diverse_bin_sample(bin_df: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    """Lấy mẫu trong một frequency bin, giới hạn domain để bớt hẹp ngữ nghĩa."""
    if len(bin_df) <= n:
        return bin_df

    chosen_parts: list[pd.DataFrame] = []
    remaining = bin_df.sort_values(
        ["quality_score", "frequency", "lexical_item"], ascending=[False, False, True]
    )

    per_domain_cap = max(1, math.ceil(n / 3))
    for _, domain_df in remaining.groupby("domain", sort=False):
        take_n = min(per_domain_cap, len(domain_df), max(0, n - sum(len(p) for p in chosen_parts)))
        if take_n > 0:
            chosen_parts.append(domain_df.head(take_n))
        if sum(len(p) for p in chosen_parts) >= n:
            break

    chosen = pd.concat(chosen_parts, ignore_index=True) if chosen_parts else remaining.iloc[0:0]
    if len(chosen) < n:
        chosen_items = set(chosen["lexical_item"])
        filler = remaining[~remaining["lexical_item"].isin(chosen_items)].head(n - len(chosen))
        chosen = pd.concat([chosen, filler], ignore_index=True)

    return chosen.head(n)


def build_shortlist(filtered: pd.DataFrame, target_per_length: int) -> pd.DataFrame:
    """Chọn cân bằng theo length và trải đều theo log_frequency."""
    parts: list[pd.DataFrame] = []

    for length in (1, 2, 3, 4):
        group = filtered[filtered["syllable_length"] == length].copy()
        if group.empty:
            continue

        # Tránh để nhóm dài bị thống trị bởi hapax/near-hapax fragment.
        if length >= 3:
            stronger = group[group["frequency"] >= (5 if length == 4 else 6)].copy()
            if len(stronger) >= target_per_length:
                group = stronger

        bins = min(FREQUENCY_BINS, group["log_frequency"].nunique())
        group["freq_bin"] = pd.qcut(
            group["log_frequency"].rank(method="first"),
            q=bins,
            labels=False,
            duplicates="drop",
        )
        bin_count = max(1, group["freq_bin"].nunique())
        per_bin = math.ceil(target_per_length / bin_count)

        bin_parts: list[pd.DataFrame] = []
        for _, bin_df in group.groupby("freq_bin", observed=True):
            bin_parts.append(take_diverse_bin_sample(bin_df, per_bin, RANDOM_SEED))

        selected = pd.concat(bin_parts, ignore_index=True)
        if len(selected) > target_per_length:
            selected = selected.sort_values(
                ["quality_score", "frequency", "lexical_item"],
                ascending=[False, False, True],
            ).head(target_per_length)

        selected = selected.sort_values(["syllable_length", "log_frequency", "lexical_item"])
        parts.append(selected)

    shortlist = pd.concat(parts, ignore_index=True)
    return shortlist[BASE_COLUMNS]


def create_manual_sheet(shortlist: pd.DataFrame) -> pd.DataFrame:
    """Tạo sheet chọn tay, để trống quyết định của người review."""
    sheet = shortlist[BASE_COLUMNS].copy()
    for col in MANUAL_COLUMNS:
        sheet[col] = ""
    return sheet[BASE_COLUMNS + MANUAL_COLUMNS]


def write_report(path: Path, shortlist: pd.DataFrame, filtered: pd.DataFrame) -> None:
    """Viết báo cáo refresh ngắn."""
    stats = shortlist.groupby("syllable_length")["log_frequency"].agg(["count", "min", "median", "max"])
    domain_counts = shortlist.assign(
        domain=shortlist["lexical_item"].map(lambda item: lexical_domain(normalize_item(item).split()))
    )["domain"].value_counts()

    lines = [
        "Candidate shortlist refresh summary",
        "===================================",
        "",
        f"Strict-filtered source size: {len(filtered):,}",
        f"New shortlist size: {len(shortlist):,}",
        "",
        "Items per syllable length and log_frequency range:",
    ]
    for length in (1, 2, 3, 4):
        if length not in stats.index:
            lines.append(f"- {length} syllable(s): 0 items")
            continue
        row = stats.loc[length]
        lines.append(
            f"- {length} syllable(s): {int(row['count'])} items; "
            f"min={row['min']:.3f}, median={row['median']:.3f}, max={row['max']:.3f}"
        )

    lines.extend(
        [
            "",
            "Semantic-domain mix in shortlist:",
        ]
    )
    for domain, count in domain_counts.items():
        lines.append(f"- {domain}: {count}")

    lines.extend(
        [
            "",
            "Lexical cleanliness comment:",
            "The refreshed shortlist is stricter than the previous shortlist: it starts from "
            "candidate_pool_kept_only.csv, removes old warning-flag items, and excludes many "
            "function-word, verb-like, quantity, foreign/code, context-dependent, and relationship-drama expressions.",
            "",
            "Semantic diversity comment:",
            "The sampler uses coarse semantic domains and per-bin domain caps, so the shortlist should be less concentrated "
            "in romance/family/everyday relationship talk and should contain more institution, education, health, economy, "
            "technology, nature/object, and abstract/cultural candidates.",
            "",
            "Manual-selection comment:",
            "This shortlist should be easier to review manually, but it is still not a final stimulus set. "
            "Native-speaker/manual lexical validation remains required before finalizing real words and constructing pseudowords.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8-sig")


def main() -> None:
    args = parse_args()
    input_dir = args.input_dir

    candidates = load_candidates(input_dir)
    filtered = strict_filter(candidates)
    shortlist = build_shortlist(filtered, args.target_per_length)
    manual_sheet = create_manual_sheet(shortlist)

    shortlist_path = input_dir / DEFAULT_SHORTLIST
    manual_path = input_dir / DEFAULT_MANUAL_SHEET
    report_path = input_dir / DEFAULT_REPORT

    # Ghi đè có chủ ý để bắt đầu vòng manual selection mới.
    shortlist.to_csv(shortlist_path, index=False, encoding="utf-8-sig")
    manual_sheet.to_csv(manual_path, index=False, encoding="utf-8-sig")
    write_report(report_path, shortlist, filtered)

    stats = shortlist.groupby("syllable_length")["log_frequency"].agg(["count", "min", "median", "max"])
    encoding = sys.stdout.encoding or "utf-8"

    def safe_text(value: object) -> str:
        return str(value).encode(encoding, errors="backslashreplace").decode(encoding)

    print("Refreshed shortlist complete.")
    print(f"Source: {safe_text(input_dir / DEFAULT_KEPT)}")
    print(f"Shortlist overwritten: {safe_text(shortlist_path)}")
    print(f"Manual sheet overwritten: {safe_text(manual_path)}")
    print(f"Report: {safe_text(report_path)}")
    print(stats.to_string())


if __name__ == "__main__":
    main()
