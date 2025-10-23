# Guide rapide de la documentation

## 🎯 Objectif

Cette documentation style ReadTheDocs fournit une référence complète et professionnelle pour le client Arzeka Payment.

## 📦 Installation

```bash
cd docs_sphinx
pip install -r requirements.txt
```

## 🚀 Génération

### Méthode rapide

```bash
./build.sh
```

### Méthode manuelle

```bash
make html
```

### Résultat

La documentation sera disponible dans `_build/html/index.html`

## 🔍 Contenu

### Structure

```
docs_sphinx/
├── index.rst              # Page d'accueil
├── installation.rst       # Guide d'installation
├── quickstart.rst         # Démarrage rapide
├── authentication.rst     # Authentification
├── payment_operations.rst # Opérations de paiement
├── error_handling.rst     # Gestion d'erreurs
├── advanced_features.rst  # Fonctionnalités avancées
├── api/                   # Référence API
│   ├── modules.rst
│   ├── arzeka.rst        # Module principal
│   ├── utils.rst         # Utilitaires
│   └── exceptions.rst    # Exceptions
├── examples/              # Exemples
│   ├── basic_usage.rst
│   ├── authentication_examples.rst
│   ├── payment_examples.rst
│   └── error_handling_examples.rst
├── contributing.rst       # Contribution
├── changelog.rst          # Historique
└── license.rst           # Licence
```

### Fonctionnalités

- ✅ **Theme ReadTheDocs** - Design professionnel
- ✅ **Autodoc** - Documentation automatique depuis le code
- ✅ **Napoleon** - Support Google/NumPy docstrings
- ✅ **Intersphinx** - Liens vers docs Python/Requests
- ✅ **Viewcode** - Voir le code source
- ✅ **CSS personnalisé** - Style amélioré
- ✅ **Recherche** - Index de recherche intégré
- ✅ **Navigation** - Sidebar avec TOC
- ✅ **Mobile-friendly** - Responsive design

## 📝 Modification

### Ajouter une page

1. Créez un fichier `.rst` dans `docs_sphinx/`
2. Ajoutez-le dans `index.rst` sous `toctree`
3. Régénérez avec `make html`

### Modifier le style

Éditez `_static/custom.css`

### Modifier la configuration

Éditez `conf.py`

## 🌐 Déploiement ReadTheDocs

### Configuration

1. Créez un compte sur readthedocs.org
2. Importez votre repo GitHub
3. ReadTheDocs détectera automatiquement `docs_sphinx/conf.py`

### Fichier `.readthedocs.yaml`

Créez à la racine du projet :

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.9"

sphinx:
  configuration: docs_sphinx/conf.py

python:
  install:
    - requirements: docs_sphinx/requirements.txt
    - requirements: requirements.txt
```

### Résultat

Votre documentation sera accessible sur :
`https://arzeka-payment.readthedocs.io`

## 💡 Conseils

### Mode développement

```bash
make livehtml
```

Ouvre un serveur avec auto-reload sur `http://127.0.0.1:8000`

### Nettoyer

```bash
make clean
```

### Vérifier les liens

```bash
make linkcheck
```

### Autres formats

```bash
make latexpdf  # PDF
make epub      # ePub
make man       # Man pages
```

## 🎨 Personnalisation

### Logo

Ajoutez votre logo dans `_static/logo.png` et configurez :

```python
# conf.py
html_logo = '_static/logo.png'
html_theme_options = {
    'logo_only': True,
}
```

### Couleurs

Créez `_static/theme_overrides.css` :

```css
.wy-side-nav-search {
    background-color: #2c3e50;
}
```

### Favicon

```python
# conf.py
html_favicon = '_static/favicon.ico'
```

## 📊 Génération automatique

### GitHub Actions

Créez `.github/workflows/docs.yml` :

```yaml
name: Documentation

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: |
          cd docs_sphinx
          pip install -r requirements.txt
          make html
      - uses: actions/upload-artifact@v2
        with:
          name: documentation
          path: docs_sphinx/_build/html
```

## 🔧 Troubleshooting

### Erreur "Module not found"

```bash
# Assurez-vous que le path est correct
sys.path.insert(0, os.path.abspath('..'))
```

### Warnings Sphinx

Vérifiez que tous les fichiers `.rst` sont bien formés

### Build échoue

```bash
make clean
make html
```

## 📚 Ressources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [ReadTheDocs Guide](https://docs.readthedocs.io/)
- [ReStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [RTD Theme](https://sphinx-rtd-theme.readthedocs.io/)

## ✨ Résultat final

Une documentation professionnelle, complète et facile à maintenir ! 🎉
