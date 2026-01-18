#!/usr/bin/env python3
"""
HACKATHON HEX - Scoring Module
Algorithmes de calcul des Trading Window Scores
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class Recommendation(Enum):
    """Recommendations de trading"""
    TRADE = "TRADE"      # Excellent - Trader activement
    WATCH = "WATCH"      # Bon - Surveiller
    HOLD = "HOLD"        # Neutre - Attendre
    AVOID = "AVOID"      # Mauvais - Eviter


@dataclass
class ScoreComponents:
    """Composantes du score"""
    volatility: float    # 0-100
    availability: float  # 0-100
    market: float        # 0-100
    sentiment: float     # 0-100 (optionnel)

    @property
    def total(self) -> int:
        """Score total pondere"""
        return int(
            self.volatility * 0.25 +
            self.availability * 0.35 +
            self.market * 0.25 +
            self.sentiment * 0.15
        )


class TradingScorer:
    """
    Calculateur de scores de trading

    Prend en compte:
    - Volatilite du marche
    - Disponibilite du professeur
    - Conditions de marche (funding, volume)
    - Sentiment (Fear & Greed)
    """

    # Poids par defaut
    WEIGHTS = {
        'volatility': 0.25,
        'availability': 0.35,
        'market': 0.25,
        'sentiment': 0.15
    }

    # Seuils de score
    THRESHOLDS = {
        'trade': 75,
        'watch': 55,
        'hold': 35
    }

    def __init__(self, custom_weights: Dict[str, float] = None):
        """Initialise avec poids optionnels"""
        if custom_weights:
            self.weights = {**self.WEIGHTS, **custom_weights}
        else:
            self.weights = self.WEIGHTS

    def calc_volatility_score(
        self,
        volatility: float,
        preference: str = 'medium'
    ) -> float:
        """
        Score volatilite selon preference utilisateur

        Args:
            volatility: Volatilite brute 0-100
            preference: 'low', 'medium', 'high'

        Returns:
            Score 0-100
        """
        if preference == 'low':
            # Prefere basse volatilite
            return max(0, 100 - volatility * 1.5)
        elif preference == 'high':
            # Prefere haute volatilite
            return min(100, volatility * 1.2)
        else:
            # Prefere volatilite moyenne (40-60)
            distance = abs(50 - volatility)
            return max(0, 100 - distance * 2)

    def calc_availability_score(
        self,
        priority: int,
        activity_type: str = None
    ) -> float:
        """
        Score disponibilite selon priorite et type activite

        Args:
            priority: Priorite trading 0-5
            activity_type: Type d'activite (cours, libre, etc.)

        Returns:
            Score 0-100
        """
        base_score = priority * 20  # 0-100

        # Bonus/malus selon type activite
        if activity_type:
            activity_lower = activity_type.lower()
            if 'cours' in activity_lower or 'class' in activity_lower:
                base_score = min(base_score, 10)  # Cap a 10 si en cours
            elif 'libre' in activity_lower or 'free' in activity_lower:
                base_score = max(base_score, 80)  # Min 80 si libre
            elif 'reunion' in activity_lower or 'meeting' in activity_lower:
                base_score = min(base_score, 30)

        return min(100, max(0, base_score))

    def calc_market_score(
        self,
        funding_rate: float,
        volume: float,
        liquidations: float = 0,
        open_interest: float = 0
    ) -> float:
        """
        Score conditions de marche

        Args:
            funding_rate: Taux de funding (-0.1 a 0.1)
            volume: Volume en USDT
            liquidations: Liquidations recentes
            open_interest: Open interest

        Returns:
            Score 0-100
        """
        # Funding: proche de 0 = meilleur
        funding_score = max(0, 100 - abs(funding_rate) * 2000)

        # Volume: normalise log
        volume_score = min(100, np.log10(max(1, volume)) * 15)

        # Liquidations: basses = meilleur
        liq_score = max(0, 100 - liquidations / 1000)

        # Combine
        return (funding_score * 0.4 + volume_score * 0.4 + liq_score * 0.2)

    def calc_sentiment_score(
        self,
        fear_greed: int = 50,
        trend: str = 'neutral'
    ) -> float:
        """
        Score sentiment de marche

        Args:
            fear_greed: Index Fear & Greed 0-100
            trend: 'bullish', 'neutral', 'bearish'

        Returns:
            Score 0-100
        """
        # Fear & Greed optimal entre 30-70 (ni extreme fear ni extreme greed)
        if 30 <= fear_greed <= 70:
            fg_score = 80 + (50 - abs(50 - fear_greed))
        else:
            fg_score = 100 - abs(50 - fear_greed)

        # Bonus trend
        trend_bonus = {'bullish': 10, 'neutral': 0, 'bearish': -10}.get(trend, 0)

        return min(100, max(0, fg_score + trend_bonus))

    def calculate_score(
        self,
        volatility: float,
        priority: int,
        funding_rate: float,
        volume: float,
        activity_type: str = None,
        fear_greed: int = 50,
        vol_preference: str = 'medium'
    ) -> Tuple[int, Recommendation, ScoreComponents]:
        """
        Calcule le score total et la recommendation

        Returns:
            Tuple (score, recommendation, components)
        """
        components = ScoreComponents(
            volatility=self.calc_volatility_score(volatility, vol_preference),
            availability=self.calc_availability_score(priority, activity_type),
            market=self.calc_market_score(funding_rate, volume),
            sentiment=self.calc_sentiment_score(fear_greed)
        )

        score = components.total

        # Determination recommendation
        if score >= self.THRESHOLDS['trade'] and components.availability >= 60:
            recommendation = Recommendation.TRADE
        elif score >= self.THRESHOLDS['watch']:
            recommendation = Recommendation.WATCH
        elif components.availability < 30:
            recommendation = Recommendation.AVOID
        else:
            recommendation = Recommendation.HOLD

        return score, recommendation, components

    def rank_windows(
        self,
        windows: List[Dict],
        top_n: int = 5
    ) -> List[Dict]:
        """
        Classe les creneaux par score

        Args:
            windows: Liste de dicts avec donnees creneaux
            top_n: Nombre de top creneaux a retourner

        Returns:
            Liste triee des meilleurs creneaux
        """
        scored_windows = []

        for window in windows:
            score, rec, components = self.calculate_score(
                volatility=window.get('volatility', 50),
                priority=window.get('priority', 3),
                funding_rate=window.get('funding_rate', 0),
                volume=window.get('volume', 5000),
                activity_type=window.get('activity_type'),
                fear_greed=window.get('fear_greed', 50),
                vol_preference=window.get('vol_preference', 'medium')
            )

            scored_windows.append({
                **window,
                'score': score,
                'recommendation': rec.value,
                'components': {
                    'volatility': components.volatility,
                    'availability': components.availability,
                    'market': components.market,
                    'sentiment': components.sentiment
                }
            })

        # Tri par score decroissant
        scored_windows.sort(key=lambda x: x['score'], reverse=True)

        return scored_windows[:top_n]


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    scorer = TradingScorer()

    # Test creneaux
    windows = [
        {'jour': 'Lundi', 'heure': '16:00', 'priority': 5, 'activity_type': 'Libre', 'volatility': 45, 'volume': 8000, 'funding_rate': 0.001},
        {'jour': 'Lundi', 'heure': '09:00', 'priority': 0, 'activity_type': 'Cours', 'volatility': 60, 'volume': 10000, 'funding_rate': -0.002},
        {'jour': 'Mardi', 'heure': '14:00', 'priority': 3, 'activity_type': 'Preparation', 'volatility': 35, 'volume': 5000, 'funding_rate': 0.0005},
        {'jour': 'Mercredi', 'heure': '10:00', 'priority': 5, 'activity_type': 'Libre', 'volatility': 55, 'volume': 12000, 'funding_rate': 0.002},
    ]

    ranked = scorer.rank_windows(windows)

    print("=== RANKING CRENEAUX ===\n")
    for i, w in enumerate(ranked, 1):
        print(f"{i}. {w['jour']} {w['heure']} - Score: {w['score']} ({w['recommendation']})")
        print(f"   Composantes: V={w['components']['volatility']:.0f} A={w['components']['availability']:.0f} M={w['components']['market']:.0f}")
        print()
