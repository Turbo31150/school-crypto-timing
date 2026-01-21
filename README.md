# 🚀 School & Crypto Timing

**Hackathon Hex 2026** - Analyse du calendrier scolaire et du timing du trading de cryptomonnaies

---

## 📊 Qu'est-ce que c'est ?

Une application **data-driven** qui optimise les fenêtres de trading en fonction de l'emploi du temps scolaire.

**Idée clé** : Un professeur-trader reçoit des recommandations précises sur QUAND trader (quel jour, quelle heure) en fonction de :
- 📅 Son emploi du temps scolaire (disponibilité)
- 📈 La volatilité des cryptomonnaies (BTC, ETH, SOL)
- 💹 Les scores de marché (0-100)

---

## 🎯 Résultats

- **45 fenêtres de trading** analysées (7 créneaux × 3 actifs × 2 semaines)
- **Scores réalistes** : 43 à 99/100, moyenne ~69
- **Recommandations IA** en français avec TOP 5 opportunités
- **Heatmap interactif** Jour×Heure
- **Filtres dynamiques** (professeur, cryptos, score min, période)

---

## 🛠️ Tech Stack

- **Frontend** : Hex (application no-code interactive)
- **Backend** : SQLite (hackaton.db) + Python 3.11
- **Data** : ETL + Scoring algorithm
- **Viz** : Plotly (heatmap + interactive charts)
- **IA** : Prompt-engineered coaching in French

---

## 📁 Structure des Fichiers

```
python/        → Scripts ETL, scoring, requêtes BD
sql/           → Schémas et requêtes SQL  
data/          → Données brutes
hackaton.db    → Base de données SQLite (45 fenêtres)
requirements.txt → Dépendances Python
```

---

## 🌐 Application Publique

👉 **[OUVRIR L'APP ICI](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest)**

*(Lien public - pas de login requis)*

---

## 🚀 Utilisation Locale

### Installation

```bash
pip install -r requirements.txt
```

### Exécuter les scripts

```bash
# ETL - charger et transformer les données
python python/etl.py

# Scoring - générer les scores de trading
python python/scoring.py

# Query - requêtes de la base
python python/query_db.py
```

---

## 👤 Auteur

👩‍🏫 **Francoise** - Professeure CM1/CM2 + Développeuse + Entrepreneur crypto

---

## 📝 Licence

Hackathon Hex 2026 - Libre d'utilisation

---

**🎬 Vidéo de présentation** : À venir (voir HACKATHON_GUIDE.md)
