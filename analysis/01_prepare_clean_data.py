from pathlib import Path
import re

import numpy as np
import pandas as pd


RAW_DIR = Path("data/experiment_results")
STIMULUS_FILE = Path("data/stimuli/final/final_ldt_stimuli_3x4_v1.csv")
OUT_CLEAN = Path("analysis/outputs/cleaned_data")
OUT_QC = Path("analysis/outputs/qc")

ENCODINGS = ["utf-8-sig", "utf-8", "cp1258"]
REQUIRED_COLUMNS = [
    "participant_id",
    "block",
    "trial_id",
    "stimulus",
    "condition",
    "is_word",
    "syllable_length",
    "frequency_group",
    "frequency",
    "log_frequency",
    "source_realword",
    "correct_response",
    "key_pressed",
    "response_label",
    "accuracy",
    "rt",
]
RESPONSE_MAP = {"f": "word", "j": "nonword"}


def read_csv_with_fallback(path):
    # Doc CSV bang encoding fallback, khong sua file goc.
    last_error = None
    for encoding in ENCODINGS:
        try:
            df = pd.read_csv(path, encoding=encoding, dtype=str, keep_default_na=False)
            return df, encoding, ""
        except Exception as exc:
            last_error = exc
    return None, "", str(last_error)


def filename_participant_id(path):
    match = re.match(r"^(\d+)_session-[^_]+_ldt_\d{8}_\d{6}\.csv$", path.name)
    return match.group(1) if match else ""


def clean_string(series):
    return series.fillna("").astype(str).str.strip()


def expected_response_label(key):
    key = str(key).strip().lower()
    if key == "":
        return ""
    return RESPONSE_MAP.get(key, "__INVALID__")


def validate_file(df, path, encoding, read_error):
    pid_from_file = filename_participant_id(path)
    row = {
        "source_file": path.name,
        "source_encoding": encoding,
        "read_success": df is not None,
        "read_error": read_error,
        "participant_id_filename": pid_from_file,
        "participant_id_inside": "",
        "participant_id_match": False,
        "row_count": 0,
        "practice_trial_count": 0,
        "main_trial_count": 0,
        "required_columns_ok": False,
        "missing_required_columns": "",
        "duplicate_main_trial_id_count": "",
        "invalid_key_count": "",
        "response_label_mismatch_count": "",
        "accuracy_mismatch_count": "",
        "non_numeric_rt_count": "",
        "validation_flags": "",
    }
    if df is None:
        row["validation_flags"] = "read_failed"
        return row

    row["row_count"] = len(df)
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    row["missing_required_columns"] = ";".join(missing_columns)
    row["required_columns_ok"] = len(missing_columns) == 0
    if missing_columns:
        row["validation_flags"] = "missing_required_columns"
        return row

    participant_ids = sorted(set(clean_string(df["participant_id"])))
    row["participant_id_inside"] = participant_ids[0] if len(participant_ids) == 1 else "|".join(participant_ids)
    row["participant_id_match"] = bool(pid_from_file and row["participant_id_inside"] == pid_from_file)

    block = clean_string(df["block"]).str.lower()
    main_df = df[block == "main"].copy()
    practice_df = df[block == "practice"].copy()
    row["main_trial_count"] = len(main_df)
    row["practice_trial_count"] = len(practice_df)
    row["duplicate_main_trial_id_count"] = int(main_df["trial_id"].duplicated().sum())

    keys = clean_string(df["key_pressed"]).str.lower()
    labels = clean_string(df["response_label"])
    correct = clean_string(df["correct_response"])
    expected_labels = keys.map(expected_response_label)
    row["invalid_key_count"] = int((expected_labels == "__INVALID__").sum())
    row["response_label_mismatch_count"] = int((expected_labels != labels).sum())

    expected_accuracy = np.where((labels != "") & (labels == correct), 1, 0)
    observed_accuracy = pd.to_numeric(df["accuracy"], errors="coerce")
    row["accuracy_mismatch_count"] = int((observed_accuracy != expected_accuracy).sum())

    rt_raw = clean_string(df["rt"])
    rt_numeric = pd.to_numeric(rt_raw.replace({"": np.nan, "NA": np.nan}), errors="coerce")
    row["non_numeric_rt_count"] = int(((rt_raw != "") & (rt_raw.str.upper() != "NA") & rt_numeric.isna()).sum())

    flags = []
    if not row["participant_id_inside"]:
        flags.append("missing_participant_id")
    if not row["participant_id_match"]:
        flags.append("participant_id_filename_mismatch")
    if row["row_count"] != 124:
        flags.append("row_count_not_124")
    if row["practice_trial_count"] != 4:
        flags.append("practice_trial_count_not_4")
    if row["main_trial_count"] != 120:
        flags.append("main_trial_count_not_120")
    if row["duplicate_main_trial_id_count"]:
        flags.append("duplicate_main_trial_id")
    if row["invalid_key_count"]:
        flags.append("invalid_key")
    if row["response_label_mismatch_count"]:
        flags.append("response_label_mismatch")
    if row["accuracy_mismatch_count"]:
        flags.append("accuracy_mismatch")
    if row["non_numeric_rt_count"]:
        flags.append("non_numeric_rt")
    row["validation_flags"] = ";".join(flags)
    return row


