"""
Finance-Claude Dashboard Server
Run: uvicorn dashboard.server:app --host 0.0.0.0 --port 8080 --reload
"""

import sqlite3
import json
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

DB_PATH = Path(os.environ.get("DB_PATH", "./data/finance.db"))
HTML_PATH = Path(__file__).parent / "index.html"

app = FastAPI(title="Finance-Claude Dashboard")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id       TEXT UNIQUE NOT NULL,
            command      TEXT NOT NULL,
            ticker       TEXT,
            direction    TEXT,
            status       TEXT DEFAULT 'ACTIVE',
            grade        TEXT,
            entry_price  REAL,
            sl_price     REAL,
            tp1_price    REAL,
            rr_ratio     REAL,
            summary_md   TEXT NOT NULL,
            raw_json     TEXT,
            notes        TEXT,
            created_at   TEXT DEFAULT (datetime('now')),
            updated_at   TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


ensure_table()


class StatusUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    return HTML_PATH.read_text(encoding="utf-8")


@app.get("/api/analyses")
def list_analyses(command: Optional[str] = None, ticker: Optional[str] = None, status: Optional[str] = None):
    conn = get_db()
    query = "SELECT * FROM analysis_history WHERE 1=1"
    params = []
    if command:
        query += " AND command = ?"
        params.append(command)
    if ticker:
        query += " AND (ticker = ? OR ticker LIKE ?)"
        params.extend([ticker.upper(), f"%{ticker.upper()}%"])
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY created_at DESC LIMIT 200"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/analyses/{run_id}")
def get_analysis(run_id: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM analysis_history WHERE run_id = ?", [run_id]).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return dict(row)


@app.patch("/api/analyses/{run_id}")
def update_analysis(run_id: str, update: StatusUpdate):
    conn = get_db()
    row = conn.execute("SELECT id FROM analysis_history WHERE run_id = ?", [run_id]).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Not found")
    fields, params = [], []
    if update.status is not None:
        fields.append("status = ?")
        params.append(update.status)
    if update.notes is not None:
        fields.append("notes = ?")
        params.append(update.notes)
    if fields:
        fields.append("updated_at = datetime('now')")
        params.append(run_id)
        conn.execute(f"UPDATE analysis_history SET {', '.join(fields)} WHERE run_id = ?", params)
        conn.commit()
    row = conn.execute("SELECT * FROM analysis_history WHERE run_id = ?", [run_id]).fetchone()
    conn.close()
    return dict(row)


@app.get("/api/stats")
def get_stats():
    conn = get_db()
    stats = {}
    for cmd in ["scan", "swing", "screen", "dca", "watch"]:
        row = conn.execute("SELECT COUNT(*) as n FROM analysis_history WHERE command = ?", [cmd]).fetchone()
        stats[cmd] = row["n"]
    stats["total"] = sum(stats.values())
    taken = conn.execute("SELECT COUNT(*) as n FROM analysis_history WHERE status = 'TAKEN'").fetchone()
    stats["taken"] = taken["n"]
    conn.close()
    return stats
