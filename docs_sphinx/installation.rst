Installation
============

Prérequis
---------

Avant d'installer Arzeka Payment, assurez-vous d'avoir :

1. **Python 3.9 ou supérieur**

.. code-block:: bash

   python --version  # Doit afficher Python 3.9.x ou supérieur

2. **Un compte API Arzeka Money** avec :

   - Username
   - Password
   - Hash Secret
   - Merchant ID

3. **Certificats SSL** (si fournis par l'opérateur)

Dépendances
-----------

Le client nécessite les packages suivants :

.. code-block:: text

   requests>=2.31.0
   setuptools
   urllib3

Ces dépendances seront automatiquement installées.

Installation via pip
--------------------

Depuis GitHub
~~~~~~~~~~~~~

.. code-block:: bash

   pip install git+https://github.com/parice02/fasoarzeka.git

Installation via Poetry
-----------------------

.. code-block:: bash

   poetry add git+https://github.com/parice02/fasoarzeka.git

Installation en mode développement
-----------------------------------

Pour contribuer au projet ou modifier le code :

.. code-block:: bash

   # Cloner le repository
   git clone https://github.com/parice02/fasoarzeka.git
   cd fasoarzeka

   # Installer en mode éditable
   pip install -e .

   # Ou avec poetry
   poetry install

Installation des dépendances de développement
----------------------------------------------

Pour installer les dépendances de développement (tests, documentation, etc.) :

.. code-block:: bash

   pip install -e ".[dev]"

Vérification de l'installation
-------------------------------

Vérifiez que l'installation a réussi :

.. code-block:: python

   import arzeka
   print(arzeka.__version__)
   # Devrait afficher: 1.0.0

Configuration initiale
----------------------

Variables d'environnement
~~~~~~~~~~~~~~~~~~~~~~~~~~

Il est recommandé d'utiliser des variables d'environnement pour stocker vos credentials :

.. code-block:: bash

   # Créez un fichier .env
   cat > .env << EOF
   ARZEKA_USERNAME=your_username
   ARZEKA_PASSWORD=your_password
   ARZEKA_MERCHANT_ID=MERCHANT_123
   ARZEKA_HASH_SECRET=your_hash_secret
   ARZEKA_BASE_URL=https://pwg-test.fasoarzeka.com/AvepayPaymentGatewayUI/avepay-payment/
   EOF

Utilisation des variables d'environnement :

.. code-block:: python

   import os
   from arzeka import ArzekaPayment

   client = ArzekaPayment(
       base_url=os.getenv('ARZEKA_BASE_URL')
   )

   client.authenticate(
       os.getenv('ARZEKA_USERNAME'),
       os.getenv('ARZEKA_PASSWORD')
   )

Environnements Test et Production
----------------------------------

Environnement de test (par défaut)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from arzeka import ArzekaPayment

   # Utilise l'URL de test par défaut
   client = ArzekaPayment()

Environnement de production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from arzeka import ArzekaPayment

   # Spécifiez l'URL de production
   client = ArzekaPayment(
       base_url="https://pwg.fasoarzeka.com/..."
   )

.. warning::
   Assurez-vous de tester votre intégration dans l'environnement de test
   avant de passer en production.

Prochaines étapes
-----------------

- Consultez le :doc:`quickstart` pour commencer rapidement
- Lisez le guide sur :doc:`authentication` pour configurer l'authentification
- Explorez les :doc:`examples/basic_usage` pour voir des exemples concrets
