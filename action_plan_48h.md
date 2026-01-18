# 📅 PLAN D'ACTION HACKATHON HEX - 48H CHRONO

**DEADLINE**: Lundi 20 Janvier 2026, 23:59 UTC (Devpost)
**Aujourd'hui**: Dimanche 18 Janvier, 00:36 CET
**Temps disponible**: ~67 heures

---

## DIMANCHE 18 JANVIER - PRÉPARATION

### 09:00-10:00 | SETUP LOCAL
```bash
# Terminal / PowerShell
cd C:\Users\franc\OneDrive\Documents\hackaton

# Vérifier la DB
sqlite3 hackaton.db ".tables"
# Expected: 17 tables

sqlite3 hackaton.db "SELECT COUNT(*) FROM trading_window_scores;"
# Expected: 90 (90 scores calculés)

# Vérifier les fichiers
python python/query_db.py stats
# Expected: 8 scripts, 2,286 lignes
```

**Durée**: 10 min  
**Livrable**: Screenshot du terminal montrant les stats ✅

---

### 10:00-11:00 | CRÉER COMPTE HEX + GITHUB

#### A. Créer compte Hex (5 min)
1. Allez sur https://app.hex.tech
2. Sign up (email ou Google)
3. Créez un **New Workspace** nommé: `hackaton-2026`

#### B. Créer repo GitHub (5 min)
1. https://github.com/new
2. Repository name: `school-crypto-timing`
3. Description: `"School & Crypto Timing - Hackathon Hex 2026"`
4. Public
5. Add README.md + .gitignore (Python template)

#### C. Push code vers GitHub (15 min)
```bash
cd C:\Users\franc\OneDrive\Documents\hackaton

# Initialiser git (si pas déjà fait)
git init
git add .
git commit -m "Initial commit: hackaton hex project setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/school-crypto-timing.git
git push -u origin main
```

**Durée**: 25 min  
**Livrables**: 
- ✅ Compte Hex créé
- ✅ Repo GitHub public avec code poussé

---

### 11:00-12:00 | INSTALLER OBS + TEST ENREGISTREMENT

#### A. Télécharger & installer OBS (10 min)
1. https://obsproject.com/download
2. Installer (Windows version)
3. Lancer OBS

#### B. Configurer OBS (15 min)
**Settings**:
- **Output** → **Recording**
  - Recording Path: `C:\Users\franc\Videos\`
  - Format: MP4
  - Encoder: NVIDIA NVENC H.264 (ou x264 si pas NVIDIA)
  - Bitrate: 8000 kbps (qualité haute)
  - Audio Bitrate: 320 kbps

- **Video**
  - Base Canvas Resolution: 1920x1080
  - Output (Scaled) Resolution: 1920x1080
  - FPS Common Values: 30

#### C. Créer une Scene (5 min)
1. **Scene** → **+** → Nommez: "Hex Demo"
2. **Sources** → **+** → **Display Capture** (pour capturer Hex)
3. Test: Record 10 sec, vérifier qualité vidéo

**Durée**: 30 min  
**Livrable**: ✅ OBS configuré et testé

---

### 12:00-13:00 | PAUSE & LUNCH

---

### 13:00-15:00 | CRÉER PROJET HEX + UPLOADER DATA

#### A. Créer nouveau Hex Project (5 min)
1. https://app.hex.tech → **New Project**
2. Sélectionnez **SQL + Python Notebook**
3. Nommez: `School & Crypto Timing`
4. Description: `Analyser les meilleurs créneaux de trading pour un enseignant via données MEXC + Hex AI`

#### B. Uploader hackaton.db comme Data Source (10 min)
1. En haut à gauche → **Data** → **+Add data**
2. **Upload file** → Sélectionnez `hackaton.db`
3. Hex reconnaît SQLite automatiquement
4. Testez: **New SQL cell** et exécutez:
```sql
SELECT COUNT(*) as total_scores FROM trading_window_scores;
```
Expected result: 90

#### C. Construire les 7 Cells (60 min) - COPIE-COLLE du `hex_notebook.py`

**Cell 1: Imports** (2 min)
```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

