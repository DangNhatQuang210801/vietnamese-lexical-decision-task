"""
Generate pseudoword_candidate_pool_v4.csv with real-word-template substitution.

Run from the repository root:
    python scripts/generate_pseudoword_candidates.py

V4 strategy:
- Use each final real-word stimulus as a template.
- Modify exactly one syllable.
- Preserve the original syllable length and surrounding syllables.
- Exclude exact matches in corpus/candidate/final-real-word files.
"""

from collections import Counter, defaultdict
import csv
import random
from pathlib import Path
import unicodedata


ROOT = Path.cwd()
DATA = ROOT / "data"
STIMULI = DATA / "stimuli"
PROCESSED = DATA / "processed"

REALWORD_FILE = STIMULI / "final_realword_candidates_v4.csv"
FREQUENCY_FILES = [
    PROCESSED / "all_1to4gram_frequency.csv",
    PROCESSED / "unigrams_frequency.csv",
    PROCESSED / "bigrams_frequency.csv",
    PROCESSED / "trigrams_frequency.csv",
    PROCESSED / "fourgrams_frequency.csv",
]
CANDIDATE_FILES = [
    STIMULI / "candidate_pool_kept_only.csv",
    STIMULI / "candidate_pool_filtered.csv",
]

OUT_CSV = STIMULI / "pseudoword_candidate_pool_v4.csv"
OUT_DIAGNOSTICS = STIMULI / "pseudoword_candidate_pool_v4_diagnostics.txt"

RANDOM_SEED = 20260501
MAX_PER_REALWORD = 3


def norm(text):
    return (text or "").strip().lower()


def deaccent(text):
    text = (text or "").lower().replace("đ", "d")
    return "".join(
        char
        for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )


