Internationalisation (i18n) — guide rapide

Ce dépôt utilise la bibliothèque standard `gettext` pour la traduction des messages renvoyés par la librairie.

Fichiers importants
- `locales/arzeka.pot` : template POT (extrait des sources)
- `locales/fr/LC_MESSAGES/arzeka.po` : traduction française (fichier PO)
- `scripts/extract_messages.sh` : script d'extraction (xgettext)
- `scripts/compile_messages.sh` : script de compilation (.po -> .mo)

Extraire les messages
- Installez les outils gettext (xgettext/msgfmt) sur votre système si nécessaire.
- Exécutez :

```bash
./scripts/extract_messages.sh
```

Créer / mettre à jour une traduction
- Après extraction, créez un répertoire `locales/<lang>/LC_MESSAGES/` et placez-y le fichier `<domain>.po`.
- Pour initialiser un fichier .po à partir du .pot :

```bash
mkdir -p locales/fr/LC_MESSAGES
msginit -i locales/arzeka.pot -o locales/fr/LC_MESSAGES/arzeka.po --locale=fr
```

Compiler les traductions
- Pour compiler toutes les `.po` en `.mo` :

```bash
./scripts/compile_messages.sh
```

Helper fourni par la librairie
---------------------------------
La librairie fournit un helper pratique `install_translations(lang=None)` que vous pouvez appeler
pour installer automatiquement la traduction fournie par le package. Exemple :
```python
from fasoarzeka import install_translations

# Installe la traduction française (cherche dans fasoarzeka/locales)
install_translations('fr')

# Ou laisse la fonction choisir la langue système
install_translations()
```
La fonction utilise `importlib.resources` pour localiser le répertoire `locales` installé
dans le package `fasoarzeka` et appelle `gettext.translation(...).install()`.
Packaging
---------
Les fichiers `.mo` (et `.po` si présents) sont inclus dans le package via la configuration
setuptools (`pyproject.toml`) sous `tool.setuptools.package-data`, donc lorsque vous
installez la librairie (`pip install fasoarzeka` ou `pip install .`), le répertoire
`fasoarzeka/locales` est présent et `install_translations()` peut charger les fichiers.
Utiliser les traductions dans votre application
 Dans l'application qui consomme la librairie, chargez le domaine et le répertoire de locales, par exemple :

```python
import gettext
gettext.bindtextdomain('arzeka', '/chemin/vers/locales')
gettext.textdomain('arzeka')
# Depuis ce point, gettext.gettext (alias _) renverra les traductions.
```

Notes
- Le domaine utilisé dans cet exemple est `arzeka`.
- Si vous modifiez les chaînes sources, ré-exécutez `extract_messages.sh`, mettez à jour les `.po` et recompilez.
