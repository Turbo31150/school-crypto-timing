# EXECUTION FINALE - HACKATHON HEX 2026
## Consensus Multi-IA: PASS 100/100
## Date: 2026-01-18

---

## STATUT VALIDATION

| IA | Role | Status | Score |
|----|------|--------|-------|
| LM Studio 1 (qwen3-30b) | Git Commands | READY | 100% |
| LM Studio 3 (mistral) | Code Validation | PASS | 100/100 |
| Gemini | Hex Review | READY | - |
| Claude Code (Opus 4.5) | Orchestration | ACTIVE | - |
| System Status | All Services | ONLINE | - |

**CONSENSUS: 4/4 READY - PROCEED**

---

## PHASE 1: GIT + GITHUB (10 min)

### Commandes PowerShell (copier-coller)

```powershell
# 1. Aller dans le dossier projet
cd "C:\Users\franc\OneDrive\Documents\hackaton"

# 2. Verifier Git installe
git --version

# 3. Configurer utilisateur (remplacer par vos infos)
git config user.name "Francois"
git config user.email "votre@email.com"

# 4. Initialiser repo (si pas deja fait)
if (-not (Test-Path .git)) { git init }

# 5. Ajouter tous les fichiers
git add .

# 6. Commit
git commit -m "Hackathon Hex 2026: School & Crypto Timing - Complete infrastructure"

# 7. Creer branche main
git branch -M main

# 8. Ajouter remote (REMPLACER YOUR_USERNAME)
$repoUrl = "https://github.com/YOUR_USERNAME/school-crypto-timing.git"

# Verifier si remote existe
$remotes = git remote
if ($remotes -contains "origin") {
    git remote set-url origin $repoUrl
} else {
    git remote add origin $repoUrl
}

# 9. Push (vous aurez besoin d'un token GitHub)
git push -u origin main
```

### Si erreur d'authentification:
1. Aller sur https://github.com/settings/tokens
2. Generer un token (cocher repo)
3. Utiliser le token comme mot de passe lors du push

---

## PHASE 2: HEX NOTEBOOK (45 min)

### Etape 2.1: Creer projet Hex
1. Aller sur https://app.hex.tech
2. New Project > SQL + Python Notebook
3. Nommer: "School & Crypto Timing"

### Etape 2.2: Uploader hackaton.db
1. Data > Add data > Upload file
2. Selectionner: `C:\Users\franc\OneDrive\Documents\hackaton\hackaton.db`
3. Tester avec SQL Cell:
```sql
SELECT COUNT(*) FROM trading_window_scores;
-- Expected: 90
```

### Etape 2.3: Copier les 7 Cells

**CELL 1 - Imports** (Python Cell):
```python
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

COLORS = {'TRADE': '#27ae60', 'WATCH': '#f39c12', 'HOLD': '#3498db', 'AVOID': '#e74c3c'}
print(f"[OK] Setup complete - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
```

**CELL 2 - Load Data** (SQL Cell):
```sql
SELECT
    ts.id, ts.prof_id, ts.date, ts.heure_debut, ts.heure_fin,
    ts.score, ts.recommendation, ts.raison,
    ts.volatility_component, ts.availability_component, ts.market_component,
    ca.symbol, ca.nom as crypto_name,
    p.name as prof_name
FROM trading_window_scores ts
LEFT JOIN crypto_actifs ca ON ts.actif_id = ca.id
LEFT JOIN professeurs p ON ts.prof_id = p.id
ORDER BY ts.score DESC
```
Output variable: `df_scores`

**CELL 3 - Preprocessing** (Python Cell):
```python
# Ordre des jours
jour_order = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

# Si 'date' existe, extraire le jour
if 'date' in df_scores.columns:
    df_scores['date'] = pd.to_datetime(df_scores['date'])
    df_scores['jour'] = df_scores['date'].dt.day_name()
    jour_map = {'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
                'Thursday': 'Jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi', 'Sunday': 'Dimanche'}
    df_scores['jour'] = df_scores['jour'].map(jour_map)

# Extraire heure numerique
if 'heure_debut' in df_scores.columns:
    df_scores['heure_num'] = df_scores['heure_debut'].apply(
        lambda x: int(str(x).split(':')[0]) if pd.notna(x) else 0
    )

# Categoriser scores
def categorize(score):
    if score >= 75: return 'TRADE'
    elif score >= 55: return 'WATCH'
    elif score >= 35: return 'HOLD'
    else: return 'AVOID'

df_scores['category'] = df_scores['score'].apply(categorize)
df_scores['color'] = df_scores['category'].map(COLORS)

print(f"[OK] {len(df_scores)} scores preprocesses")
print(f"    TRADE: {len(df_scores[df_scores['category']=='TRADE'])}")
print(f"    WATCH: {len(df_scores[df_scores['category']=='WATCH'])}")
```

**CELL 4 - Stats KPIs** (Python Cell):
```python
# KPIs
score_moyen = round(df_scores['score'].mean(), 1)
score_max = df_scores['score'].max()
creneaux_trade = len(df_scores[df_scores['category'] == 'TRADE'])
meilleur_creneau = df_scores.iloc[0] if len(df_scores) > 0 else None

print(f"=== STATS GLOBALES ===")
print(f"Score moyen: {score_moyen}/100")
print(f"Score max: {score_max}")
print(f"Creneaux TRADE: {creneaux_trade}")
if meilleur_creneau is not None:
    print(f"Meilleur: {meilleur_creneau.get('jour', 'N/A')} {meilleur_creneau.get('heure_debut', '')} - {meilleur_creneau.get('symbol', '')} (Score {meilleur_creneau['score']})")
```

