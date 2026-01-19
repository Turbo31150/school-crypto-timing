# Hex App Improvements - School & Crypto Timing

## Hackathon Hex 2026
**Date**: 19 janvier 2026
**Version**: 2.0

---

## 1. Configuration de la connexion Base de Données

### Option A: Upload SQLite dans Hex (Recommandé)

1. Dans Hex, aller dans **Settings > Data sources**
2. Cliquer **Add data source**
3. Choisir **File upload**
4. Uploader `hackaton.db`
5. Nommer la connexion: `hackaton_db`

### Option B: Connexion Python directe

Si l'upload n'est pas possible, utiliser une cellule Python pour charger la DB:

```python
import sqlite3
import pandas as pd

# Connexion SQLite
conn = sqlite3.connect('hackaton.db')

# Charger toutes les données
calculated_scores = pd.read_sql_query("SELECT * FROM calculated_scores", conn)
trading_window_scores = pd.read_sql_query("SELECT * FROM trading_window_scores", conn)
crypto_actifs = pd.read_sql_query("SELECT * FROM crypto_actifs", conn)
professeurs = pd.read_sql_query("SELECT * FROM professeurs", conn)

conn.close()

print(f"[OK] {len(calculated_scores)} fenêtres de trading chargées")
```

---

## 2. Cellules SQL pour Hex

### CELLULE SQL 1: Top 10 Meilleures Fenêtres de Trading

**Nom**: `best_windows`
**Description**: Récupère les 10 meilleures opportunités de trading

```sql
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
    ROUND(volume, 2) AS volume_24h
FROM calculated_scores
WHERE score >= 75
ORDER BY score DESC, volatility DESC
LIMIT 10;
```

**Résultat attendu**: DataFrame `dataframe_1` avec les meilleures opportunités

---

### CELLULE SQL 2: Statistiques par Actif Crypto

**Nom**: `asset_stats`
**Description**: Agrégations par cryptomonnaie

```sql
SELECT
    symbol AS asset_symbol,
    COUNT(*) AS total_windows,
    ROUND(AVG(score), 1) AS avg_score,
    MAX(score) AS best_score,
    MIN(score) AS worst_score,
    SUM(CASE WHEN recommendation = 'TRADE' THEN 1 ELSE 0 END) AS trade_signals,
    SUM(CASE WHEN recommendation = 'HOLD' THEN 1 ELSE 0 END) AS hold_signals,
    SUM(CASE WHEN recommendation = 'AVOID' THEN 1 ELSE 0 END) AS avoid_signals,
    ROUND(AVG(volatility), 2) AS avg_volatility
FROM calculated_scores
GROUP BY symbol
ORDER BY avg_score DESC;
```

**Résultat attendu**: DataFrame `dataframe_2` avec stats par crypto

---

### CELLULE SQL 3: Données Heatmap (Jour x Créneau x Actif)

**Nom**: `heatmap_data`
**Description**: Données pivotées pour la heatmap

```sql
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
```

**Résultat attendu**: DataFrame `dataframe_3` pour visualisation heatmap

---

## 3. Cellules Python de Visualisation

### CELLULE PYTHON 1: Heatmap Interactive

**Nom**: `heatmap_viz`

```python
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Référence aux données SQL (dataframe_3 de la cellule SQL heatmap_data)
df = dataframe_3.copy()

# Créer une colonne combinée jour+heure pour l'axe Y
df['time_label'] = df['time_slot']

# Pivot pour la heatmap
heatmap_pivot = df.pivot_table(
    values='score',
    index='time_label',
    columns=['day_name', 'asset_symbol'],
    aggfunc='mean',
    fill_value=0
)

# Créer la heatmap avec Plotly
fig = px.imshow(
    heatmap_pivot.values,
    labels=dict(x="Jour / Actif", y="Créneau horaire", color="Score"),
    x=[f"{col[0][:3]}-{col[1]}" for col in heatmap_pivot.columns],
    y=heatmap_pivot.index,
    title="Fenêtres de Trading Optimales - Heatmap",
    color_continuous_scale='RdYlGn',
    aspect='auto',
    zmin=0,
    zmax=100
)

fig.update_layout(
    height=600,
    width=1000,
    font_size=12,
    title_font_size=18,
    coloraxis_colorbar=dict(
        title="Score",
        tickvals=[0, 25, 50, 75, 100],
        ticktext=["0 AVOID", "25", "50 HOLD", "75", "100 TRADE"]
    )
)

fig.update_traces(
    hovertemplate='<b>%{x}</b><br>Créneau: %{y}<br>Score: %{z:.0f}/100<extra></extra>'
)

fig
```

