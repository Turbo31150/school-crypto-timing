# School & Crypto Timing - Hex Hackathon 2026

[![Hex App](https://img.shields.io/badge/Hex-Live%20App-blueviolet?style=for-the-badge&logo=hex)](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/Turbo31150/school-crypto-timing)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## Problem Solved

**Teachers want to trade crypto but have schedule conflicts!**

- No data-driven view of trading windows
- Emotional decisions lead to losses
- Missed opportunities during available time slots

---

## Data-Driven Solution

```
1. Analyze teacher's weekly schedule (availability)
2. Combine with MEXC crypto volatility data
3. Generate 180 trading window scores (0-100)
4. Display heatmap + AI recommendations
```

---

## Live Demo

**[Click here to open the live Hex App](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest)**

### Embed Code
```html
<iframe width="100%" height="600" style="border: none;"
  src="https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest?embedded=true">
</iframe>
```

---

## Real Results

| Asset | Best Slot | Score | Recommendation |
|-------|-----------|-------|----------------|
| **ETH** | Thursday 10h-12h | **89** | TRADE |
| **ETH** | Thursday 14h-18h | **89** | TRADE |
| **BTC** | Monday 16h | **85** | HOLD |

**AI Coach Says:** *"Focus on 2026-01-20 at 08:00 for best profitability!"*

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Hex Notebook → Published App |
| **Database** | SQLite (180 trading scores) |
| **Visualization** | Plotly (Heatmap + Charts) |
| **Data Processing** | Pandas + Custom Scoring |
| **AI Logic** | Trading Coach Algorithm |
| **API** | MEXC via CCXT |

---

## Project Structure

```
hackaton/
├── run.py                    # Main entry point
├── hackaton.db               # SQLite DB (180 scores)
├── hex_cells_ready.py        # All 7 Hex cells
├── requirements.txt          # Python dependencies
├── python/
│   ├── etl.py                # Extract-Transform-Load
│   ├── scoring.py            # Scoring algorithms
│   ├── query_db.py           # DB queries
│   └── register_script.py    # Script management
├── sql/
│   ├── schema.sql            # Main schema
│   └── hex_schema.sql        # Hackathon schema
├── data/
│   ├── emploi_du_temps_exemple.csv
│   └── crypto_actifs.csv
├── backups/                  # Backup files
├── screenshots/              # App screenshots
└── docs/
    └── api_endpoints.md
```

---

## Scoring Algorithm

```python
Score = (Availability * 0.35) + (Volatility * 0.25) + (Market * 0.25) + (Sentiment * 0.15)

# Thresholds:
# 75+ → TRADE (green zone)
# 50-74 → HOLD (yellow zone)
# <50 → CAUTION (red zone)
```

---

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/Turbo31150/school-crypto-timing.git
cd school-crypto-timing

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python run.py --init

# 4. Run pipeline (test mode)
python run.py --test

# 5. View results
# Open hackaton.db with SQLite viewer
# Or visit live Hex app
```

---

## Hackathon Submission

**Hex-a-thon 2026** on Devpost

| Field | Value |
|-------|-------|
| **Published** | 2026-01-18 03:11 CET |
| **Author** | claire.domingues@ac-toulouse.fr |
| **Location** | Montlaur, Occitanie, France |
| **Top Score** | ETH 89/100 |
| **Total Scores** | 180 trading windows |

---

## Links

- **Live App**: [Hex App](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest)
- **GitHub**: [school-crypto-timing](https://github.com/Turbo31150/school-crypto-timing)
- **Devpost**: [Hex-a-thon 2026](https://hex-hackathon-2026.devpost.com/)

---

## Contact

**Francois** - Montlaur, Occitanie, France
Email: claire.domingues@ac-toulouse.fr

---

*Data-driven trading > emotional decisions. Trade smart!*

Built with Claude Code (Opus 4.5) + Multi-IA Consensus
