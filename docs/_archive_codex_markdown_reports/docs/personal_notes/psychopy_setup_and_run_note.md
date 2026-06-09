# PsychoPy Setup And Run Note

## Purpose

This note explains how to run the RP2 Vietnamese lexical decision task using the PsychoPy script:

```text
scripts/run_vietnamese_ldt_psychopy.py
```

The script uses the final PsychoPy-ready stimulus file:

```text
data/stimuli/final/final_ldt_stimuli_v1.csv
```

## Recommended Setup On Windows

Install PsychoPy manually using PsychoPy Standalone for Windows.

Recommended approach:

1. Download PsychoPy Standalone from the official PsychoPy website.
2. Install it normally on Windows.
3. Open PsychoPy.
4. Open `scripts/run_vietnamese_ldt_psychopy.py` in PsychoPy.
5. Run the script from PsychoPy.

Do not install PsychoPy into this repository with `pip install psychopy`.

Do not create a virtual environment inside this repository.

Do not modify project environment files unless a project-specific environment file is intentionally added later.

## Experiment Files

Input stimulus file:

```text
data/stimuli/final/final_ldt_stimuli_v1.csv
```

Output folder:

```text
data/experiment_results/
```

Each participant run creates one CSV file with the participant ID, session number, and timestamp in the filename.

## Task Structure

The experiment is a Vietnamese lexical decision task.

Each trial follows this structure:

1. Fixation cross for 500 ms
2. Stimulus shown until response or timeout
3. Key press and reaction time recorded
4. Accuracy computed from `correct_response`

The main trials are randomized.

A short practice block is shown before the main task.

## Response Keys

```text
f = word
j = nonword
```

The script maps keys to response labels:

```text
f -> word
j -> nonword
```

Accuracy is computed by comparing the response label with the `correct_response` column.

## Output Columns

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

## Analysis Connection

For RP2 analysis, use main-trial responses.

The main real-word analysis should focus on:

- correct responses
- reaction time
- `log_frequency`
- `syllable_length`
- `log_frequency x syllable_length`

Pseudoword trials support the lexical decision task and accuracy checking, but the frequency predictor applies to real-word trials.
