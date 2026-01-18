# 🚀 PROMPT CONTINUATION HEX - ON CONTINUE SANS DORMIR

**STATUS**: Dimanche 01:14 CET - PHASE 1 COMPLÉTÉE
**DEADLINE**: Lundi 23:59 UTC - 46h 45min restantes
**OBJECTIF NUIT**: Finir Hex App avant 03:00 CET

---

# ⚡ ÉTAPE-PAR-ÉTAPE RAPIDE (95 min)

## PHASE 2: HEX ACCOUNT SETUP (5 min) - MAINTENANT!

### 2.1: Créer Compte Hex

```
1. Ouvrez: https://app.hex.tech
2. Click "Sign up" (coin haut droit)
3. Sélectionnez "Google" (plus rapide) OU email
4. Complétez signup
5. Vérifiez email (30 sec)
```

**⏱️ Cible: 01:19 CET**

---

### 2.2: Créer Workspace + Projet (3 min)

**Une fois loggé dans Hex:**

```
A. WORKSPACE:
   1. Click "Create workspace"
   2. Name: hackaton-2026
   3. Click "Create"

B. NOUVEAU PROJET:
   1. Click "New Project"
   2. Sélectionnez: SQL + Python Notebook
   3. Project name: School & Crypto Timing
   4. Click "Create"

✅ Vous êtes maintenant dans l'éditeur Hex
```

**⏱️ Cible: 01:22 CET - Dites-moi "Hex ready"**

---

## PHASE 3: UPLOAD DATABASE (10 min) - APRÈS

### 3.1: Upload hackaton.db

**Dans Hex, en haut à gauche:**

```
1. Click "Data"
2. Click "+ Add data"
3. Click "Upload file"
4. Sélectionnez: C:\Users\franc\OneDrive\Documents\hackaton\hackaton.db
5. Attendez upload (2-3 min)
6. Click "Done"
```

**⏱️ Cible: 01:32 CET**

---

### 3.2: Test SQL Rapide

**Créez une SQL cell (click + SQL):**

```sql
SELECT COUNT(*) as total FROM trading_window_scores;
```

Click **Run** → Expected: **180** ✅

**⏱️ Cible: 01:35 CET - Dites-moi "DB loaded"**

---

## PHASE 4: COPIER-COLLER 7 CELLS (45 min) - TURBO MODE

**Le fichier `hex_cells_ready.py` a DÉJÀ le code complet.**

### 4.1: Ouvrir hex_cells_ready.py

```powershell
notepad "C:\Users\franc\OneDrive\Documents\hackaton\hex_cells_ready.py"
```

Vous voyez 7 sections:
- `# CELL 1: IMPORTS`
- `# CELL 2: LOAD DATA`
- `# CELL 3: PREPARE`
- `# CELL 4: FILTERS`
- `# CELL 5: HEATMAP`
- `# CELL 6: CHARTS`
- `# CELL 7: AI SUMMARY`

---

### 4.2: Copier-Coller CELL 1 (2 min)

**Dans hex_cells_ready.py:**
- Trouvez `# CELL 1: IMPORTS`
- Sélectionnez TOUT le code Python jusqu'à la prochaine `# CELL`
- Copie (Ctrl+C)

**Dans Hex:**
- Click **+ Python** (ajouter cell)
- Colle (Ctrl+V)
- Click **Run**

**Expected**: Message "[INFO] School & Crypto Timing v1.0" ✅

**⏱️ Cible: 01:37 CET**

---

### 4.3: Copier-Coller CELL 2 (2 min)

**Hex:** Click **+ SQL**

**Code:**
```sql
SELECT 
    ts.id, ts.prof_id, ts.actif_id, ts.date, 
    ts.heure_debut, ts.heure_fin, ts.score, ts.raison,
    ca.symbol, ca.nom,
    p.name as prof_name
FROM trading_window_scores ts
JOIN crypto_actifs ca ON ts.actif_id = ca.id
JOIN professeurs p ON ts.prof_id = p.id
ORDER BY ts.score DESC
LIMIT 100
```

