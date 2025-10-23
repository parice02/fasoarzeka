Contributing
============

Nous apprécions toutes les contributions ! Voici comment contribuer au projet Arzeka Payment.

Guide de contribution
---------------------

1. **Fork** le repository
2. **Créez** une branche pour votre fonctionnalité
3. **Committez** vos changements
4. **Pushez** vers votre fork
5. **Ouvrez** une Pull Request

Processus détaillé
-------------------

Fork et clone
~~~~~~~~~~~~~

.. code-block:: bash

   # Fork sur GitHub, puis clonez
   git clone https://github.com/VOTRE_USERNAME/fasoarzeka.git
   cd fasoarzeka

Configuration de l'environnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Créez un environnement virtuel
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows

   # Installez en mode développement
   pip install -e ".[dev]"

Créez une branche
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git checkout -b feature/ma-nouvelle-fonctionnalite

Faites vos modifications
~~~~~~~~~~~~~~~~~~~~~~~~~

- Suivez le style de code existant
- Ajoutez des tests pour les nouvelles fonctionnalités
- Mettez à jour la documentation

Testez vos modifications
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Exécutez les tests
   pytest test/

   # Vérifiez le style
   flake8 arzeka.py utils.py

   # Vérifiez les types
   mypy arzeka.py

Committez
~~~~~~~~~

.. code-block:: bash

   git add .
   git commit -m "Add: Description de la fonctionnalité"

   # Utilisez des préfixes conventionnels:
   # Add: Nouvelle fonctionnalité
   # Fix: Correction de bug
   # Doc: Documentation
   # Test: Tests
   # Refactor: Refactorisation

Pushez et ouvrez une PR
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git push origin feature/ma-nouvelle-fonctionnalite

Puis ouvrez une Pull Request sur GitHub.

Guidelines de code
------------------

Style
~~~~~

- Suivez PEP 8
- Utilisez des type hints
- Docstrings Google style
- Maximum 88 caractères par ligne

Exemple :

.. code-block:: python

   def ma_fonction(param1: str, param2: int) -> Dict[str, Any]:
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

Tests
~~~~~

- Ajoutez des tests pour toute nouvelle fonctionnalité
- Visez une couverture > 90%
- Utilisez pytest
- Tests unitaires dans `test/test.py`

.. code-block:: python

   def test_ma_nouvelle_fonctionnalite():
       """Test de ma nouvelle fonctionnalité"""
       result = ma_fonction("test", 42)
       assert result['result'] == 'success'

Documentation
~~~~~~~~~~~~~

- Mettez à jour les docstrings
- Ajoutez des exemples
- Mettez à jour README.md si nécessaire
- Ajoutez une entrée dans CHANGELOG.md

Types de contributions
----------------------

Correction de bugs
~~~~~~~~~~~~~~~~~~

1. Ouvrez une issue décrivant le bug
2. Créez une branche `fix/nom-du-bug`
3. Ajoutez un test reproduisant le bug
4. Corrigez le bug
5. Vérifiez que tous les tests passent
6. Ouvrez une PR

Nouvelles fonctionnalités
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Ouvrez une issue pour discuter de la fonctionnalité
2. Attendez l'approbation
3. Créez une branche `feature/nom-fonctionnalite`
4. Implémentez la fonctionnalité
5. Ajoutez des tests
6. Mettez à jour la documentation
7. Ouvrez une PR

Documentation
~~~~~~~~~~~~~

- Corrections de typos
- Améliorations de clarté
- Ajout d'exemples
- Traductions

Toujours les bienvenues !

Processus de review
-------------------

1. Un mainteneur reviewera votre PR
2. Des changements peuvent être demandés
3. Une fois approuvée, la PR sera mergée
4. Votre contribution sera créditée

Questions ?
-----------

- Ouvrez une issue
- Contactez: m.zeba@mzeba.dev

Merci de contribuer ! 🎉