def read_rows(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing required input file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def lexical_column(rows):
    if not rows:
        return "lexical_item"
    return "lexical_item" if "lexical_item" in rows[0] else next(iter(rows[0]))


def read_items(path):
    rows = read_rows(path)
    col = lexical_column(rows)
    return [norm(row.get(col, "")) for row in rows if norm(row.get(col, ""))]


def build_collision_sets():
    corpus_items = set()
    for path in FREQUENCY_FILES:
        corpus_items.update(read_items(path))

    candidate_items = set()
    for path in CANDIDATE_FILES:
        candidate_items.update(read_items(path))

    realword_items = set(read_items(REALWORD_FILE))
    collision_items = corpus_items | candidate_items | realword_items

    unigram_items = set(read_items(PROCESSED / "unigrams_frequency.csv"))
    attested_syllables = set()
    for item in collision_items:
        attested_syllables.update(item.split())

    return collision_items, unigram_items, attested_syllables


ONSETS = [
    "",
    "b",
    "c",
    "ch",
    "d",
    "đ",
    "g",
    "gh",
    "gi",
    "h",
    "k",
    "kh",
    "l",
    "m",
    "n",
    "ng",
    "ngh",
    "nh",
    "ph",
    "qu",
    "r",
    "s",
    "t",
    "th",
    "tr",
    "v",
    "x",
]
CODAS = ["", "c", "ch", "m", "n", "ng", "nh", "p", "t"]

TONE_VARIANTS = {
    "a": ["a", "á", "ả", "ạ"],
    "ă": ["ă", "ắ", "ẳ", "ặ"],
    "â": ["â", "ấ", "ẩ", "ậ"],
    "e": ["e", "é", "ẻ", "ẹ"],
    "ê": ["ê", "ế", "ể", "ệ"],
    "i": ["i", "í", "ỉ", "ị"],
    "o": ["o", "ó", "ỏ", "ọ"],
    "ô": ["ô", "ố", "ổ", "ộ"],
    "ơ": ["ơ", "ớ", "ở", "ợ"],
    "u": ["u", "ú", "ủ", "ụ"],
    "ư": ["ư", "ứ", "ử", "ự"],
    "y": ["y", "ý", "ỷ", "ỵ"],
}
VOWEL_SWAP = {
    "a": ["ă", "â", "o"],
    "ă": ["a", "â"],
    "â": ["ă", "a", "ơ"],
    "e": ["ê", "a"],
    "ê": ["e", "i"],
    "i": ["ê", "y"],
    "o": ["ô", "ơ", "a"],
    "ô": ["o", "ơ"],
    "ơ": ["ô", "ư", "â"],
    "u": ["ư", "ô"],
    "ư": ["u", "ơ"],
    "y": ["i"],
}

BANNED_FRAGMENTS = {
    "địt",
    "ịt",
    "cặc",
    "lồn",
    "buồi",
    "đụ",
    "đéo",
    "fuck",
    "shit",
    "sex",
}
BAD_RIMES = {"ẹch", "ỷn", "ửch", "éch", "ých", "ửc", "ẹc", "ụych"}
SENSITIVE_BASE_FRAGMENTS = {"benh", "chet", "giet", "mau", "han", "dau", "toi"}


def split_onset(syllable):
    base = deaccent(syllable)
    for onset in sorted(ONSETS, key=len, reverse=True):
        onset_base = deaccent(onset)
        if onset_base and base.startswith(onset_base) and len(base) > len(onset_base):
            return onset, syllable[len(onset) :]
    return "", syllable


def split_coda(syllable):
    base = deaccent(syllable)
    for coda in sorted(CODAS, key=len, reverse=True):
        if coda and base.endswith(coda) and len(base) > len(coda):
            return syllable[: -len(coda)], coda
    return syllable, ""


def vowel_positions(syllable):
    positions = []
    for index, char in enumerate(syllable):
        base = deaccent(char)
        if base in "aeiouy":
            positions.append((index, base, char))
    return positions


def legal_syllable(syllable):
    if not syllable or " " in syllable or "?" in syllable:
        return False
    if any(fragment in syllable for fragment in BANNED_FRAGMENTS):
        return False
    if not any(ord(char) > 127 for char in syllable):
        return False
    if any(syllable.endswith(rime) for rime in BAD_RIMES):
        return False
    base = deaccent(syllable)
    if any(char in base for char in "fjwz"):
        return False
    if any(fragment in base for fragment in SENSITIVE_BASE_FRAGMENTS):
        return False
    if not base.isalpha():
        return False
    if not 2 <= len(base) <= 8:
        return False
    if base.startswith("ngh") and base[3:4] not in {"e", "i", "y"}:
        return False
    if base.startswith("gh") and base[2:3] not in {"e", "i", "y"}:
        return False
    if base.startswith("k") and not base.startswith("kh") and base[1:2] not in {"e", "i", "y"}:
        return False
    if base.startswith("c") and not base.startswith("ch") and base[1:2] in {"e", "i", "y"}:
        return False
    if base.startswith("g") and not base.startswith(("gi", "gh")) and base[1:2] in {"e", "i", "y"}:
        return False
    return True


def tone_variants(syllable):
    if len(vowel_positions(syllable)) != 1:
        return []
    variants = []
    for index, base_vowel, original_char in vowel_positions(syllable):
        for tone_char in TONE_VARIANTS.get(base_vowel, []):
            if tone_char != original_char:
                chars = list(syllable)
                chars[index] = tone_char
                variants.append(("".join(chars), "tone_change"))
    return variants


def vowel_variants(syllable):
    variants = []
    positions = vowel_positions(syllable)
    if len(positions) != 1:
        return variants
    index, base_vowel, _original_char = positions[0]
    for swap_base in VOWEL_SWAP.get(base_vowel, []):
        for tone_char in TONE_VARIANTS.get(swap_base, [swap_base])[:3]:
            chars = list(syllable)
            chars[index] = tone_char
            variants.append(("".join(chars), "vowel_change"))
    return variants


def final_consonant_variants(syllable):
    stem, old_coda = split_coda(syllable)
    if not old_coda:
        return []
    variants = []
    for new_coda in ["n", "ng", "t", "c", "m", "p"]:
        if new_coda != old_coda:
            variants.append((stem + new_coda, "final_consonant_change"))
    return variants


def onset_variants(syllable):
    old_onset, rime = split_onset(syllable)
    if not rime:
        return []
    preferred = ["b", "c", "ch", "đ", "g", "gi", "h", "kh", "l", "m", "n", "ng", "nh", "ph", "t", "th", "tr", "v", "x"]
    variants = []
    for new_onset in preferred:
        if new_onset != old_onset:
            variants.append((new_onset + rime, "onset_change"))
    return variants


def syllable_variants(syllable):
    # Smallest edits first.
    variants = []
    variants.extend(tone_variants(syllable))
    variants.extend(final_consonant_variants(syllable))
    variants.extend(vowel_variants(syllable))
    variants.extend(onset_variants(syllable))

    seen = set()
    deduped = []
    for variant, mod_type in variants:
        variant = norm(variant)
        if variant != syllable and variant not in seen:
            seen.add(variant)
            deduped.append((variant, mod_type))
    return deduped


def possible_meaning_warning(candidate, modified_syllable, unigram_items, collision_items):
    if candidate in collision_items:
        return "exact_existing_item"
    if modified_syllable in unigram_items:
        return "modified_syllable_is_attested_unigram"
    if any(fragment in candidate for fragment in BANNED_FRAGMENTS):
        return "offensive_or_inappropriate_fragment"
    base = deaccent(candidate)
    if any(fragment in base for fragment in SENSITIVE_BASE_FRAGMENTS):
        return "sensitive_or_distracting_fragment"
    return "none_detected_by_heuristic"


def quality_flag(modification_type, modified_syllable, unigram_items):
    if modified_syllable in unigram_items:
        return "reject"
    if modification_type in {"tone_change", "final_consonant_change"}:
        return "high"
    if modification_type == "vowel_change":
        return "high"
    return "medium"


def generate_candidates_for_realword(row, collision_items, unigram_items, attested_syllables):
    source = norm(row["lexical_item"])
    syllables = source.split()
    candidates = []
    rejected = Counter()
    rejected_examples = defaultdict(list)

    for position, original_syllable in enumerate(syllables, start=1):
        for modified_syllable, mod_type in syllable_variants(original_syllable):
            reason = None
            new_syllables = syllables.copy()
            new_syllables[position - 1] = modified_syllable
            pseudoword = " ".join(new_syllables)

            warning = possible_meaning_warning(
                pseudoword, modified_syllable, unigram_items, collision_items
            )
            qflag = quality_flag(mod_type, modified_syllable, unigram_items)

            if not legal_syllable(modified_syllable):
                reason = "malformed_modified_syllable"
            elif modified_syllable in attested_syllables:
                reason = "modified_syllable_attested_in_inputs"
            elif pseudoword in collision_items:
                reason = "candidate_exact_match_in_inputs"
            elif warning != "none_detected_by_heuristic":
                reason = warning
            elif qflag == "reject":
                reason = "quality_reject"

            if reason:
                rejected[reason] += 1
                if len(rejected_examples[reason]) < 8:
                    rejected_examples[reason].append(
                        f"{source} -> {pseudoword} ({mod_type})"
                    )
                continue

            candidates.append(
                {
                    "source_realword": source,
                    "pseudoword": pseudoword,
                    "syllable_length": row["syllable_length"],
                    "modified_syllable_position": str(position),
                    "original_syllable": original_syllable,
                    "modified_syllable": modified_syllable,
                    "modification_type": mod_type,
                    "corpus_match_status": "no exact match in processed corpus/candidate/final-real-word files",
                    "quality_flag": qflag,
                    "possible_meaning_warning": warning,
                    "review_status": "needs_manual_review",
                    "notes": "real-word-template substitution; exactly one syllable modified",
                }
            )

    candidates.sort(
        key=lambda item: (
            0 if item["quality_flag"] == "high" else 1,
            {
                "tone_change": 0,
                "final_consonant_change": 1,
                "vowel_change": 2,
                "onset_change": 3,
            }.get(item["modification_type"], 9),
            item["modified_syllable_position"],
            item["pseudoword"],
        )
    )
    return candidates[:MAX_PER_REALWORD], rejected, rejected_examples


def write_outputs(accepted, rejected, rejected_examples, per_item_counts):
    fields = [
        "source_realword",
        "pseudoword",
        "syllable_length",
        "modified_syllable_position",
        "original_syllable",
        "modified_syllable",
        "modification_type",
        "corpus_match_status",
        "quality_flag",
        "possible_meaning_warning",
        "review_status",
        "notes",
    ]
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(accepted)

    count_by_length = Counter(row["syllable_length"] for row in accepted)
    examples = accepted[:12]
    lines = [
        "Pseudoword candidate pool v4 diagnostics",
        "",
        "Output files:",
        f"- {OUT_CSV.as_posix()}",
        f"- {OUT_DIAGNOSTICS.as_posix()}",
        "",
        "Candidates generated by syllable_length:",
    ]
    for length in ["1", "2", "3", "4"]:
        lines.append(f"- {length} syllable(s): {count_by_length[length]}")

    per_count_summary = Counter(per_item_counts.values())
    lines.extend(["", "Candidates generated per real-word item:"])
    for number in sorted(per_count_summary):
        lines.append(f"- {number} candidate(s): {per_count_summary[number]} real-word item(s)")

    lines.extend(["", "Rejected candidates by reason:"])
    if rejected:
        for reason, count in rejected.most_common():
            lines.append(f"- {reason}: {count}")
    else:
        lines.append("- none")

    lines.extend(["", "Examples of accepted candidates:"])
    for item in examples:
        lines.append(
            f"- {item['source_realword']} -> {item['pseudoword']} "
            f"[{item['modification_type']}, syllable {item['modified_syllable_position']}]"
        )

    lines.extend(["", "Examples of rejected candidates:"])
    for reason, items in list(rejected_examples.items())[:10]:
        lines.append(f"- {reason}: {', '.join(items[:5])}")

    lines.extend(
        [
            "",
            "Method explanation:",
            (
                "V4 uses real-word-template substitution instead of random syllable "
                "recombination. Each final real-word stimulus is used as a template, "
                "and each accepted pseudoword changes exactly one syllable while "
                "preserving the original syllable length and all other syllables. "
                "The modified syllable is generated through small tone, vowel, final "
                "consonant, or onset changes, then screened for Vietnamese-like spelling, "
                "offensive/sensitive fragments, and exact matches in corpus, candidate, "
                "and final real-word files."
            ),
            "",
            "Limitations:",
            "- This is still a reviewable candidate pool, not the final pseudoword set.",
            "- Exact-match filtering cannot catch every real Vietnamese word absent from the input files.",
            "- Native-speaker review is still required for naturalness, humor, sensitivity, and accidental meaning.",
        ]
    )
    OUT_DIAGNOSTICS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    random.seed(RANDOM_SEED)
    real_rows = read_rows(REALWORD_FILE)
    collision_items, unigram_items, attested_syllables = build_collision_sets()

    accepted = []
    rejected_total = Counter()
    rejected_examples = defaultdict(list)
    per_item_counts = {}
    seen_candidates = set()

    for row in real_rows:
        candidates, rejected, examples = generate_candidates_for_realword(
            row, collision_items, unigram_items, attested_syllables
        )
        kept = []
        for candidate in candidates:
            if candidate["pseudoword"] in seen_candidates:
                rejected_total["duplicate_candidate_across_templates"] += 1
                continue
            seen_candidates.add(candidate["pseudoword"])
            kept.append(candidate)
        accepted.extend(kept)
        per_item_counts[norm(row["lexical_item"])] = len(kept)
        rejected_total.update(rejected)
        for reason, items in examples.items():
            rejected_examples[reason].extend(items)

    write_outputs(accepted, rejected_total, rejected_examples, per_item_counts)

    print("Output paths:")
    print(f"- {OUT_CSV.as_posix()}")
    print(f"- {OUT_DIAGNOSTICS.as_posix()}")
    print("")
    print("Candidates generated by syllable_length:")
    counts = Counter(row["syllable_length"] for row in accepted)
    for length in ["1", "2", "3", "4"]:
        print(f"- {length}: {counts[length]}")
    print("")
    print("Rejected candidates by reason:")
    for reason, count in rejected_total.most_common():
        print(f"- {reason}: {count}")


if __name__ == "__main__":
    main()
