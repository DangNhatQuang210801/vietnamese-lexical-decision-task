# Participant Quality Check Report

## 1. Data Files Checked

- Data folder: `data/experiment_results`
- CSV files checked: 31
- `1_session-001_ldt_20260522_213504.csv`
- `2_session-001_ldt_20260522_221125.csv`
- `3_session-001_ldt_20260522_222932.csv`
- `4_session-001_ldt_20260522_224200.csv`
- `5_session-001_ldt_20260522_224430.csv`
- `6_session-001_ldt_20260522_224700.csv`
- `7_session-001_ldt_20260522_224930.csv`
- `8_session-001_ldt_20260522_225200.csv`
- `9_session-001_ldt_20260522_231226.csv`
- `10_session-001_ldt_20260522_231506.csv`
- `11_session-001_ldt_20260523_090000.csv`
- `12_session-001_ldt_20260523_090217.csv`
- `13_session-001_ldt_20260523_090434.csv`
- `14_session-001_ldt_20260523_090600.csv`
- `15_session-001_ldt_20260523_090817.csv`
- `16_session-001_ldt_20260523_091034.csv`
- `17_session-001_ldt_20260523_091200.csv`
- `18_session-001_ldt_20260523_091417.csv`
- `19_session-001_ldt_20260523_091634.csv`
- `20_session-001_ldt_20260523_091800.csv`
- `21_session-001_ldt_20260523_092017.csv`
- `22_session-001_ldt_20260523_092234.csv`
- `23_session-001_ldt_20260523_092400.csv`
- `24_session-001_ldt_20260523_092617.csv`
- `25_session-001_ldt_20260523_092834.csv`
- `26_session-001_ldt_20260523_093000.csv`
- `27_session-001_ldt_20260523_093217.csv`
- `28_session-001_ldt_20260523_093434.csv`
- `29_session-001_ldt_20260523_093600.csv`
- `30_session-001_ldt_20260523_093817.csv`
- `31_session-001_ldt_20260524_000257.csv`

## 2. Structural Validation

- All files use the same schema.
- Each file has 124 rows, with 4 practice trials and 120 main trials.
- Participant IDs match filenames.
- No duplicate participant IDs were found.
- No duplicate trial IDs were found within participant files.
- Encoding note: some files required fallback decoding for QC only: 11_session-001_ldt_20260523_090000.csv (cp1258), 12_session-001_ldt_20260523_090217.csv (cp1258), 13_session-001_ldt_20260523_090434.csv (cp1258), 14_session-001_ldt_20260523_090600.csv (cp1258), 15_session-001_ldt_20260523_090817.csv (cp1258), 16_session-001_ldt_20260523_091034.csv (cp1258), 17_session-001_ldt_20260523_091200.csv (cp1258), 18_session-001_ldt_20260523_091417.csv (cp1258), 19_session-001_ldt_20260523_091634.csv (cp1258), 20_session-001_ldt_20260523_091800.csv (cp1258), 21_session-001_ldt_20260523_092017.csv (cp1258), 22_session-001_ldt_20260523_092234.csv (cp1258), 23_session-001_ldt_20260523_092400.csv (cp1258), 24_session-001_ldt_20260523_092617.csv (cp1258), 25_session-001_ldt_20260523_092834.csv (cp1258), 26_session-001_ldt_20260523_093000.csv (cp1258), 27_session-001_ldt_20260523_093217.csv (cp1258), 28_session-001_ldt_20260523_093434.csv (cp1258), 29_session-001_ldt_20260523_093600.csv (cp1258), 30_session-001_ldt_20260523_093817.csv (cp1258).

## 3. Participant-Level Quality

