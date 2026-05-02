# RP2 Vietnamese Lexical Decision Project

This repository contains materials for Research Project 2 on Vietnamese visual word recognition, focusing on how word frequency and syllable-based word length affect lexical decision responses.

## Current Status

The final stimulus deliverables are organized in:

```text
data/stimuli/final/
```

The final real-word set, final pseudoword set, and combined PsychoPy-ready stimulus file are now frozen for experiment setup.

## Folder Structure

- `docs/proposal_and_submission/`
  - Proposal/submission-facing files.
- `docs/personal_notes/`
  - Personal notes, RP2 reference materials, rule book, and project organization notes.
- `data/corpus/`
  - Corpus materials organized by source state.
- `data/corpus/raw/`
  - Original compressed corpus archive.
- `data/corpus/extracted/`
  - Extracted corpus folders used by scripts.
- `data/processed/`
  - Processed corpus frequency tables.
- `data/stimuli/`
  - Stimulus-selection history, review files, candidate pools, and intermediate pseudoword materials.
- `data/stimuli/final/`
  - Final stimulus deliverables for the lexical decision experiment.
- `scripts/`
  - Corpus processing and real-word stimulus-selection scripts/notebooks.
- `archive/`
  - Old intermediate stimulus-selection files, earlier final versions, review notes, and old diagnostics.

## Final Stimulus Files

- Frozen real-word set:
  `data/stimuli/final/final_realword_candidates_v4.csv`
- Frozen pseudoword set:
  `data/stimuli/final/final_pseudoword_candidates_v2.csv`
- Final combined PsychoPy-ready stimulus file:
  `data/stimuli/final/final_ldt_stimuli_v1.csv`

## Other Key Files

- Candidate shortlist:
  `data/stimuli/candidate_shortlist_by_length.csv`
- Main corpus frequency table:
  `data/processed/all_1to4gram_frequency.csv`

## Next Step

Use `data/stimuli/final/final_ldt_stimuli_v1.csv` as the PsychoPy conditions file.
