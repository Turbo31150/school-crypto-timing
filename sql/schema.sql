-- ============================================
-- HACKATON DATABASE SCHEMA v1.0
-- Tracking des scripts et travaux
-- Created: 2026-01-18
-- ============================================

-- Table principale des scripts
CREATE TABLE IF NOT EXISTS scripts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL UNIQUE,
    filepath VARCHAR(500) NOT NULL,
    language VARCHAR(50) DEFAULT 'python',
    category VARCHAR(100),
    description TEXT,
    version VARCHAR(20) DEFAULT '1.0.0',
    author VARCHAR(100) DEFAULT 'Claude + User',
    status VARCHAR(50) DEFAULT 'active',
    lines_of_code INTEGER DEFAULT 0,
    file_size INTEGER DEFAULT 0,
    checksum VARCHAR(64),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_run DATETIME,
    run_count INTEGER DEFAULT 0
);

-- Versions des scripts (historique)
CREATE TABLE IF NOT EXISTS script_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    script_id INTEGER NOT NULL,
    version VARCHAR(20) NOT NULL,
    changes TEXT,
    content_backup TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (script_id) REFERENCES scripts(id)
);

-- Logs d'exécution
CREATE TABLE IF NOT EXISTS execution_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    script_id INTEGER NOT NULL,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ended_at DATETIME,
    duration_seconds REAL,
    status VARCHAR(50),
    exit_code INTEGER,
    stdout TEXT,
    stderr TEXT,
    parameters TEXT,
    FOREIGN KEY (script_id) REFERENCES scripts(id)
);

-- Dépendances entre scripts
CREATE TABLE IF NOT EXISTS dependencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    script_id INTEGER NOT NULL,
    depends_on_script_id INTEGER,
    dependency_type VARCHAR(50),
    package_name VARCHAR(255),
    package_version VARCHAR(50),
    FOREIGN KEY (script_id) REFERENCES scripts(id),
    FOREIGN KEY (depends_on_script_id) REFERENCES scripts(id)
);

-- Tags pour catégorisation
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    color VARCHAR(20) DEFAULT '#3498db'
);

CREATE TABLE IF NOT EXISTS script_tags (
    script_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (script_id, tag_id),
    FOREIGN KEY (script_id) REFERENCES scripts(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

-- Notes et documentation
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    script_id INTEGER,
    title VARCHAR(255),
    content TEXT,
    note_type VARCHAR(50) DEFAULT 'general',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (script_id) REFERENCES scripts(id)
);

-- Sessions de travail hackaton
CREATE TABLE IF NOT EXISTS work_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_name VARCHAR(255),
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ended_at DATETIME,
    summary TEXT,
    scripts_created INTEGER DEFAULT 0,
    scripts_modified INTEGER DEFAULT 0
);

-- Tâches et TODOs
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(50) DEFAULT 'pending',
    script_id INTEGER,
    due_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (script_id) REFERENCES scripts(id)
);

-- Configuration
CREATE TABLE IF NOT EXISTS config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT,
    description TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- VUES UTILES
-- ============================================

-- Vue: Scripts récents
CREATE VIEW IF NOT EXISTS v_recent_scripts AS
SELECT
    id, name, filename, language, category,
    version, status, lines_of_code,
    created_at, updated_at, run_count
FROM scripts
ORDER BY updated_at DESC
LIMIT 20;

-- Vue: Stats par catégorie
CREATE VIEW IF NOT EXISTS v_stats_by_category AS
SELECT
    category,
    COUNT(*) as script_count,
    SUM(lines_of_code) as total_lines,
    SUM(run_count) as total_runs
FROM scripts
GROUP BY category;

-- Vue: Scripts avec dernière exécution
CREATE VIEW IF NOT EXISTS v_scripts_with_runs AS
SELECT
    s.id, s.name, s.filename, s.status,
    s.run_count, s.last_run,
    e.status as last_run_status,
    e.duration_seconds as last_duration
FROM scripts s
LEFT JOIN execution_logs e ON s.id = e.script_id
    AND e.started_at = (SELECT MAX(started_at) FROM execution_logs WHERE script_id = s.id);

-- ============================================
-- TRIGGERS
-- ============================================

-- Mise à jour automatique de updated_at
CREATE TRIGGER IF NOT EXISTS update_script_timestamp
AFTER UPDATE ON scripts
BEGIN
    UPDATE scripts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Incrémenter run_count après chaque exécution
CREATE TRIGGER IF NOT EXISTS increment_run_count
AFTER INSERT ON execution_logs
BEGIN
    UPDATE scripts
    SET run_count = run_count + 1, last_run = NEW.started_at
    WHERE id = NEW.script_id;
END;

-- ============================================
-- DONNÉES INITIALES
-- ============================================

-- Tags par défaut
INSERT OR IGNORE INTO tags (name, color) VALUES
    ('trading', '#e74c3c'),
    ('ai', '#9b59b6'),
    ('automation', '#3498db'),
    ('analysis', '#2ecc71'),
    ('utility', '#f39c12'),
    ('hackaton', '#1abc9c'),
    ('mcp', '#e91e63'),
    ('telegram', '#0088cc');

-- Config initiale
INSERT OR IGNORE INTO config (key, value, description) VALUES
    ('hackaton_path', 'C:\Users\franc\OneDrive\Documents\hackaton', 'Chemin racine hackaton'),
    ('db_version', '1.0.0', 'Version du schéma'),
    ('auto_backup', 'true', 'Backup automatique activé'),
    ('created_date', '2026-01-18', 'Date création');

-- Session initiale
INSERT INTO work_sessions (session_name, summary) VALUES
    ('Initialisation Hackaton', 'Création structure + base SQL');
