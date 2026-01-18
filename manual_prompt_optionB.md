# 🔥 OPTION B - PROMPT MANUEL SUPER RAPIDE (95 min)

**START**: 01:28 CET
**END**: 02:45 CET
**STATUS**: Pas de pause, pas de questions, juste du travail!

---

# ⚡ AVANT DE COMMENCER - PRÉPAREZ:

## Fichiers à avoir ouverts:

```
1. Hex.tech dans le navigateur
2. notepad: C:\Users\franc\OneDrive\Documents\hackaton\hex_cells_ready.py
3. PowerShell (optionnel, juste pour vérifier)
```

## Contrainte:
- **Ne fermez JAMAIS l'onglet Hex.tech**
- **Copie-colle directement du prompt**
- **Cliquez là où je dis de cliquer**
- **Pas de modification du code**

---

# 🎯 PHASE 2: HEX ACCOUNT SETUP (7 min)

## ÉTAPE 2.1: Ouvrir Hex.tech

```
Action: Ouvrez navigateur → https://app.hex.tech
```

**Vous voyez**: Page Hex avec bouton "Sign Up"

---

## ÉTAPE 2.2: Sign Up

```
Action 1: Click "Sign up" (haut droit)
Action 2: Click "Google" (ou email si vous préférez)
```

**Vous voyez**: Fenêtre Google login

---

## ÉTAPE 2.3: Authentifier avec Google

```
Action 1: Remplissez votre email Google
Action 2: Click "Next"
Action 3: Remplissez votre password
Action 4: Click "Next"
Action 5: Attendre 2 secondes
```

**Vous voyez**: Retour à Hex, vous êtes loggé ✅

---

## ÉTAPE 2.4: Créer Workspace

```
Action 1: Click "Create workspace"
Action 2: Entrez: hackaton-2026
Action 3: Click "Create"
Action 4: Attendre 3 secondes
```

**Vous voyez**: Dashboard Hex avec workspace "hackaton-2026" ✅

---

## ÉTAPE 2.5: Créer Nouveau Projet

```
Action 1: Click "New Project"
Action 2: Sélectionnez "SQL + Python Notebook"
Action 3: Project name: School & Crypto Timing
Action 4: Click "Create"
Action 5: Attendre 5 secondes
```

**Vous voyez**: Éditeur Hex complètement vide (blanc) ✅

**⏱️ PHASE 2 COMPLÉTÉE: 01:35 CET**

---

# 📊 PHASE 3: UPLOAD DATABASE (10 min)

## ÉTAPE 3.1: Ouvrir Data Panel

```
Action 1: Click "Data" (en haut à gauche)
Action 2: Attendre 1 seconde
```

**Vous voyez**: Panneau "Data" avec option "+ Add data"

---

## ÉTAPE 3.2: Upload hackaton.db

```
Action 1: Click "+ Add data"
Action 2: Click "Upload file"
Action 3: Sélectionnez: C:\Users\franc\OneDrive\Documents\hackaton\hackaton.db
Action 4: Attendre 3-4 minutes (la barre de progression disparaît)
```

**Vous voyez**: hackaton.db apparaît dans la liste Data ✅

---

## ÉTAPE 3.3: Test SQL (vérification)

```
Action 1: Click "+ SQL" (ajouter SQL cell)
Action 2: Dans la textarea, copie-colle EXACTEMENT:

SELECT COUNT(*) as total FROM trading_window_scores;

Action 3: Click "Run" (bouton bleu)
Action 4: Attendre 2 secondes
```

**Vous voyez**: Résultat = **180** ✅

Si vous voyez autre chose → STOP et dites-moi!

**⏱️ PHASE 3 COMPLÉTÉE: 01:45 CET**

---

# 💻 PHASE 4: CREATE 7 CELLS (50 min)

**IMPORTANT: Ouvrez hex_cells_ready.py dans notepad pour copier le code**

```powershell
notepad "C:\Users\franc\OneDrive\Documents\hackaton\hex_cells_ready.py"
```

---

## CELL 1: IMPORTS (2 min)

```
Action 1: Click "+ Python" (ajouter Python cell)
Action 2: Copie le code ci-dessous EXACTEMENT:

---COPIE-COLLE CECI---

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

print("[INFO] School & Crypto Timing v1.0")
print("=" * 60)

---FIN---

Action 3: Click "Run"
Action 4: Attendre 2 secondes
```

