# Participant QC Rules

Participant exclusion should be based on task quality, not on whether results match the expected hypotheses.

## Structural Exclusion Rules

Flag a participant if:

- The file does not contain 124 total rows.
- The file does not contain 4 practice trials.
- The file does not contain 120 main trials.
- Required columns are missing.
- The `participant_id` does not match the filename.
- There are duplicate main trial IDs within the participant file.

## Accuracy and Completion Rules

Flag a participant if:

- Overall main-trial accuracy is below 70%.
- Pseudoword accuracy is below 50%.
- More than 10% of main trials have missing RTs or no response.
- Accuracy values do not match `response_label` and `correct_response`.

## RT Warning Rules

Flag a participant if:

- More than 10% of valid RTs are below 250 ms.
- Median RT is below 300 ms.
- Median RT is above 2000 ms.

## Response Bias Rules

Flag a participant if:

- One response key is used for more than 90% of main trials.
- The response pattern suggests one-key pressing.

## Duplicate or Suspicious Participant Rules

Flag for review if:

- Participant IDs are duplicated.
- Response sequences are identical or nearly identical across participants.
- RT patterns are identical or nearly identical across participants.
- Filename timestamps or filesystem metadata suggest batch creation and cannot be explained by the collection log.

