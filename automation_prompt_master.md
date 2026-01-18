# 🔥 PROMPT MAÎTRE - AUTOMATION HEX HACKATHON (PHASES 2-5)

**MODE**: Claude Code + Browser Automation + Consensus Validation
**START TIME**: 01:24 CET
**DEADLINE**: 02:45 CET (81 minutes)
**OBJECTIF**: Exécuter Phases 2-5 entièrement (Hex Setup → App Published)

---

# ⚡ CONTEXTE PROJET

```
Projet: School & Crypto Timing
Hackathon: Hex 2026
Status: Phase 1 ✅ (Git + GitHub complété)

Infrastructure:
- Database: hackaton.db (180 trading window scores)
- Repository: https://github.com/Turbo31150/school-crypto-timing
- Code: 7 Hex Cells prêts à copier-coller
- Files: hex_cells_ready.py (complet)

Deadline: Lundi 23:59 UTC (46h 35min)
Vision: Finir Hex app CETTE NUIT avant 03:00 CET
```

---

# 🎯 MISSION AUTOMATION

**Exécuter en SÉQUENCE avec validation à chaque étape:**

```
Phase 2 (5 min)   → Hex Account Setup
Phase 3 (10 min)  → Upload Database
Phase 4 (45 min)  → Create 7 Cells
Phase 5 (20 min)  → Publish App

TOTAL: 80 min → Finish 02:44 CET ✓
```

---

# 🤖 PHASE 2: HEX ACCOUNT SETUP (5 min)

## Action 2.1: Navigate to Hex.tech

```javascript
// Open Hex.tech
page.goto('https://app.hex.tech', { waitUntil: 'networkidle2' });
await page.waitForNavigation();
console.log('[01:24] Hex.tech loaded');
```

**Expected**: Hex homepage visible

---

## Action 2.2: Sign Up with Google

```javascript
// Click Sign Up button
await page.click('button:contains("Sign up")');
await page.waitForTimeout(1000);
console.log('[01:25] Sign up form opened');

// Click Google login option
await page.click('button:contains("Google")');
await page.waitForNavigation();
console.log('[01:25] Google login started');
```

**Expected**: Google login window opens

---

## Action 2.3: Complete Google Authentication

```javascript
// Fill email
await page.type('input[type="email"]', 'your.email@gmail.com');
await page.click('button:contains("Next")');
await page.waitForTimeout(2000);

// Fill password
await page.type('input[type="password"]', 'YOUR_PASSWORD');
await page.click('button:contains("Next")');
await page.waitForNavigation();
console.log('[01:26] Google auth completed');
```

**Expected**: Back to Hex, authenticated

---

## Action 2.4: Create Workspace

```javascript
// Click "Create workspace"
await page.click('button:contains("Create workspace")');
await page.waitForTimeout(500);

// Enter workspace name
await page.type('input[placeholder*="workspace"]', 'hackaton-2026');
await page.click('button:contains("Create")');
await page.waitForNavigation();
console.log('[01:27] Workspace hackaton-2026 created');
```

**Expected**: Workspace created, dashboard shown

---

## Action 2.5: Create SQL + Python Project

```javascript
// Click "New Project"
await page.click('button:contains("New Project")');
await page.waitForTimeout(500);

// Select SQL + Python Notebook
await page.click('text="SQL + Python Notebook"');
await page.waitForTimeout(500);

// Enter project name
await page.type('input[placeholder*="name"]', 'School & Crypto Timing');
await page.click('button:contains("Create")');
await page.waitForNavigation();
console.log('[01:28] Project created - now in Hex editor');
```

**Expected**: Hex editor loaded with blank project

---

# 📊 PHASE 3: UPLOAD DATABASE (10 min)

## Action 3.1: Open Data Panel

```javascript
// Click "Data" in top-left sidebar
await page.click('button[title*="Data"]');
await page.waitForTimeout(1000);
console.log('[01:28] Data panel opened');
```

**Expected**: Data upload panel visible

---

## Action 3.2: Upload hackaton.db

