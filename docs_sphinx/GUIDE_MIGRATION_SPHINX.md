# Guide : Réutiliser la documentation Sphinx dans un nouveau projet

## 🎯 Objectif

Ce guide vous montre comment adapter cette documentation Sphinx/ReadTheDocs pour un nouveau projet Python.

## 📋 Prérequis

- Python 3.9+
- Un projet Python avec code documenté (docstrings)
- Git (optionnel, pour ReadTheDocs)

## 🚀 Méthode 1 : Copie complète et adaptation

### Étape 1 : Copier les fichiers

Copiez tout le dossier `docs_sphinx/` dans votre nouveau projet :

```bash
# Depuis le projet Arzeka Payment
cp -r docs_sphinx /chemin/vers/nouveau_projet/

# Ou via Git si vous avez cloné ce projet
cd /chemin/vers/nouveau_projet
git clone https://github.com/parice02/fasoarzeka.git temp
cp -r temp/docs_sphinx ./
rm -rf temp
```

### Étape 2 : Modifier `conf.py`

Éditez `docs_sphinx/conf.py` pour adapter à votre projet :

```python
# Configuration de base à modifier
project = 'Votre Nom de Projet'           # ← Changez ici
copyright = '2025, Votre Nom'             # ← Changez ici
author = 'Votre Nom'                      # ← Changez ici
release = '1.0.0'                         # ← Version de votre projet

# Vérifiez le path vers votre code source
sys.path.insert(0, os.path.abspath('..'))  # ← Ajustez si nécessaire
```

### Étape 3 : Adapter `index.rst`

Éditez `docs_sphinx/index.rst` :

```rst
Bienvenue dans la documentation de Votre Projet
================================================

.. image:: https://img.shields.io/badge/python-3.9+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.9+

**Votre Projet** est... [description de votre projet]

✨ Fonctionnalités principales
------------------------------

- ✅ Fonctionnalité 1
- ✅ Fonctionnalité 2
- ✅ Fonctionnalité 3

🚀 Démarrage rapide
-------------------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install votre-projet

Premier exemple
~~~~~~~~~~~~~~~

.. code-block:: python

   from votre_projet import votre_fonction

   result = votre_fonction()

📚 Table des matières
---------------------

.. toctree::
   :maxdepth: 2
   :caption: Guide utilisateur

   installation
   quickstart
   # ... Adaptez selon vos besoins
```

### Étape 4 : Adapter les fichiers de documentation

Modifiez chaque fichier `.rst` selon votre projet :

#### `installation.rst`

```rst
Installation
============

Prérequis
---------

Votre projet nécessite :

1. **Python 3.9 ou supérieur**
2. [Listez vos prérequis]

Dépendances
-----------

.. code-block:: text

   [vos dépendances depuis requirements.txt]

Installation via pip
--------------------

.. code-block:: bash

   pip install votre-projet
```

#### `quickstart.rst`

Adaptez les exemples de code avec votre API.

#### `api/modules.rst`

Changez les noms de modules :

```rst
Modules Python
==============

.. toctree::
   :maxdepth: 4

   votre_module         # ← Changez ici
   votre_autre_module   # ← Ajoutez vos modules
```

### Étape 5 : Créer les fichiers API autodoc

Pour chaque module de votre projet, créez un fichier `.rst` :

**Exemple : `docs_sphinx/api/mon_module.rst`**

```rst
Module mon_module
=================

.. automodule:: mon_module
   :members:
   :undoc-members:
   :show-inheritance:

Classes principales
-------------------

MaClasse
~~~~~~~~

.. autoclass:: mon_module.MaClasse
   :members:
   :undoc-members:
   :show-inheritance:

Fonctions
---------

ma_fonction
~~~~~~~~~~~

.. autofunction:: mon_module.ma_fonction
```

### Étape 6 : Adapter `.readthedocs.yaml`

Copiez à la racine de votre projet et modifiez :

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.9"

