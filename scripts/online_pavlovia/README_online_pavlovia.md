# RP2 Pavlovia Online Version

This folder contains the online/Pavlovia preparation files for the RP2 Vietnamese lexical decision task. It is separate from the working offline Python script.

## Files

- `conditions/main_trials_3x4.csv`: 120 main trials copied from the final 3 x 4 stimulus file.
- `conditions/practice_trials.csv`: 4 practice trials from the offline script.
- `docs/builder_construction_spec.md`: PsychoPy Builder routine-by-routine construction instructions, including Python and JavaScript code snippets for Code Components.
- `docs/validation_report.md`: checks for trial counts, columns, response mapping, and frequency fields.

## How to Open in PsychoPy Builder

1. Open PsychoPy.
2. Create a new Builder experiment.
3. Save the experiment inside this `online_pavlovia` folder, for example as `rp2_vietnamese_ldt_online.psyexp`.
4. Build the routines and loops described in `docs/builder_construction_spec.md`.
5. Use condition files with relative paths:
   - `conditions/practice_trials.csv`
   - `conditions/main_trials_3x4.csv`

## How to Test Locally

1. In PsychoPy Builder, run the experiment locally first.
2. Enter a test participant ID such as `pilot_local_001`.
3. Confirm:
   - instructions display correctly with Vietnamese diacritics
   - practice has 4 trials
   - practice feedback shows `Đúng`, `Sai`, or `Quá chậm`
   - main block has 120 trials
   - F maps to `word`
   - J maps to `nonword`
   - output data include `frequency_group`

## How to Sync to Pavlovia

1. In PsychoPy Builder, log in to Pavlovia.
2. Use the Pavlovia sync button.
3. Create a new Pavlovia project/repository for the online version.
4. Confirm that the `conditions/` files are included in the synced project.
5. Let Builder compile the PsychoJS/JavaScript version.

## How to Set the Project to Piloting

1. Open the project on Pavlovia.
2. Set the project status to `Piloting`.
3. Use the pilot link for internal testing.
4. Run at least one complete pilot session.
5. Download the pilot data and confirm the output columns before recruiting real participants.

## How to Set the Project to Running

1. Only switch to `Running` after the pilot data have been checked.
2. Confirm the experiment starts from the Pavlovia participant link.
3. Confirm the final data file is saved on Pavlovia after completion.
4. Then change the Pavlovia project status from `Piloting` to `Running`.

## How to Copy the Participant Link

1. Open the Pavlovia project page.
2. Use the experiment link shown under the project status controls.
3. If participant IDs are assigned manually, include the ID in the Pavlovia dialog at the start of the experiment.
4. If URL query parameters are used, test the exact URL format during Piloting before using it for real data collection.

## How to Download Data from Pavlovia

1. Open the Pavlovia project page.
2. Go to the data/download section.
3. Download the `.csv` data files after pilot or running sessions.
4. Store downloaded data separately from local offline data.
5. Check that each row contains:
   - `participant_id`
   - `block`
   - `trial_id`
   - `stimulus`
   - `condition`
   - `is_word`
   - `syllable_length`
   - `frequency_group`
   - `frequency`
   - `log_frequency`
   - `source_realword`
   - `correct_response`
   - `key_pressed`
   - `response_label`
   - `accuracy`
   - `rt`

## Known Limitations Compared with the Offline Script

- The offline script writes a local CSV file directly. Pavlovia uses PsychoJS experiment data saving instead.
- The offline script has a tested `S` save-and-exit path. For online data collection, early exit must be tested carefully in Pavlovia before use.
- Escape/browser quit behavior online depends on PsychoJS and the participant's browser.
- A `.psyexp` file still needs to be built or checked manually in PsychoPy Builder using the provided construction spec.
- Browser timing can differ from local PsychoPy timing; complete online piloting is required before real data collection.

