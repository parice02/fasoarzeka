Bienvenue dans la documentation d'Arzeka Payment
================================================

.. image:: https://img.shields.io/badge/python-3.9+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.9+

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: ../LICENSE
   :alt: License: MIT

**Arzeka Payment** est un client Python non officiel pour l'API de paiement mobile FASO ARZEKA au Burkina Faso.

Le client est conçu pour être robuste et production-ready avec gestion automatique des erreurs, retry automatique, et réauthentification automatique des tokens.

✨ Fonctionnalités principales
------------------------------

- ✅ **Authentification sécurisée** avec gestion automatique des tokens
- ✅ **Réauthentification automatique** quand le token expire
- ✅ **Gestion complète des erreurs** avec exceptions personnalisées
- ✅ **Retry automatique** avec backoff exponentiel
- ✅ **Logging intégré** pour traçabilité complète
- ✅ **Session persistante** pour meilleures performances
- ✅ **Type hints complets** pour meilleure auto-complétion
- ✅ **Context manager** pour gestion automatique des ressources
- ✅ **Validation des tokens** avec informations d'expiration
- ✅ **Tests unitaires complets** avec couverture >90%

🚀 Démarrage rapide
-------------------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   # Avec pip
   pip install git+https://github.com/parice02/fasoarzeka.git

   # Avec poetry
   poetry add git+https://github.com/parice02/fasoarzeka.git

Premier exemple
~~~~~~~~~~~~~~~

.. code-block:: python

   from arzeka import authenticate, initiate_payment, check_payment

   # 1. Authentifiez-vous une fois
   auth = authenticate("your_username", "your_password")
   print(f"Token expires in: {auth['expires_in']} seconds")

   # 2. Initiez un paiement
   payment_data = {
       "amount": 1000,
       "merchant_id": "MERCHANT_123",
       "additional_info": {
           "first_name": "Jean",
           "last_name": "Dupont",
           "mobile": "70123456"
       },
       "hash_secret": "your_hash_secret",
       "link_for_update_status": "https://example.com/webhook",
       "link_back_to_calling_website": "https://example.com/return"
   }

   response = initiate_payment(payment_data)
   print(f"Payment initiated: {response['mappedOrderId']}")

   # 3. Vérifiez le statut du paiement
   status = check_payment(response['mappedOrderId'])
   print(f"Payment status: {status}")

📚 Table des matières
---------------------

.. toctree::
   :maxdepth: 2
   :caption: Guide utilisateur

   installation
   quickstart
   authentication
   payment_operations
   error_handling
   advanced_features

.. toctree::
   :maxdepth: 2
   :caption: Référence API

   api/modules
   api/arzeka
   api/utils
   api/exceptions

.. toctree::
   :maxdepth: 1
   :caption: Exemples

   examples/basic_usage
   examples/authentication_examples
   examples/payment_examples
   examples/error_handling_examples

.. toctree::
   :maxdepth: 1
   :caption: Développement

   contributing
   changelog
   license

📞 Support
----------

- **Issues**: `GitHub Issues <https://github.com/parice02/fasoarzeka/issues>`_
- **Email**: m.zeba@mzeba.dev
- **Documentation**: `GitHub Wiki <https://github.com/parice02/fasoarzeka/wiki>`_

Indices et tables
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
