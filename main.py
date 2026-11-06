import os
import re
import sqlite3
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

app = FastAPI()

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "flame.db")

class HealthResponse(BaseModel):
    status: str

class FileItem(BaseModel):
    file_id: int
    path: str
    type: str
    source_folder: str
    investigation: str

class ExperimentItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    oxygen_levels: list[float] = []

class DocumentItem(BaseModel):
    doc_id: int
    file_id: int
    title: str
    source_folder: str
    page_count: int
    text: str

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def parse_oxygen_levels(val):
    if val is None:
        return []
    if isinstance(val, float) and (val != val):
        return []
    s = str(val).strip()
    if s == "" or s.lower() in ("nan", "none", "null"):
        return []
    try:
        return [float(x) for x in re.findall(r"\d+(?:\.\d+)?", s)]
    except Exception:
        return []

def is_empty_value(val):
    if val is None:
        return True
    if isinstance(val, (list, tuple)):
        return len(val) == 0
    if isinstance(val, float) and (val != val):
        return True
    s = str(val).strip()
    return s == "" or s.lower() in ("nan", "none", "null")

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok")

@app.get("/api/files", response_model=List[FileItem])
def get_files():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_id, path, type, source_folder, investigation FROM files")
    rows = cursor.fetchall()
    conn.close()
    return [FileItem(**dict(row)) for row in rows]

@app.get("/api/experiments", response_model=List[ExperimentItem])
def get_experiments(
    oxygen_min: Optional[float] = None,
    oxygen_max: Optional[float] = None,
    limit: int = 50
):
    conn = get_db_connection()
    cursor = conn.cursor()
    if oxygen_min is None and oxygen_max is None:
        cursor.execute("SELECT * FROM experiments LIMIT ?", (limit,))
        raw_rows = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM experiments WHERE [oxygen_conc_(percent)] IS NOT NULL")
        raw_rows = cursor.fetchall()
    conn.close()

    matched_rows = []
    for row in raw_rows:
        row_dict = dict(row)
        levels = parse_oxygen_levels(row_dict.get("oxygen_conc_(percent)"))
        row_dict["oxygen_levels"] = levels

        if oxygen_min is not None and oxygen_max is not None:
            if not any(oxygen_min <= val <= oxygen_max for val in levels):
                continue
        elif oxygen_min is not None:
            if not any(val >= oxygen_min for val in levels):
                continue
        elif oxygen_max is not None:
            if not any(val <= oxygen_max for val in levels):
                continue

        if "notes" in row_dict and row_dict["notes"] is not None:
            notes_str = str(row_dict["notes"])
            if notes_str.strip().lower() in ("nan", "none", "null"):
                row_dict["notes"] = None
            elif len(notes_str) > 200:
                row_dict["notes"] = notes_str[:200]

        matched_rows.append(row_dict)
        if len(matched_rows) >= limit:
            break

    if not matched_rows:
        return []

    all_keys = list(matched_rows[0].keys())
    active_keys = [
        k for k in all_keys
        if k in ("oxygen_levels", "notes") or any(not is_empty_value(r.get(k)) for r in matched_rows)
    ]

    cleaned_rows = []
    for r in matched_rows:
        cleaned = {k: r.get(k) for k in active_keys if k in r}
        cleaned_rows.append(ExperimentItem(**cleaned))

    return cleaned_rows

@app.get("/api/documents", response_model=List[DocumentItem])
def get_documents():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT doc_id, file_id, title, source_folder, page_count, substr(text, 1, 300) AS text
        FROM documents
    """)
    rows = cursor.fetchall()
    conn.close()
    return [DocumentItem(**dict(row)) for row in rows]