TIMEZONE = "Europe/Paris"
print("[INFO] School & Crypto Timing v1.0")
```

**Cell 2: Load Data** (3 min)
```python
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

**Cell 3: Prepare DataFrames** (5 min)
[Copier depuis hex_notebook.py - section "PREPARE DATAFRAMES"]

**Cell 4: Filters** (5 min)
[Copier depuis hex_notebook.py - section "INTERACTIVE FILTERS"]

**Cell 5: Heatmap** (5 min)
[Copier depuis hex_notebook.py - section "VISUALIZATION 1"]

**Cell 6: Charts** (5 min)
[Copier depuis hex_notebook.py - section "VISUALIZATION 2"]

**Cell 7: IA Prompt** (5 min)
[Copier depuis hex_notebook.py - section "AI SUMMARY"]

**Test** (15 min):
- Lancer chaque cell
- Vérifier qu'il n'y a PAS d'erreur
- Screenshot de la heatmap

**Durée**: 120 min (2h)  
**Livrables**:
- ✅ Hex Project créé
- ✅ hackaton.db uploadé
- ✅ 7 Cells fonctionnels
- ✅ Heatmap affichée (screenshot)

---

### 15:00-16:00 | CONVERTIR EN APP HEX

#### A. Activer App Builder (2 min)
1. En haut → **Share** → **Make it an App**
2. Hex transforme automatiquement le notebook

#### B. Ajouter Composants Interactifs (30 min)

**Component 1: Dropdown (Prof)**
- **+Component** → **Select Dropdown**
- Label: "Sélectionnez un professeur"
- Options: `prof_options` (depuis Cell 4)
- Output variable: `selected_prof`

**Component 2: Multi-Select (Actifs)**
- **+Component** → **Multi-Select**
- Label: "Actifs à analyser"
- Options: `actif_options`
- Output variable: `selected_actifs`

**Component 3: Slider (Score min)**
- **+Component** → **Numeric Slider**
- Label: "Score minimum"
- Min: 0, Max: 100, Default: 50
- Output variable: `min_score`

**Component 4: Date Range Picker**
- **+Component** → **Date Picker**
- Label: "Semaine"
- Output: `date_debut`, `date_fin`

#### C. Organiser Layout (10 min)
Order:
```
[TITLE: "School & Crypto Timing"]
[DESCRIPTION: "Trouvez vos meilleurs créneaux de trading"]
[ROW 1] Dropdown + Multi-Select + Slider + Date Picker (en ligne)
[ROW 2] Heatmap (100% width)
[ROW 3] Bar chart | Timeline (50% / 50%)
[ROW 4] Table filtrée
[ROW 5] AI Prompt (text output)
```

#### D. Test App (10 min)
1. Click **Run App**
2. Changer dropdown → verify heatmap se met à jour
3. Changer slider → verify bar chart change
4. Changer multi-select → verify new data appears

**Durée**: 60 min (1h)  
**Livrables**:
- ✅ App Hex fonctionnelle
- ✅ 4 composants interactifs
- ✅ Test interactivité OK

---

### 16:00-17:00 | FINITION + TEST COMPLET

- [ ] Vérifier pas d'erreurs dans les Cells
- [ ] Tester tous les sélecteurs (dropdown, multi-select, slider)
- [ ] Vérifier la heatmap affiche bien les données
- [ ] Vérifier les colors: rouge/jaune/vert selon score
- [ ] Tester sur mobile (Hex app responsive)
- [ ] Publish: Click **Share** → **Publish as Public App**
- [ ] Copier le lien public: `https://app.hex.tech/share/...`

**Durée**: 60 min (1h)  
**Livrable**: ✅ App Hex publique + lien copié

---

### 17:00-23:00 | FREE TIME (repos avant la démo demain)

---

## LUNDI 19 JANVIER - DÉMO VIDEO + SOUMISSION

### 09:00-10:00 | ENREGISTRER DÉMO VIDEO

