# ============================================================
# HACKATHON HEX 2026 - SCHOOL & CRYPTO TIMING
# Version 2.0 - Cellules prêtes pour Hex.tech
# ============================================================
# Instructions: Copier chaque bloc CELL dans Hex.tech
# Type de cellule indiqué: [PYTHON] ou [SQL]
# ============================================================

# ============================================================
# CELL 0: CONNEXION DB PYTHON (si SQL natif non disponible)
# Type: [PYTHON]
# ============================================================
CELL_0_DB_CONNECTION = """
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

# Connexion à la base de données SQLite
# Note: Si vous utilisez Hex Data Sources, ignorez cette cellule

try:
    conn = sqlite3.connect('hackaton.db')

    # Charger les tables principales
    calculated_scores = pd.read_sql_query("SELECT * FROM calculated_scores", conn)
    trading_window_scores = pd.read_sql_query("SELECT * FROM trading_window_scores", conn)
    crypto_actifs = pd.read_sql_query("SELECT * FROM crypto_actifs", conn)
    professeurs = pd.read_sql_query("SELECT * FROM professeurs", conn)

    conn.close()

    print("[OK] Base de données chargée avec succès")
    print(f"    - {len(calculated_scores)} fenêtres de trading")
    print(f"    - {len(crypto_actifs)} actifs crypto")
    print(f"    - {len(professeurs)} professeur(s)")
except Exception as e:
    print(f"[ERREUR] Connexion DB: {e}")
"""

# ============================================================
# CELL 1: IMPORTS ET CONFIG [PYTHON]
# ============================================================
CELL_1_IMPORTS = """
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("=" * 60)
print("   SCHOOL & CRYPTO TIMING v2.0")
print("   Hackathon Hex 2026")
print("=" * 60)
print(f"   Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
print("=" * 60)
"""

# ============================================================
# CELL 2: SQL - TOP 10 MEILLEURES FENÊTRES [SQL]
# Nom suggéré dans Hex: best_windows
# ============================================================
CELL_2_SQL_BEST_WINDOWS = """
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
    ROUND(volume, 2) AS volume_24h,
    ROUND(volatility_component, 2) AS vol_comp,
    ROUND(availability_component, 0) AS avail_comp,
    ROUND(market_component, 2) AS market_comp
FROM calculated_scores
WHERE score >= 75
ORDER BY score DESC, volatility DESC
LIMIT 10;
"""

# ============================================================
# CELL 3: SQL - STATISTIQUES PAR ACTIF [SQL]
# Nom suggéré dans Hex: asset_stats
# ============================================================
CELL_3_SQL_ASSET_STATS = """
SELECT
    symbol AS asset_symbol,
    COUNT(*) AS total_windows,
    ROUND(AVG(score), 1) AS avg_score,
    MAX(score) AS best_score,
    MIN(score) AS worst_score,
    SUM(CASE WHEN recommendation = 'TRADE' THEN 1 ELSE 0 END) AS trade_signals,
    SUM(CASE WHEN recommendation = 'HOLD' THEN 1 ELSE 0 END) AS hold_signals,
    SUM(CASE WHEN recommendation = 'AVOID' THEN 1 ELSE 0 END) AS avoid_signals,
    ROUND(AVG(volatility), 2) AS avg_volatility,
    ROUND(AVG(volume), 2) AS avg_volume
FROM calculated_scores
GROUP BY symbol
ORDER BY avg_score DESC;
"""

# ============================================================
# CELL 4: SQL - DONNÉES HEATMAP [SQL]
# Nom suggéré dans Hex: heatmap_data
# ============================================================
CELL_4_SQL_HEATMAP = """
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
"""