| Participant | Main | Valid RT | Missing RT | Overall Acc | Word Acc | Pseudo Acc | Practice Acc | Median RT | Mean RT | Flags |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 120 | 120 | 0 | 0.933333 | 0.986111 | 0.854167 | 1 | 0.660661 | 0.700661 | none |
| 2 | 120 | 120 | 0 | 0.866667 | 0.972222 | 0.708333 | 0.75 | 0.582647 | 0.630099 | none |
| 3 | 120 | 120 | 0 | 0.891667 | 0.972222 | 0.770833 | 1 | 0.574469 | 0.655298 | none |
| 4 | 120 | 119 | 1 | 0.916667 | 1 | 0.791667 | 1 | 0.755783 | 0.764897 | none |
| 5 | 120 | 120 | 0 | 0.858333 | 0.972222 | 0.6875 | 1 | 0.67463 | 0.702322 | none |
| 6 | 120 | 120 | 0 | 0.941667 | 1 | 0.854167 | 1 | 0.682276 | 0.715356 | none |
| 7 | 120 | 119 | 1 | 0.916667 | 0.986111 | 0.8125 | 1 | 0.594294 | 0.639754 | none |
| 8 | 120 | 119 | 1 | 0.925 | 0.972222 | 0.854167 | 0.5 | 0.57342 | 0.600196 | none |
| 9 | 120 | 120 | 0 | 0.875 | 0.972222 | 0.729167 | 0.75 | 0.518637 | 0.580534 | none |
| 10 | 120 | 120 | 0 | 0.916667 | 0.986111 | 0.8125 | 1 | 0.600467 | 0.645168 | none |
| 11 | 120 | 119 | 1 | 0.841667 | 0.819444 | 0.875 | 0.75 | 0.712039 | 0.755807 | none |
| 12 | 120 | 118 | 2 | 0.916667 | 0.958333 | 0.854167 | 1 | 0.662207 | 0.717903 | none |
| 13 | 120 | 120 | 0 | 0.966667 | 1 | 0.916667 | 1 | 0.67717 | 0.732386 | none |
| 14 | 120 | 120 | 0 | 0.916667 | 1 | 0.791667 | 0.75 | 0.639005 | 0.665229 | none |
| 15 | 120 | 119 | 1 | 0.85 | 0.944444 | 0.708333 | 1 | 0.645986 | 0.670762 | none |
| 16 | 120 | 119 | 1 | 0.883333 | 0.958333 | 0.770833 | 1 | 0.802687 | 0.808725 | none |
| 17 | 120 | 120 | 0 | 0.975 | 1 | 0.9375 | 1 | 0.636281 | 0.652808 | none |
| 18 | 120 | 118 | 2 | 0.833333 | 0.930556 | 0.6875 | 1 | 0.701055 | 0.723045 | none |
| 19 | 120 | 117 | 3 | 0.9 | 0.930556 | 0.854167 | 1 | 0.548188 | 0.560669 | none |
| 20 | 120 | 118 | 2 | 0.883333 | 0.930556 | 0.8125 | 1 | 0.799637 | 0.836018 | none |
| 21 | 120 | 120 | 0 | 0.966667 | 1 | 0.916667 | 1 | 0.747669 | 0.786435 | none |
| 22 | 120 | 116 | 4 | 0.916667 | 0.972222 | 0.833333 | 1 | 0.623676 | 0.662632 | none |
| 23 | 120 | 120 | 0 | 0.95 | 0.972222 | 0.916667 | 1 | 0.673709 | 0.716156 | none |
| 24 | 120 | 120 | 0 | 0.95 | 0.986111 | 0.895833 | 1 | 0.574753 | 0.599815 | none |
| 25 | 120 | 119 | 1 | 0.9 | 0.958333 | 0.8125 | 1 | 0.722265 | 0.75639 | none |
| 26 | 120 | 120 | 0 | 0.958333 | 0.986111 | 0.916667 | 1 | 0.64185 | 0.676366 | none |
| 27 | 120 | 120 | 0 | 0.825 | 0.875 | 0.75 | 1 | 0.632439 | 0.656693 | none |
| 28 | 120 | 119 | 1 | 0.933333 | 1 | 0.833333 | 1 | 0.79852 | 0.834259 | none |
| 29 | 120 | 120 | 0 | 0.95 | 0.972222 | 0.916667 | 1 | 0.86917 | 0.896411 | none |
| 30 | 120 | 117 | 3 | 0.816667 | 0.875 | 0.729167 | 1 | 0.609445 | 0.634309 | none |
| 31 | 120 | 120 | 0 | 0.816667 | 0.972222 | 0.583333 | 1 | 0.529652 | 0.580753 | none |

## 4. Participants Flagged for Possible Exclusion

- No participants were flagged by the predefined exclusion rules.

## 5. Response Bias Check

