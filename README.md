# School & Crypto Timing

Hackathon Hex 2026 - Optimisez vos sessions de trading crypto autour de votre emploi du temps professionnel.

## Concept

Un professeur/professionnel veut trader de la crypto mais a des contraintes horaires (cours, reunions, etc.). Cette application calcule automatiquement les **meilleurs creneaux de trading** en croisant:

- **Emploi du temps personnel** (disponibilites, priorites)
- **Donnees marche temps reel** (volatilite, funding rate, volume via MEXC)
- **Preferences de risque** (aversion, type de volatilite preferee)

## Quick Start

```bash
# 1. Installer dependances
pip install -r requirements.txt

# 2. Initialiser la base de donnees
python run.py --init

# 3. Lancer le pipeline complet
python run.py

# Mode test (donnees simulees)
python run.py --test
```

## Structure

```
hackaton/
├── run.py                  # Point d'entree principal
├── requirements.txt        # Dependances Python
├── hackaton.db            # Base SQLite
├── python/
│   ├── etl.py             # Extract-Transform-Load
│   ├── scoring.py         # Algorithmes de scoring
│   ├── register_script.py # Gestion scripts DB
│   └── query_db.py        # Requetes DB
├── sql/
│   ├── schema.sql         # Schema principal
│   └── hex_schema.sql     # Schema Hackathon Hex
├── data/
│   ├── emploi_du_temps_exemple.csv
│   └── crypto_actifs.csv
└── docs/
    └── api_endpoints.md
```

## Algorithme de Scoring

```
Score = (Volatilite * 0.25) + (Disponibilite * 0.35) + (Marche * 0.25) + (Sentiment * 0.15)

- Volatilite: Parkinson volatility normalisee 0-100
- Disponibilite: Priorite trading (0-5) -> 0-100
- Marche: Funding rate + Volume + Liquidations
- Sentiment: Fear & Greed Index
```

### Recommendations

| Score | Recommendation | Action |
|-------|---------------|--------|
| 75+ | TRADE | Excellent creneau |
| 55-74 | WATCH | Surveiller |
| 35-54 | HOLD | Attendre |
| <35 | AVOID | Eviter |

## API Endpoints (MEXC)

- OHLCV: `https://contract.mexc.com/api/v1/contract/kline/{symbol}`
- Funding: `https://contract.mexc.com/api/v1/contract/funding_rate/history`
- Positions: Via CCXT (`ccxt.mexc()`)

## Tech Stack

- **Python 3.8+** avec pandas, numpy, ccxt
- **SQLite** pour stockage local
- **MEXC API** pour donnees crypto temps reel
- **Hex** pour visualisation notebook

## Auteur

Projet Hackathon Hex 2026

---

Built with Claude Code (Opus 4.5) + Multi-IA Consensus
