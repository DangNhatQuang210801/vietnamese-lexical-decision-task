# RP2 Pavlovia Builder Construction Spec

This document describes the PsychoPy Builder version of the RP2 Vietnamese lexical decision task. It is intentionally separate from the offline Python script.

## Experiment Info Dialog

Suggested Builder experiment settings:

- Experiment name: `rp2_vietnamese_ldt_online`
- Participant fields:
  - `participant`
  - `session`
- Save data: use PsychoPy/PsychoJS default experiment data saving.
- Online conditions folder: `conditions/`

Participant IDs can be entered in the Pavlovia dialog. If URL parameters are used, test this in Piloting before Running.

## Flow Overview

Use this Builder Flow:

1. `instructions`
2. `practice_trials` loop using `conditions/practice_trials.csv`
   - `practice_fixation`
   - `practice_stimulus`
   - `practice_feedback`
3. `main_instructions`
4. `main_trials` loop using `conditions/main_trials_3x4.csv`
   - `main_fixation`
   - `main_stimulus`
5. `end_screen`

Set both loops to random order.

## Routine: instructions

Components:

- Text component `instructions_text`
  - Text:
    ```text
    Nhiệm vụ lexical decision

    Bạn sẽ thấy một chuỗi chữ tiếng Việt trên màn hình.

    Nhấn F nếu đó là TỪ tiếng Việt thật.
    Nhấn J nếu đó KHÔNG phải là từ tiếng Việt.

    Hãy trả lời nhanh và chính xác.

    Nhấn phím CÁCH để bắt đầu phần luyện tập.
    ```
- Keyboard component `instructions_key`
  - Allowed keys: `space`
  - Force end routine: yes

## Routine: practice_fixation

Components:

- Text component `practice_fixation_cross`
  - Text: `+`
  - Duration: `0.5`

## Routine: practice_stimulus

Components:

- Text component `practice_stimulus_text`
  - Text: `$stimulus`
  - Set every repeat
- Keyboard component `practice_resp`
  - Allowed keys: `f,j`
  - Store: first key
  - Force end routine: yes
  - Duration/max wait: `3.0`

Code component `practice_scoring`, End Routine tab:

Python:

```python
key_pressed = practice_resp.keys if practice_resp.keys else ""
response_label = {"f": "word", "j": "nonword"}.get(key_pressed, "")
accuracy = int(response_label == correct_response) if response_label else 0

thisExp.addData("participant_id", expInfo.get("participant", ""))
thisExp.addData("block", "practice")
thisExp.addData("trial_id", trial_id)
thisExp.addData("stimulus", stimulus)
thisExp.addData("condition", condition)
thisExp.addData("is_word", is_word)
thisExp.addData("syllable_length", syllable_length)
thisExp.addData("frequency_group", frequency_group)
thisExp.addData("frequency", frequency)
thisExp.addData("log_frequency", log_frequency)
thisExp.addData("source_realword", source_realword)
thisExp.addData("correct_response", correct_response)
thisExp.addData("key_pressed", key_pressed)
thisExp.addData("response_label", response_label)
thisExp.addData("accuracy", accuracy)
thisExp.addData("rt", practice_resp.rt if practice_resp.rt else "")

if accuracy == 1:
    feedback_text = "Đúng"
elif not key_pressed:
    feedback_text = "Quá chậm"
else:
    feedback_text = "Sai"
```

JavaScript:

```javascript
key_pressed = practice_resp.keys || "";
response_label = {"f": "word", "j": "nonword"}[key_pressed] || "";
accuracy = response_label ? Number(response_label === correct_response) : 0;

psychoJS.experiment.addData("participant_id", expInfo["participant"] || "");
psychoJS.experiment.addData("block", "practice");
psychoJS.experiment.addData("trial_id", trial_id);
psychoJS.experiment.addData("stimulus", stimulus);
psychoJS.experiment.addData("condition", condition);
psychoJS.experiment.addData("is_word", is_word);
psychoJS.experiment.addData("syllable_length", syllable_length);
psychoJS.experiment.addData("frequency_group", frequency_group);
psychoJS.experiment.addData("frequency", frequency);
psychoJS.experiment.addData("log_frequency", log_frequency);
psychoJS.experiment.addData("source_realword", source_realword);
psychoJS.experiment.addData("correct_response", correct_response);
psychoJS.experiment.addData("key_pressed", key_pressed);
psychoJS.experiment.addData("response_label", response_label);
psychoJS.experiment.addData("accuracy", accuracy);
psychoJS.experiment.addData("rt", practice_resp.rt || "");

if (accuracy === 1) {
    feedback_text = "Đúng";
} else if (!key_pressed) {
    feedback_text = "Quá chậm";
} else {
    feedback_text = "Sai";
}
```

