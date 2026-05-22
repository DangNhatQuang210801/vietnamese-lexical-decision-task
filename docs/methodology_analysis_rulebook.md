# RP2 Methodology and Analysis Rulebook

Project: Vietnamese lexical decision task  
Research question: Do log frequency and syllable length affect Vietnamese lexical decision reaction time?  
Task: PsychoPy lexical decision task  
Main dependent variable: reaction time (RT)  
Secondary dependent variable: accuracy  
Main predictors: `log_frequency`, `syllable_length`, and their interaction

This rulebook is for analysis decisions only. Raw data, stimulus CSV files, and existing experiment files must remain unchanged.

## 1. Participant Inclusion Rules

- Include participants who completed the main lexical decision block or have enough completed main-block trials to be informative for pilot checking.
- Exclude a participant from confirmatory RT analysis if they have no valid correct real-word trials after trial-level exclusions.
- Exclude a participant from accuracy analysis only if their file is unusable because key columns are missing, the file cannot be read, or participant identity cannot be determined.
- For the current project stage, treat all available data as preliminary/pilot data. Do not describe the sample as final.
- Report the number of participant files inspected, the number included in accuracy analysis, and the number included in RT analysis.

## 2. Trial Inclusion Rules

- Analyze only trials with interpretable values for `participant_id`, `block`, `stimulus`, `condition`, `is_word`, `syllable_length`, `correct_response`, `accuracy`, and `rt`.
- Main inferential RT models should use main-block trials only.
- Trials with missing or nonnumeric RT are excluded from RT analysis.
- Trials with missing accuracy are excluded from accuracy analysis.
- Do not edit trial rows in the raw CSV files. Any exclusions must be applied in the analysis script and reported.

## 3. Practice Trial Handling

- Practice trials are excluded from all final inferential analyses.
- Practice trials may be summarized separately for checking whether the task instructions and key mapping were understood.
- Practice-trial performance must not be combined with main-block performance when reporting RT, accuracy, or model results.

## 4. Incorrect Response Handling

- Incorrect trials are kept for accuracy analysis.
- Incorrect trials are excluded from RT analysis because the RT does not represent a correct lexical decision.
- The number and percentage of incorrect trials should be reported by condition where possible.
- If a participant has unusually low accuracy, inspect the file for possible key-mapping or task-comprehension problems before deciding whether to exclude the participant.

## 5. Timeout Handling

- Timeout trials are kept for accuracy analysis and coded as incorrect if no valid response was made.
- Timeout trials are excluded from RT analysis.
- Report the number and percentage of timeout trials separately from ordinary incorrect responses if the data contain a timeout marker.
- Do not replace timeout RTs with the timeout limit for RT analysis.

## 6. RT Cleaning Rules

RT cleaning must be explicit. Do not describe the procedure only as "standard RT cleaning."

- Use only main-block trials for RT analysis.
- Use only correct-response trials for RT analysis.
- Exclude timeout trials.
- Exclude trials with missing, zero, negative, or nonnumeric RT.
- Exclude RTs below 200 ms because they are likely anticipatory responses.
- Exclude RTs above 3000 ms because they are likely lapses, interruptions, or timeout-adjacent responses.
- After these fixed exclusions, inspect the RT distribution. If an additional outlier rule is needed, use a participant-wise rule such as excluding RTs more than 2.5 SD above or below that participant's mean after fixed trimming. Report this rule clearly if used.
- Do not apply extra trimming separately for real words and pseudowords unless this is justified and reported.

## 7. Accuracy Analysis Rules

- Accuracy analysis includes main-block real-word and pseudoword trials.
- Incorrect and timeout trials are retained for accuracy analysis.
- The main descriptive accuracy measures are overall accuracy, real-word accuracy, pseudoword accuracy, and accuracy by syllable length.
- Accuracy can be modeled with a mixed-effects logistic regression if the number of participants and error trials is sufficient.
- For pilot data, accuracy results should be treated as task-quality checks and preliminary evidence, not as final hypothesis tests.

## 8. Real-Word vs Pseudoword Analysis Rules

- The main RT frequency analysis should focus on correct real-word trials because `log_frequency` is meaningful for real lexical items.
- Pseudowords are included in the task to support the lexical decision procedure and to measure decision accuracy/error patterns.
- Pseudoword RTs may be summarized descriptively and compared with real-word RTs as a task-validity check.
- Do not interpret pseudoword "frequency effects" unless a clearly defined pseudoword-level predictor has been created and justified.
- For real-word trials, syllable length is measured by syllable count. This is appropriate because Vietnamese orthography separates syllables with spaces, so word length cannot be measured by simple whitespace-delimited tokens.

## 9. Mixed-Effects Model Plan

Primary RT model:

```text
RT ~ log_frequency * syllable_length + (1 | participant_id) + (1 | stimulus)
```

Preferred RT scale:

