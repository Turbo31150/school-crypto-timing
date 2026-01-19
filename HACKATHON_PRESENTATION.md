# SCHOOL & CRYPTO TIMING - HEX HACKATHON 2026

## Executive Summary (2-min Pitch)

> "School & Crypto Timing resolves the schedule conflict vs crypto trading for teachers.
> 45 calculated scores -> Heatmap ETH 100 -> AI recommends 'Jeudi 10h-12h'.
> Live on Hex now!"

---

## The Problem

### Market Opportunity
- **1M+ teachers** in France/EU interested in crypto
- **$2T+ crypto market** with 24/7 trading
- **Pain point:** No data-driven view combining schedule + trading

### User Pain Points
1. Teaching schedule conflicts with trading hours
2. Emotional decisions without data
3. Missing best volatility windows
4. No personalized recommendations

---

## Our Solution

### Technical Architecture
```
INPUT                    PROCESSING               OUTPUT
---------               ------------             --------
Schedule CSV    --->    ETL Pipeline    --->    180 Scores
MEXC API        --->    Scoring Algo    --->    Heatmap
Preferences     --->    AI Logic        --->    Recommendations
```

### Scoring Formula
```python
Score = (Availability × 0.35) + (Volatility × 0.25) +
        (Market × 0.25) + (Sentiment × 0.15)

# Result: 0-100 score per trading window
# 75+ = TRADE | 50-74 = HOLD | <50 = CAUTION
```

---

## Real Results

### Top Trading Windows
| Asset | Time Slot | Score | Action |
|-------|-----------|-------|--------|
| ETH | Jeudi 10:00-12:00 | 100 | TRADE |
| SOL | Jeudi 10:00-12:00 | 100 | TRADE |
| BTC | Jeudi 10:00-12:00 | 98 | TRADE |

### AI Coach Output
```
"Concentrez-vous sur Jeudi 10h-12h (score 100) pour le meilleur rendement!
Evitez les zones rouges pendant les heures de cours.
Trading data-driven > decisions emotionnelles."
```

---

## Live Demo

### Hex App (Published)
**URL:** https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest

### Features
- Interactive Heatmap (Plotly)
- TRADE/HOLD/CAUTION Charts
- AI Coach Report
- 45 Pre-calculated Scores

### Embed Ready
```html
<iframe src="https://app.hex.tech/.../latest?embedded=true" height="600"></iframe>
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Hex Notebook | Interactive App |
| Database | SQLite | 45 scores storage |
| Viz | Plotly | Heatmap + Charts |
| Processing | Pandas | Data manipulation |
| API | MEXC/CCXT | Live crypto data |
| AI | Custom Logic | Trading Coach |

---

## Implementation Stats

```
Repository: https://github.com/Turbo31150/school-crypto-timing
Lines of Code: 1,844+
Commits: 7
Database Records: 45 trading window scores
Published: 2026-01-18 03:11 CET
Top Score: 100/100 (ETH/SOL Jeudi 10h-12h)
```

---

## Scalability Roadmap

### MVP (Current)
- 1 teacher profile
- 45 pre-calculated scores (15 slots x 3 assets)
- Static schedule input

### V1.0 (Q1 2026)
- Multi-teacher support
- Dynamic schedule import
- User authentication

### V2.0 (Q2 2026)
- Live MEXC API integration
- Real-time score updates
- Push notifications

### V3.0 (Q3 2026)
- Mobile app
- Telegram bot alerts
- Portfolio tracking

---

## Business Model

| Tier | Price | Features |
|------|-------|----------|
| **Free** | $0 | 1 profile, 50 scores |
| **Pro** | $9/mo | Unlimited scores, alerts |
| **Team** | $49/mo | 10 teachers, shared insights |
| **API** | $99/mo | Full API access, webhooks |

### Revenue Projection
- Y1: 1,000 users x $9 = $108K ARR
- Y2: 5,000 users x $12 avg = $720K ARR
- Y3: 20,000 users = $2.4M ARR

---

## Competitive Advantage

| Feature | Us | TradingView | Crypto Schedulers |
|---------|-----|-------------|-------------------|
| Schedule Integration | YES | No | Partial |
| Teacher-focused | YES | No | No |
| AI Recommendations | YES | Partial | No |
| Hex Native | YES | No | No |
| Free Tier | YES | Limited | Paid |

---

## The Ask

### From Hex Hackathon
1. **Prize money** -> Scale to 10K users
2. **Mentoring** -> Live API integration
3. **Visibility** -> Featured on Hex gallery

### Partnership Opportunities
- French education ministry pilot
- Teacher unions collaboration
- Crypto exchange partnerships

---

## Team

**Francois** - Montlaur, Occitanie, France
- Full-stack developer
- Crypto trader since 2021
- Education technology enthusiast

**Contact:** claire.domingues@ac-toulouse.fr

---

## Links

| Resource | URL |
|----------|-----|
| Live App | [Hex App](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest) |
| GitHub | [school-crypto-timing](https://github.com/Turbo31150/school-crypto-timing) |
| Devpost | [Hex-a-thon 2026](https://hex-hackathon-2026.devpost.com/) |

---

## Thank You!

*"Data-driven trading > emotional decisions. Trade smart!"*

**Vote for School & Crypto Timing on Devpost!**
