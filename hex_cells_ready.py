# ============================================================
# HACKATHON HEX 2026 - ALL 7 CELLS READY TO COPY-PASTE
# ============================================================
# Instructions: Copy each CELL block into Hex.tech
# Cell type is indicated: [PYTHON] or [SQL]
# ============================================================

# ============================================================
# CELL 1: IMPORTS [PYTHON]
# ============================================================
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

print("[INFO] School & Crypto Timing v1.0")
print("=" * 60)
"""

# ============================================================
# CELL 2: LOAD DATA [SQL]
# ============================================================
"""
SELECT
    ts.id, ts.prof_id, ts.actif_id, ts.date,
    ts.heure_debut, ts.heure_fin, ts.score, ts.raison,
    ca.symbol, ca.nom,
    p.name as prof_name
FROM trading_window_scores ts
JOIN crypto_actifs ca ON ts.actif_id = ca.id
JOIN professeurs p ON ts.prof_id = p.id
ORDER BY ts.date DESC, ts.score DESC
LIMIT 100
"""

# ============================================================
# CELL 3: PREPARE DATAFRAMES [PYTHON]
# ============================================================
"""
# Reference SQL result
scores_df = sql_result.copy() if 'sql_result' in dir() else pd.DataFrame()

# Convert and prepare data
scores_df['date'] = pd.to_datetime(scores_df['date'])
scores_df['jour_semaine'] = scores_df['date'].dt.day_name()
scores_df['heure'] = scores_df['heure_debut'].str.split(':').str[0].astype(int)

# Create score categories
def score_to_category(score):
    if score >= 75:
        return "TRADE"
    elif score >= 50:
        return "HOLD"
    else:
        return "CAUTION"

scores_df['categorie'] = scores_df['score'].apply(score_to_category)

# Statistics
print("[STATS SUMMARY]")
trade_count = len(scores_df[scores_df['score'] >= 75])
hold_count = len(scores_df[(scores_df['score'] >= 50) & (scores_df['score'] < 75)])
caution_count = len(scores_df[scores_df['score'] < 50])

print(f"TRADE (>75): {trade_count} windows")
print(f"HOLD (50-75): {hold_count} windows")
print(f"CAUTION (<50): {caution_count} windows")
print(f"Total: {len(scores_df)} windows analyzed")
"""

# ============================================================
# CELL 4: INTERACTIVE FILTERS [PYTHON]
# ============================================================
"""
# Get unique values for dropdowns
prof_options = sorted(scores_df['prof_name'].unique().tolist())
actif_options = sorted(scores_df['symbol'].unique().tolist())

# Define parameters (will be replaced by Hex components later)
selected_prof = "Francois"
selected_actifs = ["BTC", "ETH"]
min_score = 50

# Date range
date_debut = scores_df['date'].min()
date_fin = scores_df['date'].max()

# Filter the data
filtered = scores_df[
    (scores_df['prof_name'] == selected_prof) &
    (scores_df['symbol'].isin(selected_actifs)) &
    (scores_df['score'] >= min_score) &
    (scores_df['date'] >= date_debut) &
    (scores_df['date'] <= date_fin)
].sort_values('score', ascending=False)

print(f"[FILTERED] {len(filtered)} windows after filtering")
print(f"\\nTop 10 trading windows:")
print(filtered[['jour_semaine', 'heure_debut', 'symbol', 'score', 'categorie']].head(10).to_string())
"""

# ============================================================
# CELL 5: HEATMAP VISUALIZATION [PYTHON]
# ============================================================
"""
# Prepare pivot table for heatmap
heatmap_pivot = filtered.pivot_table(
    values='score',
    index='heure',
    columns='symbol',
    aggfunc='max',
    fill_value=0
)

# Create interactive heatmap
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
"""

# ============================================================
# CELL 6: DISTRIBUTION & TIMELINE CHARTS [PYTHON]
# ============================================================
"""
# Chart 1: Distribution by category
category_counts = filtered['categorie'].value_counts()

fig_bar = px.bar(
    x=category_counts.index,
    y=category_counts.values,
    title="Distribution of Trading Windows by Category",
    labels={'x': 'Category', 'y': 'Count'},
    color=category_counts.index,
    color_discrete_map={'TRADE': '#2ecc71', 'HOLD': '#f39c12', 'CAUTION': '#e74c3c'},
    text=category_counts.values
)

fig_bar.update_traces(textposition='outside')
fig_bar.update_layout(height=400, showlegend=False, margin=dict(l=50, r=50, t=80, b=50))
fig_bar.show()

# Chart 2: Timeline - Average score by day
daily_stats = filtered.groupby('jour_semaine')['score'].agg(['mean', 'count']).reset_index()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_stats['jour_semaine'] = pd.Categorical(
    daily_stats['jour_semaine'],
    categories=day_order,
    ordered=True
)
daily_stats = daily_stats.sort_values('jour_semaine')

fig_line = px.line(
    daily_stats,
    x='jour_semaine',
    y='mean',
    markers=True,
    title="Average Trading Score by Day of Week",
    labels={'jour_semaine': 'Day', 'mean': 'Average Score'},
    line_shape='linear'
)

fig_line.update_traces(line=dict(color='#3498db', width=3), marker=dict(size=10))
fig_line.update_layout(height=400, margin=dict(l=50, r=50, t=80, b=50), hovermode='x unified')
fig_line.show()
"""

# ============================================================
# CELL 7: AI SUMMARY [PYTHON]
# ============================================================
"""
# Prepare AI coaching prompt
if len(filtered) > 0:
    top_5 = filtered.nlargest(5, 'score')
    avg_score = filtered['score'].mean()
    best_day = filtered.groupby('jour_semaine')['score'].mean().idxmax()
    best_hour = filtered.groupby('heure')['score'].mean().idxmax()

    ai_coaching = f'''
=== AI TRADING COACH SUMMARY ===

Profile: {selected_prof}
Assets: {', '.join(selected_actifs)}
Period: {date_debut.strftime('%Y-%m-%d')} to {date_fin.strftime('%Y-%m-%d')}

ANALYSIS:
- Total windows analyzed: {len(filtered)}
- Trade opportunities (>75): {len(filtered[filtered['score'] >= 75])}
- Hold opportunities (50-75): {len(filtered[(filtered['score'] >= 50) & (filtered['score'] < 75)])}
- Caution zones (<50): {len(filtered[filtered['score'] < 50])}
- Average score: {avg_score:.1f}/100

KEY INSIGHTS:
- Best trading day: {best_day} (avg score: {filtered[filtered['jour_semaine']==best_day]['score'].mean():.1f})
- Best trading hour: {best_hour}:00 - {best_hour+1}:00
- Top asset this week: {filtered.groupby('symbol')['score'].mean().idxmax()}

TOP 5 OPPORTUNITIES:
{top_5[['jour_semaine', 'heure_debut', 'symbol', 'score']].to_string(index=False)}

RECOMMENDATION:
Focus on {best_day.lower()} from {best_hour}h to {best_hour+2}h.
Avoid CAUTION zones (red on heatmap) due to schedule conflicts.

Data-driven trading > emotional decisions. Good luck!
    '''
    print(ai_coaching)
else:
    print("No trading windows found.")
"""

# ============================================================
# END OF HEX CELLS
# ============================================================
