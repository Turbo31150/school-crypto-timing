-- ============================================================
-- HACKATHON HEX 2026 - REQUÊTES SQL PRÊTES POUR HEX
-- ============================================================
-- Copiez chaque requête dans une cellule SQL de Hex.tech
-- ============================================================

-- ============================================================
-- REQUÊTE 1: TOP 10 MEILLEURES FENÊTRES DE TRADING
-- Nom suggéré: best_windows (produira dataframe_1)
-- ============================================================
SELECT
    jour AS day_name,
    heure_debut AS time_slot_start,
    heure_fin AS time_slot_end,
    type_activite AS activity,
    symbol AS asset_symbol,
    score,
    recommendation,
    raison AS reason,
    ROUND(volatility, 2) AS volatility_pct,
    ROUND(volume, 2) AS volume_24h,
    ROUND(volatility_component, 2) AS vol_comp,
    ROUND(availability_component, 0) AS avail_comp,
    ROUND(market_component, 2) AS market_comp
FROM calculated_scores
WHERE score >= 75
ORDER BY score DESC, volatility DESC
LIMIT 10;

-- ============================================================
-- REQUÊTE 2: STATISTIQUES PAR ACTIF CRYPTO
-- Nom suggéré: asset_stats (produira dataframe_2)
-- ============================================================
SELECT
    symbol AS asset_symbol,
    COUNT(*) AS total_windows,
    ROUND(AVG(score), 1) AS avg_score,
    MAX(score) AS best_score,
    MIN(score) AS worst_score,
    SUM(CASE WHEN recommendation = 'TRADE' THEN 1 ELSE 0 END) AS trade_signals,
    SUM(CASE WHEN recommendation = 'HOLD' THEN 1 ELSE 0 END) AS hold_signals,
    SUM(CASE WHEN recommendation = 'AVOID' THEN 1 ELSE 0 END) AS avoid_signals,
    ROUND(AVG(volatility), 2) AS avg_volatility,
    ROUND(AVG(volume), 2) AS avg_volume
FROM calculated_scores
GROUP BY symbol
ORDER BY avg_score DESC;

-- ============================================================
-- REQUÊTE 3: DONNÉES POUR HEATMAP
-- Nom suggéré: heatmap_data (produira dataframe_3)
-- ============================================================
SELECT
    jour AS day_name,
    heure_debut AS time_slot,
    symbol AS asset_symbol,
    score,
    recommendation,
    type_activite AS activity,
    ROUND(volatility_component, 2) AS vol_comp,
    ROUND(availability_component, 0) AS avail_comp,
    ROUND(market_component, 2) AS market_comp
FROM calculated_scores
ORDER BY
    CASE jour
        WHEN 'Lundi' THEN 1
        WHEN 'Mardi' THEN 2
        WHEN 'Mercredi' THEN 3
        WHEN 'Jeudi' THEN 4
        WHEN 'Vendredi' THEN 5
        WHEN 'Samedi' THEN 6
        WHEN 'Dimanche' THEN 7
    END,
    heure_debut,
    symbol;

-- ============================================================
-- REQUÊTE 4: RÉSUMÉ GLOBAL (optionnel)
-- ============================================================
SELECT
    COUNT(*) AS total_fenetres,
    SUM(CASE WHEN score >= 75 THEN 1 ELSE 0 END) AS fenetres_trade,
    SUM(CASE WHEN score >= 50 AND score < 75 THEN 1 ELSE 0 END) AS fenetres_hold,
    SUM(CASE WHEN score < 50 THEN 1 ELSE 0 END) AS fenetres_avoid,
    ROUND(AVG(score), 1) AS score_moyen,
    MAX(score) AS meilleur_score,
    MIN(score) AS pire_score
FROM calculated_scores;

-- ============================================================
-- REQUÊTE 5: MEILLEUR CRÉNEAU PAR JOUR (optionnel)
-- ============================================================
SELECT
    jour,
    heure_debut,
    symbol,
    score,
    recommendation
FROM calculated_scores c1
WHERE score = (
    SELECT MAX(score)
    FROM calculated_scores c2
    WHERE c2.jour = c1.jour
)
ORDER BY
    CASE jour
        WHEN 'Lundi' THEN 1
        WHEN 'Mardi' THEN 2
        WHEN 'Mercredi' THEN 3
        WHEN 'Jeudi' THEN 4
        WHEN 'Vendredi' THEN 5
        WHEN 'Samedi' THEN 6
        WHEN 'Dimanche' THEN 7
    END;

-- ============================================================
-- FIN DES REQUÊTES SQL
-- ============================================================
