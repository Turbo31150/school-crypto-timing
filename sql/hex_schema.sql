-- =============================================================================
-- HACKATHON HEX - PROJET "SCHOOL & CRYPTO TIMING"
-- SCHEMA SQL PRODUCTION-READY v1.0
-- =============================================================================

-- TABLE: professeurs
-- Profil des professeurs avec timezone et disponibilites
CREATE TABLE IF NOT EXISTS professeurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    timezone VARCHAR(50) NOT NULL DEFAULT 'Europe/Paris',
    disponibilites_json TEXT DEFAULT '{}',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- TABLE: crypto_actifs
-- Liste des actifs crypto suivis
CREATE TABLE IF NOT EXISTS crypto_actifs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(20) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    exchange VARCHAR(50) DEFAULT 'MEXC',
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- TABLE: emploi_du_temps
-- Planning hebdomadaire des professeurs
CREATE TABLE IF NOT EXISTS emploi_du_temps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prof_id INTEGER NOT NULL,
    jour VARCHAR(10) NOT NULL CHECK (jour IN ('Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche')),
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    type_activite VARCHAR(50) NOT NULL,
    priorite_trading INTEGER DEFAULT 3 CHECK (priorite_trading BETWEEN 0 AND 5),
    notes TEXT,
    FOREIGN KEY (prof_id) REFERENCES professeurs(id) ON DELETE CASCADE
);

-- TABLE: crypto_data_hourly
-- Donnees crypto agregees par heure (via MEXC/CCXT)
CREATE TABLE IF NOT EXISTS crypto_data_hourly (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actif_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    price_open REAL,
    price_high REAL,
    price_low REAL,
    price_close REAL,
    volume REAL,
    volatility_1h REAL,
    liquidations_long REAL DEFAULT 0,
    liquidations_short REAL DEFAULT 0,
    funding_rate REAL,
    open_interest REAL,
    fear_greed_index INTEGER,
    FOREIGN KEY (actif_id) REFERENCES crypto_actifs(id),
    UNIQUE(actif_id, timestamp)
);

-- TABLE: trading_window_scores
-- Scores calcules par creneau/prof/actif
CREATE TABLE IF NOT EXISTS trading_window_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prof_id INTEGER NOT NULL,
    actif_id INTEGER NOT NULL,
    date DATE NOT NULL,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    score INTEGER CHECK (score BETWEEN 0 AND 100),
    raison TEXT,
    volatility_component REAL,
    availability_component REAL,
    market_component REAL,
    recommendation VARCHAR(20) CHECK (recommendation IN ('TRADE','HOLD','AVOID','WATCH')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prof_id) REFERENCES professeurs(id),
    FOREIGN KEY (actif_id) REFERENCES crypto_actifs(id)
);

-- TABLE: preferences
-- Preferences de trading par professeur
CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prof_id INTEGER NOT NULL UNIQUE,
    max_minutes_par_jour INTEGER DEFAULT 60,
    pref_volatilite VARCHAR(20) DEFAULT 'medium' CHECK (pref_volatilite IN ('low','medium','high')),
    aversion_risque INTEGER DEFAULT 5 CHECK (aversion_risque BETWEEN 1 AND 10),
    actifs_preferes TEXT DEFAULT '["BTC","ETH"]',
    notifications_enabled INTEGER DEFAULT 1,
    FOREIGN KEY (prof_id) REFERENCES professeurs(id) ON DELETE CASCADE
);

-- TABLE: sessions_trading
-- Historique des sessions de trading reelles
CREATE TABLE IF NOT EXISTS sessions_trading (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prof_id INTEGER NOT NULL,
    actif_id INTEGER NOT NULL,
    date_debut DATETIME NOT NULL,
    date_fin DATETIME,
    duree_minutes INTEGER,
    pnl_usdt REAL,
    score_predit INTEGER,
    score_reel INTEGER,
    notes TEXT,
    FOREIGN KEY (prof_id) REFERENCES professeurs(id),
    FOREIGN KEY (actif_id) REFERENCES crypto_actifs(id)
);

