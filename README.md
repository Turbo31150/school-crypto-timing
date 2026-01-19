# School & Crypto Timing (Hex-a-thon 2026)

[![Live Hex App](https://img.shields.io/badge/Hex-Live%20App-blueviolet?style=for-the-badge&logo=hex)](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest)
[![Repo](https://img.shields.io/badge/GitHub-Repo-black?style=for-the-badge&logo=github)](https://github.com/Turbo31150/school-crypto-timing)

A data app built in **Hex** that helps teacher-traders find realistic crypto trading windows by combining schedule constraints with market signals and an AI coaching summary.

## Live demo

- **App**: https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest
- **Editor (draft)**: https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/hex/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/draft/logic

Embed:
```html
<iframe width="100%" height="600" style="border: none;"
  src="https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest?embedded=true">
</iframe>
```

## What it does

- Scores each available time window with a 0-100 "Trading Window Score".
- Classifies windows into:
  - **TRADE** (>= 75)
  - **HOLD** (50-74)
  - **CAUTION** (< 50)
- Renders a Day x Hour heatmap + charts + an AI coach summary in Hex.

## Demo dataset (final)

| Metric | Value |
|--------|-------|
| Schedule windows | 15 (teacher weekly timetable) |
| Scored trading windows | 45 (3 assets x 15 windows) |
| Best slot | Thursday 10:00-12:00 |
| Max score | 100 (ETH / SOL) |
| BTC max | 98 |

## Tech stack

- **Hex** (Notebook + App)
- **SQLite** (`hackaton.db`)
- **Python** (ETL + scoring)
- **Plotly** (visualizations)
- **CCXT** (MEXC-compatible market access)

## Run locally

```bash
pip install -r requirements.txt
python run.py --init
python run.py --test
```

## Repo structure

```
hackaton/
├── run.py                 # Main pipeline (init / fetch / score / test)
├── hackaton.db            # SQLite database (Hex app source)
├── hex_cells_ready.py     # 7 Hex cells ready to copy/paste
├── python/
│   └── etl.py             # ETL + scoring logic
├── sql/
│   └── hex_schema.sql     # DB schema
└── data/
    └── emploi_du_temps_exemple.csv
```

## French (mini)

Cette app Hex aide un enseignant-trader a choisir ses meilleurs creneaux (heatmap Jour x Heure) avec un score 0-100 et un resume IA.

## Contact

claire.domingues@ac-toulouse.fr

---

*Built with Claude Code (Opus 4.5) for Hex-a-thon 2026*
