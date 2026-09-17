# Asynchronous Activity 1: Student Early Warning Tool Using KNIME

**Author:** NADINE LOVE D. RAMOS

**Course & Section:** CS0065 - AN43

---

## Project Overview

This repository contains the required output for Asynchronous Activity 1. The project utilizes the KNIME Analytics Platform to predict student risk status based on academic performance data.

## Repository Contents

- **`DemoEarlyWarningTool.knwf`** — The exported KNIME workflow file. _(Note: saved/referenced as CS0065_StudentPrediction.knwf)_
- **`student_performance_knime.csv`** — The dataset used by the workflow for model training and evaluation.

## Algorithms Used

The workflow implements and compares the following machine learning algorithms:

- Decision Tree
- Logistic Regression
- Random Forest

## How to Run

1. **Import** the `.knwf` file into your KNIME Analytics Platform workspace.
2. **Configure** the _CSV Reader_ node to point to the included `student_performance_knime.csv` dataset.
3. **Execute** all nodes in the workflow.
4. **Evaluate** the models by opening the views on the _Scorer_ nodes to review the performance results.
