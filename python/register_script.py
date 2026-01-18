#!/usr/bin/env python3
"""
HACKATON - Script Registration Tool
Enregistre automatiquement les scripts dans la base SQLite
Usage: python register_script.py <filepath> [--category CAT] [--description DESC]
"""

import sqlite3
import os
import sys
import hashlib
import argparse
from datetime import datetime
from pathlib import Path

# Configuration
HACKATON_PATH = Path(r"C:\Users\franc\OneDrive\Documents\hackaton")
DB_PATH = HACKATON_PATH / "hackaton.db"

def get_file_info(filepath: Path) -> dict:
    """Récupère les infos d'un fichier"""
    content = filepath.read_text(encoding='utf-8', errors='ignore')
    lines = len(content.splitlines())
    size = filepath.stat().st_size
    checksum = hashlib.sha256(content.encode()).hexdigest()[:16]

    # Détecter le langage
    ext_lang = {
        '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
        '.ps1': 'powershell', '.sh': 'bash', '.sql': 'sql',
        '.json': 'json', '.yaml': 'yaml', '.yml': 'yaml',
        '.md': 'markdown', '.html': 'html', '.css': 'css'
    }
    lang = ext_lang.get(filepath.suffix.lower(), 'text')

    return {
        'name': filepath.stem,
        'filename': filepath.name,
        'filepath': str(filepath.absolute()),
        'language': lang,
        'lines_of_code': lines,
        'file_size': size,
        'checksum': checksum,
        'content': content
    }

def register_script(filepath: str, category: str = None, description: str = None, tags: list = None):
    """Enregistre un script dans la base"""
    path = Path(filepath)
    if not path.exists():
        print(f"Erreur: Fichier non trouvé: {filepath}")
        return False

    info = get_file_info(path)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Vérifier si existe déjà
        cursor.execute("SELECT id, version FROM scripts WHERE filename = ?", (info['filename'],))
        existing = cursor.fetchone()

        if existing:
            script_id, old_version = existing
            # Incrémenter version
            parts = old_version.split('.')
            parts[-1] = str(int(parts[-1]) + 1)
            new_version = '.'.join(parts)

            # Sauvegarder ancienne version
            cursor.execute("""
                INSERT INTO script_versions (script_id, version, changes, content_backup)
                SELECT id, version, 'Auto-backup before update',
                    (SELECT content_backup FROM script_versions WHERE script_id = ? ORDER BY created_at DESC LIMIT 1)
                FROM scripts WHERE id = ?
            """, (script_id, script_id))

            # Mettre à jour
            cursor.execute("""
                UPDATE scripts SET
                    filepath = ?, language = ?, category = COALESCE(?, category),
                    description = COALESCE(?, description), version = ?,
                    lines_of_code = ?, file_size = ?, checksum = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (info['filepath'], info['language'], category, description,
                  new_version, info['lines_of_code'], info['file_size'],
                  info['checksum'], script_id))

            print(f"[OK] Script mis a jour: {info['filename']} (v{new_version})")
        else:
            # Nouveau script
            cursor.execute("""
                INSERT INTO scripts (name, filename, filepath, language, category,
                                    description, lines_of_code, file_size, checksum)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (info['name'], info['filename'], info['filepath'], info['language'],
                  category or 'general', description or f"Script {info['name']}",
                  info['lines_of_code'], info['file_size'], info['checksum']))

            script_id = cursor.lastrowid
            print(f"[OK] Nouveau script enregistre: {info['filename']} (ID: {script_id})")

        # Ajouter tags
        if tags:
            for tag in tags:
                cursor.execute("SELECT id FROM tags WHERE name = ?", (tag,))
                tag_row = cursor.fetchone()
                if tag_row:
                    cursor.execute("""
                        INSERT OR IGNORE INTO script_tags (script_id, tag_id)
                        VALUES (?, ?)
                    """, (script_id, tag_row[0]))

        conn.commit()
        return True

    except Exception as e:
        print(f"Erreur: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def list_scripts(limit: int = 20):
    """Liste les scripts récents"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, filename, language, category, version,
               lines_of_code, run_count, updated_at
        FROM scripts
        ORDER BY updated_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    print(f"\n{'ID':<4} {'Nom':<25} {'Lang':<10} {'Cat':<12} {'Ver':<8} {'Lines':<6} {'Runs':<5}")
    print("-" * 80)
    for row in rows:
        print(f"{row[0]:<4} {row[1][:24]:<25} {row[3]:<10} {row[4] or '-':<12} {row[5]:<8} {row[6]:<6} {row[7]:<5}")

    return rows

def scan_and_register_all():
    """Scanne et enregistre tous les scripts du dossier hackaton"""
    extensions = {'.py', '.js', '.ts', '.ps1', '.sh', '.sql'}
    count = 0

    for folder in ['scripts', 'python', 'sql']:
        folder_path = HACKATON_PATH / folder
        if folder_path.exists():
            for file in folder_path.rglob('*'):
                if file.suffix.lower() in extensions and file.is_file():
                    register_script(str(file), category=folder)
                    count += 1

    print(f"\nTotal: {count} scripts enregistres/mis a jour")
    return count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enregistrer scripts dans hackaton.db")
    parser.add_argument('filepath', nargs='?', help="Chemin du script à enregistrer")
    parser.add_argument('--category', '-c', help="Catégorie du script")
    parser.add_argument('--description', '-d', help="Description du script")
    parser.add_argument('--tags', '-t', nargs='+', help="Tags (trading, ai, etc.)")
    parser.add_argument('--list', '-l', action='store_true', help="Lister les scripts")
    parser.add_argument('--scan', '-s', action='store_true', help="Scanner tous les scripts")

    args = parser.parse_args()

    if args.list:
        list_scripts()
    elif args.scan:
        scan_and_register_all()
    elif args.filepath:
        register_script(args.filepath, args.category, args.description, args.tags)
    else:
        print("Usage: python register_script.py <filepath> [options]")
        print("       python register_script.py --list")
        print("       python register_script.py --scan")