# ============================================================
# CELL 5: PYTHON - HEATMAP INTERACTIVE [PYTHON]
# Prérequis: Exécuter CELL_4 d'abord (dataframe_3)
# ============================================================
CELL_5_HEATMAP_VIZ = """
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Référence aux données SQL (adapter le nom selon Hex)
# Si vous utilisez Python pour charger: df = calculated_scores
# Si vous utilisez SQL Hex: df = dataframe_3 ou heatmap_data
df = dataframe_3.copy()

# Mapping des jours pour l'ordre
day_order = {'Lundi': 1, 'Mardi': 2, 'Mercredi': 3, 'Jeudi': 4,
             'Vendredi': 5, 'Samedi': 6, 'Dimanche': 7}
df['day_order'] = df['day_name'].map(day_order)

# Pivot pour la heatmap - moyenne des scores par créneau/actif
heatmap_pivot = df.pivot_table(
    values='score',
    index='time_slot',
    columns=['day_name', 'asset_symbol'],
    aggfunc='mean',
    fill_value=0
)

# Trier les colonnes par jour
sorted_cols = sorted(heatmap_pivot.columns, key=lambda x: day_order.get(x[0], 99))
heatmap_pivot = heatmap_pivot[sorted_cols]

# Créer la heatmap
fig = px.imshow(
    heatmap_pivot.values,
    labels=dict(x="Jour / Actif", y="Créneau horaire", color="Score"),
    x=[f"{col[0][:3]}-{col[1]}" for col in heatmap_pivot.columns],
    y=heatmap_pivot.index,
    title="📊 Fenêtres de Trading Optimales - Heatmap",
    color_continuous_scale='RdYlGn',
    aspect='auto',
    zmin=0,
    zmax=100
)

fig.update_layout(
    height=600,
    width=1100,
    font=dict(size=11),
    title_font_size=20,
    coloraxis_colorbar=dict(
        title="Score",
        tickvals=[0, 25, 50, 75, 100],
        ticktext=["0 AVOID", "25", "50 HOLD", "75", "100 TRADE"],
        len=0.8
    ),
    xaxis_tickangle=-45
)

fig.update_traces(
    hovertemplate='<b>%{x}</b><br>Créneau: %{y}<br>Score: %{z:.0f}/100<extra></extra>'
)

fig
"""

# ============================================================
# CELL 6: PYTHON - GRAPHIQUE BARRES PAR ACTIF [PYTHON]
# Prérequis: Exécuter CELL_3 d'abord (dataframe_2)
# ============================================================
CELL_6_ASSET_BARS = """
import plotly.express as px
import plotly.graph_objects as go

# Référence aux données SQL
df_stats = dataframe_2.copy()

# Graphique en barres groupées
fig = go.Figure()

# Ajouter les barres pour chaque type de signal
fig.add_trace(go.Bar(
    name='TRADE',
    x=df_stats['asset_symbol'],
    y=df_stats['trade_signals'],
    marker_color='#2ecc71',
    text=df_stats['trade_signals'],
    textposition='outside'
))

fig.add_trace(go.Bar(
    name='HOLD',
    x=df_stats['asset_symbol'],
    y=df_stats['hold_signals'],
    marker_color='#f39c12',
    text=df_stats['hold_signals'],
    textposition='outside'
))

fig.add_trace(go.Bar(
    name='AVOID',
    x=df_stats['asset_symbol'],
    y=df_stats['avoid_signals'],
    marker_color='#e74c3c',
    text=df_stats['avoid_signals'],
    textposition='outside'
))

fig.update_layout(
    title="📈 Distribution des Recommandations par Actif",
    xaxis_title="Cryptomonnaie",
    yaxis_title="Nombre de fenêtres",
    barmode='group',
    height=450,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)

fig
"""