## Routine: practice_feedback

Components:

- Text component `practice_feedback_text`
  - Text: `$feedback_text`
  - Set every repeat
  - Duration: `0.7`

## Routine: main_instructions

Components:

- Text component `main_instructions_text`
  - Text:
    ```text
    Kết thúc phần luyện tập.

    Phần chính sẽ bắt đầu ngay sau đây.
    Trong phần chính sẽ không có phản hồi đúng/sai.

    Nhấn phím CÁCH để bắt đầu.
    ```
- Keyboard component `main_instructions_key`
  - Allowed keys: `space`
  - Force end routine: yes

## Routine: main_fixation

Components:

- Text component `main_fixation_cross`
  - Text: `+`
  - Duration: `0.5`

## Routine: main_stimulus

Components:

- Text component `main_stimulus_text`
  - Text: `$stimulus`
  - Set every repeat
- Keyboard component `main_resp`
  - Allowed keys: `f,j`
  - Store: first key
  - Force end routine: yes
  - Duration/max wait: `3.0`

Code component `main_scoring`, End Routine tab:

Python:

```python
key_pressed = main_resp.keys if main_resp.keys else ""
response_label = {"f": "word", "j": "nonword"}.get(key_pressed, "")
accuracy = int(response_label == correct_response) if response_label else 0

thisExp.addData("participant_id", expInfo.get("participant", ""))
thisExp.addData("block", "main")
thisExp.addData("trial_id", trial_id)
thisExp.addData("stimulus", stimulus)
thisExp.addData("condition", condition)
thisExp.addData("is_word", is_word)
thisExp.addData("syllable_length", syllable_length)
thisExp.addData("frequency_group", frequency_group)
thisExp.addData("frequency", frequency)
thisExp.addData("log_frequency", log_frequency)
thisExp.addData("source_realword", source_realword)
thisExp.addData("correct_response", correct_response)
thisExp.addData("key_pressed", key_pressed)
thisExp.addData("response_label", response_label)
thisExp.addData("accuracy", accuracy)
thisExp.addData("rt", main_resp.rt if main_resp.rt else "")
```

JavaScript:

```javascript
key_pressed = main_resp.keys || "";
response_label = {"f": "word", "j": "nonword"}[key_pressed] || "";
accuracy = response_label ? Number(response_label === correct_response) : 0;

psychoJS.experiment.addData("participant_id", expInfo["participant"] || "");
psychoJS.experiment.addData("block", "main");
psychoJS.experiment.addData("trial_id", trial_id);
psychoJS.experiment.addData("stimulus", stimulus);
psychoJS.experiment.addData("condition", condition);
psychoJS.experiment.addData("is_word", is_word);
psychoJS.experiment.addData("syllable_length", syllable_length);
psychoJS.experiment.addData("frequency_group", frequency_group);
psychoJS.experiment.addData("frequency", frequency);
psychoJS.experiment.addData("log_frequency", log_frequency);
psychoJS.experiment.addData("source_realword", source_realword);
psychoJS.experiment.addData("correct_response", correct_response);
psychoJS.experiment.addData("key_pressed", key_pressed);
psychoJS.experiment.addData("response_label", response_label);
psychoJS.experiment.addData("accuracy", accuracy);
psychoJS.experiment.addData("rt", main_resp.rt || "");
```

## Routine: end_screen

Components:

- Text component `end_text`
  - Text:
    ```text
    Cảm ơn bạn đã tham gia.

    Dữ liệu đã được lưu.
    ```
- Keyboard component `end_key`
  - Allowed keys: `space,return`
  - Force end routine: yes

## Save and Exit / Escape Notes

The offline Python script supports `S` save-and-exit and Escape emergency quit. Online Pavlovia data saving is controlled by PsychoJS and the browser session. For the first Pavlovia version, the safer approach is:

- Do not add `S` as a normal response key in lexical decision trials.
- Do not rely on local file writing.
- Use Pavlovia/PsychoJS default saving at normal experiment completion.

If an online early-exit feature is required, add a separate Builder Code Component and test it in Piloting. It should call PsychoJS quit functions only after confirming that partial data are saved correctly on Pavlovia.

