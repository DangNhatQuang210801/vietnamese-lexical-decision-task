# Item QC Rules

## Item Key

Use `trial_id` as the primary item key. Do not group items only by raw stimulus text, because Vietnamese encoding can vary across files and environments.

## Item-Level Checks

For each main-trial item, calculate:

- Number of presentations.
- Accuracy.
- Mean RT for correct responses.
- Median RT for correct responses.
- Missing RT count.
- Condition.
- Syllable length.
- Frequency group.

## Item Flags

Flag an item for monitoring if:

- Accuracy is below 60%.
- Median correct RT is unusually high, for example above 1500 ms.
- Many participants confuse the item.
- A pseudoword is often classified as a real word.

## Interpretation

An item flag does not automatically mean the item should be removed. It means the item should be reviewed before final analysis. Item removal should be documented and applied consistently.