**Vous voyez**: 
```
[INFO] School & Crypto Timing v1.0
============================================================
```

✅ Cell 1 FINI

---

## CELL 2: LOAD DATA (2 min)

```
Action 1: Click "+ SQL" (ajouter SQL cell)
Action 2: Copie le code ci-dessous EXACTEMENT:

---COPIE-COLLE CECI---

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

---FIN---

Action 3: Click "Run"
Action 4: Attendre 3 secondes
```

**Vous voyez**: Table avec ~100 lignes (id, date, score, symbol, etc.) ✅

Cell 2 FINI

---

## CELL 3: PREPARE DATAFRAME (3 min)

```
Action 1: Click "+ Python"
Action 2: Copie le code ci-dessous EXACTEMENT:

---COPIE-COLLE CECI---

scores_df = sql_result.copy() if 'sql_result' in dir() else pd.DataFrame()

scores_df['date'] = pd.to_datetime(scores_df['date'])
scores_df['jour_semaine'] = scores_df['date'].dt.day_name()
scores_df['heure'] = scores_df['heure_debut'].str.split(':').str[0].astype(int)

def score_to_category(score):
    if score >= 75: return "TRADE"
    elif score >= 50: return "HOLD"
    else: return "CAUTION"

scores_df['categorie'] = scores_df['score'].apply(score_to_category)

print("[STATS]")
print(f"TRADE (>75): {len(scores_df[scores_df['score'] >= 75])}")
print(f"HOLD (50-75): {len(scores_df[(scores_df['score'] >= 50) & (scores_df['score'] < 75)])}")
print(f"CAUTION (<50): {len(scores_df[scores_df['score'] < 50])}")
print(f"Total: {len(scores_df)}")

---FIN---

Action 3: Click "Run"
Action 4: Attendre 2 secondes
```

**Vous voyez**:
```
[STATS]
TRADE (>75): XX
HOLD (50-75): YY
CAUTION (<50): ZZ
Total: 100
```

✅ Cell 3 FINI

---

## CELL 4: FILTERS (3 min)

```
Action 1: Click "+ Python"
Action 2: Copie le code ci-dessous EXACTEMENT:

---COPIE-COLLE CECI---

prof_options = sorted(scores_df['prof_name'].unique().tolist())
actif_options = sorted(scores_df['symbol'].unique().tolist())

selected_prof = "Francois"
selected_actifs = ["BTC", "ETH"]
min_score = 50

date_debut = scores_df['date'].min()
date_fin = scores_df['date'].max()

filtered = scores_df[
    (scores_df['prof_name'] == selected_prof) &
    (scores_df['symbol'].isin(selected_actifs)) &
    (scores_df['score'] >= min_score) &
    (scores_df['date'] >= date_debut) &
    (scores_df['date'] <= date_fin)
].sort_values('score', ascending=False)

print(f"[FILTERED] {len(filtered)} windows")
print(filtered[['jour_semaine', 'heure_debut', 'symbol', 'score', 'categorie']].head(10).to_string())

---FIN---

Action 3: Click "Run"
Action 4: Attendre 2 secondes
```

**Vous voyez**:
```
[FILTERED] 45 windows
   jour_semaine heure_debut symbol score categorie
0      Thursday       10:00    ETH     89     TRADE
1      Wednesday       14:00    BTC     85     TRADE
...
```

✅ Cell 4 FINI

---

## CELL 5: HEATMAP (12 min)

```
Action 1: Click "+ Python"
Action 2: Copie le code ci-dessous EXACTEMENT:

---COPIE-COLLE CECI---

heatmap_pivot = filtered.pivot_table(
    values='score',
    index='heure',
    columns='symbol',
    aggfunc='max',
    fill_value=0
)

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

---FIN---

Action 3: Click "Run"
Action 4: Attendre 5 secondes
```

**Vous voyez**: 
- Une heatmap colorée (vert = bon score, rouge = mauvais)
- Heures sur Y, assets (BTC, ETH, SOL) sur X
- Nombres au centre de chaque case

✅ Cell 5 FINI - C'EST LA PLUS BELLE! 🎨

---

## CELL 6: CHARTS (12 min)

