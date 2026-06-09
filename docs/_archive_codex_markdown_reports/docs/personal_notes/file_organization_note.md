# RP2 File Organization Note

This cleanup organizes the project for the next phase: pseudoword construction.

## Final / Current Stimulus Files

Current real-word stimulus set:

- `data/final_stimuli/final_realword_candidates_v4.csv`

Current diagnostics for that file:

- `data/final_stimuli/final_realword_candidates_v4_diagnostics.txt`

Use `final_realword_candidates_v4.csv` as the real-word source for pseudoword construction.

## Processed Corpus Outputs

Corpus-derived frequency tables are stored in:

- `data/processed_corpus/unigrams_frequency.csv`
- `data/processed_corpus/bigrams_frequency.csv`
- `data/processed_corpus/trigrams_frequency.csv`
- `data/processed_corpus/fourgrams_frequency.csv`
- `data/processed_corpus/all_1to4gram_frequency.csv`

These files are the processed corpus frequency resources used for candidate generation and frequency lookup.

## Candidate Pools

Candidate pool and shortlist files are stored in:

- `data/candidate_pools/candidate_pool_filtered.csv`
- `data/candidate_pools/candidate_pool_kept_only.csv`
- `data/candidate_pools/candidate_pool_manual_review.csv`
- `data/candidate_pools/candidate_shortlist_by_length.csv`

These are not the final stimulus set; they are source/reference files for review, replacement, and future stimulus expansion.

## Diagnostics

Review notes, summaries, and diagnostics are stored in:

- `docs/diagnostics/`

This includes candidate summaries, shortlist summaries, syllable-length summaries, rebalance notes, and older final-set diagnostics.

## Archived Stimulus-Selection History

Intermediate review files and previous real-word candidate versions are stored in:

- `archive/stimulus_selection_history/`

This includes:

- `final_realword_candidates_v1.csv`
- `final_realword_candidates_v2.csv`
- proposal/replacement review CSVs
- the manual selection sheet
- exported review/check files
- `file_organization_moved_files.csv`

These files preserve the selection history but should not be used as the current source for pseudoword construction.

## Next File To Use

For pseudoword construction, use:

```text
data/final_stimuli/final_realword_candidates_v4.csv
```

This is the current quality-polished final real-word stimulus file.

## Folder Cleanup Update

Additional folder cleanup on 2026-04-26:

- The old `data_sample/` folder was moved to `archive/legacy_sample_corpus_2026-04-26/`.
- The old `Note and examples/` folder was moved to `docs/reference_notes/`.
- `r_package_status.csv` was moved to `docs/diagnostics/r_package_status.csv`.
- Empty duplicate/processed folders were removed after confirming they contained no files.

The active project map is now documented in:

```text
docs/project_map.md
```
