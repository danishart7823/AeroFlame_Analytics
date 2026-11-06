# AeroFlame_Analytics: Project Analysis

## 1. Project Overview

This project addresses NASA Space Apps 2026 Challenge 7, "Flame in Freefall", under the team name **AeroFlame_Analytics**. The goal of the project is to build an interactive aerospace fire safety analysis platform that unifies microgravity combustion data from NASA repositories into structured databases, clean backend APIs, and visual dashboards for assessing spacecraft and habitat fire risks.

---

## 2. Data Collected

The data is collected from two primary NASA resources stored in local folders:
- **NTRS Folder**: NASA Technical Reports Server documents stored as PDF files.
- **PSI Folder**: NASA Physical Sciences Informatics datasets stored as CSV, XLSX, TXT, and PDF files.

### Database Record Counts

| Category | Source Repositories | Record Count |
| :--- | :--- | :--- |
| Indexed Files | NTRS & PSI | 22 files |
| Experiments | PSI Data Sheets | 166 rows |
| Documents | NTRS Technical Papers | 12 documents |

### Investigations Cataloged

The files table indexes records across the following NASA ground and spaceflight investigations:
- Spacecraft Fire Safety Experiment-I (SAFFIRE-I)
- Spacecraft Fire Safety Experiment-II (SAFFIRE-II)
- SAFFIRE III & Saffire flammability research
- Advanced Combustion via Microgravity Experiments - Burning Rate Emulator (ACME BRE)
- Burning and Suppression of Solids - II (BASS-II)
- Solid Fuel Ignition and Extinction (SOFIE)
- FM2 flammability in lunar gravity
- Lunar gravity flame spread investigations
- Fire suppression in microgravity
- Spacecraft fire safety operational studies
- NASA Materials Flammability Updates & NASA-STD-6001 test standards

---

## 3. Data Pipeline

The pipeline is implemented in `build_db.py`. It ingests raw files from the data directory, sanitizes headers into standardized SQL column names, and populates a relational SQLite database at `data/flame.db`.

```
Raw Files (NTRS & PSI) ──> build_db.py ──> SQLite Database (data/flame.db)
```

### Database Table Schemas

#### Table: `files`
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `file_id` | INTEGER | Primary key |
| `path` | TEXT | Local file path |
| `type` | TEXT | File extension (csv, xlsx, txt, pdf) |
| `source_folder` | TEXT | Folder source (NTRS or PSI) |
| `investigation` | TEXT | Associated NASA mission or study |

#### Table: `experiments`
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `file_id` | INTEGER | Foreign key referencing `files.file_id` |
| `year`, `month`, `date` | REAL / TEXT | Experiment date information |
| `burner_size_(mm)` | REAL | Diameter of experimental burner nozzle |
| `fuel_bottle` | TEXT | Fuel gas mixture designation |
| `oxygen_conc_(percent)` | TEXT | Recorded oxygen concentration string |
| `flames_ignited` | REAL | Total flame events ignited during test |
| `notes` | TEXT | Operator and engineering log entries |
| Additional columns | Various | Burner flow rates, radiometer, and sample fields |

#### Table: `documents`
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `doc_id` | INTEGER | Primary key |
| `file_id` | INTEGER | Foreign key referencing `files.file_id` |
| `title` | TEXT | Extracted document title |
| `source_folder` | TEXT | Folder origin (`NTRS`) |
| `page_count` | INTEGER | Total pages processed |
| `text` | TEXT | Full extracted document text |

---

## 4. Data Cleaning Done

The pipeline and backend apply specific transformations to handle inconsistencies across raw experimental logs:

- **Oxygen String Parsing**: Raw oxygen values recorded as text or ranges are converted into lists of floating-point numbers (`oxygen_levels`) for filtering and math calculations.
- **Empty Column Removal**: Columns where every entry is null or empty are excluded from the `/api/experiments` API response.
- **Notes Field Truncation**: Free-form engineering notes are truncated to 200 characters in API responses to maintain fast load times and clean table views.
- **Fuel Name Normalization**: Fuel designations with varying whitespace or notation (such as `100%C2H4` and `100% C2H4`, or `100%CH4` and `100% CH4`) are normalized into single unified names.
- **Missing Fuel Replacement**: Experiments without a listed fuel name are mapped to `"Not Specified"` in dashboard displays.

---

## 5. Exploratory Analysis Done in the Dashboard

The dashboard provides visual and analytical tools to explore the combustion dataset:

