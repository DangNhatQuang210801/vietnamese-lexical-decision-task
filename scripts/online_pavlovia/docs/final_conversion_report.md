# RP2 Pavlovia Conversion Report

## Source Files Inspected

- Offline script: `scripts/run_vietnamese_ldt_psychopy.py`
- Main stimulus file: `data/stimuli/final/final_ldt_stimuli_3x4_v1.csv`

The offline script was not modified.

## Confirmed Offline Trial Flow

- Participant info dialog with participant ID, session, and fullscreen option.
- Instruction screen.
- Four practice trials.
- Practice feedback after each practice trial.
- Main instructions.
- Main trials without feedback.
- Fixation cross before each trial.
- Stimulus presentation until response or timeout.
- Response mapping: `F = word`, `J = nonword`.
- Offline-only controls: `S` save and exit, Escape emergency quit.

## Confirmed Output Variables

The offline script records:

- `participant_id`
- `block`
- `trial_id`
- `stimulus`
- `condition`
- `is_word`
- `syllable_length`
- `frequency_group`
- `frequency`
- `log_frequency`
- `source_realword`
- `correct_response`
- `key_pressed`
- `response_label`
- `accuracy`
- `rt`

The Builder/Pavlovia spec is designed to log the same essential variables through PsychoJS experiment data saving.

## Files Created

- `online_pavlovia/conditions/main_trials_3x4.csv`
- `online_pavlovia/conditions/practice_trials.csv`
- `online_pavlovia/docs/builder_construction_spec.md`
- `online_pavlovia/docs/validation_report.md`
- `online_pavlovia/docs/final_conversion_report.md`
- `online_pavlovia/README_online_pavlovia.md`

## Validation Summary

- Main trial count: 120.
- Practice trial count: 4.
- Main real words: 72.
- Main pseudowords: 48.
- Required columns are present in both condition files.
- Response mapping is documented as `f = word`, `j = nonword`.
- Real words have `frequency` and `log_frequency`.
- Main pseudowords have `NA` frequency and `NA` log_frequency, as expected.
- `frequency_group` is preserved:
  - real words: `low`, `mid`, `high`
  - pseudowords: `control`
  - practice trials: `practice`

## What Still Needs Manual Checking in PsychoPy Builder

- Build the `.psyexp` file manually from `docs/builder_construction_spec.md`.
- Confirm Vietnamese diacritics display correctly in the selected online font.
- Confirm the Builder keyboard components store the first valid key only.
- Confirm timeout trials save blank key/RT and `accuracy = 0`.
- Confirm generated PsychoJS code runs in a browser.
- Confirm Pavlovia saves the data columns after a complete pilot run.
- Confirm data are saved if a participant closes the browser early; do not assume this works without piloting.

## Is It Ready to Sync to Pavlovia?

The condition files and Builder construction plan are ready. The experiment is not fully ready to sync until the `.psyexp` file has been built in PsychoPy Builder and tested locally.

After the `.psyexp` file is built, it should be synced first in Pavlovia `Piloting` mode, not `Running` mode.

## Issues That Cannot Be Automatically Converted

- The offline script uses local Python file writing. Pavlovia must use PsychoJS/Pavlovia data saving instead.
- The offline `S` save-and-exit behavior cannot be assumed to work online without custom PsychoJS testing.
- Escape behavior and browser quit behavior differ online.
- PsychoPy Builder/PsychoJS conversion must be checked manually because custom Python scripts do not run directly on Pavlovia.

