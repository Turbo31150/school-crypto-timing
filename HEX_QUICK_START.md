# Hex Quick Start Guide - School & Crypto Timing

## Cellule 1 : Connexion DB (CELL_0)

```python
import sqlite3
import pandas as pd

# Connexion à hackaton.db
conn = sqlite3.connect('hackaton.db')

# Dataset 1: Top 10 meilleures fenêtres (score >= 75)
best_windows = pd.read_sql_query("""
    SELECT
        jour AS day_name,
        heure_debut AS time_slot_start,
        heure_fin AS time_slot_end,
        symbol AS asset_symbol,
        score,
        recommendation,
        ROUND(volatility, 2) AS volatility_pct
    FROM calculated_scores
    WHERE score >= 75
    ORDER BY score DESC
    LIMIT 10
""", conn)

# Dataset 2: Stats par actif crypto
asset_stats = pd.read_sql_query("""
    SELECT
        symbol AS asset_symbol,
        COUNT(*) AS total_windows,
        ROUND(AVG(score), 1) AS avg_score,
        MAX(score) AS best_score,
        SUM(CASE WHEN recommendation = 'TRADE' THEN 1 ELSE 0 END) AS trade_signals
    FROM calculated_scores
    GROUP BY symbol
    ORDER BY avg_score DESC
""", conn)

# Dataset 3: Données heatmap (180 fenêtres)
heatmap_data = pd.read_sql_query("""
    SELECT
        jour AS day_name,
        heure_debut AS time_slot,
        symbol AS asset_symbol,
        score,
        recommendation
    FROM calculated_scores
    ORDER BY jour, heure_debut
""", conn)

conn.close()

print(f"Données chargées:")
print(f"  - best_windows: {len(best_windows)} fenêtres")
print(f"  - asset_stats: {len(asset_stats)} actifs")
print(f"  - heatmap_data: {len(heatmap_data)} créneaux")
print(f"\nMeilleure fenêtre: {best_windows.iloc[0]['day_name']} {best_windows.iloc[0]['time_slot_start']} ({best_windows.iloc[0]['asset_symbol']}) - Score: {best_windows.iloc[0]['score']}/100")
```

---

## Cellule 2 : Heatmap (CELL_5)

```python
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "iframe"

heatmap_pivot = heatmap_data.pivot_table(
    values='score',
    index='time_slot',
    columns=['day_name', 'asset_symbol'],
    aggfunc='mean'
)

fig = px.imshow(
    heatmap_pivot,
    labels=dict(x="Jour / Actif", y="Créneau horaire", color="Score"),
    title="Fenêtres de Trading Optimales - Heatmap",
    color_continuous_scale='RdYlGn',
    range_color=[0, 100],
    aspect="auto"
)

fig.update_layout(height=600, font_size=11, xaxis_tickangle=-45)
fig.show()
```

---

## Cellule 3 : Coach IA (CELL_8)

```python
from datetime import datetime

best = best_windows.iloc[0]
trade_count = len(best_windows[best_windows['recommendation'] == 'TRADE'])

ai_coach = f"""
COACH IA - Recommandation du {datetime.now().strftime('%d/%m/%Y')}

MEILLEURE OPPORTUNITE
  Actif: {best['asset_symbol']}
  Jour: {best['day_name']}
  Créneau: {best['time_slot_start']} - {best['time_slot_end']}
  Score: {best['score']}/100
  Action: {best['recommendation']}

STRATEGIE
  {trade_count} signaux TRADE sur les 10 meilleures fenêtres.
  Concentrez-vous sur les créneaux verts (score > 75).
"""

print(ai_coach)
```

---

## Cellule 4 : Tableau Top 10 (CELL_10)

```python
top_10_display = best_windows.copy()
top_10_display['Créneau'] = top_10_display['time_slot_start'] + ' - ' + top_10_display['time_slot_end']
top_10_display['Score'] = top_10_display['score'].astype(str) + '/100'

final_table = top_10_display[[
    'day_name', 'Créneau', 'asset_symbol', 'Score', 'recommendation', 'volatility_pct'
]].rename(columns={
    'day_name': 'Jour',
    'asset_symbol': 'Actif',
    'recommendation': 'Action',
    'volatility_pct': 'Volatilité %'
})

final_table
```

---

## Checklist

- [ ] CELL_0 exécutée sans erreur
- [ ] Heatmap affiche les couleurs
- [ ] Coach IA affiche "Jeudi 10:00 ETH - 89/100"
- [ ] Tableau affiche 10 lignes
- [ ] Onglet App configuré
- [ ] App publiée

---

## Résultat attendu

```
Meilleure fenêtre: Jeudi 10:00-12:00 (ETH) - Score: 89/100
```
