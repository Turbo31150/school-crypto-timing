#!/usr/bin/env python3
"""
HACKATHON HEX - School & Crypto Timing
Point d'entree principal

Usage:
    python run.py              # Pipeline complet
    python run.py --init       # Initialise DB seulement
    python run.py --fetch      # Fetch crypto data seulement
    python run.py --score      # Calcule scores seulement
    python run.py --test       # Mode test (donnees simulees)
"""

import sys
import argparse
import sqlite3
import logging
from pathlib import Path
from datetime import datetime

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Paths
HACKATON_PATH = Path(__file__).parent
DB_PATH = HACKATON_PATH / "hackaton.db"
SQL_SCHEMA = HACKATON_PATH / "sql" / "hex_schema.sql"
CSV_EXAMPLE = HACKATON_PATH / "data" / "emploi_du_temps_exemple.csv"


def init_database() -> bool:
    """Initialise la base de donnees avec le schema"""
    logger.info("Initialisation base de donnees...")

    try:
        conn = sqlite3.connect(DB_PATH)

        # Executer schema
        if SQL_SCHEMA.exists():
            with open(SQL_SCHEMA, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            logger.info(f"Schema charge depuis {SQL_SCHEMA}")
        else:
            logger.warning(f"Schema non trouve: {SQL_SCHEMA}")
            return False

        conn.commit()
        conn.close()

        logger.info("[OK] Base initialisee")
        return True

    except Exception as e:
        logger.error(f"Erreur init DB: {e}")
        return False


def fetch_crypto_data(symbols: list = None) -> bool:
    """Recupere les donnees crypto via CCXT/MEXC"""
    from python.etl import HackathonETL

    symbols = symbols or ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    logger.info(f"Fetch crypto data pour {len(symbols)} actifs...")

    etl = HackathonETL()
    all_data = []

    for symbol in symbols:
        df = etl.fetch_mexc_hourly(symbol, limit=168)  # 7 jours
        if not df.empty:
            all_data.append(df)
            logger.info(f"  {symbol}: {len(df)} bougies")

    if all_data:
        import pandas as pd
        df_combined = pd.concat(all_data, ignore_index=True)

        # Calculer volatilite par actif
        for symbol in df_combined['symbol'].unique():
            subset = df_combined[df_combined['symbol'] == symbol]
            vol = etl.calc_volatility_1h(subset.tail(24))
            logger.info(f"  {symbol} volatilite 24h: {vol:.1f}")

        etl.export_to_sql(df_combined, 'crypto_data_raw', if_exists='replace')
        logger.info(f"[OK] {len(df_combined)} lignes exportees")
        return True

    return False


def calculate_scores() -> bool:
    """Calcule les Trading Window Scores"""
    from python.etl import HackathonETL
    import pandas as pd

    logger.info("Calcul des Trading Window Scores...")

    etl = HackathonETL()

    # Charger emploi du temps depuis DB
    df_horaire = etl.load_from_sql("""
        SELECT jour, heure_debut, heure_fin, type_activite, priorite_trading
        FROM emploi_du_temps WHERE prof_id = 1
    """)

    if df_horaire.empty:
        logger.warning("Pas d'emploi du temps trouve - utilisation CSV exemple")
        if CSV_EXAMPLE.exists():
            df_horaire = etl.load_horaire_prof(str(CSV_EXAMPLE))
        else:
            logger.error("Aucune donnee emploi du temps")
            return False

    # Charger crypto data
    df_crypto = etl.load_from_sql("""
        SELECT * FROM crypto_data_raw ORDER BY timestamp DESC
    """)

    if df_crypto.empty:
        logger.warning("Pas de crypto data - mode simulation")
        df_crypto = etl.fetch_mexc_hourly('BTC/USDT', limit=48)

    # Merge et calcul scores
    df_scores = etl.merge_horaire_crypto(
        df_horaire,
        df_crypto,
        symbols=['BTC', 'ETH', 'SOL']
    )

    if not df_scores.empty:
        # Export scores
        etl.export_to_sql(df_scores, 'calculated_scores', if_exists='replace')

        # Afficher top 5
        logger.info("\n=== TOP 5 CRENEAUX ===")
        top5 = df_scores.nlargest(5, 'score')
        for _, row in top5.iterrows():
            logger.info(f"  {row['jour']} {row['heure_debut']}-{row['heure_fin']} | {row['symbol']} | Score: {row['score']} ({row['recommendation']})")

        # Generer resume IA
        resume = etl.gen_resume_ia(df_scores, 'Francois')
        logger.info(f"\n[IA PROMPT]\n{resume['prompt'][:500]}...")

        return True

    return False


def run_full_pipeline(test_mode: bool = False) -> bool:
    """Execute le pipeline complet"""
    logger.info("=" * 50)
    logger.info("HACKATHON HEX - School & Crypto Timing")
    logger.info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    logger.info("=" * 50)

    # Etape 1: Init DB
    if not init_database():
        return False

    # Etape 2: Fetch data (skip en mode test)
    if not test_mode:
        fetch_crypto_data()
    else:
        logger.info("[TEST] Mode simulation active")

    # Etape 3: Calculate scores
    if not calculate_scores():
        return False

    logger.info("\n" + "=" * 50)
    logger.info("[OK] Pipeline termine avec succes")
    logger.info("=" * 50)

    return True


def main():
    parser = argparse.ArgumentParser(description="Hackathon Hex - School & Crypto Timing")
    parser.add_argument('--init', action='store_true', help="Initialise DB seulement")
    parser.add_argument('--fetch', action='store_true', help="Fetch crypto data")
    parser.add_argument('--score', action='store_true', help="Calcule scores")
    parser.add_argument('--test', action='store_true', help="Mode test (simulation)")
    parser.add_argument('--symbols', nargs='+', default=['BTC/USDT', 'ETH/USDT'], help="Symboles a fetch")

    args = parser.parse_args()

    if args.init:
        init_database()
    elif args.fetch:
        fetch_crypto_data(args.symbols)
    elif args.score:
        calculate_scores()
    else:
        run_full_pipeline(test_mode=args.test)


if __name__ == "__main__":
    main()
