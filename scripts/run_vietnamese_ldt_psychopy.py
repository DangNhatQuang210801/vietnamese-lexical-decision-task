"""
Run the RP2 Vietnamese lexical decision task in PsychoPy.

Run from the repository root:
    python scripts/run_vietnamese_ldt_psychopy.py

Input:
    data/stimuli/final/final_ldt_stimuli_v1.csv

Output:
    data/experiment_results/<participant_id>_ldt_<timestamp>.csv
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
import random
import re
import sys
from typing import Any, Dict, List, Optional

from psychopy import core, event, gui, visual


ROOT = Path(__file__).resolve().parents[1]
STIMULUS_FILE = ROOT / "data" / "stimuli" / "final" / "final_ldt_stimuli_v1.csv"
RESULTS_DIR = ROOT / "data" / "experiment_results"

FIXATION_SECONDS = 0.5
TIMEOUT_SECONDS = 3.0
RESPONSE_KEYS = {"f": "word", "j": "nonword"}
QUIT_KEYS = {"escape"}

OUTPUT_COLUMNS = [
    "participant_id",
    "block",
    "trial_id",
    "stimulus",
    "condition",
    "is_word",
    "syllable_length",
    "frequency",
    "log_frequency",
    "source_realword",
    "correct_response",
    "key_pressed",
    "response_label",
    "accuracy",
    "rt",
]

PRACTICE_TRIALS = [
    {
        "trial_id": "PRACTICE_001",
        "stimulus": "mèo",
        "condition": "word",
        "is_word": "1",
        "correct_response": "word",
        "source_realword": "mèo",
        "frequency": "NA",
        "log_frequency": "NA",
        "syllable_length": "1",
    },
    {
        "trial_id": "PRACTICE_002",
        "stimulus": "mẻo",
        "condition": "pseudoword",
        "is_word": "0",
        "correct_response": "nonword",
        "source_realword": "mèo",
        "frequency": "NA",
        "log_frequency": "NA",
        "syllable_length": "1",
    },
    {
        "trial_id": "PRACTICE_003",
        "stimulus": "ghế đá",
        "condition": "word",
        "is_word": "1",
        "correct_response": "word",
        "source_realword": "ghế đá",
        "frequency": "NA",
        "log_frequency": "NA",
        "syllable_length": "2",
    },
    {
        "trial_id": "PRACTICE_004",
        "stimulus": "tủ lảnh",
        "condition": "pseudoword",
        "is_word": "0",
        "correct_response": "nonword",
        "source_realword": "tủ lạnh",
        "frequency": "NA",
        "log_frequency": "NA",
        "syllable_length": "4",
    },
]


def read_stimuli(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing stimulus file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Stimulus file is empty: {path}")
    return rows


def participant_dialog() -> Optional[Dict[str, Any]]:
    info = {
        "participant_id": "",
        "session": "001",
        "full_screen": True,
    }
    dialog = gui.DlgFromDict(
        dictionary=info,
        title="RP2 Vietnamese Lexical Decision Task",
        order=["participant_id", "session", "full_screen"],
    )
    if not dialog.OK:
        return None
    info["participant_id"] = str(info["participant_id"]).strip()
    if not info["participant_id"]:
        info["participant_id"] = "anonymous"
    return info


def safe_filename_part(text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", text.strip())
    return cleaned.strip("._") or "anonymous"


def show_text(win: visual.Window, text: visual.TextStim, message: str, wait_keys: Optional[List[str]] = None) -> None:
    text.text = message
    text.draw()
    win.flip()
    event.waitKeys(keyList=wait_keys)


def response_to_accuracy(response_label: str, correct_response: str) -> int:
    return int(response_label == correct_response)


def run_trial(
    win: visual.Window,
    fixation: visual.TextStim,
    stimulus_text: visual.TextStim,
    trial: Dict[str, str],
    participant_id: str,
    block: str,
) -> Dict[str, Any]:
    # Hiện dấu cộng để ổn định chú ý trước khi trình bày stimulus.
    fixation.draw()
    win.flip()
    core.wait(FIXATION_SECONDS)

    # Hiện stimulus cho đến khi người tham gia trả lời hoặc hết thời gian.
    event.clearEvents(eventType="keyboard")
    clock = core.Clock()
    stimulus_text.text = trial["stimulus"]
    stimulus_text.draw()
    win.flip()

    key_pressed = ""
    response_label = ""
    rt = ""

    keys = event.waitKeys(
        maxWait=TIMEOUT_SECONDS,
        keyList=list(RESPONSE_KEYS.keys()) + list(QUIT_KEYS),
        timeStamped=clock,
    )
    if keys:
        key_pressed, rt_value = keys[0]
        if key_pressed in QUIT_KEYS:
            raise KeyboardInterrupt
        response_label = RESPONSE_KEYS.get(key_pressed, "")
        rt = round(float(rt_value), 6)

    correct_response = trial["correct_response"]
    accuracy = response_to_accuracy(response_label, correct_response) if response_label else 0

    return {
        "participant_id": participant_id,
        "block": block,
        "trial_id": trial["trial_id"],
        "stimulus": trial["stimulus"],
        "condition": trial["condition"],
        "is_word": trial["is_word"],
        "syllable_length": trial["syllable_length"],
        "frequency": trial.get("frequency", "NA") or "NA",
        "log_frequency": trial.get("log_frequency", "NA") or "NA",
        "source_realword": trial["source_realword"],
        "correct_response": correct_response,
        "key_pressed": key_pressed,
        "response_label": response_label,
        "accuracy": accuracy,
        "rt": rt,
    }


def show_practice_feedback(
    win: visual.Window,
    text: visual.TextStim,
    trial_result: Dict[str, Any],
) -> None:
    # Feedback chỉ dùng cho practice, không dùng trong main trials.
    if trial_result["accuracy"] == 1:
        message = "Đúng"
    elif not trial_result["key_pressed"]:
        message = "Quá chậm"
    else:
        message = "Sai"
    text.text = message
    text.draw()
    win.flip()
    core.wait(0.7)


def save_results(path: Path, rows: List[Dict[str, Any]]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    try:
        stimuli = read_stimuli(STIMULUS_FILE)
    except Exception as exc:
        print(exc, file=sys.stderr)
        return 1

    info = participant_dialog()
    if info is None:
        return 0

    participant_id = str(info["participant_id"])
    session = str(info["session"]).strip() or "001"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = RESULTS_DIR / (
        f"{safe_filename_part(participant_id)}_session-{safe_filename_part(session)}_ldt_{timestamp}.csv"
    )

    random.shuffle(stimuli)
    practice_trials = PRACTICE_TRIALS.copy()
    random.shuffle(practice_trials)

    win = visual.Window(
        fullscr=bool(info["full_screen"]),
        color="white",
        units="height",
    )
    instruction_text = visual.TextStim(
        win,
        color="black",
        height=0.04,
        wrapWidth=1.35,
        font="Arial",
    )
    fixation = visual.TextStim(win, text="+", color="black", height=0.08, font="Arial")
    stimulus_text = visual.TextStim(win, text="", color="black", height=0.07, font="Arial")

    results: List[Dict[str, Any]] = []
    try:
        show_text(
            win,
            instruction_text,
            (
                "Nhiệm vụ lexical decision\n\n"
                "Bạn sẽ thấy một chuỗi chữ tiếng Việt trên màn hình.\n\n"
                "Nhấn F nếu đó là TỪ tiếng Việt thật.\n"
                "Nhấn J nếu đó KHÔNG phải là từ tiếng Việt.\n\n"
                "Hãy trả lời nhanh và chính xác.\n\n"
                "Nhấn phím CÁCH để bắt đầu phần luyện tập."
            ),
            wait_keys=["space"],
        )

        for trial in practice_trials:
            result = run_trial(win, fixation, stimulus_text, trial, participant_id, "practice")
            results.append(result)
            show_practice_feedback(win, instruction_text, result)

        show_text(
            win,
            instruction_text,
            (
                "Kết thúc phần luyện tập.\n\n"
                "Phần chính sẽ bắt đầu ngay sau đây.\n"
                "Trong phần chính sẽ không có phản hồi đúng/sai.\n\n"
                "Nhấn phím CÁCH để bắt đầu."
            ),
            wait_keys=["space"],
        )

        for trial in stimuli:
            results.append(run_trial(win, fixation, stimulus_text, trial, participant_id, "main"))

        show_text(
            win,
            instruction_text,
            "Cảm ơn bạn đã tham gia.\n\nDữ liệu đã được lưu.",
            wait_keys=["space", "return"],
        )
    except KeyboardInterrupt:
        show_text(
            win,
            instruction_text,
            "Thí nghiệm đã dừng.\n\nDữ liệu hiện có sẽ được lưu.",
            wait_keys=["space", "return"],
        )
    finally:
        save_results(output_path, results)
        win.close()
        core.quit()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
