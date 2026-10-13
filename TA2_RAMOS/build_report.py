"""Run the examples and build TA2_RAMOS.pdf (requires reportlab)."""

import contextlib
import io
import random
import runpy
from pathlib import Path
from unittest.mock import patch
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak,
)

ROOT = Path(__file__).resolve().parent


def capture(filename, answers, seed=None):
    values = iter(answers)
    output = io.StringIO()

    def reply(prompt):
        value = next(values)
        print(prompt + value)
        return value

    old_state = random.getstate()
    if seed is not None:
        random.seed(seed)
    try:
        with contextlib.redirect_stdout(output), patch("builtins.input", reply):
            runpy.run_path(str(ROOT / filename), run_name="__main__")
    finally:
        random.setstate(old_state)
    return output.getvalue()


def check_programs():
    from TA2_RAMOS import VacuumAgent, read_state, read_steps
    from TA2_RAMOS_BONUS import BonusAgent

    # Every initial two-room state must follow the two stated rules.
    for a in ("Clean", "Dirty"):
        for b in ("Clean", "Dirty"):
            rooms = {"A": a, "B": b}
            agent = VacuumAgent(rooms)
            for _ in range(6):
                previous = agent.location
                dirty = rooms[previous] == "Dirty"
                action = agent.perceive_and_act()
                if dirty:
                    assert agent.location == previous
                    assert rooms[previous] == "Clean"
                    assert action.startswith("Cleaned")
                else:
                    assert agent.location != previous
                    assert action.startswith("Moved")
            assert all(state == "Clean" for state in rooms.values())

    # Check every three-room state across several random choices.
    original_random_state = random.getstate()
    for mask in range(8):
        for seed in range(10):
            random.seed(seed)
            rooms = {room: "Dirty" if mask & (1 << i) else "Clean"
                     for i, room in enumerate("ABC")}
            agent = BonusAgent(rooms)
            for _ in range(6):
                agent.perceive_and_act()
            assert all(state == "Clean" for state in rooms.values())
            assert "idle" in agent.perceive_and_act()
    random.setstate(original_random_state)

    with contextlib.redirect_stdout(io.StringIO()):
        with patch("builtins.input", side_effect=["wet", " DIRTY "]):
            assert read_state("A") == "Dirty"
        with patch("builtins.input", side_effect=["x", "1.5", "-1", "0"]):
            assert read_steps() == 0
    zero = capture("TA2_RAMOS.py", ["dirty", "clean", "0"])
    assert "Step 1" not in zero
    assert "Final state: {'A': 'Dirty', 'B': 'Clean'}" in zero


ANSWERS = [
    ("1. What rules does the agent follow?",
     "If the current room is dirty, the agent cleans it. If the current "
     "room is clean, the agent moves to the other room."),
    ("2. How does the agent decide when to clean and when to move?",
     "It checks the current room in the dictionary. A Dirty value means "
     "it should clean. A Clean value means it should move. It takes one "
     "action per step."),
    ("3. What happens if both rooms are already clean at the start?",
     "The two-room agent keeps moving between A and B until the chosen "
     "number of steps is finished. It does not clean anything because "
     "both rooms are clean. The bonus agent stays idle when all rooms "
     "are clean."),
    ("4. How would you modify the agent to handle more than two rooms?",
     "I would add more rooms to the dictionary and change the move "
     "method so it can choose from those rooms. In the bonus program, "
     "the agent picks a dirty room at random when its current room is "
     "clean. It moves there, then cleans it on the next step. The grid "
     "shows each room's state and the agent's location."),
]