| Participant | F responses | J responses | Word response proportion | Nonword response proportion | Bias flag |
|---:|---:|---:|---:|---:|---|
| 1 | 78 | 42 | 0.65 | 0.35 | no |
| 2 | 84 | 36 | 0.7 | 0.3 | no |
| 3 | 81 | 39 | 0.675 | 0.325 | no |
| 4 | 81 | 38 | 0.680672 | 0.319328 | no |
| 5 | 85 | 35 | 0.708333 | 0.291667 | no |
| 6 | 79 | 41 | 0.658333 | 0.341667 | no |
| 7 | 80 | 39 | 0.672269 | 0.327731 | no |
| 8 | 76 | 43 | 0.638655 | 0.361345 | no |
| 9 | 83 | 37 | 0.691667 | 0.308333 | no |
| 10 | 80 | 40 | 0.666667 | 0.333333 | no |
| 11 | 64 | 55 | 0.537815 | 0.462185 | no |
| 12 | 76 | 42 | 0.644068 | 0.355932 | no |
| 13 | 76 | 44 | 0.633333 | 0.366667 | no |
| 14 | 82 | 38 | 0.683333 | 0.316667 | no |
| 15 | 81 | 38 | 0.680672 | 0.319328 | no |
| 16 | 79 | 40 | 0.663866 | 0.336134 | no |
| 17 | 75 | 45 | 0.625 | 0.375 | no |
| 18 | 81 | 37 | 0.686441 | 0.313559 | no |
| 19 | 72 | 45 | 0.615385 | 0.384615 | no |
| 20 | 74 | 44 | 0.627119 | 0.372881 | no |
| 21 | 76 | 44 | 0.633333 | 0.366667 | no |
| 22 | 75 | 41 | 0.646552 | 0.353448 | no |
| 23 | 74 | 46 | 0.616667 | 0.383333 | no |
| 24 | 76 | 44 | 0.633333 | 0.366667 | no |
| 25 | 77 | 42 | 0.647059 | 0.352941 | no |
| 26 | 75 | 45 | 0.625 | 0.375 | no |
| 27 | 75 | 45 | 0.625 | 0.375 | no |
| 28 | 79 | 40 | 0.663866 | 0.336134 | no |
| 29 | 74 | 46 | 0.616667 | 0.383333 | no |
| 30 | 75 | 42 | 0.641026 | 0.358974 | no |
| 31 | 90 | 30 | 0.75 | 0.25 | no |

## 6. Item-Level Problems

- Flagged items: 6
| Stimulus | Condition | Length | Frequency group | Presentations | Accuracy | Median RT | Flags |
|---|---|---:|---|---:|---:|---:|---|
| nhà thiết ké | pseudoword | 3 | control | 11 | 0.454545 | 0.720656 | accuracy_below_60;many_participants_confuse_item |
| nướp | pseudoword | 1 | control | 11 | 0.454545 | 0.552722 | accuracy_below_60;many_participants_confuse_item |
| sọng | pseudoword | 1 | control | 11 | 0.454545 | 0.433384 | accuracy_below_60;many_participants_confuse_item |
| trính độ học vấn | pseudoword | 4 | control | 11 | 0.272727 | 0.829266 | accuracy_below_60;many_participants_confuse_item |
| trý | pseudoword | 1 | control | 11 | 0.454545 | 0.480804 | accuracy_below_60;many_participants_confuse_item |
| địm kiến xã hội | pseudoword | 4 | control | 11 | 0.363636 | 0.683573 | accuracy_below_60;many_participants_confuse_item |

## 7. Design-Level Pattern

| Level type | Level | Trials | Valid RT | Accuracy | Mean RT | Median RT |
|---|---|---:|---:|---:|---:|---:|
| overall | all | 3720 | 3696 | 0.902957 | 0.695434 | 0.651662 |
| condition | word | 2232 | 2224 | 0.963262 | 0.585098 | 0.553173 |
| condition | pseudoword | 1488 | 1472 | 0.8125 | 0.862136 | 0.832723 |
| syllable_length | 1 | 930 | 923 | 0.896774 | 0.513429 | 0.492507 |
| syllable_length | 2 | 930 | 926 | 0.916129 | 0.627527 | 0.600028 |
| syllable_length | 3 | 930 | 921 | 0.912903 | 0.784142 | 0.770089 |
| syllable_length | 4 | 930 | 926 | 0.886022 | 0.856525 | 0.816576 |
| real_word_frequency_group | low | 744 | 740 | 0.954301 | 0.646496 | 0.619973 |
| real_word_frequency_group | mid | 744 | 742 | 0.97043 | 0.609066 | 0.576104 |
| real_word_frequency_group | high | 744 | 742 | 0.965054 | 0.499898 | 0.486036 |

## 8. Recommendation

- Currently usable participants by the predefined rules: 31 of 31.
- No participants need exclusion based on the current rules.
- Data collection can continue; the current files are structurally consistent with the final 3x4 design.
- 6 items should be reviewed before final analysis because they met item-level flag criteria.
- Continue monitoring pseudoword accuracy because it is expected to be lower than real-word accuracy, but very low pseudoword accuracy would indicate task difficulty or response-mapping problems.
