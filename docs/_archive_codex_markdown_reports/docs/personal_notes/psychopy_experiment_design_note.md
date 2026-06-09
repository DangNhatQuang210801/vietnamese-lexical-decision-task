# PsychoPy Experiment Design Note

## Task Structure

This experiment is a Vietnamese lexical decision task for RP2. Each participant sees one stimulus at a time and decides whether it is a real Vietnamese lexical item or a pseudoword.

The PsychoPy script uses:

- `data/stimuli/final/final_ldt_stimuli_v1.csv`
- randomized main-trial order
- a short built-in practice block before the main task
- one output CSV per participant in `data/experiment_results/`

## Response Keys

- `f` = word
- `j` = nonword

The script maps key presses to `response_label` and compares this value with the `correct_response` column.

## Trial Timing

Each trial follows this sequence:

1. Fixation cross: 500 ms
2. Stimulus display: until response or timeout
3. Timeout: 3000 ms
4. Response and reaction time recorded

Practice trials include brief feedback. Main trials do not include feedback.

## Output Data Columns

The participant output file includes:

- `participant_id`
- `block`
- `trial_id`
- `stimulus`
- `condition`
- `is_word`
- `syllable_length`
- `frequency`
- `log_frequency`
- `source_realword`
- `correct_response`
- `key_pressed`
- `response_label`
- `accuracy`
- `rt`

## Connection To RP2 Analysis

The main analysis will use reaction time from correct main-trial responses. The key predictors are:

- `log_frequency`
- `syllable_length`
- `log_frequency x syllable_length`

Real-word trials provide the frequency and syllable-length predictors for the linear mixed-effects model. Pseudoword trials support the lexical decision task structure and accuracy checking but are not the main frequency-effect analysis target.
