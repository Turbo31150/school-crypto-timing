#!/usr/bin/env python3
"""
HACKATON - Database Query Tool
Requêtes rapides sur hackaton.db
Usage: python query_db.py [command]
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

DB_PATH = Path(r"C:\Users\franc\OneDrive\Documents\hackaton\hackaton.db")

def connect():
    return sqlite3.connect(DB_PATH)

def scripts():
    """Liste tous les scripts"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, language, category, version, lines_of_code, status, updated_at
        FROM scripts ORDER BY updated_at DESC
    """)
    rows = cur.fetchall()
    conn.close()

    print(f"\n{'ID':<4} {'Nom':<30} {'Lang':<10} {'Cat':<12} {'Ver':<8} {'Lines':<6} {'Status':<10}")
    print("=" * 90)
    for r in rows:
        print(f"{r[0]:<4} {r[1][:29]:<30} {r[2]:<10} {r[3] or '-':<12} {r[4]:<8} {r[5]:<6} {r[6]:<10}")
    print(f"\nTotal: {len(rows)} scripts")

def stats():
    """Statistiques globales"""
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*), SUM(lines_of_code), SUM(run_count) FROM scripts")
    total, lines, runs = cur.fetchone()

    cur.execute("SELECT category, COUNT(*) FROM scripts GROUP BY category")
    cats = cur.fetchall()

    cur.execute("SELECT language, COUNT(*) FROM scripts GROUP BY language")
    langs = cur.fetchall()

    conn.close()

    print("\n[STATS] HACKATON")
    print("=" * 40)
    print(f"Scripts totaux:     {total or 0}")
    print(f"Lignes de code:     {lines or 0}")
    print(f"Executions totales: {runs or 0}")

    print("\n[CATEGORIES]")
    for cat, count in cats:
        print(f"  {cat or 'non-classe':<20} {count}")

    print("\n[LANGAGES]")
    for lang, count in langs:
        print(f"  {lang:<20} {count}")

def recent():
    """5 derniers scripts modifiés"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM v_recent_scripts LIMIT 5")
    rows = cur.fetchall()
    conn.close()

    print("\n[RECENT]")
    for r in rows:
        print(f"  [{r[0]}] {r[1]} ({r[3]}) - v{r[4]} - {r[9]}")

def search(term: str):
    """Recherche dans les scripts"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, filename, category, description
        FROM scripts
        WHERE name LIKE ? OR filename LIKE ? OR description LIKE ?
    """, (f'%{term}%', f'%{term}%', f'%{term}%'))
    rows = cur.fetchall()
    conn.close()

    print(f"\n[SEARCH] Resultats pour '{term}':")
    for r in rows:
        print(f"  [{r[0]}] {r[1]} ({r[2]}) - {r[3]}")
        if r[4]:
            print(f"       {r[4][:60]}...")

def tasks():
    """Liste les tâches"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, priority, status, due_date
        FROM tasks ORDER BY
            CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
            created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()

    print("\n[TASKS]")
    for r in rows:
        prio = "[HIGH]" if r[2] == 'high' else "[MED]" if r[2] == 'medium' else "[LOW]"
        status = "[DONE]" if r[3] == 'completed' else "[WIP]" if r[3] == 'in_progress' else "[TODO]"
        print(f"  {prio} [{r[0]}] {status} {r[1]}")

def sql(query: str):
    """Exécute une requête SQL personnalisée"""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(query)
        if query.strip().upper().startswith('SELECT'):
            rows = cur.fetchall()
            cols = [desc[0] for desc in cur.description]
            print("\n" + " | ".join(cols))
            print("-" * 60)
            for row in rows:
                print(" | ".join(str(v) for v in row))
            print(f"\n({len(rows)} rows)")
        else:
            conn.commit()
            print(f"[OK] Query executed, {cur.rowcount} rows affected")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

def help():
    print("""
HACKATON Database Query Tool
=============================
Commands:
  python query_db.py scripts   - Liste tous les scripts
  python query_db.py stats     - Statistiques globales
  python query_db.py recent    - 5 derniers scripts
  python query_db.py search X  - Rechercher 'X'
  python query_db.py tasks     - Liste des tâches
  python query_db.py sql "..." - Requête SQL custom
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        help()
    else:
        cmd = sys.argv[1].lower()
        if cmd == 'scripts':
            scripts()
        elif cmd == 'stats':
            stats()
        elif cmd == 'recent':
            recent()
        elif cmd == 'search' and len(sys.argv) > 2:
            search(sys.argv[2])
        elif cmd == 'tasks':
            tasks()
        elif cmd == 'sql' and len(sys.argv) > 2:
            sql(sys.argv[2])
        else:
            help()
