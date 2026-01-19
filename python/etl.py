#!/usr/bin/env python3
"""
HACKATHON HEX - ETL Module
School & Crypto Timing - Extract, Transform, Load

Extract: MEXC API (live crypto data) + CSV (emploi du temps prof)
Transform: agregations, scores, nettoyage
Load: DataFrames + SQLite
"""

import pandas as pd
import numpy as np
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Paths
HACKATON_PATH = Path(r"C:\Users\franc\OneDrive\Documents\hackaton")
DB_PATH = HACKATON_PATH / "hackaton.db"

# CCXT import avec fallback
try:
    import ccxt
    CCXT_AVAILABLE = True
except ImportError:
    CCXT_AVAILABLE = False
    logger.warning("CCXT non disponible - mode simulation")


class HackathonETL:
    """
    ETL Pipeline pour School & Crypto Timing

    Attributes:
        db_path: Chemin vers la base SQLite
        exchange: Instance CCXT MEXC (si disponible)
    """

    def __init__(self, db_path: Path = DB_PATH):
        """Initialise l'ETL avec connexion DB et exchange"""
        self.db_path = db_path
        self.exchange = None

        if CCXT_AVAILABLE:
            try:
                self.exchange = ccxt.mexc({
                    'apiKey': 'mx0vglrR6uWgWEB6Vm',
                    'secret': 'ba096c7a96c149409914dc0eebdfa53f',
                    'enableRateLimit': True,
                    'options': {'defaultType': 'swap'}
                })
                logger.info("MEXC exchange connecte via CCXT")
            except Exception as e:
                logger.error(f"Erreur connexion MEXC: {e}")

    # =========================================================================
    # EXTRACT
    # =========================================================================

    def load_horaire_prof(self, csv_path: str) -> pd.DataFrame:
        """
        Charge un CSV d'emploi du temps professeur

        Args:
            csv_path: Chemin vers le fichier CSV

        Returns:
            DataFrame avec colonnes normalisees:
            [jour, heure_debut, heure_fin, type_activite, priorite_trading]
        """
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')

            # Normaliser les colonnes
            col_mapping = {
                'Jour': 'jour',
                'Day': 'jour',
                'Heure Debut': 'heure_debut',
                'Start': 'heure_debut',
                'Heure Fin': 'heure_fin',
                'End': 'heure_fin',
                'Activite': 'type_activite',
                'Activity': 'type_activite',
                'Priorite': 'priorite_trading',
                'Priority': 'priorite_trading'
            }
            df.rename(columns=col_mapping, inplace=True)

            # Valeurs par defaut
            if 'priorite_trading' not in df.columns:
                df['priorite_trading'] = df['type_activite'].apply(
                    lambda x: 0 if 'cours' in str(x).lower() else 5
                )

            # Convertir heures en format standard
            for col in ['heure_debut', 'heure_fin']:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], format='%H:%M', errors='coerce').dt.strftime('%H:%M')

            logger.info(f"Charge {len(df)} creneaux depuis {csv_path}")
            return df

        except Exception as e:
            logger.error(f"Erreur chargement CSV: {e}")
            return pd.DataFrame()

    def fetch_mexc_hourly(
        self,
        symbol: str = 'BTC/USDT',
        limit: int = 100,
        timeframe: str = '1h'
    ) -> pd.DataFrame:
        """
        Recupere les donnees OHLCV depuis MEXC via CCXT

        Args:
            symbol: Paire trading (ex: 'BTC/USDT')
            limit: Nombre de bougies
            timeframe: Intervalle ('1h', '4h', '1d')

        Returns:
            DataFrame avec colonnes:
            [timestamp, open, high, low, close, volume]
        """
        if not self.exchange:
            logger.warning("Exchange non disponible - donnees simulees")
            return self._generate_mock_ohlcv(symbol, limit)

        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

            df = pd.DataFrame(ohlcv, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume'
            ])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['symbol'] = symbol.replace('/USDT', '')

            logger.info(f"Recupere {len(df)} bougies pour {symbol}")
            return df

        except Exception as e:
            logger.error(f"Erreur fetch MEXC {symbol}: {e}")
            return self._generate_mock_ohlcv(symbol, limit)

    def _generate_mock_ohlcv(self, symbol: str, limit: int) -> pd.DataFrame:
        """Genere des donnees OHLCV simulees pour test"""
        base_price = {'BTC': 95000, 'ETH': 3200, 'SOL': 180}.get(
            symbol.replace('/USDT', ''), 100
        )

        timestamps = pd.date_range(
            end=datetime.now(),
            periods=limit,
            freq='1H'
        )

        np.random.seed(42)
        prices = base_price * (1 + np.cumsum(np.random.randn(limit) * 0.01))

        df = pd.DataFrame({
            'timestamp': timestamps,
            'open': prices,
            'high': prices * (1 + np.abs(np.random.randn(limit) * 0.005)),
            'low': prices * (1 - np.abs(np.random.randn(limit) * 0.005)),
            'close': prices * (1 + np.random.randn(limit) * 0.002),
            'volume': np.random.uniform(1000, 10000, limit),
            'symbol': symbol.replace('/USDT', '')
        })

        return df

    def fetch_funding_rate(self, symbol: str = 'BTC_USDT') -> Optional[float]:
        """Recupere le funding rate actuel"""
        if not self.exchange:
            return np.random.uniform(-0.01, 0.01)

        try:
            ticker = self.exchange.fetch_ticker(symbol.replace('_', '/'))
            return ticker.get('info', {}).get('fundingRate', 0)
        except:
            return 0.0

    # =========================================================================
    # TRANSFORM
    # =========================================================================

    def calc_volatility_1h(self, df_ohlcv: pd.DataFrame) -> float:
        """
        Calcule la volatilite horaire (methode Parkinson)

        Parkinson volatility = sqrt(1/(4*ln(2)) * mean((ln(H/L))^2))
        Plus stable que std dev pour donnees OHLC

        Args:
            df_ohlcv: DataFrame avec colonnes high, low

        Returns:
            Volatilite normalisee 0-100
        """
        if df_ohlcv.empty:
            return 50.0

        try:
            # Parkinson volatility
            log_hl = np.log(df_ohlcv['high'] / df_ohlcv['low'])
            parkinson = np.sqrt((1 / (4 * np.log(2))) * np.mean(log_hl ** 2))

            # Normaliser sur echelle 0-100
            # 0.01 = faible (10), 0.05 = moyen (50), 0.10+ = eleve (90+)
            normalized = min(100, max(0, parkinson * 1000))

            return round(normalized, 2)

        except Exception as e:
            logger.error(f"Erreur calcul volatilite: {e}")
            return 50.0

    def calc_trading_window_score(
        self,
        prof_id: int,
        horaire_row: Dict[str, Any],
        crypto_data: Dict[str, Any],
        preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Calcule le score d'un creneau de trading (0-100)

        Formule:
        Score = (Volatilite * 0.3) + (Disponibilite * 0.4) + (Market * 0.3)

        Args:
            prof_id: ID du professeur
            horaire_row: Dict avec jour, heure_debut, heure_fin, priorite_trading
            crypto_data: Dict avec volatility, funding_rate, volume
            preferences: Dict avec pref_volatilite, aversion_risque

        Returns:
            Dict avec score, raison, composants
        """
        preferences = preferences or {
            'pref_volatilite': 'medium',
            'aversion_risque': 5
        }

        # Composante disponibilite (0-100)
        priorite = horaire_row.get('priorite_trading', 3)
        availability = priorite * 20  # 0-5 -> 0-100

        # Bonus pour creneaux "Libre" (type_activite)
        type_act = str(horaire_row.get('type_activite', '')).lower()
        libre_bonus = 15 if 'libre' in type_act else 0

        # Composante volatilite (0-100) - OPTIMISEE
        volatility = crypto_data.get('volatility', 50)
        pref_vol = preferences.get('pref_volatilite', 'medium')

        if pref_vol == 'low':
            # Basse volatilite = bon score
            vol_score = max(0, 100 - volatility)
        elif pref_vol == 'high':
            vol_score = min(100, volatility * 2)
        else:
            # Medium: volatilite 3-15% est ideale, score 70-100
            if volatility <= 20:
                vol_score = min(100, 70 + volatility * 1.5)
            else:
                vol_score = max(40, 100 - (volatility - 20))

        # Composante marche (funding + volume) - OPTIMISEE
        funding = abs(crypto_data.get('funding_rate', 0)) * 1000
        volume = crypto_data.get('volume', 5000)
        # Normaliser volume (>10k = bon)
        volume_norm = min(100, (volume / 500) + 50)
        market_score = (volume_norm * 0.6) + ((100 - min(funding, 50)) * 0.4)

        # Score final pondere + bonus libre
        raw_score = (
            (vol_score * 0.25) +
            (availability * 0.40) +
            (market_score * 0.35)
        )
        score = min(100, int(raw_score + libre_bonus))

        # Determination recommendation - SEUILS AJUSTES
        if score >= 75 and availability >= 80:
            recommendation = 'TRADE'
            raison = f"Excellent creneau: score {score}, volatilite {volatility:.1f}%"
        elif score >= 60:
            recommendation = 'WATCH'
            raison = f"Creneau correct: score {score}, surveiller"
        elif availability < 40:
            recommendation = 'AVOID'
            raison = f"Occupe ({horaire_row.get('type_activite', 'activite')})"
        else:
            recommendation = 'HOLD'
            raison = f"Conditions non optimales (score {score})"

        return {
            'score': score,
            'raison': raison,
            'recommendation': recommendation,
            'volatility_component': round(vol_score, 2),
            'availability_component': round(availability, 2),
            'market_component': round(market_score, 2)
        }

    def merge_horaire_crypto(
        self,
        df_horaire: pd.DataFrame,
        df_crypto: pd.DataFrame,
        symbols: List[str] = ['BTC', 'ETH']
    ) -> pd.DataFrame:
        """
        Fusionne emploi du temps et donnees crypto

        Cree une ligne par (creneau, actif) avec scores calcules

        Args:
            df_horaire: Emploi du temps prof
            df_crypto: Donnees OHLCV multi-actifs
            symbols: Liste des actifs a inclure

        Returns:
            DataFrame avec tous les scores
        """
        results = []

        for _, horaire in df_horaire.iterrows():
            for symbol in symbols:
                # Filtrer crypto data pour ce symbol
                crypto_subset = df_crypto[df_crypto['symbol'] == symbol]

                if not crypto_subset.empty:
                    volatility = self.calc_volatility_1h(crypto_subset.tail(24))
                    volume = crypto_subset['volume'].tail(24).mean()
                else:
                    volatility = 50
                    volume = 5000

                crypto_data = {
                    'volatility': volatility,
                    'funding_rate': self.fetch_funding_rate(f"{symbol}_USDT"),
                    'volume': volume
                }

                score_result = self.calc_trading_window_score(
                    prof_id=1,
                    horaire_row=horaire.to_dict(),
                    crypto_data=crypto_data
                )

                results.append({
                    'jour': horaire.get('jour'),
                    'heure_debut': horaire.get('heure_debut'),
                    'heure_fin': horaire.get('heure_fin'),
                    'type_activite': horaire.get('type_activite'),
                    'symbol': symbol,
                    'volatility': volatility,
                    'volume': volume,
                    **score_result
                })

        df_result = pd.DataFrame(results)
        logger.info(f"Genere {len(df_result)} scores (creneaux x actifs)")
        return df_result

    # =========================================================================
    # LOAD
    # =========================================================================

    def export_to_sql(
        self,
        df: pd.DataFrame,
        table_name: str,
        if_exists: str = 'append'
    ) -> bool:
        """
        Exporte un DataFrame vers SQLite

        Args:
            df: DataFrame a exporter
            table_name: Nom de la table cible
            if_exists: 'append', 'replace', 'fail'

        Returns:
            True si succes
        """
        try:
            conn = sqlite3.connect(self.db_path)
            df.to_sql(table_name, conn, if_exists=if_exists, index=False)
            conn.close()

            logger.info(f"Exporte {len(df)} lignes vers {table_name}")
            return True

        except Exception as e:
            logger.error(f"Erreur export SQL: {e}")
            return False

    def load_from_sql(self, query: str) -> pd.DataFrame:
        """Execute une requete SQL et retourne DataFrame"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            logger.error(f"Erreur query SQL: {e}")
            return pd.DataFrame()

    # =========================================================================
    # IA INTEGRATION
    # =========================================================================

    def gen_resume_ia(
        self,
        df_scores: pd.DataFrame,
        prof_name: str = 'Francois'
    ) -> Dict[str, Any]:
        """
        Prepare un prompt pour l'IA avec resume des scores

        Args:
            df_scores: DataFrame avec les scores calcules
            prof_name: Nom du professeur

        Returns:
            Dict avec prompt et data subset
        """
        if df_scores.empty:
            return {'prompt': '', 'data': df_scores}

        # Meilleurs creneaux
        top_windows = df_scores.nlargest(5, 'score')

        # Stats globales
        avg_score = df_scores['score'].mean()
        trade_count = len(df_scores[df_scores['recommendation'] == 'TRADE'])

        prompt = f"""Analyse les creneaux de trading pour {prof_name} cette semaine:

RESUME:
- Score moyen: {avg_score:.0f}/100
- Creneaux TRADE recommandes: {trade_count}
- Meilleur creneau: {top_windows.iloc[0]['jour']} {top_windows.iloc[0]['heure_debut']}-{top_windows.iloc[0]['heure_fin']} ({top_windows.iloc[0]['symbol']}) - Score {top_windows.iloc[0]['score']}

TOP 5 CRENEAUX:
"""
        for _, row in top_windows.iterrows():
            prompt += f"- {row['jour']} {row['heure_debut']}: {row['symbol']} Score={row['score']} ({row['recommendation']})\n"

        prompt += "\nDonne une recommandation personnalisee en 3 phrases max."

        return {
            'prompt': prompt,
            'data': top_windows,
            'stats': {
                'avg_score': avg_score,
                'trade_count': trade_count,
                'total_windows': len(df_scores)
            }
        }


# =============================================================================
# MAIN - Test standalone
# =============================================================================

if __name__ == "__main__":
    print("=== HACKATHON ETL TEST ===\n")

    etl = HackathonETL()

    # Test fetch OHLCV
    print("1. Fetching BTC data...")
    df_btc = etl.fetch_mexc_hourly('BTC/USDT', limit=48)
    print(f"   -> {len(df_btc)} bougies")

    # Test volatilite
    print("\n2. Calculating volatility...")
    vol = etl.calc_volatility_1h(df_btc)
    print(f"   -> Volatilite 1h: {vol}")

    # Test score
    print("\n3. Calculating score...")
    score = etl.calc_trading_window_score(
        prof_id=1,
        horaire_row={'jour': 'Lundi', 'heure_debut': '16:00', 'heure_fin': '18:00', 'priorite_trading': 5, 'type_activite': 'Libre'},
        crypto_data={'volatility': vol, 'funding_rate': 0.001, 'volume': 5000}
    )
    print(f"   -> Score: {score['score']} - {score['recommendation']}")
    print(f"   -> Raison: {score['raison']}")

    print("\n=== TEST COMPLETE ===")