**CELL 5 - Heatmap** (Python Cell):
```python
# Pivot pour heatmap
if 'jour' in df_scores.columns and 'heure_num' in df_scores.columns:
    pivot = df_scores.pivot_table(
        values='score',
        index='heure_num',
        columns='jour',
        aggfunc='mean'
    )

    # Reordonner colonnes
    cols_order = [j for j in jour_order if j in pivot.columns]
    if cols_order:
        pivot = pivot[cols_order]

    fig_heatmap = px.imshow(
        pivot,
        labels=dict(x="Jour", y="Heure", color="Score"),
        color_continuous_scale='RdYlGn',
        aspect='auto',
        title='Trading Window Scores par Jour et Heure'
    )
    fig_heatmap.update_layout(height=500)
    fig_heatmap
else:
    print("Colonnes jour/heure non disponibles pour heatmap")
```

**CELL 6 - Top Creneaux Chart** (Python Cell):
```python
# Top 10 creneaux
top10 = df_scores.nlargest(10, 'score').copy()

if 'jour' in top10.columns and 'heure_debut' in top10.columns:
    top10['label'] = top10['jour'].astype(str) + ' ' + top10['heure_debut'].astype(str)
    if 'symbol' in top10.columns:
        top10['label'] = top10['label'] + ' (' + top10['symbol'].astype(str) + ')'

    fig_top = px.bar(
        top10,
        x='label',
        y='score',
        color='category',
        color_discrete_map=COLORS,
        title='Top 10 Creneaux de Trading'
    )
    fig_top.add_hline(y=75, line_dash="dash", line_color="green", annotation_text="Seuil TRADE")
    fig_top.update_layout(xaxis_tickangle=-45, height=400)
    fig_top
else:
    print("Donnees insuffisantes pour le chart")
```

**CELL 7 - IA Prompt** (Python Cell):
```python
# Generer prompt pour IA
top5 = df_scores.nlargest(5, 'score')

prompt = f"""Analyse les creneaux de trading pour Francois cette semaine:

RESUME:
- Score moyen: {score_moyen}/100
- Creneaux TRADE recommandes: {creneaux_trade}
- Total creneaux analyses: {len(df_scores)}

TOP 5 CRENEAUX:
"""

for _, row in top5.iterrows():
    jour = row.get('jour', 'N/A')
    heure = row.get('heure_debut', 'N/A')
    symbol = row.get('symbol', 'N/A')
    score = row['score']
    cat = row.get('category', 'N/A')
    prompt += f"- {jour} {heure}: {symbol} Score={score} ({cat})\n"

prompt += """
Donne une recommandation personnalisee en 3 phrases:
1. Quel est le meilleur moment pour trader?
2. Quelle crypto privilegier?
3. Un conseil pratique?
"""

print("=== PROMPT POUR IA ===")
print(prompt)
```

---

## PHASE 3: APP BUILDER (15 min)

### Etape 3.1: Activer App Mode
1. Cliquer "Share" > "Make it an App"

### Etape 3.2: Ajouter Composants
- Dropdown: Professeur
- Multi-select: Cryptos (BTC, ETH, SOL)
- Slider: Score minimum (0-100, default 50)

### Etape 3.3: Layout
```
[TITRE]
[Dropdown | Multi-select | Slider]
[HEATMAP - full width]
[TOP 10 CHART]
[IA PROMPT]
```

### Etape 3.4: Publier
1. Run App > Test interactivite
2. Share > Publish as Public
3. Copier URL: https://app.hex.tech/share/...

---

## PHASE 4: VIDEO (Lundi 09:00)

### OBS Config
- Resolution: 1920x1080
- FPS: 30
- Format: MP4
- Encoder: x264

### Script Video (2-3 min)
```
[0:00-0:10] "Bonjour! Je presente School & Crypto Timing"
[0:10-0:40] Montrer la heatmap, expliquer les couleurs
[0:40-1:20] Changer les filtres, montrer interactivite
[1:20-1:50] Montrer le prompt IA
[1:50-2:10] "Built avec Hex, MEXC API, SQLite. Merci!"
```

---

## PHASE 5: DEVPOST (Lundi 14:00)

### URL: https://hex-a-thon.devpost.com

### Champs a remplir:
- Project Name: School & Crypto Timing
- Tagline: Data-driven trading windows for teacher-traders
- Hex URL: [votre lien]
- Video URL: [YouTube]
- GitHub: [votre repo]
- Category: Wildcard

---

## CHECKLIST FINALE

### Dimanche soir:
- [ ] Git push OK
- [ ] Hex Notebook 7 Cells OK
- [ ] App publique + lien copie
- [ ] OBS installe + teste

### Lundi:
- [ ] Video enregistree (2-3 min)
- [ ] YouTube upload
- [ ] Devpost soumis

---

## COMMANDES DE VERIFICATION

```powershell
# Verifier DB
cd "C:\Users\franc\OneDrive\Documents\hackaton"
sqlite3 hackaton.db "SELECT COUNT(*) FROM trading_window_scores;"
# Expected: 90

# Verifier scripts
python python/query_db.py stats
# Expected: 9 scripts, 2887 lignes

# Test pipeline
python run.py --test
```

---

## SUPPORT

Si erreur:
1. Verifier les imports (pandas, plotly)
2. Verifier hackaton.db est uploade
3. Verifier les noms de colonnes (SELECT * LIMIT 5)

**CONSENSUS MULTI-IA: READY - EXECUTE NOW!**
