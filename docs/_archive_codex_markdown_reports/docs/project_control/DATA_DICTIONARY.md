# Data Dictionary

## participant_id

Participant identifier entered at the start of the PsychoPy session. It should match the number at the beginning of the filename.

## block

Trial block. Expected values are `practice` and `main`.

## trial_id

Unique trial identifier. This should be used as the primary item key for analysis and QC.

## stimulus

The written Vietnamese stimulus shown to the participant.

## condition

Lexical condition of the stimulus. Expected values are `word` and `pseudoword`.

## is_word

Binary lexical status. `1` indicates a real word and `0` indicates a pseudoword.

## syllable_length

Number of written syllables in the stimulus. This is the project measure of word length.

## frequency_group

Frequency category. Real words use `low`, `mid`, or `high`. Pseudowords use `control`. Practice trials use `practice`.

## frequency

Raw corpus frequency count for real words. Pseudowords and practice items may have `NA`.

## log_frequency

Log-transformed corpus frequency for real words. Pseudowords and practice items may have `NA`.

## source_realword

The source word used for the item. For real words, this is usually the stimulus itself. For pseudowords, it may indicate the real-word template/source.

## correct_response

Correct lexical decision response. Expected values are `word` and `nonword`.

## key_pressed

Physical key pressed by the participant. Expected main response keys are `f` and `j`. Blank values indicate no response or timeout.

## response_label

Response label derived from the key press. `f` maps to `word`; `j` maps to `nonword`.

## accuracy

Trial accuracy. `1` means `response_label` matches `correct_response`. `0` means incorrect or missing response.

## rt

Reaction time in seconds, measured from stimulus onset to response. Missing values indicate timeout or no response.

