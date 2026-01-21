# 🚀 GUIDE RAPIDE - EXÉCUTION DU NETTOYAGE

## ⚡ Ce qui a été préparé pour vous

✅ **README_OPTIMIZED.md** (167 lignes) - Version professionnelle pour le jury  
✅ **HACKATHON_GUIDE_OPTIMIZED.md** (287 lignes) - Guide enrichi avec FAQ, script vidéo, tips  
✅ **CLEANUP_HACKATHON.ps1** - Script automatisé qui fait tout en 1 clic  
✅ **RAPPORT_NETTOYAGE.json** - Documentation technique complète

---

## 🎯 Comment exécuter le nettoyage (2 MINUTES)

### ÉTAPE 1 : Ouvrir PowerShell

1. Appuyez sur **Windows + X**
2. Cliquez sur **"Windows PowerShell (Admin)"** ou **"Terminal (Admin)"**

> ⚠️ **IMPORTANT** : Vous devez ouvrir PowerShell **en tant qu'administrateur**

---

### ÉTAPE 2 : Naviguer vers le dossier

Dans PowerShell, tapez :

```powershell
cd F:\onedrive\Bureau\hackaton
```

Appuyez sur **Entrée**.

Vous devriez voir quelque chose comme :

```
PS F:\onedrive\Bureau\hackaton>
```

---

### ÉTAPE 3 : Autoriser l'exécution de scripts (si nécessaire)

Si vous n'avez jamais exécuté de script PowerShell, tapez d'abord :

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Appuyez sur **Entrée**, puis tapez **O** (pour Oui) si demandé.

> ℹ️ **Note** : Cette commande est nécessaire une seule fois sur votre PC.

---

### ÉTAPE 4 : Exécuter le script

Tapez :

```powershell
.\CLEANUP_HACKATHON.ps1
```

Appuyez sur **Entrée**.

Le script va :
1. ✅ Vérifier que vous êtes dans un repo Git
2. ✅ Remplacer README.md par la version optimisée
3. ✅ Remplacer HACKATHON_GUIDE.md par la version enrichie
4. ✅ Supprimer 16 fichiers de brouillon
5. ✅ Supprimer le dossier backups/
6. ✅ Faire un `git add .`
7. ✅ Faire un `git commit` avec un message détaillé

---

### ÉTAPE 5 : Confirmer le push

À la fin, le script vous demandera :

```
Voulez-vous PUSHER vers GitHub maintenant ?
  (Cela enverra tous les changements sur le repo distant)
Taper 'oui' pour continuer, 'non' pour arrêter:
```

**Option A** : Tapez **oui** et appuyez sur **Entrée**  
→ Le script fera `git push origin main` automatiquement.

**Option B** : Tapez **non** et appuyez sur **Entrée**  
→ Les changements restent en LOCAL. Vous pourrez pusher manuellement plus tard avec `git push origin main`.

---

### ÉTAPE 6 : Vérifier sur GitHub

1. Allez sur https://github.com/Turbo31150/school-crypto-timing
2. Vérifiez que :
   - ✅ README.md est mis à jour (avec badges et emojis)
   - ✅ HACKATHON_GUIDE.md est enrichi (287 lignes)
   - ✅ Les fichiers de brouillon ont disparu
   - ✅ Le dossier backups/ a disparu

---

## 🎬 CE QUI VA ÊTRE SUPPRIMÉ

Le script va supprimer ces 16 fichiers (brouillons inutiles) :

- EXECUTION_FINAL.md
- HEX_QUICK_START.md
- Hex-a-thon.docx
- LUNDI_PLAN.md
- action_plan_48h.md
- automation_prompt_master.md
- hex_app_improvements.md
- hex_cells_ready.py
- hex_integration_guide.md
- hex_notebook.py
- manual_prompt_optionB.md
- prompt_continuation.md
- run.py
- Le projet School.docx
- HEX_APP_LINKS.txt
- **backups/** (dossier complet)

---

## 🛡️ CE QUI SERA PRÉSERVÉ

**TOUS LES FICHIERS CRITIQUES sont préservés** :

✅ **hackaton.db** (votre base de données - 45 fenêtres)  
✅ **requirements.txt** (dépendances Python)  
✅ **python/** (tous les scripts : etl.py, scoring.py, query_db.py, etc.)  
✅ **sql/** (tous les schémas et requêtes SQL)  
✅ **data/** (vos données brutes)  
✅ **docs/** (votre documentation)  
✅ **HACKATHON_PRESENTATION.md** (vos notes personnelles)

---

## 🆘 EN CAS DE PROBLÈME

### Erreur : "L'exécution de scripts est désactivée"

**Solution** :
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Puis réessayez `.\CLEANUP_HACKATHON.ps1`

---

### Erreur : "Le fichier CLEANUP_HACKATHON.ps1 est introuvable"

**Solution** : Vérifiez que vous êtes dans le bon dossier :
```powershell
Get-Location
```
Devrait afficher : `F:\onedrive\Bureau\hackaton`

Si ce n'est pas le cas :
```powershell
cd F:\onedrive\Bureau\hackaton
```

---

### Je veux annuler et tout restaurer

**Si vous n'avez PAS encore dit "oui" au push** :
```powershell
git reset --hard HEAD~1
```
Cela annulera le commit local.

**Si vous AVEZ déjà pushé sur GitHub** :
1. Allez sur GitHub
2. Cliquez sur "Commits"
3. Trouvez le commit précédent
4. Cliquez sur "Browse files" pour voir l'état avant nettoyage

Ou contactez-moi pour aide !

---

## 📊 APRÈS LE NETTOYAGE

Votre structure finale sera :

```
school-crypto-timing/
├── README.md                          ✅ Optimisé (167 lignes)
├── HACKATHON_GUIDE.md                 ✅ Enrichi (287 lignes)
├── requirements.txt                   ✅ Préservé
├── hackaton.db                        ✅ Préservé (45 fenêtres)
│
├── python/                            ✅ Préservé intact
├── sql/                               ✅ Préservé intact
├── data/                              ✅ Préservé intact
└── docs/                              ✅ Préservé intact
```

**Propre. Professionnel. Prêt pour le jury.** ✨

---

## 🎯 PROCHAINES ÉTAPES

1. ✅ Exécuter le script (c'est ce guide)
2. 📖 Lire le nouveau **HACKATHON_GUIDE.md** (FAQ jury, script vidéo, tips)
3. 🎬 Préparer votre vidéo de présentation (2-3 min)
4. 📱 Tester l'app sur mobile : https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest
5. 🏆 Présenter au hackathon avec confiance !

---

**Durée totale** : < 2 minutes  
**Difficulté** : ⭐ Facile (juste suivre les étapes)  
**Résultat** : Repo GitHub propre et optimisé pour le jury

**Vous êtes prêt(e) ! 🚀**
