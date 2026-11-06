# AeroFlame_Analytics

Interactive dashboard for analyzing NASA microgravity combustion experiments. Built for the NASA Space Apps Challenge 2026, Challenge 7: "Flame in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data."

## What it does

- Shows flame experiment data from NASA Physical Sciences Informatics (PSI).
- Filters tests by oxygen level, fuel type, and flames ignited.
- Plots oxygen vs flames caught fire, and fuel distribution.
- Includes a What-If simulator for oxygen-based fire risk levels.
- Lists NASA research papers (NTRS) and source files.

## Project structure

```
flame_project/
├── app.py              # Streamlit dashboard (frontend)
├── main.py             # FastAPI backend
├── build_db.py         # Builds the SQLite database from raw data
├── inspect_db.py       # Checks database tables
├── requirements.txt    # Python packages
├── data/
│   └── flame.db        # SQLite database
├── PSI/                # NASA PSI experiment files
└── NTRS/               # NASA technical reports
```

## Setup

```bash
pip install -r requirements.txt
```

## Run locally

Open two terminals in the project folder.

Terminal 1 (backend):
```bash
python -m uvicorn main:app --reload
```

Terminal 2 (dashboard):
```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

Check the backend at `http://127.0.0.1:8000/health`. It should return `{"status":"ok"}`.

## Rebuild the database (only if raw data changes)

```bash
python build_db.py
```

## Data sources

- NASA Technical Reports Server (NTRS)
- NASA Physical Sciences Informatics (PSI)

## Notes

- Risk levels (below 23% O2 low, 23 to 30% medium, above 30% high) are a simple educational rule, not a scientific model.
- The dataset is small, so charts show trends, not final results.

## Team

AeroFlame_Analytics 
