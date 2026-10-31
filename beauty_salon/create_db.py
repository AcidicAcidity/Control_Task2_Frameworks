"""Создаёт data/beauty.db из sql/init.sql:  python create_db.py"""
import sqlite3
from pathlib import Path

base = Path(__file__).resolve().parent
db = base / "data" / "beauty.db"
db.parent.mkdir(exist_ok=True)
conn = sqlite3.connect(db)
conn.executescript((base / "sql" / "init.sql").read_text(encoding="utf-8"))
conn.commit()
conn.close()
print("База создана:", db)
