# Data Collection Protocol

## Before the Participant Starts

1. Open PsychoPy on the testing computer.
2. Open or run `scripts/run_vietnamese_ldt_psychopy.py` from the project root.
3. Confirm that the script uses `data/stimuli/final/final_ldt_stimuli_3x4_v1.csv`.
4. Prepare the next participant ID. Use one participant ID per person.

## Starting the Session

1. Run the script.
2. Enter the participant ID in the dialog.
3. Keep the session value as `001` unless there is a documented reason to change it.
4. Explain the task clearly:
   - Press F for a real Vietnamese word.
   - Press J for a nonword/pseudoword.
   - Respond as quickly and accurately as possible.
5. Explain that practice trials come first.

## During the Session

1. Do not coach the participant during the main trials.
2. If the participant needs to stop, use the save-and-exit option where possible.
3. Escape should be treated as an emergency quit.

## After the Session

1. Check that a new CSV appears in `data/experiment_results`.
2. Confirm that the filename begins with the participant ID.
3. Do not manually edit the raw CSV.
4. Record any unusual events in a separate research log.

## If a Participant Quits Early

1. Keep the partial CSV if one is saved.
2. Do not fill in missing trials manually.
3. Mark the participant for QC review.
4. Decide exclusion only after applying the documented QC rules.

