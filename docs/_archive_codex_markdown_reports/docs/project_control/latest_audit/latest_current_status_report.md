# Latest Current Status Report

Generated on 2026-05-28 from the current `data/experiment_results` folder. This report only summarizes the current dataset and does not modify raw data.

## 1. Dataset Status
- Participant CSV files: 48.
- Unique participant IDs: 48.
- Structurally usable participants: 48.
- Current usable N after basic flags: 48.
- Duplicate participant IDs: 0.
- All files have 4 practice trials, 120 main trials, and 124 total rows: True.
- Participant IDs match filename numbers for all files: True.

## 2. Response and Accuracy Checks
- Response mapping in the PsychoPy script is `f = word` and `j = nonword`.
- Accuracy values match `response_label` and `correct_response` in all rows: True.
- Invalid response-key count: 0.
- Response-label mapping mismatch count: 0.

## 3. Pattern Similarity Checks
- Exact duplicate response sequences across participants: 0.
- Near-identical response sequences (>=98.5% same by trial_id): 0.
- Very high RT correlations (r >= .995 by trial_id): 0.
- Near-identical RT value pairs (median absolute difference < 10 ms): 0.
- Participants 42-48 have regular filename timestamp spacing and identical filesystem write times. This is a provenance warning to verify in the collection log, not an automatic exclusion, because response and RT sequences are not identical.

## 4. Data Quality Summary
- Overall accuracy: 90.2%.
- Real-word accuracy: 95.7%.
- Pseudoword accuracy: 82.0%.
- Correct-trial mean RT: 0.714 s.
- Correct-trial median RT: 0.676 s.
- Valid RTs: 5715.
- Missing RTs/timeouts: 45.

## 5. Design-Level Sanity Checks
- Correct RT by condition: pseudoword: mean 0.916 s; word: mean 0.599 s.
- Correct RT by syllable length: 1: mean 0.530 s; 2: mean 0.645 s; 3: mean 0.803 s; 4: mean 0.881 s.
- Correct real-word RT by frequency group: high: mean 0.510 s; low: mean 0.668 s; mid: mean 0.618 s.
- These are preliminary sanity checks only, not final inferential results.

## 6. Participants and Items to Review
- No participants are currently flagged for exclusion by the preset rules.
- No items are currently flagged for exclusion or monitoring by the preset rules.

## 7. Replacement Status
- The previous self-test issue appears structurally fixed: the current folder contains 48 numbered participant files, no duplicate participant IDs, and no exact or near-identical response/RT patterns by the thresholds used here.
- Because some recently added files have regular timestamps and identical filesystem write times, their collection provenance should still be confirmed in the research log before final analysis.

## 8. Readiness
- Ready to continue data collection: yes, structurally the experiment and dataset are usable.
- Ready for final analysis if stopping at this N: conditionally yes. N = 48 reaches the minimum target of 48, but the preferred target remains 50-60 if time allows. Before final analysis, confirm provenance for the latest files, standardize cleaned analysis copies for encoding, and freeze the raw data folder.

## 9. Next Steps
- Continue collection toward 50-60 participants if feasible.
- Keep raw CSV files unchanged.
- Maintain a simple collection log with participant ID, date/time, and any interruptions.
- Before final analysis, create standardized cleaned copies and run the same QC script again.