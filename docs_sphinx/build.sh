#!/bin/bash

# Script de build pour la documentation Arzeka Payment

echo "🚀 Construction de la documentation Arzeka Payment"
echo "=================================================="

# Vérifier si Sphinx est installé
if ! command -v sphinx-build &> /dev/null; then
    echo "❌ Sphinx n'est pas installé"
    echo "📦 Installation de Sphinx..."
    pip install -r requirements.txt
fi

# Se placer dans le dossier docs_sphinx
cd "$(dirname "$0")"

# Nettoyer les anciens builds
echo "🧹 Nettoyage des anciens builds..."
make clean

# Générer la documentation HTML
echo "📚 Génération de la documentation HTML..."
make html

# Vérifier si la génération a réussi
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Documentation générée avec succès!"
    echo "📂 Emplacement: _build/html/index.html"
    echo ""
    echo "Pour visualiser:"
    echo "  - Linux/Mac: open _build/html/index.html"
    echo "  - Windows: start _build/html/index.html"
    echo "  - Ou naviguez manuellement vers le fichier"
    echo ""
    echo "Pour mode développement avec auto-reload:"
    echo "  make livehtml"
else
    echo ""
    echo "❌ Erreur lors de la génération"
    exit 1
fi