# ============================================================
# CELL 7: PYTHON - JAUGE SCORE GLOBAL [PYTHON]
# ============================================================
CELL_7_SCORE_GAUGE = """
import plotly.graph_objects as go

# Calculer le score moyen global
avg_score = dataframe_3['score'].mean()
trade_pct = len(dataframe_3[dataframe_3['recommendation'] == 'TRADE']) / len(dataframe_3) * 100

# Créer la jauge
fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=avg_score,
    number={'suffix': '/100', 'font': {'size': 40}},
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Score Moyen Global<br><span style='font-size:14px;color:gray'>Performance trading</span>",
           'font': {'size': 20}},
    delta={'reference': 50, 'increasing': {'color': "#2ecc71"}, 'decreasing': {'color': "#e74c3c"}},
    gauge={
        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#2c3e50",
                 'tickvals': [0, 25, 50, 75, 100]},
        'bar': {'color': "#3498db", 'thickness': 0.75},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "#bdc3c7",
        'steps': [
            {'range': [0, 50], 'color': '#fadbd8'},
            {'range': [50, 75], 'color': '#fef9e7'},
            {'range': [75, 100], 'color': '#d5f5e3'}
        ],
        'threshold': {
            'line': {'color': "#27ae60", 'width': 4},
            'thickness': 0.8,
            'value': 75
        }
    }
))

fig.add_annotation(
    x=0.5, y=-0.15,
    text=f"🎯 {trade_pct:.1f}% des créneaux sont TRADE",
    showarrow=False,
    font=dict(size=14, color="#2c3e50")
)

fig.update_layout(
    height=350,
    margin=dict(l=30, r=30, t=80, b=50)
)

fig
"""

# ============================================================
# CELL 8: PYTHON - COACH IA [PYTHON]
# ============================================================
CELL_8_AI_COACH = """
from datetime import datetime
import pandas as pd

# Références aux données SQL
best_windows = dataframe_1.copy()
asset_stats = dataframe_2.copy()
all_data = dataframe_3.copy()

# Métriques globales
total_windows = len(all_data)
trade_count = len(all_data[all_data['recommendation'] == 'TRADE'])
hold_count = len(all_data[all_data['recommendation'] == 'HOLD'])
avoid_count = len(all_data[all_data['recommendation'] == 'AVOID'])
avg_score = all_data['score'].mean()

# Meilleures stats
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
    best_time_score = time_scores.max()

    # Pire moment
    worst_day = day_scores.idxmin()
    worst_time = time_scores.idxmin()

# Génération du rapport
ai_report = f'''
{'='*65}
   🤖 COACH IA - SCHOOL & CRYPTO TIMING
   📅 Rapport du {datetime.now().strftime('%d/%m/%Y à %H:%M')}
{'='*65}

   📊 ANALYSE GLOBALE
   ──────────────────
   Fenêtres analysées: {total_windows}
   Score moyen: {avg_score:.1f}/100

   ✅ TRADE (score ≥ 75): {trade_count:>3} ({trade_count/total_windows*100:.1f}%)
   ⏸️  HOLD  (score 50-74): {hold_count:>3} ({hold_count/total_windows*100:.1f}%)
   ❌ AVOID (score < 50): {avoid_count:>3} ({avoid_count/total_windows*100:.1f}%)

   🏆 MEILLEURE OPPORTUNITÉ
   ────────────────────────
   Actif: {top_window['asset_symbol']}
   Jour: {top_window['day_name']}
   Créneau: {top_window['time_slot_start']} - {top_window['time_slot_end']}
   Score: {top_window['score']}/100
   Volatilité: {top_window['volatility_pct']}%
   ➡️  Action: {top_window['recommendation']}

   💡 INSIGHTS CLÉS
   ────────────────
   • Meilleur actif: {best_asset['asset_symbol']} (moy: {best_asset['avg_score']:.1f})
   • Meilleur jour: {best_day} (moy: {best_day_score:.1f})
   • Meilleur créneau: {best_time} (moy: {best_time_score:.1f})
   • À éviter: {worst_day} / {worst_time}

   📋 TOP 5 FENÊTRES DE TRADING
   ────────────────────────────
'''

# Ajouter le top 5
for i, row in best_windows.head(5).iterrows():
    ai_report += f"   {i+1}. {row['asset_symbol']:>4} | {row['day_name'][:3]} {row['time_slot_start']} | Score: {row['score']}/100\\n"

ai_report += f'''
   🎯 STRATÉGIE RECOMMANDÉE
   ────────────────────────
   1. Concentrez-vous sur {best_asset['asset_symbol']} et {best_day}
   2. Tradez pendant vos créneaux LIBRES uniquement
   3. Évitez les moments de cours (zones rouges)
   4. Utilisez un stop-loss de 2-3%

   ⚠️  AVERTISSEMENT: Le trading comporte des risques.
       Ne tradez jamais pendant vos heures de travail!
{'='*65}
'''

print(ai_report)
"""

