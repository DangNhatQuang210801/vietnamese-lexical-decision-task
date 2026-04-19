"""Refresh the existing manual selection sheet in place.

This is a light, annotation-preserving refresh: keep user choices when possible,
remove weak unselected options, and add better candidates from the filtered pool.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

import pandas as pd


DEFAULT_DIR = Path("data_sample") / "_processed"
MANUAL_FILE = "manual_selection_sheet (chọn tay).csv"
KEPT_FILE = "candidate_pool_kept_only.csv"
REVIEW_FILE = "candidate_pool_manual_review.csv"

TARGET_PER_LENGTH = 75
RANDOM_SEED = 20260419
FREQUENCY_BINS = 6

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
ANNOTATION_COLUMNS = ["keep", "confidence", "reason", "notes"]


# Các rule này cố tình conservative, để hỗ trợ review chứ không thay thế review.
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
    "với",
    "ơi",
}

CONTEXT_WORDS = {"anh", "bạn", "cháu", "chị", "cô", "con", "em", "họ", "mình", "nó", "ông", "tôi", "vợ"}

VERB_LIKE_WORDS = {
    "ăn",
    "bảo",
    "biết",
    "bị",
    "bỏ",
    "chia",
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
    "lấy",
    "mang",
    "mua",
    "muốn",
    "nấu",
    "nghĩ",
    "nhận",
    "sống",
    "thấy",
    "thích",
    "thương",
    "tìm",
    "viết",
    "yêu",
}

QUANTITY_WORDS = {"bát", "bộ", "cái", "chiếc", "gam", "gói", "kg", "lần", "lít", "ml", "muỗng", "phần", "số", "triệu", "vài"}

FOREIGN_CODE_WORDS = {
    "alert",
    "baby",
    "blog",
    "cm",
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
    "login",
    "ml",
    "online",
    "password",
    "sex",
    "shop",
    "usd",
    "url",
    "valentine",
    "web",
}

RELATIONSHIP_DRAMA_PHRASES = {
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
    "vợ",
}

FRAGMENT_EDGE_WORDS = {
    "ban",
    "bán",
    "bắt",
    "can",
    "chấn",
    "chính",
    "đại",
    "góp",
    "giống",
    "khám",
    "khuyến",
    "nấu",
    "nguyên",
    "nội",
    "sản",
    "sinh",
    "thông",
    "thiết",
    "tiếp",
    "tim",
    "tuần",
    "vàng",
    "vấn",
    "xã",
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
    parser = argparse.ArgumentParser(description="Refresh manual_selection_sheet in place.")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--target-per-length", type=int, default=TARGET_PER_LENGTH)
    return parser.parse_args()


def safe_print(text: str) -> None:
    encoding = sys.stdout.encoding or "utf-8"
    print(text.encode(encoding, errors="backslashreplace").decode(encoding))


def normalize_item(value: object) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip().lower())


def is_keep_one(value: object) -> bool:
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    return pd.notna(numeric) and numeric == 1


def contains_phrase(item: str, phrases: set[str]) -> bool:
    return any(phrase in item for phrase in phrases)


def lexical_domain(item: str) -> str:
    words = set(item.split())
    best_domain = "other"
    best_count = 0
    for domain, keywords in DOMAIN_KEYWORDS.items():
        count = len(words & keywords)
        if count > best_count:
            best_domain = domain
            best_count = count
    return best_domain


def severe_bad(item: str, length: int) -> bool:
    """Chỉ dùng để loại cả item đã keep=1 nếu rõ ràng rất tệ."""
    words = item.split()
    if not item or len(words) != length:
        return True
    if not VIETNAMESE_RE.match(item) or FOREIGN_LETTER_RE.search(item):
        return True
    if any(word in FOREIGN_CODE_WORDS or len(word) == 1 for word in words):
        return True
    if length == 1 and len(item) >= 5 and not VIETNAMESE_DIACRITIC_RE.search(item):
        return True
    if words[0] in FUNCTION_WORDS or words[-1] in FUNCTION_WORDS:
        return True
    return False


def weak_option(item: str, length: int, row: pd.Series) -> bool:
    """Đánh dấu option yếu để loại nếu chưa được user chọn."""
    words = item.split()
    warning = "" if pd.isna(row.get("warning_flag")) else str(row.get("warning_flag")).strip()
    if severe_bad(item, length):
        return True
    if warning:
        return True
    if any(word in FUNCTION_WORDS for word in words):
        return True
    if any(word in CONTEXT_WORDS for word in words):
        return True
    if any(word in QUANTITY_WORDS for word in words):
        return True
    if contains_phrase(item, RELATIONSHIP_DRAMA_PHRASES):
        return True
    if length >= 2 and any(word in VERB_LIKE_WORDS for word in words):
        return True
    if length >= 2 and (words[0] in FRAGMENT_EDGE_WORDS or words[-1] in FRAGMENT_EDGE_WORDS):
        return True
    if length >= 2 and not (words[0] in NOUNISH_TOKENS or words[-1] in NOUNISH_TOKENS or lexical_domain(item) != "other"):
        return True
    if length == 1 and item not in ONE_SYLLABLE_NOUNISH and item not in NOUNISH_TOKENS:
        return True
    return False


def quality_score(row: pd.Series) -> float:
    item = normalize_item(row["lexical_item"])
    words = item.split()
    length = int(row["syllable_length"])
    freq = float(row["frequency"])
    domain = lexical_domain(item)
    score = 0.0
    if domain != "other":
        score += 2.0
    if length == 1 and item in ONE_SYLLABLE_NOUNISH:
        score += 3.0
    if length >= 2 and words and words[0] in NOUNISH_TOKENS:
        score += 1.5
    if length >= 2 and words and words[-1] in NOUNISH_TOKENS:
        score += 1.5
    if freq >= 10:
        score += 1.0
    if freq >= 30:
        score += 0.5
    if contains_phrase(item, RELATIONSHIP_DRAMA_PHRASES):
        score -= 3.0
    return score


def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    df["lexical_item"] = df["lexical_item"].map(normalize_item)
    df["frequency"] = pd.to_numeric(df["frequency"], errors="coerce")
    df["log_frequency"] = pd.to_numeric(df["log_frequency"], errors="coerce")
    df["syllable_length"] = pd.to_numeric(df["syllable_length"], errors="coerce").astype("Int64")
    return df


def compatible_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Bảo đảm có đủ cột annotation để merge item mới."""
    for col in BASE_COLUMNS + ANNOTATION_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df