def add_metadata(df, source_file, source_encoding):
    # Chuan hoa ban sao phan tich, khong thay doi raw CSV.
    df = df.copy()
    df["source_file"] = source_file
    df["source_encoding"] = source_encoding
    df["row_in_file"] = np.arange(1, len(df) + 1)

    for col in REQUIRED_COLUMNS:
        df[col] = clean_string(df[col])

    df["participant_id"] = df["participant_id"].astype(str)
    df["item_id"] = df["trial_id"]
    df["rt_numeric"] = pd.to_numeric(df["rt"].replace({"": np.nan, "NA": np.nan}), errors="coerce")
    df["log_rt"] = np.where(df["rt_numeric"] > 0, np.log(df["rt_numeric"]), np.nan)
    df["is_timeout"] = df["key_pressed"].eq("") | df["rt_numeric"].isna()
    df["is_main_trial"] = df["block"].str.lower().eq("main")
    df["is_practice_trial"] = df["block"].str.lower().eq("practice")
    df["is_real_word"] = df["condition"].eq("word")
    df["is_pseudoword"] = df["condition"].eq("pseudoword")
    df["is_correct"] = pd.to_numeric(df["accuracy"], errors="coerce").eq(1)
    df["accuracy_numeric"] = pd.to_numeric(df["accuracy"], errors="coerce")
    df["syllable_length_numeric"] = pd.to_numeric(df["syllable_length"], errors="coerce")
    df["frequency_numeric"] = pd.to_numeric(df["frequency"].replace({"NA": np.nan, "": np.nan}), errors="coerce")
    df["log_frequency_numeric"] = pd.to_numeric(df["log_frequency"].replace({"NA": np.nan, "": np.nan}), errors="coerce")
    return df


