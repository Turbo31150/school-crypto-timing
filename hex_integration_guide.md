# 🚀 HACKATHON HEX - GUIDE INTÉGRATION NOTEBOOK

## Phase 1: Préparation

### Étape 1.1 : Créer un nouveau Hex Project
1. Allez sur https://app.hex.tech
2. **New Project** → **SQL + Python Notebook**
3. Nommez-le: `School & Crypto Timing`
4. Description: `"Analyser les meilleurs créneaux de trading pour un enseignant via données MEXC"`

### Étape 1.2 : Uploader la base SQLite
1. Téléchargez `hackaton.db` depuis `C:\Users\franc\OneDrive\Documents\hackaton\`
2. Dans Hex, allez à **Data** → **Upload Dataset**
3. Uploadez `hackaton.db` 
4. Hex reconnaîtra qu'c'est une SQLite, vous permettra de requêter directement

---

## Phase 2: Construire le Notebook (7 Cells)

### Cell 1: Imports + Config

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Config
TIMEZONE = "Europe/Paris"
print("[INFO] School & Crypto Timing v1.0")
```

### Cell 2: Load Data from SQLite

```python
# Dans Hex, utiliser le data source SQLite uploadé
# Hex SQL cell (ou Python avec sqlite3)

query = """
SELECT 
    ts.id, ts.prof_id, ts.actif_id, ts.date, 
    ts.heure_debut, ts.heure_fin, ts.score, ts.raison,
    ca.symbol, ca.nom,
    p.name as prof_name
FROM trading_window_scores ts
JOIN crypto_actifs ca ON ts.actif_id = ca.id
JOIN professeurs p ON ts.prof_id = p.id
ORDER BY ts.date DESC, ts.score DESC
"""

scores_df = sql(query)
print(f"[LOADED] {len(scores_df)} scores calcules")
```

### Cell 3: Prepare DataFrames

```python
# Convertir dates et ajouter colonnes helper
scores_df['date'] = pd.to_datetime(scores_df['date'])
scores_df['jour_semaine'] = scores_df['date'].dt.day_name()
scores_df['heure'] = scores_df['heure_debut'].str.split(':').str[0].astype(int)

# Catégorie trading
def score_to_category(score):
    if score >= 75:
        return "🟢 TRADE"
    elif score >= 50:
        return "🟡 HOLD"
    else:
        return "🔴 CAUTION"

scores_df['categorie'] = scores_df['score'].apply(score_to_category)

print(f"[OK] DataFrames préparés")
print(f"  TRADE (>75): {len(scores_df[scores_df['score'] >= 75])}")
print(f"  HOLD (50-75): {len(scores_df[(scores_df['score'] >= 50) & (scores_df['score'] < 75)])}")
print(f"  CAUTION (<50): {len(scores_df[scores_df['score'] < 50])}")
```

### Cell 4: Interactive Filters (Hex App Params)

```python
# IMPORTANT: Ces variables deviennent des SÉLECTEURS dans l'App Builder

# Dropdown: Sélectionner un professeur
prof_options = scores_df['prof_name'].unique().tolist()
selected_prof = "François"  # Remplacé par Hex dropdown

# Multi-select: Actifs
actif_options = scores_df['symbol'].unique().tolist()
selected_actifs = ["BTC", "ETH"]  # Remplacé par Hex multi-select

# Slider: Score minimum
min_score = 50  # Remplacé par Hex slider (0-100)

# Date range
date_debut = datetime.now().replace(hour=0, minute=0, second=0)
date_fin = date_debut + timedelta(days=7)

# Filtrer
filtered = scores_df[
    (scores_df['prof_name'] == selected_prof) &
    (scores_df['symbol'].isin(selected_actifs)) &
    (scores_df['score'] >= min_score) &
    (scores_df['date'] >= date_debut) &
    (scores_df['date'] <= date_fin)
].sort_values('score', ascending=False)

print(f"[FILTERED] {len(filtered)} créneaux")
```

### Cell 5: Visualization 1 - Heatmap

```python
# Heatmap: Score par heure et actif
heatmap_pivot = filtered.pivot_table(
    values='score',
    index='heure',
    columns='symbol',
    aggfunc='max'
)

fig_heat = go.Figure(data=go.Heatmap(
    z=heatmap_pivot.values,
    x=heatmap_pivot.columns,
    y=heatmap_pivot.index,
    colorscale='RdYlGn',
    text=np.round(heatmap_pivot.values, 0),
    texttemplate='%{text}',
    textfont={"size": 12},
))

fig_heat.update_layout(
    title="📊 Trading Window Score - Meilleurs créneaux par heure",
    xaxis_title="Cryptomonnaie",
    yaxis_title="Heure du jour",
    height=450,
    width=1000,
    showlegend=False
)

fig_heat.show()
```

