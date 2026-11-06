import sqlite3
import pandas as pd

conn = sqlite3.connect("data/flame.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM experiments")
print(f"Query Result -> SELECT COUNT(*) FROM experiments: {cursor.fetchone()[0]}\n")

tables = ["files", "experiments", "documents"]
for table in tables:
    print("=" * 70)
    print(f"Table: {table} (First 3 rows)")
    print("=" * 70)
    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 3", conn)
    if table == "documents" and "text" in df.columns:
        df["text"] = df["text"].apply(lambda t: (t[:60] + "...") if isinstance(t, str) and len(t) > 60 else t)
    print(df.to_string(index=False))
    print("\n")

conn.close()
