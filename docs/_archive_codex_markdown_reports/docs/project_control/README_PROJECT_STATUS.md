# RP2 Project Status

## Current Final Design

The RP2 experiment is a within-participant Vietnamese visual lexical decision task.

- Core real-word design: 3 x 4.
- Frequency group: low, mid, high.
- Syllable length: 1, 2, 3, and 4 syllables.
- Real-word conditions: 12.
- Real words per condition: 6.
- Total real-word items: 72.
- Pseudoword controls: 48.
- Pseudowords per syllable-length level: 12.
- Total main trials per participant: 120.
- Practice trials: 4.

Frequency groups are defined within each syllable-length group. Pseudowords are lexical decision controls and are not part of the frequency manipulation.

## Current Participant Status

- Current participant CSV files in `data/experiment_results`: 48.
- Current unique participant IDs: 48.
- Current structurally usable participants: 48.
- Current usable N after latest basic QC: 48.
- Participants currently flagged for exclusion: 0.

## Target N

- Minimum target: 48 participants.
- Preferred target: about 50-60 participants.

The dataset has reached the minimum target, but data collection can continue toward the preferred range if feasible.

## Current Status

Data collection is still ongoing unless the dataset is explicitly frozen. The current descriptive patterns should be treated as progress and quality checks, not as final results.

## Current Final/Frozen Experiment Files

These files should be treated as the current final experiment materials:

- `data/stimuli/final/final_ldt_stimuli_3x4_v1.csv`
- `data/stimuli/final/final_ldt_stimuli_3x4_v1_diagnostics.txt`
- `scripts/run_vietnamese_ldt_psychopy.py`
- `docs/proposal_and_submission/Dang_NhatQuang_Proposal_24.05.docx`

## Files That Should Not Be Edited Directly

- Raw participant CSV files in `data/experiment_results`.
- The final stimulus CSV.
- The PsychoPy script during active data collection, unless a new tested version is documented.
- Existing proposal files; create a new version instead of overwriting.

