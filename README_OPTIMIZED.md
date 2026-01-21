# 🚀 School & Crypto Timing

[![Hex](https://img.shields.io/badge/Built%20with-Hex-blueviolet?style=for-the-badge&logo=hex)](https://hex.tech) [![Live App](https://img.shields.io/badge/Live%20App-hex.tech-00d1b2?style=for-the-badge)](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest) [![GitHub](https://img.shields.io/badge/GitHub-Repo-black?style=for-the-badge&logo=github)](https://github.com/Turbo31150/school-crypto-timing)

**Hackathon Hex 2026** - Analyse du calendrier scolaire et du timing optimal de trading de cryptomonnaies

---

## 📊 Qu'est-ce que c'est ?

Une application **data-driven** qui optimise les fenêtres de trading crypto en fonction de l'emploi du temps scolaire d'un professeur-trader.

**Idée clé** : Recevoir des recommandations précises sur **QUAND trader** (quel jour, quelle heure) en fonction de :
- 📅 Son emploi du temps scolaire (disponibilité réelle)
- 📈 La volatilité des cryptomonnaies (BTC, ETH, SOL)
- 💹 Les scores de marché calculés (0-100)
- 🤖 Coaching IA personnalisé en français

---

## 🎯 Résultats Concrets

- **45 fenêtres de trading** analysées (7 créneaux × 3 actifs × 2 semaines)
- **Scores réalistes** : 43 à 99/100, moyenne ~69
- **Recommandations IA** en français avec TOP 5 opportunités
- **Heatmap interactif** Jour × Heure pour visualisation instantanée
- **Filtres dynamiques** (professeur, cryptos, score min, période)
- **100% fonctionnel** - aucune erreur, rechargeable à l'infini

---

## 🛠️ Tech Stack

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| **Frontend** | Hex (no-code interactif) | Application web + dashboard |
| **Backend** | SQLite (`hackaton.db`) | Base de données (45 scénarios) |
| **Data Pipeline** | Python 3.11 | ETL + Scoring algorithm |
| **Visualisation** | Plotly | Heatmap + graphiques interactifs |
| **IA** | Prompt engineering | Coaching en français |

---

## 📁 Structure des Fichiers

```
school-crypto-timing/
├── README.md                          ✅ Ce fichier
├── HACKATHON_GUIDE.md                 ✅ Guide de présentation
├── requirements.txt                   ✅ Dépendances Python
├── hackaton.db                        ✅ Base de données SQLite (45 fenêtres)
│
├── python/
│   ├── etl.py                         ✅ ETL principal
│   ├── scoring.py                     ✅ Algorithme de scoring
│   ├── query_db.py                    ✅ Requêtes BD
│   └── register_script.py             ✅ Enregistrement
│
├── sql/
│   ├── schema.sql                     ✅ Schéma principal
│   ├── hex_schema.sql                 ✅ Schéma Hex
│   └── hex_queries.sql                ✅ Requêtes Hex
│
├── data/                              ✅ Données brutes
└── docs/                              ✅ Documentation
```

---

## 🌐 Application Publique

👉 **[OUVRIR L'APP ICI](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest)**

*(Lien public - pas de login requis)*

**Mode Éditeur** : [Voir le Draft](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/hex/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/draft/logic)

---

## 🚀 Utilisation Locale

### Installation

```bash
git clone https://github.com/Turbo31150/school-crypto-timing.git
cd school-crypto-timing
pip install -r requirements.txt
```

### Exécuter les scripts

```bash
# ETL - charger et transformer les données
python python/etl.py

# Scoring - générer les scores de trading (0-100)
python python/scoring.py

# Query - requêtes de la base de données
python python/query_db.py
```

---

## 💡 Comment ça marche ?

### 1. **Analyse des Fenêtres de Trading**
Chaque créneau disponible reçoit un **score 0-100** basé sur :
- Disponibilité du professeur (emploi du temps)
- Volatilité du marché (crypto-monnaie)
- Indicateurs de profitabilité
- Historique de performance

### 2. **Classification Intelligente**
- 🔴 **RED** (0-20) : Éviter
- 🟠 **ORANGE** (21-50) : Prudence
- 🟡 **YELLOW** (51-79) : Acceptable
- 🟢 **GREEN** (80-100) : Optimal

### 3. **Dashboard Interactif**
- Heatmap Jour × Heure montrant les scores
- Tableau détaillé des 45+ fenêtres
- Filtres multi-critères (prof, crypto, score min)
- Mise à jour en temps réel

---

## 📊 Cas d'Usage

**Scénario typique** : Un professeur CM1/CM2 souhaite trader des cryptos mais a peu de temps libre.

1. **Jeudi 10h-12h** : Score 99/100 pour ETH/SOL → **Fenêtre idéale**
2. **Lundi 8h-10h** : Score 43/100 pour BTC → **À éviter**
3. **Mercredi 14h-16h** : Score 78/100 pour SOL → **Correct mais pas optimal**

L'application montre instantanément les **TOP 5 opportunités** de la semaine.

---

## ✅ Status de Production

**🎬 PRODUCTION READY - Prêt pour présentation hackathon**

- ✓ Les 7 cellules Hex s'exécutent sans erreur
- ✓ Application responsive et stable
- ✓ Heatmap précis et interactif
- ✓ Filtres dynamiques fonctionnels
- ✓ Base de données vérifiée (45 scénarios, max score 100)
- ✓ Rechargement (Ctrl+F5) maintient l'état
- ✓ Aucun stacktrace ni crash
- ✓ Testable sur mobile et desktop

---

## 🎥 Démonstration

**Pour la présentation au jury** :
1. Ouvrir l'app publique (lien ci-dessus)
2. Montrer le heatmap avec le pic jeudi 10h-12h (~99 pour ETH/SOL)
3. Démontrer les filtres interactifs (prof, cryptos, score_min)
4. Afficher la table de 45 lignes avec scénarios variés
5. Recharger la page pour prouver la stabilité

**Temps de démo recommandé** : 2-3 minutes

---

## 📝 Licence

Hackathon Hex 2026 - Libre d'utilisation éducative et compétitive

---

## 👤 Auteure

👩‍🏫 **Francoise** - Professeure CM1/CM2 + Développeuse + Entrepreneur crypto

*"Combiner pédagogie et finance, c'est montrer aux élèves qu'on peut utiliser l'IA et les données intelligemment."*

---

## 📚 Documentation

- **[HACKATHON_GUIDE.md](HACKATHON_GUIDE.md)** - Guide complet de présentation, checklist, FAQ jury
- **[sql/schema.sql](sql/schema.sql)** - Schéma de la base de données
- **[python/scoring.py](python/scoring.py)** - Algorithme de scoring (code à montrer au jury)

---

**Last Updated**: Janvier 2026  
**Hackathon**: Hex 2026  
**Status**: ✅ **PRODUCTION READY**

🎬 **Vidéo de présentation** : À venir (voir HACKATHON_GUIDE.md)
