# ============================================================
# SCRIPT DE NETTOYAGE GITHUB POUR HACKATHON HEX 2026
# Auteur : Multi-Consensus AI Orchestrator
# Date : Janvier 2026
# ============================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NETTOYAGE REPO HACKATHON HEX 2026" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Naviguer vers le repo
Set-Location "F:\onedrive\Bureau\hackaton"

Write-Host "[1/5] Vérification du repo..." -ForegroundColor Yellow
if (!(Test-Path ".git")) {
    Write-Host "ERREUR : Pas de repo Git trouvé !" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Repo Git trouvé" -ForegroundColor Green
Write-Host ""

# Remplacer les fichiers principaux par les versions optimisées
Write-Host "[2/5] Mise à jour des fichiers principaux..." -ForegroundColor Yellow

Copy-Item "README_OPTIMIZED.md" "README.md" -Force
Write-Host "✓ README.md mis à jour" -ForegroundColor Green

Copy-Item "HACKATHON_GUIDE_OPTIMIZED.md" "HACKATHON_GUIDE.md" -Force
Write-Host "✓ HACKATHON_GUIDE.md mis à jour" -ForegroundColor Green

# Supprimer les fichiers temporaires
Remove-Item "README_OPTIMIZED.md" -Force -ErrorAction SilentlyContinue
Remove-Item "HACKATHON_GUIDE_OPTIMIZED.md" -Force -ErrorAction SilentlyContinue
Write-Host ""

# Supprimer les fichiers inutiles
Write-Host "[3/5] Suppression des fichiers de brouillon..." -ForegroundColor Yellow

$filesToDelete = @(
    "EXECUTION_FINAL.md",
    "HEX_QUICK_START.md",
    "Hex-a-thon.docx",
    "LUNDI_PLAN.md",
    "action_plan_48h.md",
    "automation_prompt_master.md",
    "hex_app_improvements.md",
    "hex_cells_ready.py",
    "hex_integration_guide.md",
    "hex_notebook.py",
    "manual_prompt_optionB.md",
    "prompt_continuation.md",
    "run.py",
    "Le projet School.docx",
    "HEX_APP_LINKS.txt"
)

$deletedCount = 0
foreach ($file in $filesToDelete) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  ✓ Supprimé : $file" -ForegroundColor Gray
        $deletedCount++
    }
}
Write-Host "✓ $deletedCount fichiers supprimés" -ForegroundColor Green
Write-Host ""

# Supprimer le dossier backups
Write-Host "[3b/5] Suppression du dossier backups..." -ForegroundColor Yellow
if (Test-Path "backups") {
    Remove-Item "backups" -Recurse -Force
    Write-Host "✓ Dossier backups/ supprimé" -ForegroundColor Green
} else {
    Write-Host "  (Dossier backups/ déjà absent)" -ForegroundColor Gray
}
Write-Host ""

# Git add all
Write-Host "[4/5] Ajout des modifications à Git..." -ForegroundColor Yellow
git add .
Write-Host "✓ Modifications ajoutées" -ForegroundColor Green
Write-Host ""

# Git commit
Write-Host "[5/5] Commit des changements..." -ForegroundColor Yellow
$commitMessage = "🧹 Nettoyage repo pour Hackathon Hex 2026

- README.md optimisé pour jury
- HACKATHON_GUIDE.md enrichi avec FAQ et script vidéo
- Suppression de $deletedCount fichiers de brouillon
- Suppression du dossier backups/
- Structure finale propre et professionnelle

Status: ✅ PRODUCTION READY"

git commit -m $commitMessage
Write-Host "✓ Commit créé" -ForegroundColor Green
Write-Host ""

# Afficher le statut
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  STATUT FINAL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
git status --short
Write-Host ""

# Demander confirmation pour le push
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "Voulez-vous PUSHER vers GitHub maintenant ?" -ForegroundColor Yellow
Write-Host "  (Cela enverra tous les changements sur le repo distant)" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Yellow
$confirmation = Read-Host "Taper 'oui' pour continuer, 'non' pour arrêter"

if ($confirmation -eq "oui") {
    Write-Host ""
    Write-Host "Push vers GitHub..." -ForegroundColor Yellow
    git push origin main
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ✅ NETTOYAGE TERMINÉ AVEC SUCCÈS !" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Votre repo GitHub est maintenant propre et prêt pour le hackathon !" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Prochaines étapes :" -ForegroundColor White
    Write-Host "  1. Vérifier sur GitHub que tout est OK" -ForegroundColor Gray
    Write-Host "  2. Lire le HACKATHON_GUIDE.md" -ForegroundColor Gray
    Write-Host "  3. Préparer votre vidéo de présentation" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "  PUSH ANNULÉ" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Les changements sont commités en LOCAL uniquement." -ForegroundColor Gray
    Write-Host "Pour pusher plus tard, tapez : git push origin main" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