sphinx:
  configuration: docs_sphinx/conf.py
  fail_on_warning: false

formats:
  - pdf
  - epub

python:
  install:
    - requirements: docs_sphinx/requirements.txt
    - requirements: requirements.txt
    - method: pip
      path: .
```

### Étape 7 : Tester localement

```bash
cd docs_sphinx
pip install -r requirements.txt
make html
# Ouvrir _build/html/index.html
```

## 🔧 Méthode 2 : Création à partir de zéro (avec template)

### Étape 1 : Initialiser Sphinx

```bash
cd votre_projet
mkdir docs
cd docs
sphinx-quickstart
```

Répondez aux questions :

```
> Separate source and build directories (y/n) [n]: n
> Project name: Votre Projet
> Author name(s): Votre Nom
> Project release []: 1.0.0
> Project language [en]: fr
```

### Étape 2 : Installer le thème ReadTheDocs

```bash
pip install sphinx-rtd-theme
```

### Étape 3 : Configurer `conf.py`

Ajoutez au fichier `docs/conf.py` généré :

```python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

html_theme = 'sphinx_rtd_theme'

# Napoleon settings pour docstrings Google/NumPy
napoleon_google_docstring = True
napoleon_numpy_docstring = True
```

### Étape 4 : Copier les fichiers utiles du template

Copiez depuis le projet Arzeka Payment :

```bash
# Structure de base
cp -r /chemin/arzeka-payment/docs_sphinx/_static docs/
cp -r /chemin/arzeka-payment/docs_sphinx/_templates docs/
cp /chemin/arzeka-payment/docs_sphinx/Makefile docs/

# Fichiers de documentation (à adapter)
cp /chemin/arzeka-payment/docs_sphinx/installation.rst docs/
cp /chemin/arzeka-payment/docs_sphinx/quickstart.rst docs/
# etc.
```

### Étape 5 : Adapter les fichiers copiés

Modifiez chaque fichier `.rst` pour votre projet.

## 📝 Structure recommandée

```
votre_projet/
├── votre_module/
│   ├── __init__.py
│   ├── main.py
│   └── utils.py
├── docs_sphinx/  (ou docs/)
│   ├── conf.py
│   ├── index.rst
│   ├── installation.rst
│   ├── quickstart.rst
│   ├── Makefile
│   ├── requirements.txt
│   ├── api/
│   │   ├── modules.rst
│   │   └── votre_module.rst
│   ├── examples/
│   │   └── basic_usage.rst
│   ├── _static/
│   │   └── custom.css
│   └── _templates/
├── tests/
├── requirements.txt
├── setup.py
├── README.md
└── .readthedocs.yaml
```

## 🎨 Personnalisation

### Changer le logo

1. Ajoutez votre logo dans `docs_sphinx/_static/logo.png`
2. Dans `conf.py` :

```python
html_logo = '_static/logo.png'
html_theme_options = {
    'logo_only': True,
}
```

### Changer les couleurs

1. Éditez `docs_sphinx/_static/custom.css`
2. Ajoutez dans `conf.py` :

```python
html_css_files = ['custom.css']
```

### Ajouter un favicon

```python
# conf.py
html_favicon = '_static/favicon.ico'
```

## 📚 Écrire la documentation

### Docstrings dans le code

Utilisez le format Google ou NumPy :

```python
def ma_fonction(param1: str, param2: int) -> dict:
    """
    Description courte de la fonction.

    Description plus détaillée si nécessaire.

    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2

    Returns:
        Description du retour

    Raises:
        ValueError: Quand param2 est négatif

    Example:
        >>> ma_fonction("test", 42)
        {'result': 'success'}
    """
    if param2 < 0:
        raise ValueError("param2 doit être positif")
    return {'result': 'success'}
```

### Fichiers RST

Syntaxe de base :

```rst
Titre Principal
===============

Sous-titre
----------

Paragraphe normal avec du texte.

