import os
import re
import sys
import traceback
import sqlite3
import pandas as pd
import pypdf

def sanitize_column_name(col):
    return re.sub(r'\s+', '_', str(col).strip().lower())

def scan_directories(base_dir):
    targets = [
        ("NTRS", os.path.join(base_dir, "NTRS")),
        ("PSI", os.path.join(base_dir, "PSI"))
    ]
    file_records = []
    for source_name, target_dir in targets:
        if not os.path.exists(target_dir):
            continue
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                ext = os.path.splitext(file)[1].lower()
                size = os.path.getsize(full_path)
                parts = rel_path.split(os.sep)
                investigation = parts[1] if len(parts) > 2 else "General"
                file_records.append({
                    "full_path": full_path,
                    "rel_path": rel_path,
                    "ext": ext,
                    "size": size,
                    "source_folder": source_name,
                    "investigation": investigation
                })
    return file_records

def log_failure(log_file_path, file_path, error_message):
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{file_path}\n{error_message}\n" + "-" * 40 + "\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    db_path = os.path.join(data_dir, "flame.db")
    log_path = os.path.join(base_dir, "build_db_errors.log")
    dry_run_only = "--dry-run" in sys.argv

    files = scan_directories(base_dir)

    print(f"Discovered {len(files)} files.")
    print(f"{'Type':<8} {'Size (KB)':<12} {'Source':<8} {'Path'}")
    print("-" * 80)
    for item in files:
        size_kb = f"{item['size'] / 1024:.1f}"
        status = "READ" if item['ext'] in [".csv", ".xlsx", ".txt", ".pdf"] else "SKIP"
        print(f"[{status}] {item['ext']:<6} {size_kb:<12} {item['source_folder']:<8} {item['rel_path']}")

    if dry_run_only:
        print("\nDry run complete. Exiting without database creation.")
        return

    os.makedirs(data_dir, exist_ok=True)
    if os.path.exists(log_path):
        os.remove(log_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS experiments")
    cursor.execute("DROP TABLE IF EXISTS documents")
    cursor.execute("DROP TABLE IF EXISTS files")

    cursor.execute("""
    CREATE TABLE files (
        file_id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT,
        type TEXT,
        source_folder TEXT,
        investigation TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE documents (
        doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER,
        title TEXT,
        source_folder TEXT,
        page_count INTEGER,
        text TEXT,
        FOREIGN KEY (file_id) REFERENCES files (file_id)
    )
    """)
    conn.commit()

    experiment_dfs = []

    for item in files:
        cursor.execute("""
        INSERT INTO files (path, type, source_folder, investigation)
        VALUES (?, ?, ?, ?)
        """, (item['rel_path'], item['ext'], item['source_folder'], item['investigation']))
        conn.commit()
        file_id = cursor.lastrowid
        ext = item['ext']
        full_path = item['full_path']

        if ext in [".csv", ".xlsx"]:
            try:
                if ext == ".csv":
                    df = pd.read_csv(full_path)
                    df.columns = [sanitize_column_name(c) for c in df.columns]
                    df["file_id"] = file_id
                    experiment_dfs.append(df)
                elif ext == ".xlsx":
                    excel_file = pd.ExcelFile(full_path)
                    for sheet_name in excel_file.sheet_names:
                        df = pd.read_excel(excel_file, sheet_name=sheet_name)
                        df.columns = [sanitize_column_name(c) for c in df.columns]
                        df["file_id"] = file_id
                        experiment_dfs.append(df)
            except Exception:
                log_failure(log_path, full_path, traceback.format_exc())

        elif ext == ".txt":
            try:
                try:
                    df = pd.read_csv(full_path, sep=None, engine='python')
                    if len(df.columns) > 1:
                        df.columns = [sanitize_column_name(c) for c in df.columns]
                        df["file_id"] = file_id
                        experiment_dfs.append(df)
                    else:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        cursor.execute("""
                            INSERT INTO documents (file_id, title, source_folder, page_count, text)
                            VALUES (?, ?, ?, ?, ?)
                            """, (file_id, os.path.basename(full_path), item['source_folder'], 1, content))
                        conn.commit()
                except Exception:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    cursor.execute("""
                        INSERT INTO documents (file_id, title, source_folder, page_count, text)
                        VALUES (?, ?, ?, ?, ?)
                        """, (file_id, os.path.basename(full_path), item['source_folder'], 1, content))
                    conn.commit()
            except Exception:
                log_failure(log_path, full_path, traceback.format_exc())

        elif ext == ".pdf":
            try:
                reader = pypdf.PdfReader(full_path)
                page_count = len(reader.pages)
                title = os.path.basename(full_path)
                text_parts = []
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text_parts.append(extracted)
                full_text = "\n".join(text_parts).encode("utf-8", "ignore").decode("utf-8")
                cursor.execute("""
                INSERT INTO documents (file_id, title, source_folder, page_count, text)
                VALUES (?, ?, ?, ?, ?)
                """, (file_id, title, item['source_folder'], page_count, full_text))
                conn.commit()
            except Exception:
                log_failure(log_path, full_path, traceback.format_exc())

    if experiment_dfs:
        try:
            combined_df = pd.concat(experiment_dfs, ignore_index=True)
            combined_df.to_sql("experiments", conn, if_exists="replace", index=False)
        except Exception:
            log_failure(log_path, "Combined Experiments Table", traceback.format_exc())

    tables = ["files", "experiments", "documents"]
    print("\nDATABASE SUMMARY:")
    for tbl in tables:
        cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{tbl}'")
        if cursor.fetchone()[0] == 0:
            continue
        cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
        count = cursor.fetchone()[0]
        cursor.execute(f"PRAGMA table_info({tbl})")
        columns = cursor.fetchall()
        print("=" * 70)
        print(f"Table: {tbl} | Total Rows: {count}")
        print("-" * 70)
        print(f"{'CID':<5} {'Column Name':<40} {'Data Type':<15}")
        print("-" * 70)
        for col in columns:
            print(f"{col[0]:<5} {col[1]:<40} {col[2]:<15}")
    print("=" * 70)

    conn.close()

if __name__ == "__main__":
    main()
