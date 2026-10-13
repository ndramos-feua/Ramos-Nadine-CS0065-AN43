# CS0065 - Technical Assessment 1

Run commands from this folder. The completed program is `TA1_RAMOS.py`.
The extensionless `TA1_RAMOS` file is the original starter code.

## Run using the prepared environment (Windows PowerShell)

Enter your own settings:

```powershell
.\.venv\Scripts\python.exe .\TA1_RAMOS.py --animate
```

Repeat the six scenarios used in the PDF:

```powershell
.\.venv\Scripts\python.exe .\TA1_RAMOS.py --demo --animate
```

Leave out `--animate` for a faster run that saves only plots and data.
The program prints the results in the terminal. Open an `animation.gif`
to watch the dots move and leave paths. Open `plot.png` to see all paths
and the final distribution. No plot window is required.

## Set up on another computer

Use Python 3.11, which was used for this submission:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\TA1_RAMOS.py --demo --animate
```

The NumPy and SALib versions keep this older AgentPy release compatible.

## Files and results

- `TA1_RAMOS.pdf`: completed report, answers, results, and full program code.
- `TA1_RAMOS.py`: commented AgentPy program.
- `requirements.txt`: packages needed to run the program.
- `outputs/comparison.json`: results from the six demo scenarios.
- Each scenario folder contains `paths.csv`, `final_positions.csv`,
  `summary.json`, `console.txt`, and `plot.png`.
- `animation.gif` is also saved when `--animate` is used.

Paths include the starting position at step 0 and one position after each
simulation step. Agents may share cells. The `right` rule gives right a
60% chance, left a 10% chance, and up and down a 15% chance each.
Coordinates stay between 0 and grid size minus 1.

All output paths are relative to the Python file, so results stay in this
folder even if the program is launched from another location. Repeating a
scenario replaces its saved outputs. The default seed is 65; use
`--seed 100` to try a different repeatable run.