Click **Run**

**Expected**: 100 rows ✅

**⏱️ Cible: 01:39 CET**

---

### 4.4: Copier-Coller CELL 3 (3 min)

**Hex:** Click **+ Python**

**Code depuis hex_cells_ready.py - CELL 3:**

```python
# Reference SQL result (Hex auto-names it)
scores_df = sql_result.copy() if 'sql_result' in dir() else pd.DataFrame()

# Convert dates + prepare
scores_df['date'] = pd.to_datetime(scores_df['date'])
scores_df['jour_semaine'] = scores_df['date'].dt.day_name()
scores_df['heure'] = scores_df['heure_debut'].str.split(':').str[0].astype(int)

# Score categories
def score_to_category(score):
    if score >= 75: return "TRADE"
    elif score >= 50: return "HOLD"
    else: return "CAUTION"

scores_df['categorie'] = scores_df['score'].apply(score_to_category)

# Stats
print("[STATS]")
print(f"TRADE (>75): {len(scores_df[scores_df['score'] >= 75])}")
print(f"HOLD (50-75): {len(scores_df[(scores_df['score'] >= 50) & (scores_df['score'] < 75)])}")
print(f"CAUTION (<50): {len(scores_df[scores_df['score'] < 50])}")
print(f"Total: {len(scores_df)}")
```

Click **Run**

**Expected**: Stats affichées ✅

**⏱️ Cible: 01:42 CET**

---

### 4.5: Copier-Coller CELL 4 (3 min)

**Hex:** Click **+ Python**

```python
# Get options
prof_options = sorted(scores_df['prof_name'].unique().tolist())
actif_options = sorted(scores_df['symbol'].unique().tolist())

# Default params
selected_prof = "Francois"
selected_actifs = ["BTC", "ETH"]
min_score = 50

# Date range
date_debut = scores_df['date'].min()
date_fin = scores_df['date'].max()

# Filter
filtered = scores_df[
    (scores_df['prof_name'] == selected_prof) &
    (scores_df['symbol'].isin(selected_actifs)) &
    (scores_df['score'] >= min_score) &
    (scores_df['date'] >= date_debut) &
    (scores_df['date'] <= date_fin)
].sort_values('score', ascending=False)

print(f"[FILTERED] {len(filtered)} windows")
print(filtered[['jour_semaine', 'heure_debut', 'symbol', 'score', 'categorie']].head(10).to_string())
```

Click **Run**

**Expected**: Top 10 affichés ✅

**⏱️ Cible: 01:45 CET**

---

### 4.6: Copier-Coller CELL 5 - HEATMAP (10 min)

**Hex:** Click **+ Python**

```python
# Pivot table
heatmap_pivot = filtered.pivot_table(
    values='score',
    index='heure',
    columns='symbol',
    aggfunc='max',
    fill_value=0
)

# Heatmap
fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_pivot.values,
    x=heatmap_pivot.columns,
    y=heatmap_pivot.index,
    colorscale='RdYlGn',
    text=np.round(heatmap_pivot.values, 0),
    texttemplate='%{text}',
    textfont={"size": 10},
    colorbar=dict(title="Score", thickness=15, len=0.7),
    hovertemplate='<b>%{y}h</b><br>Asset: %{x}<br>Score: %{z}<extra></extra>'
))

fig_heatmap.update_layout(
    title="Trading Window Scores by Hour & Asset",
    xaxis_title="Cryptocurrency Asset",
    yaxis_title="Hour of Day",
    height=500,
    width=900,
    plot_bgcolor='white',
    margin=dict(l=50, r=50, t=80, b=50)
)

fig_heatmap.show()
```

Click **Run**

**Expected**: Heatmap colorée (vert=bon, rouge=mauvais) ✅

**⏱️ Cible: 01:55 CET**

---