Liste à puces
~~~~~~~~~~~~~

- Item 1
- Item 2
- Item 3

Liste numérotée
~~~~~~~~~~~~~~~

1. Premier
2. Deuxième
3. Troisième

Bloc de code Python
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from mon_module import ma_fonction

   result = ma_fonction("hello", 42)

Bloc de code bash
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install mon-package

Notes
~~~~~

.. note::
   Ceci est une note importante.

.. warning::
   Ceci est un avertissement.

.. tip::
   Ceci est un conseil.

Liens
~~~~~

- Lien externe : `GitHub <https://github.com>`_
- Lien interne : :doc:`installation`
- Référence API : :class:`mon_module.MaClasse`

Tables
~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Colonne 1
     - Colonne 2
   * - Valeur 1
     - Valeur 2
```

## 🌐 Déployer sur ReadTheDocs

### Configuration

1. Créez un compte sur [readthedocs.org](https://readthedocs.org)
2. Importez votre repository GitHub/GitLab/Bitbucket
3. ReadTheDocs détecte automatiquement `.readthedocs.yaml`
4. Build automatique à chaque push

### Fichier `.readthedocs.yaml` à la racine

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

## ✅ Checklist de migration

- [ ] Copier `docs_sphinx/` dans votre projet
- [ ] Modifier `conf.py` (project, author, release)
- [ ] Adapter `index.rst` avec votre description
- [ ] Modifier `installation.rst` avec vos prérequis
- [ ] Adapter `quickstart.rst` avec vos exemples
- [ ] Créer les fichiers API pour vos modules
- [ ] Supprimer les fichiers non pertinents (authentication.rst, etc.)
- [ ] Ajouter vos propres guides selon vos besoins
- [ ] Personnaliser le CSS si désiré
- [ ] Copier `.readthedocs.yaml` à la racine
- [ ] Tester localement : `make html`
- [ ] Commit et push sur GitHub
- [ ] Configurer ReadTheDocs

## 🔧 Commandes utiles

```bash
# Générer la documentation
cd docs_sphinx
make html

# Mode développement avec auto-reload
make livehtml

# Nettoyer
make clean

# Vérifier les liens
make linkcheck

# Générer PDF
make latexpdf
```

## 📦 Fichiers minimaux requis

Pour un projet minimal, vous avez besoin de :

```
docs_sphinx/
├── conf.py          # Configuration Sphinx
├── index.rst        # Page d'accueil
├── Makefile         # Automation
└── requirements.txt # Dépendances Sphinx
```

Le reste est optionnel et peut être ajouté progressivement.

## 💡 Conseils

1. **Commencez simple** : Créez d'abord `index.rst` et `installation.rst`
2. **Utilisez autodoc** : Laissez Sphinx générer la doc depuis vos docstrings
3. **Testez souvent** : `make html` après chaque modification
4. **Versionnez** : Committez la documentation avec le code
5. **Automatisez** : Utilisez ReadTheDocs pour build automatique

## 🆘 Problèmes courants

### Module not found

```python
# Dans conf.py, ajustez le path
sys.path.insert(0, os.path.abspath('..'))
# ou
sys.path.insert(0, os.path.abspath('../..'))
```

### Warnings Sphinx

Vérifiez la syntaxe RST avec :

```bash
sphinx-build -W docs_sphinx docs_sphinx/_build/html
```

### Theme non trouvé

```bash
pip install sphinx-rtd-theme
```

## 📚 Ressources

- [Documentation Sphinx](https://www.sphinx-doc.org/)
- [Guide RST](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [ReadTheDocs Guide](https://docs.readthedocs.io/)
- [Theme RTD](https://sphinx-rtd-theme.readthedocs.io/)

## 🎉 Résultat

Vous aurez une documentation professionnelle style ReadTheDocs pour votre projet !

---

**Astuce** : Gardez ce template Arzeka Payment comme référence pour vos futurs projets Python !
