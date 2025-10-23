# Documentation Arzeka Payment

Documentation complète style ReadTheDocs pour le client Arzeka Payment.

## Installation des dépendances

```bash
pip install -r requirements.txt
```

## Générer la documentation

### HTML

```bash
make html
```

La documentation sera générée dans `_build/html/`. Ouvrez `_build/html/index.html` dans votre navigateur.

### PDF

```bash
make latexpdf
```

### Autres formats

```bash
make help  # Voir tous les formats disponibles
```

## Mode développement avec auto-reload

```bash
make livehtml
```

La documentation sera accessible sur `http://127.0.0.1:8000` et se rechargera automatiquement à chaque modification.

## Nettoyage

```bash
make clean
```

## Structure

```
docs_sphinx/
├── conf.py                 # Configuration Sphinx
├── index.rst              # Page d'accueil
├── installation.rst       # Guide d'installation
├── quickstart.rst         # Démarrage rapide
├── authentication.rst     # Guide authentification
├── payment_operations.rst # Opérations de paiement
├── error_handling.rst     # Gestion d'erreurs
├── advanced_features.rst  # Fonctionnalités avancées
├── api/                   # Référence API
│   ├── modules.rst
│   ├── arzeka.rst
│   ├── utils.rst
│   └── exceptions.rst
├── examples/              # Exemples de code
│   ├── basic_usage.rst
│   ├── authentication_examples.rst
│   ├── payment_examples.rst
│   └── error_handling_examples.rst
├── contributing.rst       # Guide de contribution
├── changelog.rst          # Historique des versions
└── license.rst           # Licence
```

## Déploiement sur ReadTheDocs

1. Créez un compte sur [ReadTheDocs.org](https://readthedocs.org/)
2. Importez votre repository GitHub
3. ReadTheDocs détectera automatiquement `docs_sphinx/conf.py`
4. La documentation sera disponible sur `https://votre-projet.readthedocs.io`

## Personnalisation

Modifiez `conf.py` pour personnaliser :

- Le thème
- Les extensions
- Les couleurs
- Le logo
- Etc.