```text
log(RT) ~ log_frequency * syllable_length + (1 | participant_id) + (1 | stimulus)
```

Use the log-RT model if residual diagnostics show the raw RT model is strongly skewed. Report which RT scale was used.

Model rules:

- Fit the main RT model on correct main-block real-word trials only.
- Include `log_frequency`, `syllable_length`, and their interaction.
- Treat `participant_id` and `stimulus` as random intercepts where the dataset is large enough.
- If the model fails to converge, simplify the random-effects structure before removing fixed effects.
- If the interaction is not reliable, report the main effects model as a simpler descriptive model.
- For accuracy, use a logistic mixed-effects model if the data support it:

```text
accuracy ~ condition * syllable_length + (1 | participant_id) + (1 | stimulus)
```

Frequency-focused accuracy model for real words:

```text
accuracy ~ log_frequency * syllable_length + (1 | participant_id) + (1 | stimulus)
```

These models are appropriate for the final dataset. For the current pilot stage, they should be described as exploratory.

## 10. Reporting Language for Pilot/Preliminary Data

Use cautious wording:

- "The current data are preliminary and are used to check the task pipeline."
- "Patterns in the pilot data are descriptive and should not be treated as final evidence."
- "The analysis plan is intended for the full dataset after data collection."
- "Pilot results suggest whether the expected frequency and syllable-length effects are detectable, but they do not establish the final effect sizes."

Avoid overclaiming:

- Do not write that the study has proven an effect from the pilot data.
- Do not describe the pilot sample as representative.
- Do not claim that this is the first Vietnamese lexical decision study.
- Do not present simulated or pilot-generated files as real final participant data.

## 11. What Can Be Claimed From Pilot Data

- Pilot data can support task feasibility, including whether instructions, timing, key mapping, and output saving work as intended.
- Pilot data can show preliminary descriptive patterns in RT and accuracy.
- Pilot data cannot prove final frequency effects, syllable-length effects, or their interaction.
- Pilot results should be used to improve the task and analysis pipeline before the full study.

## 12. Required Output Tables Before Presentation

- Participant summary table: participant count, included/excluded files, trial counts, mean accuracy, and mean RT.
- Stimulus validation table: item type, syllable length, frequency availability, and validation status.
- RT exclusion table: number of trials removed at each cleaning step.
- Descriptive RT/accuracy summary table: RT and accuracy by condition, syllable length, and frequency group where relevant.

## 13. Methodology Weaknesses to Improve Before Presentation

- The current participant sample is still preliminary and too small for strong inference.
- Stimulus validation should continue, especially for multi-syllable Vietnamese words, because frequent n-syllable strings are not automatically valid lexical words.
- Frequency values should be checked for source consistency, corpus coverage, and extreme outliers.
- Syllable length should be checked manually for all real-word stimuli and pseudowords.
- Pseudoword construction should be documented clearly, including how pseudowords preserve Vietnamese orthographic plausibility.
- RT exclusion thresholds should be justified before final analysis and applied consistently.
- The final analysis script should produce a reproducible exclusion table showing how many trials are removed at each step.
- More participants are needed before interpreting mixed-effects model estimates as substantive findings.

## 14. Suggested References to Support the Methodology

- Brysbaert, M., & Stevens, M. (2018). Power analysis and effect size in mixed effects models: A tutorial. *Journal of Cognition, 1*(1), Article 9. https://doi.org/10.5334/joc.10
- Dinh, Q. T., Le, H. P., Nguyen, T. M. H., Nguyen, C. T., Rossignol, M., & Vu, X. L. (2008). Word segmentation of Vietnamese texts: A comparison of approaches. In *Proceedings of LREC 2008*. European Language Resources Association.
- Ha, L. A. (2003). A method for word segmentation in Vietnamese. In *Proceedings of Corpus Linguistics 2003* (pp. 282-287). UCREL.
- Hieu Nguyen, N., Nguyen, D. T., & Nguyen, N. L.-T. (2025). Vietnamese words are not constructed from syllables: Rethinking the role of word segmentation in natural language processing for Vietnamese texts. *Proceedings of the AAAI Conference on Artificial Intelligence, 39*(22), 24069-24077.
- Nguyen, D.-H. (1997). *Vietnamese*. John Benjamins.
- Pham, H., & Baayen, H. (2015). Vietnamese compounds show an anti-frequency effect in visual lexical decision. *Language, Cognition and Neuroscience, 30*(9), 1077-1095.
- Pham, H., Tucker, B. V., & Baayen, R. H. (2019). Constructing two Vietnamese corpora and building a lexical database. *Language Resources and Evaluation, 53*(3), 465-498.
- Verdonschot, R. G., Hoang, T. L. P., & Tamaoka, K. (2022). Phonological encoding in Vietnamese: An experimental investigation. *Quarterly Journal of Experimental Psychology, 75*(7), 1355-1366.