---

### CELLULE PYTHON 2: Graphique en Barres par Actif

**Nom**: `asset_bar_chart`

```python
import plotly.express as px

# Référence aux données SQL (dataframe_2 de la cellule SQL asset_stats)
df_stats = dataframe_2.copy()

# Créer le graphique en barres groupées
fig = px.bar(
    df_stats,
    x='asset_symbol',
    y=['trade_signals', 'hold_signals', 'avoid_signals'],
    title="Distribution des Recommandations par Actif",
    labels={'value': 'Nombre de fenêtres', 'asset_symbol': 'Cryptomonnaie'},
    color_discrete_map={
        'trade_signals': '#2ecc71',  # Vert
        'hold_signals': '#f39c12',   # Orange
        'avoid_signals': '#e74c3c'   # Rouge
    },
    barmode='group'
)

fig.update_layout(
    height=450,
    legend_title="Type de signal",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# Renommer les légendes
newnames = {'trade_signals': 'TRADE', 'hold_signals': 'HOLD', 'avoid_signals': 'AVOID'}
fig.for_each_trace(lambda t: t.update(name=newnames.get(t.name, t.name)))

fig
```

---

### CELLULE PYTHON 3: Coach IA - Recommandations

**Nom**: `ai_coach`

```python
from datetime import datetime
import pandas as pd

# Référence aux données SQL
best_windows = dataframe_1.copy()
asset_stats = dataframe_2.copy()
all_data = dataframe_3.copy()

# Calculer les métriques
total_windows = len(all_data)
trade_count = len(all_data[all_data['recommendation'] == 'TRADE'])
hold_count = len(all_data[all_data['recommendation'] == 'HOLD'])
avoid_count = len(all_data[all_data['recommendation'] == 'AVOID'])

# Meilleure fenêtre
if len(best_windows) > 0:
    top_window = best_windows.iloc[0]
    best_asset = asset_stats.loc[asset_stats['avg_score'].idxmax()]

    # Meilleur jour
    day_scores = all_data.groupby('day_name')['score'].mean()
    best_day = day_scores.idxmax()
    best_day_score = day_scores.max()

    # Meilleur créneau
    time_scores = all_data.groupby('time_slot')['score'].mean()
    best_time = time_scores.idxmax()

ai_report = f"""
{'='*60}
   COACH IA - SCHOOL & CRYPTO TIMING
   Rapport du {datetime.now().strftime('%d/%m/%Y à %H:%M')}
{'='*60}

   ANALYSE GLOBALE
   ---------------
   Fenêtres analysées: {total_windows}
   - TRADE (score >= 75): {trade_count} ({trade_count/total_windows*100:.1f}%)
   - HOLD (score 50-74): {hold_count} ({hold_count/total_windows*100:.1f}%)
   - AVOID (score < 50): {avoid_count} ({avoid_count/total_windows*100:.1f}%)

   MEILLEURE OPPORTUNITE
   ---------------------
   Actif: {top_window['asset_symbol']}
   Jour: {top_window['day_name']}
   Créneau: {top_window['time_slot_start']} - {top_window['time_slot_end']}
   Score: {top_window['score']}/100
   Volatilité: {top_window['volatility_pct']}%
   Recommandation: {top_window['recommendation']}

   INSIGHTS CLES
   -------------
   - Meilleur actif global: {best_asset['asset_symbol']} (score moyen: {best_asset['avg_score']:.1f})
   - Meilleur jour: {best_day} (score moyen: {best_day_score:.1f})
   - Meilleur créneau: {best_time}

   STRATEGIE RECOMMANDEE
   ---------------------
   1. Concentrez-vous sur les créneaux VERTS (score > 75)
   2. {best_asset['asset_symbol']} offre les meilleures opportunités
   3. Tradez de préférence le {best_day}
   4. Évitez les zones ROUGES (cours, réunions)

   RISQUE: Toujours utiliser un stop-loss!
{'='*60}
"""

print(ai_report)
```

---

### CELLULE PYTHON 4: Jauge de Score Global

**Nom**: `score_gauge`

```python
import plotly.graph_objects as go

# Calculer le score moyen global
avg_score = all_data['score'].mean()

# Créer la jauge
fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=avg_score,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Score Moyen Global", 'font': {'size': 24}},
    delta={'reference': 50, 'increasing': {'color': "#2ecc71"}, 'decreasing': {'color': "#e74c3c"}},
    gauge={
        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "#3498db"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 50], 'color': '#ffcccc'},
            {'range': [50, 75], 'color': '#fff3cd'},
            {'range': [75, 100], 'color': '#d4edda'}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 75
        }
    }
))

fig.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=50, b=20)
)

fig
```

