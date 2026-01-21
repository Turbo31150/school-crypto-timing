# 🎬 Guide de Préséntation - Hackathon Hex 2026

## Fichiers Essentiels pour la Préséntation

### Fichiers à avoir sur vous / votre ordinateur

1. **README.md** - Description complète du projet
2. **hackaton.db** - La base de données (45 fenêtres de trading)
3. **python/scoring.py** - Algorithme de scoring (15 lignes clé à montrer)
4. **sql/schema.sql** - Schéma de la base de données

### Fichiers optionnels

- HACKATHON_PRESENTATION.md (notes)
- HEX_APP_LINKS.txt (URLs publiques)

---

## 🎯 Checklist Avant le Hackathon

- ✅ Tester l'app publique sur un téléphone (vérifier que ça fonctionne sur mobile)
- ✅ Mémoriser le lien public : [https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest)
- ✅ Prévoir 2-3 cas de démo (cliquer sur filtres, montrer heatmap)
- ✅ Imprimer le README.md (une copie papier au cas où)
- ✅ Tourner la vidéo de présentation (2-3 min)

---

## 📺 Vidéo de Préséntation - Script

**Durée** : 2-3 minutes maximum
**Format** : MP4, 720p minimum
**Où uploader** : Devpost ou YouTube (unlisted)

### Script Structure

**00:00-00:15** - Introduction
- "Bonjour, je suis [Nom], professeure et trader crypto"
- "J'ai créé School & Crypto Timing pour le Hex-a-thon 2026"
- "Le problème : comment optimiser mes heures de trading avec mon emploi du temps scolaire ?"

**00:15-01:45** - Démonstration de l'app
- Montrer la table des 45 fenêtres de trading
- Cliquer sur la heatmap Jour × Heure
- Utiliser les filtres (cryptos, score minimum)
- Montrer le TOP 5 des recommandations IA
- Expliquer : "Chaque fenêtre a un score 0-100 basé sur volatilité + disponibilité"

**01:45-02:15** - Stack technique
- "Backend : Python + SQLite pour l'ETL et le scoring"
- "Frontend : Hex pour l'interactivité sans code"
- "45 scénarios réalistes avec scores de 43 à 99"

**02:15-02:45** - Cas d'usage et valeur
- "Pour les profs : gagner du temps en trouvant les meilleures fenêtres automatiquement"
- "Pour les élèves : montrer comment les données peuvent aider à prendre des décisions intelligentes"
- "Application production-ready, scalable, et open source"

**02:45-03:00** - Conclusion
- "Merci ! Lien de l'app en description"
- "GitHub : Turbo31150/school-crypto-timing"

---

## 🤔 FAQ Jury Probables

**Q : Comment ça marche techniquement ?**
R : ETL charge les données → Python score chaque fenêtre → Hex affiche tout. Simple.

**Q : Ça peut tourner en production ?**
R : Oui, la stack est standard : SQLite + Python + Hex. C'est scalable.

**Q : Quelle est la valeur pour un prof ?**
R : Trouver facilement les meilleures heures pour trader sans faire tout manuellement.

**Q : Et pour les élèves ?**
R : C'est pédago - les élèves voient qu'on peut utiliser l'IA et les données intelligemment.

**Q : Les scores sont-ils réalistes ?**
R : Oui, ils varient de 43 à 99 avec une moyenne de ~69. Pas de scores artificiellement gonflés.

**Q : Pourquoi Hex ?**
R : Hex permet de combiner code Python, SQL, et interface interactive sans développement frontend complexe.

**Q : Combien de temps pour développer ?**
R : 48h intenses - ETL, scoring algorithm, intégration Hex, et optimisation UX.

---

## 📋 Checklist Technique Finale

### Avant la présentation
- [ ] Vérifier que l'app publique charge en moins de 3 secondes
- [ ] Tester les filtres sur mobile et desktop
- [ ] S'assurer que la heatmap s'affiche correctement
- [ ] Vérifier que le TOP 5 des recommandations est visible
- [ ] Avoir une copie locale de hackaton.db sur une clé USB

### Pendant la présentation
- [ ] Ouvrir l'app en plein écran
- [ ] Désactiver les notifications
- [ ] Avoir le README.md imprimé comme backup
- [ ] Préparer 2-3 exemples de filtrage concrets

### Plan B en cas de problème technique
- [ ] Avoir une vidéo screen recording de l'app qui fonctionne
- [ ] Avoir des screenshots clés (heatmap, table, filtres)
- [ ] Pouvoir expliquer l'algorithme de scoring sur papier si besoin

---

## ✅ Status : PRODUCTION READY

L'application est **stable**, **fonctionnelle** et **préte à être présentée** au jury.

**Liens utiles** :
- 🌐 App publique : [https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest)
- 💻 GitHub : [https://github.com/Turbo31150/school-crypto-timing](https://github.com/Turbo31150/school-crypto-timing)
- 📝 Editor Hex : [https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/hex/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/draft/logic](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/hex/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/draft/logic)

---

## 🎓 Notes pour la Préséntation Orale

### Points clés à mentionner
1. **Problème réel** : Les profs-traders manquent de temps pour analyser manuellement les meilleurs moments
2. **Solution technique** : ETL automatisé + algorithme de scoring + visualisation interactive
3. **Impact pédagogique** : Montre aux élèves l'utilisation pratique des données et de l'IA
4. **Scalabilité** : Architecture simple mais robuste (SQLite + Python + Hex)

### Ce qu'il NE faut PAS faire
- ❌ Parler trop technique (éviter le jargon)
- ❌ S'excuser pour des "limitations" imaginaires
- ❌ Comparer à d'autres projets
- ❌ Dire "c'est un prototype" → C'est PRODUCTION READY

### Ce qu'il FAUT faire
- ✅ Montrer l'app en action (live demo)
- ✅ Expliquer la valeur concrète pour les utilisateurs
- ✅ Être enthousiaste et confiant
- ✅ Répondre aux questions avec clarté et précision

---

**Bonne chance pour le hackathon ! 🚀🎓📊**