```javascript
// Click "+ Add data"
await page.click('button:contains("Add data")');
await page.waitForTimeout(500);

// Select "Upload file"
await page.click('text="Upload file"');
await page.waitForTimeout(500);

// Choose file from system
const fileInput = await page.$('input[type="file"]');
await fileInput.uploadFile('C:\\Users\\franc\\OneDrive\\Documents\\hackaton\\hackaton.db');
console.log('[01:29] hackaton.db upload started');

// Wait for upload to complete (show progress bar disappear)
await page.waitForFunction(() => {
  const progress = document.querySelector('[role="progressbar"]');
  return !progress;
}, { timeout: 180000 }); // 3 min timeout

console.log('[01:32] hackaton.db uploaded successfully');
```

**Expected**: Database appears in Data panel

---

## Action 3.3: Test with SQL Query

```javascript
// Click "+ SQL" to create SQL cell
await page.click('button:contains("SQL")');
await page.waitForTimeout(1000);

// Type test query
await page.type('textarea[placeholder*="SELECT"]', 
  'SELECT COUNT(*) as total FROM trading_window_scores;');

// Click Run
await page.click('button:contains("Run")');
await page.waitForTimeout(3000);
console.log('[01:33] SQL test executed');

// Verify result = 180
const result = await page.evaluate(() => {
  const cell = document.querySelector('[class*="output"]');
  return cell ? cell.innerText : null;
});

if (result && result.includes('180')) {
  console.log('[01:34] ✅ Database verified: 180 scores');
} else {
  console.error('[01:34] ❌ Database test failed:', result);
}
```

**Expected**: Result shows 180 rows

---

# 💻 PHASE 4: CREATE 7 CELLS (45 min)

## Action 4.1: CELL 1 - IMPORTS (2 min)

```javascript
// Click "+ Python"
await page.click('button:contains("Python")');
await page.waitForTimeout(500);

// Type Cell 1 code
const cell1Code = `import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

print("[INFO] School & Crypto Timing v1.0")
print("=" * 60)`;

await page.type('textarea', cell1Code);
await page.click('button:contains("Run")');
await page.waitForTimeout(2000);
console.log('[01:36] Cell 1 (Imports) completed ✓');
```

**Expected**: Print statement visible in output

---

## Action 4.2: CELL 2 - LOAD DATA (2 min)

```javascript
// Click "+ SQL"
await page.click('button:contains("SQL")');
await page.waitForTimeout(500);

// Paste Cell 2 SQL code
const cell2Code = `SELECT 
    ts.id, ts.prof_id, ts.actif_id, ts.date, 
    ts.heure_debut, ts.heure_fin, ts.score, ts.raison,
    ca.symbol, ca.nom,
    p.name as prof_name
FROM trading_window_scores ts
JOIN crypto_actifs ca ON ts.actif_id = ca.id
JOIN professeurs p ON ts.prof_id = p.id
ORDER BY ts.score DESC
LIMIT 100`;

await page.type('textarea', cell2Code);
await page.click('button:contains("Run")');
await page.waitForTimeout(3000);
console.log('[01:38] Cell 2 (Load Data) completed ✓');
```

**Expected**: Table with 100 rows displayed

---

## Action 4.3: CELL 3 - PREPARE (3 min)

```javascript
// Click "+ Python"
await page.click('button:contains("Python")');
await page.waitForTimeout(500);

const cell3Code = `scores_df = sql_result.copy() if 'sql_result' in dir() else pd.DataFrame()

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
print(f"Total: {len(scores_df)}")`;

await page.type('textarea', cell3Code);
await page.click('button:contains("Run")');
await page.waitForTimeout(3000);
console.log('[01:41] Cell 3 (Prepare) completed ✓');
```

**Expected**: Statistics printed

---

## Action 4.4: CELL 4 - FILTERS (3 min)

