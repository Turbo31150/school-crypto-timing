"""
HACKATHON HEX - School & Crypto Timing
Notebook complet pour Hex
Auteur: Claude Code
Date: 2026-01-18
"""

# ============================================
# CELL 1: IMPORTS + CONFIG
# ============================================
import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import json
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple

# Config
DB_PATH = "hackaton.db"  # Hex auto-remplace par path correct
TIMEZONE_DEFAULT = "Europe/Paris"

print("[INFO] Hex Notebook - School & Crypto Timing v1.0")
print(f"[INFO] Database: {DB_PATH}")

# ============================================
# CELL 2: LOAD DATA FROM SQLite
# ============================================

def load_data(db_path: str) -> Dict[str, pd.DataFrame]:
    """Charge toutes les données depuis SQLite"""
    conn = sqlite3.connect(db_path)
    
    dfs = {
        'professeurs': pd.read_sql("SELECT * FROM professeurs", conn),
        'crypto_actifs': pd.read_sql("SELECT * FROM crypto_actifs", conn),
        'emploi_du_temps': pd.read_sql("SELECT * FROM emploi_du_temps", conn),
        'crypto_data_hourly': pd.read_sql("SELECT * FROM crypto_data_hourly", conn),
        'trading_window_scores': pd.read_sql("SELECT * FROM trading_window_scores", conn),
    }
    
    conn.close()
    
    # Validation
    for table_name, df in dfs.items():
        print(f"[OK] {table_name}: {len(df)} lignes")
    
    return dfs

# Charger
data = load_data(DB_PATH)
prof_df = data['professeurs']
crypto_df = data['crypto_actifs']
horaire_df = data['emploi_du_temps']
scores_df = data['trading_window_scores']

print(f"\n[LOADED] Total scores calcules: {len(scores_df)}")

# ============================================
# CELL 3: PREPARE DATAFRAMES
# ============================================

# Enrichir scores_df avec infos crypto
scores_enrichis = scores_df.merge(
    crypto_df[['id', 'symbol', 'nom']],
    left_on='actif_id',
    right_on='id',
    how='left'
).drop('id', axis=1)

# Ajouter jour semaine
scores_enrichis['date'] = pd.to_datetime(scores_enrichis['date'])
scores_enrichis['jour_semaine'] = scores_enrichis['date'].dt.day_name()
scores_enrichis['heure'] = scores_enrichis['heure_debut'].str.split(':').str[0].astype(int)

# Ajouter catégorie (TRADE vs HOLD vs CAUTION)
def score_to_category(score):
    if score >= 75:
        return "🟢 TRADE"
    elif score >= 50:
        return "🟡 HOLD"
    else:
        return "🔴 CAUTION"

scores_enrichis['categorie'] = scores_enrichis['score'].apply(score_to_category)

print(f"[OK] DataFrames enrichis")
print(f"    TRADE (>75): {len(scores_enrichis[scores_enrichis['score'] >= 75])}")
print(f"    HOLD (50-75): {len(scores_enrichis[(scores_enrichis['score'] >= 50) & (scores_enrichis['score'] < 75)])}")
print(f"    CAUTION (<50): {len(scores_enrichis[scores_enrichis['score'] < 50])}")

# ============================================
# CELL 4: APP PARAMS (Hex Interactive)
# ============================================

# Ces variables sont remplacées par Hex App Builder
# Si en notebook local, utiliser les defaults

# Par défaut: semaine prochaine
date_debut = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
date_fin = date_debut + timedelta(days=7)

# Paramètres (à adapter via Hex UI)
param_prof_id = 1  # Professeur sélectionné (via dropdown)
param_actifs = ['BTC', 'ETH']  # Actifs sélectionnés (via multi-select)
param_min_score = 50  # Score minimum (via slider)

print(f"[PARAMS]")
print(f"  Prof ID: {param_prof_id}")
print(f"  Actifs: {param_actifs}")
print(f"  Score min: {param_min_score}")
print(f"  Période: {date_debut.date()} à {date_fin.date()}")

# ============================================
# CELL 5: FILTER + VISUALIZATIONS
# ============================================

# Filtrer selon params
filtered_scores = scores_enrichis[
    (scores_enrichis['prof_id'] == param_prof_id) &
    (scores_enrichis['symbol'].isin(param_actifs)) &
    (scores_enrichis['score'] >= param_min_score) &
    (scores_enrichis['date'] >= date_debut) &
    (scores_enrichis['date'] <= date_fin)
].sort_values('score', ascending=False)

print(f"\n[FILTERED] {len(filtered_scores)} creneaux correspondants")

if len(filtered_scores) > 0:
    print(f"TOP 3:")
    for idx, row in filtered_scores.head(3).iterrows():
        print(f"  {row['jour_semaine']} {row['heure_debut']}-{row['heure_fin']} | {row['symbol']} | Score {row['score']:.0f} | {row['categorie']}")

# ============================================
# VIZ 1: Heatmap Score par heure/actif
# ============================================

heatmap_data = filtered_scores.pivot_table(
    values='score',
    index='heure',
    columns='symbol',
    aggfunc='max'
)

fig1 = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale='RdYlGn',
    text=heatmap_data.values.round(0),
    texttemplate='%{text}',
    textfont={"size": 12},
    colorbar=dict(title="Score (0-100)")
))

fig1.update_layout(
    title=f"Trading Window Score - Semaine {date_debut.strftime('%d/%m')} à {date_fin.strftime('%d/%m')}",
    xaxis_title="Crypto",
    yaxis_title="Heure du jour",
    height=400,
    width=800
)