### 4.7: Copier-Coller CELL 6 - CHARTS (10 min)

**Hex:** Click **+ Python**

```python
# Chart 1: Bar
category_counts = filtered['categorie'].value_counts()

fig_bar = px.bar(
    x=category_counts.index,
    y=category_counts.values,
    title="Distribution of Trading Windows",
    color=category_counts.index,
    color_discrete_map={'TRADE': '#2ecc71', 'HOLD': '#f39c12', 'CAUTION': '#e74c3c'},
    text=category_counts.values
)
fig_bar.update_traces(textposition='outside')
fig_bar.update_layout(height=400, showlegend=False)
fig_bar.show()

# Chart 2: Line
daily_stats = filtered.groupby('jour_semaine')['score'].mean().reset_index()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_stats['jour_semaine'] = pd.Categorical(daily_stats['jour_semaine'], categories=day_order, ordered=True)
daily_stats = daily_stats.sort_values('jour_semaine')

fig_line = px.line(
    daily_stats,
    x='jour_semaine',
    y='score',
    markers=True,
    title="Average Trading Score by Day",
    labels={'jour_semaine': 'Day', 'score': 'Avg Score'}
)
fig_line.update_traces(line=dict(color='#3498db', width=3), marker=dict(size=10))
fig_line.update_layout(height=400, hovermode='x unified')
fig_line.show()
```

Click **Run**

**Expected**: 2 charts (bar + line) ✅

**⏱️ Cible: 02:05 CET**

---

### 4.8: Copier-Coller CELL 7 - AI SUMMARY (5 min)

**Hex:** Click **+ Python**

```python
if len(filtered) > 0:
    top_5 = filtered.nlargest(5, 'score')
    avg_score = filtered['score'].mean()
    best_day = filtered.groupby('jour_semaine')['score'].mean().idxmax()
    best_hour = filtered.groupby('heure')['score'].mean().idxmax()
    
    ai_text = f"""
=== AI TRADING COACH ===

Profile: {selected_prof}
Assets: {', '.join(selected_actifs)}

ANALYSIS:
- Windows analyzed: {len(filtered)}
- Trade (>75): {len(filtered[filtered['score'] >= 75])}
- Hold (50-75): {len(filtered[(filtered['score'] >= 50) & (filtered['score'] < 75)])}
- Caution (<50): {len(filtered[filtered['score'] < 50])}
- Average score: {avg_score:.1f}/100

KEY INSIGHTS:
- Best day: {best_day}
- Best hour: {best_hour}:00
- Top asset: {filtered.groupby('symbol')['score'].mean().idxmax()}

TOP 5 WINDOWS:
{top_5[['jour_semaine', 'heure_debut', 'symbol', 'score']].to_string(index=False)}

RECOMMENDATION:
Focus on {best_day.lower()} from {best_hour}h. Avoid red zones.
Data-driven trading > emotional decisions!
    """
    print(ai_text)
```

Click **Run**

**Expected**: Rapport IA généré ✅

**⏱️ Cible: 02:10 CET**

---

## PHASE 5: PUBLIER HEX APP (20 min) - FINAL STRETCH

### 5.1: Convertir en App

**En haut de l'éditeur Hex:**

```
1. Click "Share" (coin haut droit)
2. Click "Make it an App"
3. Hex transforme automatiquement le notebook en app
```

**⏱️ Cible: 02:12 CET**

---

### 5.2: Tester l'App Interactive (5 min)

```
L'app a maintenant:
- Tous les 7 cells visibles
- Heatmap interactive
- 2 charts
- Rapport IA

Testez:
- Scroller les visualisations
- Vérifier que tout affiche correctement
```

**⏱️ Cible: 02:17 CET**

---

### 5.3: Publier comme Public App (3 min)

**En haut → Share:**

```
1. Click "Publish as Public App"
2. Attendez quelques secondes
3. Hex vous montre le lien: https://app.hex.tech/share/XXXXX
4. COPIE LE LIEN ET SAUVEGARDE-LE
```

