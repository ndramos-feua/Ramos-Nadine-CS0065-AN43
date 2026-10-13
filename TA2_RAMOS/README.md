# CS0065 Technical Assessment 2

- `TA2_RAMOS.pdf`: Complete activity code, actual sample outputs, and analysis answers.
- `TA2_RAMOS.py`: Required two-room program (Tasks 1-3).
- `TA2_RAMOS_BONUS.py`: Optional three-room program with random moves and a text grid.
- `TA2_RAMOS_Analysis.md`: Simple answers to Task 4.
- `output_required.txt`, `output_both_clean.txt`, `output_bonus.txt`: Captured runs.

## Run the activity

Open a terminal in this folder and run:

```console
python TA2_RAMOS.py
```

For the bonus activity:

```console
python TA2_RAMOS_BONUS.py
```

Keep both activity scripts together. They use only Python's standard library.
Enter `dirty` or `clean` for each room and a whole number of steps of 0 or more.
The agent starts in room A. Each step takes one action. The location printed
after the action is the agent's current location.

The bonus sample uses seed 7 for a repeatable report. Interactive runs use
random choices, so the room order can change.

## Rebuild the PDF

The report helper needs ReportLab. Install it and run:

```console
python -m pip install reportlab
python build_report.py
```

This reruns the program checks and recreates the PDF, transcripts, and answers.
Submit the PDF and both activity scripts if including the bonus task.
