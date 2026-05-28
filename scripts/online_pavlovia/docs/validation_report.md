# RP2 Pavlovia Validation Report

## Condition Files

- Main condition file: `conditions\main_trials_3x4.csv`
- Practice condition file: `conditions\practice_trials.csv`

## Trial Counts

- Main trials: 120
- Practice trials: 4
- Main real words: 72
- Main pseudowords: 48
- Practice words: 2
- Practice pseudowords: 2

## Main Trial Balance

| Check | Result |
|---|---:|
| Syllable length 1 | 30 |
| Syllable length 2 | 30 |
| Syllable length 3 | 30 |
| Syllable length 4 | 30 |
| frequency_group `low` | 24 |
| frequency_group `mid` | 24 |
| frequency_group `high` | 24 |
| frequency_group `control` | 48 |

## Required Columns

- Main missing columns: none
- Practice missing columns: none

## Missing Value Checks

- Main required-value problems: 0
- Practice required-value problems: 0
- Real-word missing frequency/log_frequency in main trials: 0
- Pseudowords with `NA` frequency/log_frequency in main trials: 48
- Practice trials with `NA` frequency/log_frequency: 4 (expected)

## Response Mapping

- Required mapping: `f = word`, `j = nonword`.
- This mapping must be set in the Builder keyboard components and scoring Code Components.

## PsychoPy/Pavlovia Readiness

- Condition files ready for Builder: yes
- `.psyexp` still needs to be built and manually tested in PsychoPy Builder/Pavlovia Piloting.