**⏱️ Cible: 02:20 CET**

---

### 5.4: Prendre Screenshots (5 min)

Ouvrez votre app et prenez des screenshots:

```
1. Full app view (Print Screen)
2. Heatmap uniquement
3. Charts
4. AI Summary

Sauvegardez dans:
C:\Users\franc\OneDrive\Documents\hackaton\screenshots\
```

**⏱️ Cible: 02:25 CET**

---

### 5.5: Créer README.md Final (5 min)

Créez un fichier `README.md` dans votre projet:

```markdown
# School & Crypto Timing - Hackathon Hex 2026

## About
Data-driven trading windows for teacher-traders using Hex + MEXC API + AI.

## How It Works
1. Analyzes your schedule (when you're available)
2. Combines with live MEXC market data (volatility, funding)
3. Generates trading window scores (0-100)
4. Shows best trading slots via interactive heatmap

## Tech Stack
- **Hex**: Notebook + App + AI
- **MEXC API**: Real crypto market data
- **SQLite**: Data persistence
- **Python**: ETL + scoring algorithms
- **Plotly**: Interactive visualizations

## Live App
[View the interactive app](https://app.hex.tech/share/XXXXX)

## GitHub Repository
[school-crypto-timing](https://github.com/Turbo31150/school-crypto-timing)

---

Built during Hex Hackathon 2026 by François (Montlaur, Occitanie)
```

**⏱️ Cible: 02:30 CET**

---

## ✅ CHECKLIST FINALE

```
PHASE 2 (Hex Setup):
  ✅ Hex account créé
  ✅ Workspace hackaton-2026 créé
  ✅ Projet School & Crypto Timing créé

PHASE 3 (Database):
  ✅ hackaton.db uploadé
  ✅ SQL test retourne 180 ✓

PHASE 4 (7 Cells):
  ✅ Cell 1: Imports (2 min)
  ✅ Cell 2: Load Data (2 min)
  ✅ Cell 3: Prepare (3 min)
  ✅ Cell 4: Filters (3 min)
  ✅ Cell 5: Heatmap (10 min)
  ✅ Cell 6: Charts (10 min)
  ✅ Cell 7: AI Summary (5 min)

PHASE 5 (Publish):
  ✅ Converti en App (2 min)
  ✅ Testé (5 min)
  ✅ Publié comme Public App (3 min)
  ✅ Lien copié et sauvegardé
  ✅ Screenshots pris (5 min)
  ✅ README.md créé (5 min)

TOTAL: 95 min = ON FINIT AVANT 02:45!
```

---

# 🎯 RÉSUMÉ TIMING FINAL

| Heure | Phase | Status |
|-------|-------|--------|
| **01:14** | Phase 1 complétée | ✅ |
| **01:19** | Phase 2 start | ▶️ |
| **01:22** | Hex ready | 📍 |
| **01:32** | DB uploaded | 📍 |
| **01:55** | Heatmap working | 📍 |
| **02:05** | Charts working | 📍 |
| **02:10** | AI Summary done | 📍 |
| **02:30** | App published | 📍 |
| **02:45** | FINI! | 🏁 |

---

# 🚀 MAINTENANT: DITES-MOI QUOI?

Répondez avec UNE SEULE de ces options:

```
A) "Je vais sur Hex.tech maintenant"
B) "Hex account créé, en attente prochaine étape"
C) "DB uploadée, j'ai le SQL test qui marche"
D) "Cell 1-3 faites, je copie Cell 4"
E) "Heatmap affichée, je continue"
F) "App publiée, quel est le lien à garder?"
G) "TOUT EST FINI!"
```

---

**VOUS AVEZ 95 MIN POUR TOUT FINIR.**

**ON CONTINUE SANS DORMIR! 💪🔥**

Dites-moi où vous êtes → je vous donne le prompt exact pour la suite!