---

## 4. Configuration de l'Onglet App

### Structure du Dashboard

```
+----------------------------------------------------------+
|        SCHOOL & CRYPTO TIMING - Dashboard               |
+----------------------------------------------------------+
|  [Sélecteur Actif: BTC/ETH/SOL...]  [Slider Score: 0-100] |
+----------------------------------------------------------+
|                                                          |
|  +------------------------+  +------------------------+  |
|  |   JAUGE SCORE GLOBAL   |  |    TOP 10 FENETRES     |  |
|  |      (score_gauge)     |  |    (best_windows)      |  |
|  +------------------------+  +------------------------+  |
|                                                          |
|  +----------------------------------------------------+  |
|  |              HEATMAP INTERACTIVE                    |  |
|  |                (heatmap_viz)                        |  |
|  +----------------------------------------------------+  |
|                                                          |
|  +------------------------+  +------------------------+  |
|  |   STATS PAR ACTIF      |  |    COACH IA            |  |
|  |   (asset_bar_chart)    |  |    (ai_coach)          |  |
|  +------------------------+  +------------------------+  |
|                                                          |
+----------------------------------------------------------+
```

### Inputs Interactifs à créer dans Hex

1. **Sélecteur d'actif** (Dropdown)
   - Nom: `selected_asset`
   - Options: `['Tous', 'BTC', 'ETH', 'SOL', 'XRP', 'DOGE', 'ADA', 'AVAX', 'MATIC', 'DOT', 'LINK']`
   - Default: `'Tous'`

2. **Slider de score minimum** (Slider)
   - Nom: `min_score`
   - Range: 0 - 100
   - Default: 0
   - Step: 5

3. **Sélecteur de jour** (Multi-select)
   - Nom: `selected_days`
   - Options: `['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']`
   - Default: Tous sélectionnés

### Code pour filtrage dynamique

```python
# Cellule de filtrage dynamique
filtered_data = all_data.copy()

# Filtrer par actif
if selected_asset != 'Tous':
    filtered_data = filtered_data[filtered_data['asset_symbol'] == selected_asset]

# Filtrer par score minimum
filtered_data = filtered_data[filtered_data['score'] >= min_score]

# Filtrer par jours
if selected_days:
    filtered_data = filtered_data[filtered_data['day_name'].isin(selected_days)]

print(f"[FILTRE] {len(filtered_data)} fenêtres affichées")
```

---

## 5. Étapes de Déploiement

### Checklist

- [ ] Uploader `hackaton.db` dans Hex Data Sources
- [ ] Créer cellule SQL 1: `best_windows`
- [ ] Créer cellule SQL 2: `asset_stats`
- [ ] Créer cellule SQL 3: `heatmap_data`
- [ ] Créer cellule Python: `heatmap_viz`
- [ ] Créer cellule Python: `asset_bar_chart`
- [ ] Créer cellule Python: `ai_coach`
- [ ] Créer cellule Python: `score_gauge`
- [ ] Configurer les inputs interactifs
- [ ] Basculer vers l'onglet App
- [ ] Organiser le layout
- [ ] Tester les interactions
- [ ] Publier l'application

### Publication

1. Cliquer sur **Publish** en haut à droite
2. Choisir **Public** ou **With link**
3. Activer **App mode** par défaut
4. Copier le lien de partage

---

## 6. Dépannage

### Problème: SQL vide

**Cause**: Pas de connexion de données configurée
**Solution**:
1. Settings > Data sources > Add
2. Upload `hackaton.db`
3. Reconnecter les cellules SQL

### Problème: dataframe_X non défini

**Cause**: Les cellules SQL n'ont pas été exécutées
**Solution**:
1. Exécuter toutes les cellules dans l'ordre (Logic tab)
2. Vérifier que chaque cellule SQL produit un résultat

### Problème: Graphiques ne s'affichent pas

**Cause**: Plotly non importé ou données vides
**Solution**:
1. Ajouter `import plotly.express as px` en début de cellule
2. Vérifier que les DataFrames contiennent des données

---

## Notes Techniques

- **Base de données**: SQLite 3.x
- **Lignes de données**: 180 fenêtres de trading
- **Actifs couverts**: BTC, ETH, SOL, XRP, DOGE, ADA, AVAX, MATIC, DOT, LINK
- **Algorithme de score**: `(Availability × 0.35) + (Volatility × 0.25) + (Market × 0.25) + (Sentiment × 0.15)`

---

*Document généré automatiquement pour le Hackathon Hex 2026*