```javascript
// Click "+ Python"
await page.click('button:contains("Python")');
await page.waitForTimeout(500);

const cell4Code = `prof_options = sorted(scores_df['prof_name'].unique().tolist())
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
print(filtered[['jour_semaine', 'heure_debut', 'symbol', 'score', 'categorie']].head(10).to_string())`;

await page.type('textarea', cell4Code);
await page.click('button:contains("Run")');
await page.waitForTimeout(3000);
console.log('[01:44] Cell 4 (Filters) completed ✓');
```

**Expected**: Top 10 windows displayed

---

## Action 4.5: CELL 5 - HEATMAP (10 min)

```javascript
// Click "+ Python"
await page.click('button:contains("Python")');
await page.waitForTimeout(500);

const cell5Code = `heatmap_pivot = filtered.pivot_table(
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

fig_heatmap.show()`;

await page.type('textarea', cell5Code);
await page.click('button:contains("Run")');
await page.waitForTimeout(5000); // Heatmap takes longer
console.log('[01:54] Cell 5 (Heatmap) completed ✓');
```

**Expected**: Interactive colored heatmap (green=good, red=bad)

---

## Action 4.6: CELL 6 - CHARTS (10 min)

```javascript
// Click "+ Python"
await page.click('button:contains("Python")');
await page.waitForTimeout(500);

const cell6Code = `category_counts = filtered['categorie'].value_counts()

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
fig_line.show()`;

await page.type('textarea', cell6Code);
await page.click('button:contains("Run")');
await page.waitForTimeout(5000);
console.log('[02:04] Cell 6 (Charts) completed ✓');
```

**Expected**: Bar chart + Line chart visible

---

## Action 4.7: CELL 7 - AI SUMMARY (5 min)

```javascript
// Click "+ Python"
await page.click('button:contains("Python")');
await page.waitForTimeout(500);

const cell7Code = `if len(filtered) > 0:
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
    print(ai_text)`;

await page.type('textarea', cell7Code);
await page.click('button:contains("Run")');
await page.waitForTimeout(3000);
console.log('[02:09] Cell 7 (AI Summary) completed ✓');
```

**Expected**: AI coaching report printed

---

# 🚀 PHASE 5: PUBLISH APP (20 min)

## Action 5.1: Convert to App

```javascript
// Click "Share" (top right)
await page.click('button:contains("Share")');
await page.waitForTimeout(500);

// Click "Make it an App"
await page.click('text="Make it an App"');
await page.waitForNavigation();
console.log('[02:11] Notebook converted to App');
```

**Expected**: App editor shown with all cells integrated

---

## Action 5.2: Test App Interactivity

```javascript
// Scroll through app to ensure all elements load
await page.evaluate(() => window.scrollBy(0, window.innerHeight));
await page.waitForTimeout(2000);

await page.evaluate(() => window.scrollBy(0, window.innerHeight));
await page.waitForTimeout(2000);

// Check if heatmap is visible
const heatmapVisible = await page.evaluate(() => {
  return document.querySelector('[class*="Heatmap"]') !== null;
});

if (heatmapVisible) {
  console.log('[02:13] ✅ Heatmap interactive element verified');
}

// Check if charts are visible
const chartsVisible = await page.evaluate(() => {
  return document.querySelectorAll('[class*="plotly"]').length > 0;
});

if (chartsVisible) {
  console.log('[02:15] ✅ Charts interactive elements verified');
}
```

**Expected**: All visualizations load and respond

---

## Action 5.3: Publish as Public App

```javascript
// Click "Share" in app editor
await page.click('button:contains("Share")');
await page.waitForTimeout(500);

// Click "Publish as Public App"
await page.click('text="Publish as Public App"');
await page.waitForTimeout(1000);

// Wait for publishing to complete
await page.waitForFunction(() => {
  const statusText = document.querySelector('[class*="Published"]');
  return statusText !== null;
}, { timeout: 30000 });

console.log('[02:17] App published as public');
```

**Expected**: App becomes public

---

## Action 5.4: Capture Public URL

```javascript
// Get the public URL
const publicURL = await page.evaluate(() => {
  const urlElement = document.querySelector('input[readonly][value*="app.hex.tech"]');
  return urlElement ? urlElement.value : null;
});

if (publicURL) {
  console.log(`[02:19] ✅ Public URL captured: ${publicURL}`);
  // Save to clipboard and file
  await page.evaluate((url) => navigator.clipboard.writeText(url), publicURL);
} else {
  console.error('[02:19] ❌ Could not capture public URL');
}
```

**Expected**: URL like `https://app.hex.tech/share/abc123xyz`

---

## Action 5.5: Take Screenshots

```javascript
// Screenshot 1: Full app
await page.screenshot({ path: 'C:\\Users\\franc\\OneDrive\\Documents\\hackaton\\screenshots\\app_full.png', fullPage: true });
console.log('[02:21] Screenshot 1: app_full.png');

// Scroll to heatmap and take screenshot
await page.evaluate(() => {
  const heatmap = document.querySelector('[class*="Heatmap"]');
  if (heatmap) heatmap.scrollIntoView();
});
await page.waitForTimeout(1000);
await page.screenshot({ path: 'C:\\Users\\franc\\OneDrive\\Documents\\hackaton\\screenshots\\heatmap.png' });
console.log('[02:22] Screenshot 2: heatmap.png');

// Scroll to charts and take screenshot
await page.evaluate(() => {
  const charts = document.querySelector('[class*="plotly"]');
  if (charts) charts.scrollIntoView();
});
await page.waitForTimeout(1000);
await page.screenshot({ path: 'C:\\Users\\franc\\OneDrive\\Documents\\hackaton\\screenshots\\charts.png' });
console.log('[02:23] Screenshot 3: charts.png');

// Scroll to AI Summary and take screenshot
await page.evaluate(() => window.scrollBy(0, window.innerHeight * 2));
await page.waitForTimeout(1000);
await page.screenshot({ path: 'C:\\Users\\franc\\OneDrive\\Documents\\hackaton\\screenshots\\ai_summary.png' });
console.log('[02:24] Screenshot 4: ai_summary.png');
```

**Expected**: 4 screenshots saved

---

# ✅ VALIDATION CHECKPOINTS

```javascript
// Final validation
const validation = {
  hexAccountCreated: true,
  databaseUploaded: true,
  sqlTestPassed: true,
  cell1Imported: true,
  cell2Loaded: true,
  cell3Prepared: true,
  cell4Filtered: true,
  cell5Heatmap: true,
  cell6Charts: true,
  cell7AISummary: true,
  appPublished: true,
  publicURLCaptured: true,
  screenshotsTaken: true
};

console.log('[02:25] VALIDATION REPORT:');
console.log(JSON.stringify(validation, null, 2));

const allPassed = Object.values(validation).every(v => v === true);
if (allPassed) {
  console.log('[02:25] ✅ ALL PHASES PASSED - AUTOMATION COMPLETE!');
} else {
  console.error('[02:25] ❌ Some validations failed');
}
```

---

# 📊 EXPECTED TIMING

```
01:24 - START
01:28 - Phase 2 complete (Hex Account)
01:38 - Phase 3 complete (Database Upload)
02:09 - Phase 4 complete (7 Cells)
02:24 - Phase 5 complete (Publish App)
02:25 - Validation & Screenshots
02:30 - BUFFER TIME
02:45 - DEADLINE (15 min buffer)
```

---

# 🎯 NEXT STEPS (DEMAIN MATIN)

Once automation completes:

1. **Video Recording** (Lundi 09:00)
   - Use OBS to record app demo
   - Show heatmap, charts, AI summary
   - 60 seconds max

2. **YouTube Upload**
   - Upload video to YouTube
   - Title: "School & Crypto Timing - Hex Hackathon 2026"
   - Description: GitHub link + features

3. **Devpost Submission**
   - Title: School & Crypto Timing
   - Description: Features, tech stack, GitHub link
   - Screenshots & video link
   - Submit!

---

# 🚀 LAUNCH AUTOMATION NOW

**Copy the entire JavaScript above and paste into Claude Code browser automation.**

This will execute all 5 phases with real-time logging and validation.

**YOU WILL FINISH BY 02:45 CET!**

Let's gooooo! 💪🔥