def candidate_pool(input_dir: Path, existing_items: set[str]) -> pd.DataFrame:
    """Lấy ứng viên mới từ pool chính, dùng manual_review phụ nếu cần."""
    frames = []
    for name in [KEPT_FILE, REVIEW_FILE]:
        path = input_dir / name
        if path.exists():
            df = compatible_columns(load_csv(path))
            frames.append(df)
    pool = pd.concat(frames, ignore_index=True).drop_duplicates("lexical_item")
    pool = pool[~pool["lexical_item"].isin(existing_items)].copy()

    rows = []
    for row in pool.itertuples(index=False):
        item = row.lexical_item
        length = int(row.syllable_length)
        series = pd.Series(row._asdict())
        if not weak_option(item, length, series):
            rows.append(series)
    if not rows:
        return pool.iloc[0:0].copy()

    out = pd.DataFrame(rows)
    out["domain"] = out["lexical_item"].map(lexical_domain)
    out["quality_score"] = out.apply(quality_score, axis=1)
    return out


def pick_additions(pool: pd.DataFrame, needed_by_length: dict[int, int]) -> pd.DataFrame:
    """Thêm item theo từng length, có trải log_frequency và domain."""
    parts = []
    for length, needed in needed_by_length.items():
        if needed <= 0:
            continue
        group = pool[pool["syllable_length"] == length].copy()
        if group.empty:
            continue

        bins = min(FREQUENCY_BINS, max(1, group["log_frequency"].nunique()))
        group["freq_bin"] = pd.qcut(
            group["log_frequency"].rank(method="first"),
            q=bins,
            labels=False,
            duplicates="drop",
        )
        per_bin = max(1, math.ceil(needed / max(1, group["freq_bin"].nunique())))

        chosen = []
        for _, bin_df in group.groupby("freq_bin", observed=True):
            ranked = bin_df.sort_values(
                ["quality_score", "frequency", "lexical_item"],
                ascending=[False, False, True],
            )
            # Giới hạn nhẹ theo domain trong từng bin.
            ranked = ranked.groupby("domain", group_keys=False).head(max(1, math.ceil(per_bin / 2)))
            chosen.append(ranked.head(per_bin))

        selected = pd.concat(chosen, ignore_index=True)
        if len(selected) < needed:
            used = set(selected["lexical_item"])
            filler = group[~group["lexical_item"].isin(used)].sort_values(
                ["quality_score", "frequency", "lexical_item"],
                ascending=[False, False, True],
            )
            selected = pd.concat([selected, filler.head(needed - len(selected))], ignore_index=True)
        parts.append(selected.head(needed))

    if not parts:
        return pool.iloc[0:0].copy()
    return pd.concat(parts, ignore_index=True)


