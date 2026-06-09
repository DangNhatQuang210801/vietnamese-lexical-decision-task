# Analysis Plan Draft

This is a draft plan for final analysis. It should be applied only after the dataset is frozen and QC decisions are documented.

## Dependent Variables

- Main dependent variable: reaction time (RT).
- Secondary measure: accuracy.

## RT Inclusion Rules

The main RT analysis should use correct real-word trials only. Exclude from RT analysis:

- Practice trials.
- Pseudoword trials for the main frequency analysis.
- Incorrect trials.
- Missing RTs.
- Timeouts/no-response trials.

Incorrect trials and timeouts should still be retained for accuracy summaries.

## RT Transformation

RT may be log-transformed if the distribution is skewed. The final report should state whether raw RT or log RT is used in the model.

## Main Mixed-Effects Model

The main model should test categorical frequency group and syllable length:

`log_rt ~ frequency_group * syllable_length + random effects for participant and trial_id/item`

Random intercepts for participants and items should be included, with `trial_id` used as the item identifier. More complex random-effects structures can be considered only if the data support them.

## Accuracy Analysis

Accuracy should be summarized by condition, syllable length, and frequency group for real words. If appropriate, a logistic mixed-effects model can be used for accuracy.

## Supplementary Analysis

Raw `log_frequency` can be retained for exploratory continuous analysis. This should be described as supplementary because the final design uses categorical frequency groups.

## Reporting Rule

Do not write final conclusions until the dataset is frozen, exclusion decisions are complete, and the planned models have been run.

