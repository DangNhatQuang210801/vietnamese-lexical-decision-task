# Workflow Overview

## 1. Corpus and Stimulus Construction

Vietnamese corpus data were used to support frequency estimation for candidate real words. Because Vietnamese writing separates syllables with spaces, corpus n-grams cannot automatically be treated as lexical words. Candidate real-word items therefore require manual lexical checking.

## 2. Final Stimulus Selection

The final stimulus file is `data/stimuli/final/final_ldt_stimuli_3x4_v1.csv`. It contains 72 real words and 48 pseudowords. Real words are balanced across frequency group and syllable length. Pseudowords are balanced by syllable length and serve as lexical decision controls.

## 3. PsychoPy Experiment

The experiment is run with `scripts/run_vietnamese_ldt_psychopy.py`. The script loads the final 3 x 4 stimulus file, presents 4 practice trials, then presents 120 randomized main trials. The response mapping is F = word and J = nonword.

## 4. Participant Data Collection

Each participant creates one CSV file in `data/experiment_results`. Raw files should not be edited manually. If a participant quits early, the partial file should be kept and documented rather than repaired by hand.

## 5. Quality Control

Quality control should be run after each collection batch. Checks include row counts, practice/main trial counts, participant ID matching, duplicate IDs, response mapping, accuracy consistency, missing RTs, participant accuracy, response bias, and item-level accuracy/RT.

## 6. Final Analysis

Final analysis should use cleaned analysis copies derived from the raw files. The main RT analysis should focus on correct real-word trials. Incorrect trials, missing RTs, and timeouts should be excluded from RT analysis but retained for accuracy summaries.

## 7. Proposal and Report Updates

Proposal and report text should reflect the finalized 3 x 4 design. Descriptive progress summaries can be updated during data collection, but inferential claims should wait until the final dataset is frozen and analyzed.