def main() -> None:
    args = parse_args()
    input_dir = args.input_dir
    manual_path = input_dir / MANUAL_FILE
    if not manual_path.exists():
        raise FileNotFoundError(f"Missing manual sheet: {manual_path}")

    manual = compatible_columns(load_csv(manual_path))
    original_count = len(manual)

    retained_rows = []
    removed_count = 0
    selected_kept = 0
    selected_removed = 0

    for _, row in manual.iterrows():
        item = normalize_item(row["lexical_item"])
        length = int(row["syllable_length"])
        user_selected = is_keep_one(row.get("keep"))
        if user_selected:
            if severe_bad(item, length):
                selected_removed += 1
                removed_count += 1
                continue
            selected_kept += 1
            retained_rows.append(row)
        else:
            if weak_option(item, length, row):
                removed_count += 1
                continue
            retained_rows.append(row)

    retained = pd.DataFrame(retained_rows) if retained_rows else manual.iloc[0:0].copy()
    retained = compatible_columns(retained)

    existing_items = set(retained["lexical_item"].map(normalize_item))
    counts = retained["syllable_length"].value_counts().to_dict()
    needed_by_length = {
        length: max(0, args.target_per_length - int(counts.get(length, 0)))
        for length in [1, 2, 3, 4]
    }

    pool = candidate_pool(input_dir, existing_items)
    additions = pick_additions(pool, needed_by_length)
    additions = compatible_columns(additions)

    # Item mới thêm vào để trống annotation.
    for col in ANNOTATION_COLUMNS:
        additions[col] = ""

    updated = pd.concat([retained, additions[retained.columns]], ignore_index=True)
    updated = updated.drop_duplicates("lexical_item", keep="first")

    # Giữ cột hiện có, không làm mất annotation thật của user.
    front = BASE_COLUMNS + ANNOTATION_COLUMNS
    remaining = [col for col in updated.columns if col not in front and not col.startswith("Unnamed")]
    updated = updated[[col for col in front if col in updated.columns] + remaining]
    updated = updated.sort_values(["syllable_length", "log_frequency", "lexical_item"], ascending=[True, False, True])
    updated.to_csv(manual_path, index=False, encoding="utf-8-sig")

    final_counts = updated.groupby("syllable_length").size()
    safe_print("Refresh manual sheet hoàn tất.")
    safe_print(f"Option cũ ban đầu: {original_count}")
    safe_print(f"Option cũ được giữ lại: {len(retained)}")
    safe_print(f"Option cũ bị loại: {removed_count}")
    safe_print(f"Trong đó keep==1 được giữ: {selected_kept}")
    if selected_removed:
        safe_print(f"CẢNH BÁO: keep==1 bị loại vì rất kém lexical validity: {selected_removed}")
    safe_print(f"Option mới được thêm: {len(additions)}")
    safe_print("Phân bố sau refresh theo syllable_length:")
    print(final_counts.to_string())
    safe_print(
        "Ghi chú: shortlist đã được refresh nhẹ tại chỗ, giữ annotation cũ khi có thể, "
        "loại bớt option yếu chưa chọn và thêm candidate noun-like/ổn định hơn để review tiếp."
    )


if __name__ == "__main__":
    main()