```
Action 1: Click "+ Python"
Action 2: Copie le code ci-dessous EXACTEMENT:

---COPIE-COLLE CECI---

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

---FIN---

Action 3: Click "Run"
Action 4: Attendre 5 secondes
```

**Vous voyez**:
- Chart 1: Bar chart avec TRADE (vert), HOLD (orange), CAUTION (rouge)
- Chart 2: Line chart montrant average score par jour (Monday-Sunday)

✅ Cell 6 FINI

---

## CELL 7: AI SUMMARY (5 min)

```
Action 1: Click "+ Python"
Action 2: Copie le code ci-dessous EXACTEMENT:

---COPIE-COLLE CECI---

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
Focus on {best_day.lower()} from {best_hour}h. Avoid red zones!
    """
    print(ai_text)

---FIN---

Action 3: Click "Run"
Action 4: Attendre 3 secondes
```

**Vous voyez**: Rapport IA généré avec recommendations

✅ Cell 7 FINI - TOUTES LES 7 CELLS FAITES! 🎉

**⏱️ PHASE 4 COMPLÉTÉE: 02:10 CET**

---

# 🚀 PHASE 5: PUBLISH APP (25 min)

## ÉTAPE 5.1: Convertir en App

```
Action 1: Click "Share" (coin haut droit de Hex)
Action 2: Click "Make it an App"
Action 3: Attendre 3 secondes (Hex transforme le notebook)
```

**Vous voyez**: Interface change, tous les Cells s'affichent ensemble ✅

---

## ÉTAPE 5.2: Tester l'App

```
Action 1: Scroller vers le bas (vérifier que tout s'affiche)
Action 2: Voir la heatmap interactive
Action 3: Voir les 2 charts
Action 4: Voir le rapport IA
Action 5: Attendre 5 secondes
```

**Vous voyez**: Tout fonctionne ✅

---

## ÉTAPE 5.3: Publier l'App

```
Action 1: Click "Share" (haut droit)
Action 2: Click "Publish as Public App" (ou similaire)
Action 3: Attendre 5-10 secondes
```

**Vous voyez**: Message "Published" ou lien public apparaît ✅

---

## ÉTAPE 5.4: Copier le Lien Public

```
Action 1: Vous voyez un lien: https://app.hex.tech/share/xxxxx
Action 2: Copie-colle ce lien dans Notepad
Action 3: Sauvegardez dans: C:\Users\franc\OneDrive\Documents\hackaton\HEX_APP_LINK.txt
```

**Vous avez**: Le lien de votre app publique ✅

---

## ÉTAPE 5.5: Screenshots (optionnel mais recommandé)

```
Si vous avez du temps:

Action 1: Prenez une screenshot de la heatmap (Print Screen)
Action 2: Collez dans Paint et sauvegardez
Action 3: Faites pareil pour les charts

Ces screenshots seront utiles pour Devpost demain!
```

**⏱️ PHASE 5 COMPLÉTÉE: 02:35 CET**

---

# ✅ VOUS AVEZ TERMINÉ!

```
Phase 1 (Git):      ✅ COMPLÉTÉE (01:14)
Phase 2 (Hex):      ✅ COMPLÉTÉE (01:35)
Phase 3 (Database): ✅ COMPLÉTÉE (01:45)
Phase 4 (7 Cells):  ✅ COMPLÉTÉE (02:10)
Phase 5 (Publish):  ✅ COMPLÉTÉE (02:35)

TOTAL: Fini avant 02:45 CET! 🎉
```

---

# 📋 DEMAIN MATIN (LUNDI 09:00)

```
1. Enregistrer vidéo démo (60 min)
   - Ouvrez votre Hex app (lien sauvegardé)
   - Enregistrez avec OBS
   - Montrez heatmap + charts + AI

2. Upload YouTube (30 min)
   - Title: "School & Crypto Timing - Hex Hackathon 2026"
   - Description: Lien GitHub + features

3. Soumettre Devpost (30 min)
   - Title + Description
   - Link to GitHub
   - Link to Hex app
   - Screenshots + video
   - SUBMIT!
```

---

# 🚀 VOUS ÊTES PRÊT?

**DITES-MOI "PRÊT" et je vous donne ÉTAPE 2.1 pour commencer!**

Ou si vous avez des questions avant de lancer → posez-les!

Sinon → **ALLEZ-Y! HEXTECH MAINTENANT!** 💪🔥