def validate_stimulus_file(path):
    # Kiem tra stimulus file da khoa truoc khi xu ly du lieu nguoi tham gia.
    stimulus, encoding, read_error = read_csv_with_fallback(path)
    if stimulus is None:
        return stimulus, pd.DataFrame([{"check": "stimulus_file_readable", "passed": False, "detail": read_error}]), encoding

    for col in REQUIRED_COLUMNS:
        if col not in stimulus.columns:
            stimulus[col] = ""
        stimulus[col] = clean_string(stimulus[col])

    real_words = stimulus[stimulus["condition"].eq("word")]
    pseudowords = stimulus[stimulus["condition"].eq("pseudoword")]
    rows = [
        {"check": "stimulus_file_readable", "passed": True, "detail": f"encoding={encoding}"},
        {"check": "stimulus_row_count_120", "passed": len(stimulus) == 120, "detail": len(stimulus)},
        {"check": "stimulus_real_word_count_72", "passed": len(real_words) == 72, "detail": len(real_words)},
        {"check": "stimulus_pseudoword_count_48", "passed": len(pseudowords) == 48, "detail": len(pseudowords)},
        {
            "check": "stimulus_unique_trial_id_120",
            "passed": stimulus["trial_id"].nunique() == 120,
            "detail": stimulus["trial_id"].nunique(),
        },
    ]

    real_counts = real_words.groupby(["frequency_group", "syllable_length"], dropna=False).size().to_dict()
    for freq in ["low", "mid", "high"]:
        for length in ["1", "2", "3", "4"]:
            count = int(real_counts.get((freq, length), 0))
            rows.append({"check": f"real_cell_{freq}_{length}_count_6", "passed": count == 6, "detail": count})

    pseudo_counts = pseudowords.groupby("syllable_length", dropna=False).size().to_dict()
    for length in ["1", "2", "3", "4"]:
        count = int(pseudo_counts.get(length, 0))
        rows.append({"check": f"pseudoword_length_{length}_count_12", "passed": count == 12, "detail": count})

    return stimulus, pd.DataFrame(rows), encoding


def validate_data_against_stimulus(main_trials, stimulus):
    # Doi chieu trial_id trong raw-derived data voi stimulus file cuoi.
    participants = sorted(main_trials["participant_id"].dropna().astype(str).unique())
    expected_n = len(participants)
    expected_trial_ids = set(stimulus["trial_id"])
    actual_trial_ids = set(main_trials["trial_id"])
    missing = sorted(expected_trial_ids - actual_trial_ids)
    unexpected = sorted(actual_trial_ids - expected_trial_ids)

    rows = [
        {
            "check_type": "dataset",
            "item_id": "",
            "expected_presentations": "",
            "actual_presentations": "",
            "passed": len(actual_trial_ids) == 120,
            "detail": f"unique_main_trial_ids={len(actual_trial_ids)}",
        },
        {
            "check_type": "dataset",
            "item_id": "",
            "expected_presentations": "",
            "actual_presentations": "",
            "passed": len(missing) == 0,
            "detail": "missing_trial_ids=" + (";".join(missing) if missing else "none"),
        },
        {
            "check_type": "dataset",
            "item_id": "",
            "expected_presentations": "",
            "actual_presentations": "",
            "passed": len(unexpected) == 0,
            "detail": "unexpected_trial_ids=" + (";".join(unexpected) if unexpected else "none"),
        },
    ]

    presentation_counts = main_trials.groupby("trial_id", dropna=False).size()
    participant_item_counts = main_trials.groupby(["participant_id", "trial_id"], dropna=False).size()
    duplicate_cells = int((participant_item_counts != 1).sum())
    rows.append(
        {
            "check_type": "dataset",
            "item_id": "",
            "expected_presentations": "",
            "actual_presentations": "",
            "passed": duplicate_cells == 0,
            "detail": f"participant_trial_id_cells_not_equal_1={duplicate_cells}",
        }
    )

    for trial_id in sorted(expected_trial_ids):
        actual = int(presentation_counts.get(trial_id, 0))
        rows.append(
            {
                "check_type": "item_presentation_count",
                "item_id": trial_id,
                "expected_presentations": expected_n,
                "actual_presentations": actual,
                "passed": actual == expected_n,
                "detail": "",
            }
        )
    return pd.DataFrame(rows)