### Cell 6: Visualization 2 - Distribution + Timeline

```python
# Bar chart: Catégories
cat_counts = filtered['categorie'].value_counts()
fig_bar = px.bar(
    x=cat_counts.index,
    y=cat_counts.values,
    title="🎯 Distribution des créneaux par type",
    labels={'x': 'Type', 'y': 'Nombre'}
)
fig_bar.show()

# Timeline: Score par jour
timeline = filtered.groupby('jour_semaine')['score'].mean().sort_values(ascending=False)
fig_line = px.bar(
    x=timeline.index,
    y=timeline.values,
    title="📈 Score moyen par jour",
    labels={'x': 'Jour', 'y': 'Score'}
)
fig_line.show()
```

### Cell 7: AI Summary Block

```python
# Préparer le prompt pour l'IA Hex (via bloc "Ask AI" ou Threads)

if len(filtered) > 0:
    top_5 = filtered.nlargest(5, 'score')[['jour_semaine', 'heure_debut', 'symbol', 'score']]
    
    ai_prompt = f"""
Tu es coach trading pour enseignants.

Données de cette semaine pour {selected_prof}:
- {len(filtered)} créneaux analysés
- {len(filtered[filtered['score'] >= 75])} créneaux TRADE recommandés (score > 75)
- Meilleurs créneaux:
{top_5.to_string()}

Rédige un résumé court (150 mots):
1. Résumé de la semaine (bon/mauvais timing?)
2. Top 3 créneaux à ne pas manquer
3. 1 conseil pratique
Style: Bienveillant, pratique, pas de jargon crypto.
    """
    
    print("[AI PROMPT]")
    print(ai_prompt)
else:
    print("[ATTENTION] Aucun créneau trouvé avec ces paramètres")

# Table interactive des résultats
print(filtered[['jour_semaine', 'heure_debut', 'symbol', 'score', 'categorie']].head(10))
```

---

## Phase 3: Convertir en App Hex (APP BUILDER)

### Étape 3.1 : Activer App Builder
1. En haut du notebook, cliquez sur **Share** → **Make it an App**
2. Hex convertira votre notebook en **Data App**

### Étape 3.2 : Ajouter des Composants Interactifs

#### Composant 1: Dropdown (Professeur)
- **Component** → **Select Dropdown**
- **Label**: "Sélectionnez un professeur"
- **Options**: `prof_options` (de la Cell 4)
- **Variable output**: `selected_prof`

#### Composant 2: Multi-Select (Actifs)
- **Component** → **Multi-Select**
- **Label**: "Actifs à analyser"
- **Options**: `actif_options`
- **Variable output**: `selected_actifs`

#### Composant 3: Slider (Score min)
- **Component** → **Numeric Slider**
- **Label**: "Score minimum"
- **Min**: 0, **Max**: 100, **Default**: 50
- **Variable output**: `min_score`

#### Composant 4: Date Range
- **Component** → **Date Picker**
- **Label**: "Semaine"
- **Variable output**: `date_debut`, `date_fin`

### Étape 3.3 : Organiser la mise en page

Ordre recommandé:
```
[HEADER - Titre + description]
[ROW 1] Dropdown Prof + Multi-Select Actifs + Slider Score + Date Range
[ROW 2] Heatmap (pleine largeur)
[ROW 3] Bar chart + Timeline (côte à côte)
[ROW 4] Table des résultats filtrés
[ROW 5] Bloc IA (AI Chat ou Text Output)
```

---

## Phase 4: Ajouter un Bloc IA (Hex Threads ou Ask AI)

### Option A: Hex Threads (Chatbot interactif)
1. **Add Component** → **Threads**
2. Paramètres:
   - **Système**: "Tu es un coach trading pour enseignants"
   - **Context**: Passer `filtered` DataFrame en contexte
   - Laisser l'utilisateur discuter avec l'IA sur les résultats

### Option B: Bloc "Ask AI" statique
1. **Add Component** → **Text Output**
2. Remplir avec le prompt (Cell 7)
3. Appeler l'API LLM (Gemini/Claude) via Hex
4. Afficher le résumé généré

---

## Phase 5: Test + Démo

### Tester en mode App
1. Cliquez **Run App** en haut
2. Interagir avec les sélecteurs
3. Vérifier que les charts se mettent à jour
4. Tester le bloc IA