def main():
    check_programs()
    examples = [
        ("Required simulation", "TA2_RAMOS.py",
         ["dirty", "clean", "5"], None, "output_required.txt"),
        ("Both rooms start clean", "TA2_RAMOS.py",
         ["clean", "clean", "3"], None, "output_both_clean.txt"),
        ("Bonus simulation", "TA2_RAMOS_BONUS.py",
         ["clean", "dirty", "dirty", "5"], 7, "output_bonus.txt"),
    ]
    transcripts = []
    for title, script, inputs, seed, output_name in examples:
        output = capture(script, inputs, seed)
        (ROOT / output_name).write_text(output, encoding="utf-8")
        transcripts.append((title, output, seed))

    answers_md = "# Task 4: Analysis Questions\n\n" + "\n\n".join(
        f"## {question}\n\n{answer}" for question, answer in ANSWERS)
    (ROOT / "TA2_RAMOS_Analysis.md").write_text(answers_md + "\n",
                                              encoding="utf-8")
    styles = getSampleStyleSheet()
    styles["Title"].alignment = TA_LEFT
    styles["Title"].textColor = colors.HexColor("#14503a")
    styles["BodyText"].fontSize = 11
    styles["BodyText"].leading = 16
    code_style = ParagraphStyle("CodeBlock", fontName="Courier",
                                fontSize=9, leading=11.5)
    output_style = ParagraphStyle("OutputBlock", fontName="Courier",
                                  fontSize=9, leading=12)
    story = []

    def para(text, style="BodyText"):
        story.append(Paragraph(escape(text), styles[style]))
        story.append(Spacer(1, 8))

    para("CS0065 | Intelligent Systems", "Heading2")
    para("Technical Assessment 2", "Title")
    para("Rule-Based Agent", "Heading1")
    para("Student: Ramos")
    para("Date: October 13, 2026")
    para("Activity Summary", "Heading2")
    para("This activity uses a vacuum cleaner agent. Rooms are stored in "
         "a Python dictionary. The user enters each room's state and the "
         "number of steps. The agent starts in room A.")
    para("Tasks 1-3: Two rooms", "Heading2")
    para("TA2_RAMOS.py sets up rooms A and B, checks and cleans rooms, "
         "and runs the agent. Each step shows its action, its location "
         "after the action, and the room states.")
    para("Optional bonus: Three rooms", "Heading2")
    para("TA2_RAMOS_BONUS.py adds room C. When its current room is clean, "
         "the agent randomly chooses a dirty room to visit. It becomes "
         "idle when all rooms are clean. A text grid shows the room states "
         "and the agent.")
    para("How to Run", "Heading2")
    para("Keep both Python files in the same folder. Open a terminal in "
         "that folder and run either command. The activity programs use "
         "only Python's standard library.")
    story.append(Preformatted("python TA2_RAMOS.py\n"
                              "python TA2_RAMOS_BONUS.py", output_style))
    para("The following pages contain the complete activity code, actual "
         "program runs, and answers to the analysis questions.")

    # Use explicit code-page boundaries to keep every line readable.
    for filename, label in [("TA2_RAMOS.py", "Tasks 1-3: Python Code"),
                            ("TA2_RAMOS_BONUS.py", "Bonus: Python Code")]:
        lines = (ROOT / filename).read_text(encoding="utf-8").splitlines()
        split = lines.index("def main():")
        for start, end in [(0, split), (split, len(lines))]:
            story.append(PageBreak())
            para(label + (" (continued)" if start else ""), "Heading1")
            para(f"{filename} | Lines {start + 1}-{end}")
            story.append(Preformatted("\n".join(lines[start:end]),
                                      code_style))

    for title, output, seed in transcripts:
        story.append(PageBreak())
        para(title, "Heading1")
        if seed is not None:
            para("This captured run uses random seed 7 so it can be "
                 "repeated. Normal runs may choose a different room first.")
        else:
            para("Actual program output; typed inputs appear after each prompt.")
        story.append(Preformatted(output.rstrip(), output_style))

    story.append(PageBreak())
    para("Task 4: Analysis Questions", "Heading1")
    for question, answer in ANSWERS:
        para(question, "Heading3")
        para(answer)
    para("Program Checks", "Heading2")
    para("Checks passed for all four starting states of the two-room "
         "program and all eight starting states of the bonus program "
         "using ten random seeds each. Invalid inputs are rejected. "
         "Zero steps leaves the room states unchanged.")

    def footer(canvas, doc):
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(48, 27, "CS0065 | TA2 | Ramos")
        canvas.drawRightString(564, 27, str(doc.page))

    doc = SimpleDocTemplate(str(ROOT / "TA2_RAMOS.pdf"),
                            pagesize=(612, 792), rightMargin=48,
                            leftMargin=48, topMargin=42, bottomMargin=44,
                            title="TA2 Ramos - Rule-Based Agent", author="Ramos")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("All program checks passed. Created TA2_RAMOS.pdf and outputs.")


if __name__ == "__main__":
    main()