def participant_qc(all_trials, file_summary):
    rows = []
    for participant_id, df in all_trials.groupby("participant_id", dropna=False):
        main = df[df["is_main_trial"]]
        practice = df[df["is_practice_trial"]]
        valid_rt = main["rt_numeric"].dropna()
        word = main[main["condition"].eq("word")]
        pseudo = main[main["condition"].eq("pseudoword")]

        overall_acc = main["accuracy_numeric"].mean()
        pseudo_acc = pseudo["accuracy_numeric"].mean()
        f_count = int(main["key_pressed"].str.lower().eq("f").sum())
        j_count = int(main["key_pressed"].str.lower().eq("j").sum())
        source_file = str(main["source_file"].iloc[0]) if len(main) else str(df["source_file"].iloc[0])
        file_row = file_summary[file_summary["source_file"].eq(source_file)].iloc[0]

        flags = []
        if len(main) != 120:
            flags.append("main_trial_count_not_120")
        if len(practice) != 4:
            flags.append("practice_trial_count_not_4")
        if pd.notna(overall_acc) and overall_acc < 0.70:
            flags.append("overall_accuracy_below_70")
        if pd.notna(pseudo_acc) and pseudo_acc < 0.50:
            flags.append("pseudoword_accuracy_below_50")
        if len(main) and main["rt_numeric"].isna().mean() > 0.10:
            flags.append("missing_rt_above_10_percent")
        if len(valid_rt) and (valid_rt < 0.250).mean() > 0.10:
            flags.append("fast_rt_above_10_percent")
        if len(valid_rt) and valid_rt.median() < 0.300:
            flags.append("median_rt_below_300ms")
        if len(valid_rt) and valid_rt.median() > 2.000:
            flags.append("median_rt_above_2000ms")
        if len(main) and max(f_count, j_count) / len(main) > 0.90:
            flags.append("one_key_response_above_90_percent")
        if not bool(file_row["participant_id_match"]):
            flags.append("participant_id_filename_mismatch")
        if str(file_row["validation_flags"]):
            flags.append("file_validation_warning")

        rows.append(
            {
                "participant_id": participant_id,
                "source_file": source_file,
                "source_encoding": df["source_encoding"].iloc[0],
                "total_rows": len(df),
                "practice_trial_count": len(practice),
                "main_trial_count": len(main),
                "valid_rt_count": int(valid_rt.count()),
                "missing_rt_count": int(main["rt_numeric"].isna().sum()),
                "timeout_count": int(main["is_timeout"].sum()),
                "overall_main_accuracy": overall_acc,
                "word_accuracy": word["accuracy_numeric"].mean(),
                "pseudoword_accuracy": pseudo_acc,
                "practice_accuracy": practice["accuracy_numeric"].mean(),
                "mean_rt": valid_rt.mean(),
                "median_rt": valid_rt.median(),
                "min_rt": valid_rt.min() if len(valid_rt) else np.nan,
                "max_rt": valid_rt.max() if len(valid_rt) else np.nan,
                "pct_rt_below_250ms": (valid_rt < 0.250).mean() if len(valid_rt) else np.nan,
                "pct_rt_above_2500ms": (valid_rt > 2.500).mean() if len(valid_rt) else np.nan,
                "f_response_count": f_count,
                "j_response_count": j_count,
                "word_response_proportion": f_count / len(main) if len(main) else np.nan,
                "nonword_response_proportion": j_count / len(main) if len(main) else np.nan,
                "qc_flags": ";".join(dict.fromkeys(flags)),
            }
        )
    return pd.DataFrame(rows).sort_values("participant_id")


def item_qc(main_trials, expected_presentations):
    rows = []
    for item_id, df in main_trials.groupby("item_id", dropna=False):
        correct = df[df["is_correct"] & df["rt_numeric"].notna()]
        accuracy = df["accuracy_numeric"].mean()
        median_rt = correct["rt_numeric"].median()
        presentation_count_ok = len(df) == expected_presentations
        flags = []
        if pd.notna(accuracy) and accuracy < 0.60:
            flags.append("accuracy_below_60")
        if pd.notna(median_rt) and median_rt > 1.500:
            flags.append("median_correct_rt_above_1500ms")
        if not presentation_count_ok:
            flags.append("presentation_count_mismatch")

        first = df.iloc[0]
        rows.append(
            {
                "item_id": item_id,
                "trial_id": item_id,
                "expected_presentations": expected_presentations,
                "actual_presentations": len(df),
                "presentation_count_ok": presentation_count_ok,
                "presentations": len(df),
                "stimulus": first["stimulus"],
                "condition": first["condition"],
                "syllable_length": first["syllable_length"],
                "frequency_group": first["frequency_group"],
                "frequency": first["frequency"],
                "log_frequency": first["log_frequency"],
                "accuracy": accuracy,
                "mean_rt_correct": correct["rt_numeric"].mean(),
                "median_rt_correct": median_rt,
                "missing_rt_count": int(df["rt_numeric"].isna().sum()),
                "qc_flags": ";".join(flags),
            }
        )
    return pd.DataFrame(rows).sort_values("item_id")


