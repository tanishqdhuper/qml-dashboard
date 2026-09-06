# Quantum Machine Learning for Network Intrusion Detection — Streamlit Dashboard

A local research dashboard for the **reported** KDD Cup99 experiments supplied by the project author.

## Important scope

This is an **Offline Experimental Mode — KDD Cup 99** dashboard. It is not a live NIDS and does not collect network traffic, make live predictions, or fabricate missing evaluation artifacts.

The included CSVs reproduce the values visible in the supplied experiment-results screenshot:
- `classical_results.csv`
- `qml_results.csv`
- `pegasos_results.csv`
- `dataset_metadata.csv`

No confusion matrices, ROC/PR curves, training times, prediction times, loss curves, or other unprovided results are invented.

## Included views

1. Overview
2. Classical vs QML
3. Interactive Experiment Explorer
4. PegasosQSVC C-Value Analysis
5. Metric Comparison
6. Best-Model Summary

The UI includes experiment tables, filters, metric plots, and the reported PegasosQSVC C-value analysis.

## Local installation

Recommended: Python 3.10–3.12.

### Windows PowerShell

```powershell
cd qml_nids_dashboard
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

### Windows CMD

```bat
cd qml_nids_dashboard
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

### macOS / Linux

```bash
cd qml_nids_dashboard
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit will print a local address, normally:

`http://localhost:8501`

## Project structure

```text
qml_nids_dashboard/
├── app.py
├── requirements.txt
├── README.md
├── classical_results.csv
├── qml_results.csv
├── pegasos_results.csv
└── dataset_metadata.csv
```

## Data integrity note

The dashboard uses the exact values shown in the provided screenshot, including:
- KDD Cup99
- 41 original KDD features
- 311029 records
- 41 → 114 feature transition
- OHE encoding
- PCA experiments using 8 features
- Classical baseline metrics
- QSVC/VQC subset results for 200, 500 and 1000
- PegasosQSVC C values 0.1, 1, 10 and 100
- PegasosQSVC subset sizes 200, 500 and 1000
- PegasosQSVC num_steps values 200 and 500

The dashboard intentionally does not infer values for experiments that were not shown.

## Important: how to start it

Do **not** start the dashboard with `python app.py`. That runs the script as an ordinary Python program, so Streamlit reports `missing ScriptRunContext`. Start it with:

```bash
python -m streamlit run app.py
```

The current version of `app.py` also uses Streamlit's current `width="stretch"` API instead of the deprecated `use_container_width=True`.

## Visual upgrade

Version 2 adds a more presentation-ready research-console aesthetic:
- dark glassmorphism-style panels
- cyan/purple research accents
- stronger hero/header section
- improved metric cards
- research snapshot cards
- consistent dark Plotly charts
- cleaner sidebar navigation
- responsive layout and typography

The data and reported experiment values remain unchanged.


## Theme support

Dark / Light appearance switch is available in the sidebar. Light mode uses a soft blue-gray research palette with cyan/violet accents instead of plain white. Theme changes are visual-only; experiment data and analysis logic are unchanged.