-- =============================================================================
-- INDEX POUR PERFORMANCE
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_emploi_prof_jour ON emploi_du_temps(prof_id, jour);
CREATE INDEX IF NOT EXISTS idx_crypto_data_actif_ts ON crypto_data_hourly(actif_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_scores_prof_date ON trading_window_scores(prof_id, date);
CREATE INDEX IF NOT EXISTS idx_scores_actif_date ON trading_window_scores(actif_id, date);
CREATE INDEX IF NOT EXISTS idx_scores_recommendation ON trading_window_scores(recommendation, score);

-- =============================================================================
-- VUES UTILES
-- =============================================================================

-- Vue: Meilleurs creneaux de la semaine
CREATE VIEW IF NOT EXISTS v_best_windows AS
SELECT
    p.name as professeur,
    c.symbol as crypto,
    s.date,
    s.heure_debut,
    s.heure_fin,
    s.score,
    s.recommendation,
    s.raison
FROM trading_window_scores s
JOIN professeurs p ON s.prof_id = p.id
JOIN crypto_actifs c ON s.actif_id = c.id
WHERE s.score >= 70
ORDER BY s.score DESC;

-- Vue: Stats par professeur
CREATE VIEW IF NOT EXISTS v_prof_stats AS
SELECT
    p.id,
    p.name,
    COUNT(DISTINCT e.id) as nb_creneaux,
    AVG(s.score) as score_moyen,
    MAX(s.score) as meilleur_score,
    SUM(CASE WHEN s.recommendation = 'TRADE' THEN 1 ELSE 0 END) as creneaux_trade
FROM professeurs p
LEFT JOIN emploi_du_temps e ON p.id = e.prof_id
LEFT JOIN trading_window_scores s ON p.id = s.prof_id
GROUP BY p.id, p.name;

-- Vue: Volatilite moyenne par heure
CREATE VIEW IF NOT EXISTS v_volatility_by_hour AS
SELECT
    c.symbol,
    strftime('%H', timestamp) as heure,
    AVG(volatility_1h) as volatility_moyenne,
    AVG(volume) as volume_moyen,
    COUNT(*) as nb_samples
FROM crypto_data_hourly d
JOIN crypto_actifs c ON d.actif_id = c.id
GROUP BY c.symbol, strftime('%H', timestamp)
ORDER BY c.symbol, heure;

-- =============================================================================
-- TRIGGERS
-- =============================================================================

CREATE TRIGGER IF NOT EXISTS update_prof_timestamp
AFTER UPDATE ON professeurs
BEGIN
    UPDATE professeurs SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- =============================================================================
-- DONNEES INITIALES
-- =============================================================================

-- Actifs crypto principaux
INSERT OR IGNORE INTO crypto_actifs (symbol, nom, exchange) VALUES
    ('BTC', 'Bitcoin', 'MEXC'),
    ('ETH', 'Ethereum', 'MEXC'),
    ('SOL', 'Solana', 'MEXC'),
    ('XRP', 'Ripple', 'MEXC'),
    ('DOGE', 'Dogecoin', 'MEXC'),
    ('ADA', 'Cardano', 'MEXC'),
    ('AVAX', 'Avalanche', 'MEXC'),
    ('MATIC', 'Polygon', 'MEXC'),
    ('DOT', 'Polkadot', 'MEXC'),
    ('LINK', 'Chainlink', 'MEXC');

-- Professeur exemple
INSERT OR IGNORE INTO professeurs (id, name, email, timezone) VALUES
    (1, 'Francois', 'francois@education.fr', 'Europe/Paris');

-- Preferences exemple
INSERT OR IGNORE INTO preferences (prof_id, max_minutes_par_jour, pref_volatilite, aversion_risque) VALUES
    (1, 45, 'medium', 4);

-- Emploi du temps exemple (semaine type)
INSERT OR IGNORE INTO emploi_du_temps (prof_id, jour, heure_debut, heure_fin, type_activite, priorite_trading) VALUES
    (1, 'Lundi', '08:00', '10:00', 'Cours Math', 0),
    (1, 'Lundi', '10:15', '12:15', 'Cours Physique', 0),
    (1, 'Lundi', '14:00', '16:00', 'Preparation', 3),
    (1, 'Lundi', '16:00', '18:00', 'Libre', 5),
    (1, 'Mardi', '08:00', '12:00', 'Cours', 0),
    (1, 'Mardi', '14:00', '15:00', 'Reunion', 1),
    (1, 'Mardi', '15:00', '18:00', 'Libre', 5),
    (1, 'Mercredi', '08:00', '12:00', 'Libre', 5),
    (1, 'Mercredi', '14:00', '16:00', 'Cours', 0),
    (1, 'Jeudi', '08:00', '10:00', 'Cours', 0),
    (1, 'Jeudi', '10:00', '12:00', 'Libre', 5),
    (1, 'Jeudi', '14:00', '18:00', 'Libre', 5),
    (1, 'Vendredi', '08:00', '12:00', 'Cours', 0),
    (1, 'Vendredi', '14:00', '16:00', 'Correction', 2),
    (1, 'Vendredi', '16:00', '18:00', 'Libre', 5);