### Enregistrer une Démo Video (<3 min)
**Script de la démo:**

```
[INTRO - 10sec]
"Bonjour! Aujourd'hui on explore comment utiliser Hex 
pour trouver les meilleurs créneaux de trading quand on est enseignant."

[DÉMO 1 - 30sec]
"Voici nos données: emploi du temps réaliste + données MEXC live"
→ Montrer la heatmap
"On voit les meilleurs créneaux en vert: jeudi 10-12 pour ETH"

[DÉMO 2 - 30sec]
"Maintenat je change les paramètres - sélectionner BTC seulement"
→ Changer le multi-select
"Les résultats se mettent à jour instantanément"
→ Montrer la distribution bar chart

[DÉMO 3 - 20sec]
"Et voici l'IA qui résume ma semaine:"
→ Montrer le prompt IA
"Elle me dit: 'Les mercredis sont excellents pour trader, mais tes classes démarrent tôt'"

[OUTRO - 10sec]
"Cette app résout un vrai problème: combiner données réelles + IA pour prendre de meilleures décisions"
→ Cliquer "Partager"
```

### Commande pour enregistrer (OBS ou autre):
- Resolution: 1920x1080
- FPS: 30
- Codec: H.264
- Durée: 2min-3min max
- Format: MP4

---

## Phase 6: Soumettre sur Devpost

### Éléments à préparer:

#### 1. Project Overview (texte)
```
TITRE: School & Crypto Timing: Finding Your Trading Window

DESCRIPTION (150 mots):

Side-traders (teachers, freelancers) fail because they try to trade 
at the wrong times. This Hex project solves it.

Using live MEXC data (volatility, liquidations, funding rates) + 
realistic teacher schedules, it calculates a "Trading Window Score" 
for each hour of the week.

The app:
- Shows best trading slots via interactive heatmap
- Filters by crypto asset + score threshold
- Provides AI-generated daily summaries
- Uses semantic modeling (Hex) to connect education data + crypto

Result: Teachers can now trade 2h/day and actually profit, 
not burn out or make emotional decisions.

Built with Hex (notebook + app + AI), MEXC API, SQLite.
```

#### 2. Public Hex Project Link
- Faire "Publish" dans Hex
- Copier le lien public
- Format: `https://app.hex.tech/share/...-XXXXX`

#### 3. Demo Video Link
- Upload sur YouTube (non-listée ou publique)
- Copier le lien

#### 4. Code Repository (Optional but good)
- Push sur GitHub (optionnel)
- Inclure: `etl.py`, `scoring.py`, `schema.sql`, `README.md`

#### 5. Devpost Submission Form
```
Project Name: School & Crypto Timing
Description: [voir ci-dessus]
Hex Project URL: [lien public]
Demo Video URL: [YouTube]
GitHub (optional): [repo]
```

---

## ✅ CHECKLIST FINALE

- [ ] Cell 1: Imports OK
- [ ] Cell 2: Data loaded + 5 tables visibles
- [ ] Cell 3: DataFrames enrichis (score_to_category fonctionne)
- [ ] Cell 4: Filtres actifs (selected_prof, selected_actifs, etc.)
- [ ] Cell 5: Heatmap affiche les données
- [ ] Cell 6: Bar + Line charts OK
- [ ] Cell 7: AI Prompt généré sans erreur
- [ ] App Builder: Dropdwon + Multi-select + Slider actifs
- [ ] Interactivité: Changer params → charts se mettent à jour
- [ ] Test vidéo: 2-3 min, démo fluide
- [ ] GitHub push: Code public
- [ ] Devpost: Soumis

---

## 🚀 COMMANDES RAPIDES

```bash
# Vérifier la DB avant d'uploader
sqlite3 hackaton.db ".tables"
sqlite3 hackaton.db "SELECT COUNT(*) FROM trading_window_scores;"

# Vérifier les scripts locaux
python python/query_db.py stats

# Export pour Hex
sqlite3 hackaton.db ".dump" > backup_before_hex.sql
```

---

## 📞 SUPPORT

Si erreur dans Hex:
- Vérifier l'encoding UTF-8 de la DB
- Checker que pandas/plotly sont dispo dans Hex
- Si Hex refuse la DB: exporter en CSV et charger
- Si bug IA: tester le prompt manuellement dans Gemini/Claude first

---

**Vous êtes à 80% du finish line! 🎉**

Prochaine étape: Me montrer que la Cell 2 charge les data correctement, puis on fine-tune les visualizations.