print("\n[VIZ1] Heatmap créée")
fig1.show()

# ============================================
# VIZ 2: Distribution par catégorie
# ============================================

category_counts = filtered_scores['categorie'].value_counts()

fig2 = px.bar(
    x=category_counts.index,
    y=category_counts.values,
    labels={'x': 'Catégorie', 'y': 'Nombre de créneaux'},
    title="Distribution des créneaux par catégorie",
    color=category_counts.index,
    color_discrete_map={
        '🟢 TRADE': '#2ecc71',
        '🟡 HOLD': '#f39c12',
        '🔴 CAUTION': '#e74c3c'
    }
)

fig2.update_layout(height=400, width=600, showlegend=False)
print("[VIZ2] Bar chart créé")
fig2.show()

# ============================================
# VIZ 3: Timeline score par jour
# ============================================

timeline = filtered_scores.groupby('jour_semaine')['score'].agg(['mean', 'max', 'count'])
timeline = timeline.reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
], fill_value=0)

jour_fr = {
    'Monday': 'Lun', 'Tuesday': 'Mar', 'Wednesday': 'Mer',
    'Thursday': 'Jeu', 'Friday': 'Ven', 'Saturday': 'Sam', 'Sunday': 'Dim'
}

fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=[jour_fr[j] for j in timeline.index if timeline.loc[j, 'count'] > 0],
    y=timeline[timeline['count'] > 0]['mean'],
    mode='lines+markers',
    name='Score moyen',
    line=dict(color='#3498db', width=3),
    marker=dict(size=10)
))

fig3.update_layout(
    title="Evolution du score de trading par jour",
    xaxis_title="Jour",
    yaxis_title="Score moyen",
    height=400,
    width=700,
    hovermode='x unified'
)

print("[VIZ3] Timeline créée")
fig3.show()

# ============================================
# CELL 6: AI SUMMARY (Prompt pour IA)
# ============================================

# Préparer data pour l'IA
top_slots = filtered_scores.nlargest(5, 'score')
weak_slots = filtered_scores.nsmallest(5, 'score')

ai_prompt = f"""
Tu es un coach trading pour enseignants.

Analyse cette semaine de trading pour FRANÇOIS (prof à Montlaur, Occitanie):

DONNÉES:
- Total créneaux analysés: {len(filtered_scores)}
- Créneaux recommandés (score > 75): {len(filtered_scores[filtered_scores['score'] >= 75])}
- Meilleurs créneaux: 
{top_slots[['jour_semaine', 'heure_debut', 'symbol', 'score']].to_string()}

- Créneaux à éviter:
{weak_slots[['jour_semaine', 'heure_debut', 'symbol', 'score']].to_string()}

- Actifs tradés: {', '.join(param_actifs)}
- Période: {date_debut.strftime('%A %d/%m')} à {date_fin.strftime('%A %d/%m')}

TÂCHE:
Rédige un résumé court (150 mots max) en français qui:
1. Résume la semaine de trading de François (bon/mauvais timing?)
2. Donne 3 créneaux PRIORITAIRES à ne pas manquer
3. Donne 2 créneaux A EVITER absolument
4. Termine par 1 conseil pratique (ex: "Jeudi matin avant classe = zone verte")

Style: Bienveillant, pratique, pas d'jargon crypto trop téchnique.
"""

print("\n[IA PROMPT READY]")
print("=" * 60)
print(ai_prompt)
print("=" * 60)

# ============================================
# CELL 7: EXPORT RESULTS
# ============================================

# Exporter filtered_scores en CSV
export_path = f"trading_week_{date_debut.strftime('%Y%m%d')}.csv"
filtered_scores.to_csv(export_path, index=False)
print(f"\n[EXPORT] {export_path} créé")

# Résumé final
summary = {
    "semaine": f"{date_debut.strftime('%Y-%m-%d')} à {date_fin.strftime('%Y-%m-%d')}",
    "professeur": param_prof_id,
    "actifs": param_actifs,
    "total_creneaux": len(filtered_scores),
    "trade_score_75plus": len(filtered_scores[filtered_scores['score'] >= 75]),
    "hold_score_50_75": len(filtered_scores[(filtered_scores['score'] >= 50) & (filtered_scores['score'] < 75)]),
    "caution_score_less50": len(filtered_scores[filtered_scores['score'] < 50]),
    "meilleur_creneau": {
        "jour": filtered_scores.iloc[0]['jour_semaine'] if len(filtered_scores) > 0 else "N/A",
        "heure": filtered_scores.iloc[0]['heure_debut'] if len(filtered_scores) > 0 else "N/A",
        "actif": filtered_scores.iloc[0]['symbol'] if len(filtered_scores) > 0 else "N/A",
        "score": float(filtered_scores.iloc[0]['score']) if len(filtered_scores) > 0 else 0
    }
}

print("\n[SUMMARY]")
print(json.dumps(summary, indent=2, ensure_ascii=False))

# ============================================
# OUTPUT FINAL
# ============================================

print("\n" + "=" * 60)
print("HEX NOTEBOOK - READY FOR APP BUILDER")
print("=" * 60)
print("""
Prochaines étapes:
1. Convertir en Hex App avec App Builder
2. Ajouter sélecteurs (prof_id, actifs, date range)
3. Ajouter bloc IA pour résumés personnalisés
4. Tester interactivité
5. Enregistrer démo video
6. Soumettre Devpost
""")