# ============================================================
# CELL 9: PYTHON - TIMELINE PAR JOUR [PYTHON]
# ============================================================
CELL_9_TIMELINE = """
import plotly.express as px
import pandas as pd

# Données
df = dataframe_3.copy()

# Ordre des jours
day_order = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

# Calculer score moyen par jour
daily_avg = df.groupby('day_name')['score'].mean().reset_index()
daily_avg['day_name'] = pd.Categorical(daily_avg['day_name'], categories=day_order, ordered=True)
daily_avg = daily_avg.sort_values('day_name')

# Graphique ligne
fig = px.line(
    daily_avg,
    x='day_name',
    y='score',
    markers=True,
    title="📆 Score Moyen par Jour de la Semaine",
    labels={'day_name': 'Jour', 'score': 'Score moyen'}
)

fig.update_traces(
    line=dict(color='#3498db', width=3),
    marker=dict(size=12, color='#2980b9', line=dict(width=2, color='white'))
)

# Ajouter zone de seuil
fig.add_hline(y=75, line_dash="dash", line_color="#27ae60",
              annotation_text="Seuil TRADE (75)")
fig.add_hline(y=50, line_dash="dash", line_color="#f39c12",
              annotation_text="Seuil HOLD (50)")

fig.update_layout(
    height=400,
    hovermode='x unified',
    yaxis_range=[0, 100]
)

fig
"""

# ============================================================
# CELL 10: PYTHON - TABLEAU TOP 10 FORMATÉ [PYTHON]
# ============================================================
CELL_10_TOP_TABLE = """
import pandas as pd

# Formater le tableau des meilleures fenêtres
top_df = dataframe_1.copy()

# Ajouter des émojis selon la recommandation
def add_emoji(rec):
    if rec == 'TRADE':
        return '🟢 TRADE'
    elif rec == 'HOLD':
        return '🟡 HOLD'
    else:
        return '🔴 AVOID'

top_df['status'] = top_df['recommendation'].apply(add_emoji)

# Sélectionner et renommer les colonnes pour l'affichage
display_df = top_df[[
    'day_name', 'time_slot_start', 'time_slot_end',
    'asset_symbol', 'score', 'status', 'volatility_pct'
]].rename(columns={
    'day_name': 'Jour',
    'time_slot_start': 'Début',
    'time_slot_end': 'Fin',
    'asset_symbol': 'Actif',
    'score': 'Score',
    'status': 'Recommandation',
    'volatility_pct': 'Volatilité %'
})

print("🏆 TOP 10 MEILLEURES FENÊTRES DE TRADING")
print("=" * 70)
display_df
"""

# ============================================================
# FIN DES CELLULES HEX
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("HACKATHON HEX 2026 - CELLULES PRÊTES")
    print("=" * 60)
    print("\nCellules disponibles:")
    print("  CELL_0: Connexion DB Python (optionnel)")
    print("  CELL_1: Imports et configuration")
    print("  CELL_2: SQL - Top 10 meilleures fenêtres")
    print("  CELL_3: SQL - Statistiques par actif")
    print("  CELL_4: SQL - Données heatmap")
    print("  CELL_5: Heatmap interactive")
    print("  CELL_6: Graphique barres par actif")
    print("  CELL_7: Jauge score global")
    print("  CELL_8: Coach IA")
    print("  CELL_9: Timeline par jour")
    print("  CELL_10: Tableau top 10 formaté")
    print("\nCopiez le contenu de chaque CELL_X dans Hex.tech")
    print("=" * 60)
