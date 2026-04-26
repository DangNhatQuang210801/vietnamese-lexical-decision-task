# RP2 Vietnamese Lexical Decision Project

This repository contains materials for Research Project 2 on Vietnamese visual word recognition, focusing on how word frequency and syllable-based word length affect lexical decision responses.

## Current Status

The real-word stimulus set is frozen at:

```text
data/stimuli/final_realword_candidates_v4.csv
```

This v4 file is the quality-polished final real-word set. The next step is pseudoword construction matched by `syllable_length`.

## Folder Structure

- `docs/proposal_and_submission/`
  - Proposal/submission-facing files and final real-word diagnostics.
- `docs/personal_notes/`
  - Personal notes, RP2 reference materials, rule book, and project organization notes.
- `data/corpus/`
  - Raw/extracted Vietnamese corpus materials.
- `data/processed/`
  - Processed corpus frequency tables.
- `data/stimuli/`
  - Final real-word stimuli and candidate pools needed for reproducibility or pseudoword construction.
- `scripts/`
  - Corpus processing and real-word stimulus-selection scripts/notebooks.
- `archive/`
  - Old intermediate stimulus-selection files, earlier final versions, review notes, and old diagnostics.

## Key Files

- Real-word stimuli for pseudoword construction:
  `data/stimuli/final_realword_candidates_v4.csv`
- Final real-word diagnostics:
  `docs/proposal_and_submission/final_realword_candidates_v4_diagnostics.txt`
- Candidate shortlist:
  `data/stimuli/candidate_shortlist_by_length.csv`
- Main corpus frequency table:
  `data/processed/all_1to4gram_frequency.csv`

## Next Step

Construct pseudowords matched to the v4 real-word stimuli by `syllable_length`, while preserving the final real-word file unchanged.
