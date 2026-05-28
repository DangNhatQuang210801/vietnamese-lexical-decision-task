# RP2 Data Collection Progress Summary

## 1. Final Experimental Design
- Design: within-participant Vietnamese visual lexical decision task.
- Core real-word design: 3 x 4 factorial design.
- Independent variables: word frequency group and syllable length.
- Frequency levels: low, mid, high, defined within each syllable-length group.
- Length levels: 1, 2, 3, and 4 syllables.
- Real-word conditions: 12, with 6 real words per condition.
- Real-word items: 72.
- Pseudoword controls: 48, balanced as 12 per syllable length.
- Total main trials per participant: 120.

## 2. Data Collection Tool
- The experiment is implemented in PsychoPy.
- The script points to `data/stimuli/final/final_ldt_stimuli_3x4_v1.csv`.
- Results are saved in `data/experiment_results`.
- Recorded variables include participant_id, block, trial_id, stimulus, condition, is_word, syllable_length, frequency_group, frequency, log_frequency, source_realword, correct_response, key_pressed, response_label, accuracy, and rt.
- Response mapping: F = word, J = nonword.

## 3. Data Collected So Far
- Participant CSV files in the current results folder: 48.
- Unique participant IDs: 48.
- Structurally usable participants: 48.
- Participants currently flagged for exclusion: 0.
- Current usable N after structural and basic quality checks: 48.
- Main trials collected from usable participants: 5760.
- Valid RTs available from usable main trials: 5715.

## 4. Current Data Quality
- Overall main-trial accuracy: 90.2%.
- Real-word accuracy: 95.7%.
- Pseudoword accuracy: 82.0%.
- All valid main-trial RTs: mean 0.721 s, median 0.683 s (n = 5715)
- Correct main-trial RTs: mean 0.714 s, median 0.676 s (n = 5196)
- Missing RTs/timeouts in usable main trials: 45.
- No participants are currently flagged by the basic exclusion rules.
- No item is currently flagged by the basic item rules.

## 5. Sanity-Check Patterns
- Correct real-word RTs: mean 0.599 s, median 0.574 s.
- Correct pseudoword RTs: mean 0.916 s, median 0.885 s.
- Real words are currently faster than pseudowords.
- Pseudoword accuracy is lower than real-word accuracy.
- Correct RT by syllable length: 1 syllable(s): mean 0.530 s; 2 syllable(s): mean 0.645 s; 3 syllable(s): mean 0.803 s; 4 syllable(s): mean 0.881 s.
- Correct real-word RT by frequency group: high: mean 0.510 s; low: mean 0.668 s; mid: mean 0.618 s.
- High-frequency real words are currently faster than low-frequency real words.

## 6. Progress Toward Target Sample Size
- Minimum target N: 48 participants.
- Preferred target N: about 50-60 participants.
- More usable participants needed to reach N = 48: 0.
- More usable participants needed to reach N = 50: 2.
- More usable participants needed to reach N = 60: 12.

## 7. Current Risks and Limitations
- Encoding is not fully uniform across files: {'utf-8-sig': 11, 'cp1258': 37}. This should be checked before final analysis.
- `docs/current_status_audit/current_status_report.md` was not found, so this summary was calculated directly from the current result files.
- Data collection is still ongoing. These summaries should be treated as progress checks, not final results.
- The current patterns are useful for monitoring task feasibility, but final claims should wait until the dataset is complete and the analysis plan is applied.

## 8. Short Recommendation
- The task appears structurally ready to continue data collection. The current usable N is 48.
- Continue collecting participants until at least the minimum target is reached, preferably closer to 50-60 participants.