def summarize_group(df, group_cols, label):
    rows = []
    for group_values, group_df in df.groupby(group_cols, dropna=False):
        if not isinstance(group_values, tuple):
            group_values = (group_values,)
        correct_rt = group_df[group_df["is_correct"] & group_df["rt_numeric"].notna()]["rt_numeric"]
        row = {"summary_type": label}
        for col, value in zip(group_cols, group_values):
            row[col] = value
        row.update(
            {
                "n_trials": len(group_df),
                "accuracy": group_df["accuracy_numeric"].mean(),
                "valid_rt_count": int(group_df["rt_numeric"].notna().sum()),
                "correct_valid_rt_count": int(correct_rt.count()),
                "mean_rt_correct": correct_rt.mean(),
                "median_rt_correct": correct_rt.median(),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def design_summary(main_trials):
    correct_rt = main_trials[main_trials["is_correct"] & main_trials["rt_numeric"].notna()]["rt_numeric"]
    rows = [
        {
            "summary_type": "overall",
            "n_trials": len(main_trials),
            "accuracy": main_trials["accuracy_numeric"].mean(),
            "valid_rt_count": int(main_trials["rt_numeric"].notna().sum()),
            "correct_valid_rt_count": int(correct_rt.count()),
            "mean_rt_correct": correct_rt.mean(),
            "median_rt_correct": correct_rt.median(),
            "missing_rt_count": int(main_trials["rt_numeric"].isna().sum()),
            "timeout_count": int(main_trials["is_timeout"].sum()),
        }
    ]
    pieces = [pd.DataFrame(rows)]
    pieces.append(summarize_group(main_trials, ["condition"], "by_condition"))
    pieces.append(summarize_group(main_trials, ["syllable_length"], "by_syllable_length"))
    real_words = main_trials[main_trials["condition"].eq("word")]
    pieces.append(summarize_group(real_words, ["frequency_group"], "realword_by_frequency_group"))
    pieces.append(
        summarize_group(
            real_words,
            ["frequency_group", "syllable_length"],
            "realword_by_frequency_group_x_syllable_length",
        )
    )
    return pd.concat(pieces, ignore_index=True, sort=False)


def write_processing_log(path, lines):
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    OUT_CLEAN.mkdir(parents=True, exist_ok=True)
    OUT_QC.mkdir(parents=True, exist_ok=True)

    stimulus, stimulus_summary, stimulus_encoding = validate_stimulus_file(STIMULUS_FILE)
    raw_files = sorted(RAW_DIR.glob("*.csv"))
    file_rows = []
    frames = []

    for path in raw_files:
        df, encoding, read_error = read_csv_with_fallback(path)
        file_rows.append(validate_file(df, path, encoding, read_error))
        if df is not None and all(col in df.columns for col in REQUIRED_COLUMNS):
            frames.append(add_metadata(df[REQUIRED_COLUMNS], path.name, encoding))

    if not frames:
        raise RuntimeError("No readable participant files with the required schema were found.")
    if stimulus is None:
        raise RuntimeError("Final stimulus file could not be read.")

    all_trials = pd.concat(frames, ignore_index=True)
    file_summary = pd.DataFrame(file_rows).sort_values("source_file")
    main_trials = all_trials[all_trials["is_main_trial"]].copy()
    stimulus_validation = validate_data_against_stimulus(main_trials, stimulus)
    rt_realword_correct = main_trials[
        main_trials["condition"].eq("word")
        & main_trials["is_correct"]
        & main_trials["rt_numeric"].notna()
        & ~main_trials["is_timeout"]
    ].copy()
    accuracy_main = main_trials.copy()

    participant_summary = participant_qc(all_trials, file_summary)
    unique_participants = all_trials["participant_id"].nunique()
    item_summary = item_qc(main_trials, unique_participants)
    design = design_summary(main_trials)
    full_stimulus_validation = pd.concat([stimulus_summary, stimulus_validation], ignore_index=True, sort=False)

    all_trials.to_csv(OUT_CLEAN / "all_trials_clean.csv", index=False, encoding="utf-8-sig")
    main_trials.to_csv(OUT_CLEAN / "main_trials_clean.csv", index=False, encoding="utf-8-sig")
    rt_realword_correct.to_csv(OUT_CLEAN / "rt_realword_correct.csv", index=False, encoding="utf-8-sig")
    accuracy_main.to_csv(OUT_CLEAN / "accuracy_main_trials.csv", index=False, encoding="utf-8-sig")

    participant_summary.to_csv(OUT_QC / "participant_qc_summary.csv", index=False, encoding="utf-8-sig")
    item_summary.to_csv(OUT_QC / "item_qc_by_trial_id.csv", index=False, encoding="utf-8-sig")
    design.to_csv(OUT_QC / "design_level_summary.csv", index=False, encoding="utf-8-sig")
    file_summary.to_csv(OUT_QC / "file_reading_summary.csv", index=False, encoding="utf-8-sig")
    full_stimulus_validation.to_csv(
        OUT_QC / "stimulus_validation_summary.csv", index=False, encoding="utf-8-sig"
    )

    flagged_participants = participant_summary["qc_flags"].fillna("").ne("").sum()
    stimulus_checks_passed = bool(full_stimulus_validation["passed"].all())
    each_trial_has_expected_n = bool(item_summary["presentation_count_ok"].all())
    minimum_n_reached = unique_participants >= 48
    r_ready = bool(flagged_participants == 0 and stimulus_checks_passed and minimum_n_reached)
    log_lines = [
        "RP2 clean data preparation log",
        "Step: analysis/01_prepare_clean_data.py",
        f"Raw input folder: {RAW_DIR}",
        f"Final stimulus reference: {STIMULUS_FILE}",
        f"Final stimulus encoding: {stimulus_encoding}",
        f"Files read: {len(raw_files)}",
        f"Unique participants: {unique_participants}",
        f"Participants flagged: {flagged_participants}",
        f"All trials rows: {len(all_trials)}",
        f"Main trial rows: {len(main_trials)}",
        f"RT real-word correct rows: {len(rt_realword_correct)}",
        f"Accuracy main trial rows: {len(accuracy_main)}",
        f"All trial_id values have expected presentations: {each_trial_has_expected_n}",
        f"Output cleaned data folder: {OUT_CLEAN}",
        f"Output QC folder: {OUT_QC}",
        f"Minimum N=48 reached: {minimum_n_reached}",
        f"All stimulus validation checks passed: {stimulus_checks_passed}",
        f"Cleaned data ready for R analysis: {r_ready}",
        "Raw data were not modified.",
    ]
    write_processing_log(OUT_QC / "processing_log.txt", log_lines)

    print("RP2 clean data preparation complete")
    print(f"Files read: {len(raw_files)}")
    print(f"Unique participants: {unique_participants}")
    print(f"Participants flagged: {flagged_participants}")
    print(f"Stimulus validation passed: {stimulus_checks_passed}")
    print(f"Each trial_id has {unique_participants} presentations: {each_trial_has_expected_n}")
    print(f"Total main trials: {len(main_trials)}")
    print(f"Total valid RTs: {main_trials['rt_numeric'].notna().sum()}")
    print("Cleaned data files created: yes")
    print(f"Output folder: {OUT_CLEAN}")
    print(f"QC folder: {OUT_QC}")


if __name__ == "__main__":
    main()