**Script (à lire à voix haute pendant l'enregistrement):**

```
[INTRO - 10 sec]
"Bonjour! Je suis François, enseignant en Occitanie et trader crypto en même temps.

Le problème: comment trader quand on a une classe à 9h, des réunions à 11h, 
et une famille qui compte sur toi? 

Aujourd'hui je vous montre comment j'ai résolu ça avec Hex."

[TRANSITION - 5 sec]
"Voici mon app: School & Crypto Timing"

[DÉMO 1: Heatmap - 30 sec]
"Cette heatmap montre les meilleurs créneaux pour trader BTC et ETH cette semaine.

Les zones vertes = créneaux TRADE (score > 75)
Les zones jaunes = HOLD (score 50-75)
Les rouges = CAUTION (score < 50)

Par exemple: jeudi de 10h à 12h, j'ai un créneau vert pour ETH. 
C'est APRÈS ma classe qui finit à 10h, AVANT ma réunion à 14h. Parfait."

[DÉMO 2: Interaction - 30 sec]
"Maintenant je change mes paramètres. Je sélectionne SEULEMENT BTC:"

→ Cliquez sur Multi-Select → Désélectionnez ETH → Keep BTC only

"Et voilà! Les données se mettent à jour en temps réel. 

Maintenant je vois les créneaux BTC. Intéressant: les lundis et mercredis sont meilleurs pour BTC."

[DÉMO 3: Distribution - 20 sec]
"Voici un résumé: sur 90 créneaux analysés cette semaine,
- 24 sont TRADE (vert) - où je devrais vraiment trader
- 35 sont HOLD (jaune) - où je peux attendre
- 31 sont CAUTION (rouge) - où je dois absolument éviter (classe, réunion, fatigue)

Et voici la timeline par jour. Les jeudis sont les meilleurs jours pour moi."

[DÉMO 4: AI Summary - 15 sec]
"Et maintenant, ma IA coach:

[Montrer le texte du prompt IA]

'François, cette semaine est excellente pour toi:
- Jeudi 10h-12h ETH est ton meilleur créneau (score 89)
- Les lundis sont bons pour BTC (score 71+)
- Évite absolument les mardis: classe 9h, volatilité forte'

L'IA comprend MES données (mon emploi du temps) + les données MEXC (volatilité, funding).
Pas juste des stats - c'est personnalisé pour MOI."

[OUTRO - 10 sec]
"C'est ça que Hex peut faire: combiner tes données perso, des APIs externes, 
et l'IA pour prendre des décisions smart.

Pas de plus de trading émotionnel. Juste du timing data-driven.

Merci!"

[FINAL - 5 sec]
Cliquez sur "Share" pour montrer que c'est public.
```

**Procédure d'enregistrement:**

1. Lancez OBS
2. Allez sur votre app Hex (https://app.hex.tech/share/...)
3. Click **Record** dans OBS
4. Lisez le script (lentement, naturellement)
5. Montrez chaque élement au fur et à mesure
6. Click **Stop Recording** dans OBS
7. Vidéo sauvegardée dans `C:\Users\franc\Videos\`

**Durée**: 60 min (avec prises multiples si besoin)  
**Format final**: 2-3 min, MP4, 1920x1080@30fps  
**Livrable**: ✅ Fichier video.mp4

---

### 10:00-11:00 | UPLOAD VIDEO YOUTUBE

#### A. Créer compte YouTube (si besoin)
- Gmail → YouTube.com

#### B. Upload vidéo
1. YouTube Studio → **Create** → **Upload videos**
2. Sélectionnez `video.mp4` (ou drag-drop)
3. **Title**: `School & Crypto Timing - Hackathon Hex 2026`
4. **Description**:
```
Hex hackathon project: Finding optimal trading windows for teacher-traders.

Using live MEXC data + realistic teacher schedules + AI, 
this app calculates best trading times.

GitHub: https://github.com/YOUR_USERNAME/school-crypto-timing
Hex App: https://app.hex.tech/share/...

Built with Hex (notebook + app + semantic modeling), MEXC API, SQLite.
```
5. **Visibility**: Public (ou Unlisted)
6. **Upload**

#### C. Copier lien YouTube
```
Format: https://www.youtube.com/watch?v=XXXX
```

**Durée**: 30 min (incluant upload + processing)  
**Livrable**: ✅ YouTube link

---

### 11:00-12:00 | CRÉER PROJET OVERVIEW (TEXTE DEVPOST)

Ouvrez Notepad ou Word, écrivez ceci (adapté à votre style):

```
TITRE:
School & Crypto Timing: Finding Your Trading Window

DESCRIPTION (150-200 mots):

The Challenge:
Side-traders (teachers, freelancers, full-time employees with passion for crypto) 
face a brutal reality: trading requires constant attention. But they don't have it.

The Problem:
Most side-traders fail because they trade at the wrong times. 
They see a 5% pump, jump in during lunch break while teaching, 
lose 2x on liquidation because they can't monitor, then give up.

The Solution:
School & Crypto Timing uses Hex to combine:
1. Realistic schedules (teacher duties, family, commute)
2. Live MEXC data (volatility, liquidations, funding rates per hour)
3. Hex AI to generate personalized insights

The Algorithm:
For each hour of the week, we calculate a "Trading Window Score" (0-100) based on:
- Your availability (free time after classes/meetings)
- Market conditions (volatility, liquidity, funding)
- Risk tolerance (customizable)

The Result:
An interactive app that shows:
- Best trading slots via visual heatmap (green = TRADE, yellow = HOLD, red = CAUTION)
- AI-generated daily summaries ("Thursday 10-12 is your golden window for ETH")
- Filters by asset, time, risk level

Impact:
Teachers can now safely trade 2h/day instead of burning out. 
Data-driven timing > emotional decisions.

Technologies:
- Hex (notebook + app + AI semantic modeling)
- MEXC API (real crypto data)
- SQLite (data persistence)
- Python (ETL + scoring)
- Plotly (interactive viz)

Why Hex:
This is ONLY possible in Hex. Traditional BI tools (Tableau, Power BI) 
can't blend education data + crypto APIs + AI into a conversational, 
interactive experience that feels natural.
```

**Durée**: 30 min  
**Livrable**: ✅ Texte copied pour Devpost

---

### 12:00-13:00 | LUNCH

---

### 13:00-14:00 | FAIRE SCREENSHOTS POUR DEVPOST

Prenez des screenshots de votre app Hex:

1. **Screenshot 1**: Heatmap full
   - Filename: `01-heatmap.png`
   - Alt text: "Trading Window Score heatmap showing best trading times by hour and asset"

2. **Screenshot 2**: App avec interactors
   - Filename: `02-app-interactive.png`
   - Alt text: "Interactive filters: professor selector, asset multi-select, score slider"

3. **Screenshot 3**: Distribution charts
   - Filename: `03-distribution.png`
   - Alt text: "Distribution of trading windows by category (TRADE/HOLD/CAUTION)"

4. **Screenshot 4**: Table résultats
   - Filename: `04-results-table.png`
   - Alt text: "Filtered results showing top trading windows with scores"

5. **Screenshot 5**: AI prompt
   - Filename: `05-ai-summary.png`
   - Alt text: "AI-generated coaching summary for the week"

Folder: `C:\Users\franc\Documents\hackaton\screenshots\`

**Durée**: 20 min  
**Livrables**: ✅ 5 screenshots en PNG

---

### 14:00-15:30 | SOUMETTRE SUR DEVPOST

#### A. Allez sur Devpost
https://hex-a-thon.devpost.com

#### B. Click "Submit to Challenge"

#### C. Remplissez le formulaire:

**Basic Info**
- Project Name: `School & Crypto Timing`
- Tagline: `Data-driven trading windows for teacher-traders`
- Project Description: [Copier le texte de 12:00-13:00]
- Category: **Wildcard: Build Whatever Haunts You**

**Files & Links**
- **Hex Project (public URL)**:
  - https://app.hex.tech/share/...

- **Demo Video**:
  - https://www.youtube.com/watch?v=XXXX

- **GitHub Repo** (optional but recommended):
  - https://github.com/YOUR_USERNAME/school-crypto-timing

- **Project Pictures**:
  - Upload 5 screenshots depuis `C:\Users\franc\Documents\hackaton\screenshots\`

**Video Details**
- URL: [YouTube link]
- Duration: 2:47 (ou votre durée réelle)

#### D. Review + Submit
- Vérifier tout est correct
- Click **SUBMIT**

**Durée**: 45 min  
**Livrable**: ✅ Devpost submission complétée

---

### 15:30-23:59 | CÉLÉBRATION!

Vous avez **fini le hackathon**! 🎉

Attendez les résultats (jugement dans ~2 semaines).

---

## 📋 RÉSUMÉ TIMELINE

| Phase | Jour | Durée | Livrables |
|-------|------|-------|-----------|
| **Setup** | Dim 18 | 2h | DB OK, GitHub, OBS |
| **Hex Notebook** | Dim 18 | 2h | 7 Cells, 1 heatmap |
| **Hex App** | Dim 18 | 1h | App publique interactive |
| **Démo Video** | Lun 19 | 1h | MP4, YouTube |
| **Devpost** | Lun 19 | 2h | Submission complétée |
| **Buffer** | Lun 19 | 6h+ | Pour fixes d'emergencies |

**TOTAL**: ~14-16 heures de travail réparti sur 48h

---

## ⚠️ PROBLÈMES COURANTS + SOLUTIONS

### Problème 1: Hex refuse la DB SQLite
**Solution**: Exporter en CSV au lieu
```bash
# Dans terminal
sqlite3 hackaton.db ".mode csv"
sqlite3 hackaton.db "SELECT * FROM trading_window_scores;" > scores.csv
# Upload CSV dans Hex instead
```

### Problème 2: Cell ne se lance pas (error)
**Solution**: 
- Vérifier que pandas/plotly sont dispos (Hex les a par défaut)
- Si emoji cause erreur: remplacer 🟢 par [TRADE], 🟡 par [HOLD], etc.
- Si date cause erreur: utiliser `pd.to_datetime()` explicite

### Problème 3: App Hex non interactive (sélecteurs ne changent rien)
**Solution**:
- Vérifier que Cell 4 a `selected_prof = param.selected_prof` (avec `param.`)
- Vérifier que le component output variable == nom de la variable Python
- Cliquer **Re-run dependent cells** si besoin

### Problème 4: Vidéo OBS est pixelée/lag
**Solution**:
- Réduire résolution enregistrement à 1280x720 au lieu 1920x1080
- Utiliser x264 encoder au lieu NVIDIA NVENC
- Réduire bitrate à 4000 kbps

### Problème 5: YouTube processing prend trop longtemps
**Solution**:
- Uploader 2h avant deadline avec qualité 720p au lieu 1080p
- Ou: uploader "Unlisted" pour plus rapide

---

## ✅ CHECKLIST FINAL

Avant de dormir Dimanche soir:
- [ ] `python python/query_db.py stats` affiche 8 scripts, 2,286 lignes ✅
- [ ] GitHub repo public avec code poussé ✅
- [ ] OBS installé + testé (record 10 sec, vérifier qualité) ✅
- [ ] Compte Hex créé ✅

Avant d'enregistrer la vidéo Lundi:
- [ ] Hex app publique + lien copié ✅
- [ ] 7 Cells fonctionnels sans erreur ✅
- [ ] App interactive (sélecteurs changent les charts) ✅
- [ ] Script démo mémorisé ou noté ✅
- [ ] OBS prêt, settings correct ✅

Avant de soumettre Devpost:
- [ ] Video YouTube en ligne + lien accessible ✅
- [ ] Texte projet overview copié ✅
- [ ] 5 screenshots en PNG ✅
- [ ] GitHub repo repo clean (README.md à jour) ✅
- [ ] Hex project link correct + fonctionne ✅

---

## 🎯 PUNCHLINE FINALE

**Vous avez une infrastructure SOLIDE. Le reste c'est juste copier-coller + cliquer.**

Samedi soir vous serez en train de célébrer avec 1/3 chance de TOP 3.

*Bonne chance! 🚀*