### Summary Cards
- **Total Experiments**: Displays total count of experiment rows (166 tests).
- **Flames Caught Fire**: Displays total flame ignition occurrences across all tests (194 ignitions).
- **Average Oxygen Level**: Computes mean oxygen percentage across all recorded oxygen data points (31.1%).
- **Fuel Types Tested**: Displays the count of distinct normalized fuel mixtures (3 types).

### Visualizations
- **Oxygen vs. Flames Scatter Plot**: Plots oxygen concentration against total flames ignited. An interactive fuel selector allows isolating individual fuels or displaying all fuels together.
- **Fuel Distribution Bar Chart**: Displays fuel mixture distribution with an interactive toggle to switch between total experiment count and total flames ignited.

### Risk Rules Engine (What-If)
- **Atmospheric Evaluation**: An interactive slider-based risk calculator that evaluates fire safety using predefined oxygen safety rules:
  - **Normal / Low Risk**: Oxygen below 21.0%
  - **Elevated Risk**: Oxygen between 21.0% and 30.0%
  - **Critical Risk**: Oxygen exceeding 30.0%
- **Ventilation Factor**: Adjusts risk ratings based on cabin forced ventilation airflow.

---

## 6. Backend

The backend is built with FastAPI in `main.py` and runs on port 8000. It serves structured data directly from `data/flame.db`.

| Endpoint | Method | Response Description |
| :--- | :--- | :--- |
| `/health` | GET | Returns service status `{"status": "ok", "database": "connected"}` |
| `/api/files` | GET | Returns array of all 22 indexed files with path, type, source folder, and investigation |
| `/api/experiments` | GET | Returns array of experiment rows with parsed `oxygen_levels`, truncated notes, and non-empty columns |
| `/api/documents` | GET | Returns array of 12 research documents with titles, page counts, and text snippets |

---

## 7. Frontend

The frontend provides an interactive user interface built with Streamlit across seven main pages:

| Page | Contents & Features |
| :--- | :--- |
| **Home** | Hero header, four metric summary cards, and mission insight cards linking to deeper analyses |
| **Explorer** | Searchable data table with range slider for oxygen, fuel dropdown, text search, and CSV export |
| **Charts** | Interactive Plotly scatter plot (Oxygen vs. Flames) and toggleable fuel distribution bar chart |
| **What-If** | Risk rule simulation tool calculating fire safety risk tiers from oxygen and airflow inputs |
| **Documents** | Research paper browser featuring text search, document viewer, and keyword filtering |
| **Basics** | Visual guide to microgravity combustion physics, diffusion flames, and NASA safety standards |
| **About** | Project overview, NASA challenge references, system architecture summary, and data sources |

### Dashboard Layout Versions
- **`app.py`**: Top navigation layout running on port 8501.
- **`app_v2_sidebar.py`**: Left sidebar navigation layout with Space Grotesk / DM Sans typography and a full-width footer strip running on port 8502.

---

## 8. Key Results

The data across the processed microgravity experiments yields the following summary values:

| Metric | Value |
| :--- | :--- |
| Total Experiments | 166 |
| Total Flames Ignited | 194 |
| Average Oxygen Concentration | 31.1% |
| Distinct Fuel Types | 3 (`100% C2H4`, `100% CH4`, `50% C2H4`) |

*Note: The scatter plot analysis uses only the 43 data points that contain recorded oxygen concentration values.*

---

## 9. How to Run

### Backend Server
```powershell
uvicorn main:app --reload --port 8000
```
Runs at: `http://127.0.0.1:8000`

### Frontend Dashboards
- **Version 1 (Top Navigation)**:
  ```powershell
  streamlit run app.py --server.port 8501
  ```
  Runs at: `http://localhost:8501`

- **Version 2 (Sidebar Layout)**:
  ```powershell
  streamlit run app_v2_sidebar.py --server.port 8502
  ```
  Runs at: `http://localhost:8502`

---

## 10. Next Steps

- **Solid Material Data Merge**: Integrate solid fuel burn samples from BASS-II and SAFFIRE data sheets into the primary experiments table.
- **Full PDF Table Extraction**: Extract tabular experiment logs embedded in NTRS PDF technical reports into structured database records.
- **Richer Risk Model**: Expand the What-If rule to include chamber total pressure, flow velocity, and gaseous fire suppressants like CO2 and nitrogen.
- **Machine Learning Classification**: Train predictive models to classify ignition probability based on fuel composition and oxygen concentration.
