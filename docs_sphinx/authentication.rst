Authentification
================

L'authentification est la première étape pour utiliser l'API Arzeka Payment. Ce guide couvre tout ce que vous devez savoir sur l'authentification.

Vue d'ensemble
--------------

Le processus d'authentification :

1. Vous fournissez vos credentials (username/password)
2. L'API retourne un token d'accès avec une durée de validité
3. Le client stocke le token et les credentials
4. Le token est automatiquement utilisé pour toutes les requêtes
5. Le client se réauthentifie automatiquement si le token expire

Méthodes d'authentification
----------------------------

Méthode 1 : Fonction de convenance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from arzeka import authenticate

   auth = authenticate("your_username", "your_password")

   print(f"Access Token: {auth['access_token']}")
   print(f"Token Type: {auth['token_type']}")
   print(f"Expires In: {auth['expires_in']} seconds")

Méthode 2 : Méthode de classe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from arzeka import ArzekaPayment

   client = ArzekaPayment()
   auth = client.authenticate("your_username", "your_password")

   print(f"Token: {auth['access_token']}")

Réponse d'authentification
---------------------------

L'authentification retourne un dictionnaire contenant :

.. code-block:: python

   {
       'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
       'token_type': 'Bearer',
       'expires_in': 3600  # Durée en secondes
   }

Gestion du token
----------------

Stockage automatique
~~~~~~~~~~~~~~~~~~~~

Le client stocke automatiquement :

- Le token d'accès (``_token``)
- Le timestamp d'expiration (``_expires_at``)
- Les credentials pour réauthentification (``_username``, ``_password``)

.. code-block:: python

   client = ArzekaPayment()
   client.authenticate("username", "password")

   # Le token est stocké automatiquement
   # Vous n'avez pas besoin de le gérer manuellement

Validation du token
~~~~~~~~~~~~~~~~~~~

Vérification simple
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   if client.is_token_valid():
       print("✅ Token est valide")
   else:
       print("❌ Token a expiré")

Vérification avec marge de sécurité
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Considérer le token invalide 5 minutes avant expiration
   if client.is_token_valid(margin_seconds=300):
       print("Token valide pour au moins 5 minutes")

Informations détaillées
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   info = client.get_token_expiry_info()

   print(f"Token valide: {info['is_valid']}")
   print(f"Token expiré: {info['is_expired']}")
   print(f"Expire dans: {info['expires_in_minutes']:.1f} minutes")
   print(f"Expire dans: {info['expires_in_seconds']:.0f} secondes")
   print(f"Timestamp expiration: {info['expires_at']}")
   print(f"A un token: {info['has_token']}")

Réauthentification automatique
-------------------------------

Le client se réauthentifie automatiquement quand nécessaire :

.. code-block:: python

   client = ArzekaPayment()
   client.authenticate("username", "password")

   # Première requête (token valide)
   response1 = client.initiate_payment(...)

   # ... le temps passe, le token expire ...

   # Deuxième requête (token expiré)
   # Le client se RÉAUTHENTIFIE AUTOMATIQUEMENT
   response2 = client.initiate_payment(...)  # ✅ Fonctionne!

Comment ça marche
~~~~~~~~~~~~~~~~~

1. Avant chaque requête, le client vérifie la validité du token
2. Si le token est expiré, le client se réauthentifie automatiquement
3. La requête est ensuite effectuée avec le nouveau token

.. note::
   La réauthentification automatique nécessite que les credentials
   aient été stockés lors de l'authentification initiale.

Sécurité
--------

Utilisation de variables d'environnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Recommandé** : Ne jamais mettre vos credentials dans le code.

.. code-block:: python

   import os
   from arzeka import authenticate

   # Charger depuis l'environnement
   username = os.getenv('ARZEKA_USERNAME')
   password = os.getenv('ARZEKA_PASSWORD')

   auth = authenticate(username, password)

Fichier .env
^^^^^^^^^^^^

.. code-block:: bash

   # .env
   ARZEKA_USERNAME=your_username
   ARZEKA_PASSWORD=your_password
   ARZEKA_MERCHANT_ID=MERCHANT_123
   ARZEKA_HASH_SECRET=your_hash_secret

.. code-block:: python

   # Charger le fichier .env
   from dotenv import load_dotenv
   import os

   load_dotenv()

   username = os.getenv('ARZEKA_USERNAME')
   password = os.getenv('ARZEKA_PASSWORD')

Stockage sécurisé
~~~~~~~~~~~~~~~~~

Les credentials sont stockés :

- ✅ En mémoire uniquement (non persistés sur disque)
- ✅ Dans des attributs privés (``_username``, ``_password``)
- ✅ Supprimés à la fermeture du client

.. code-block:: python

   with ArzekaPayment() as client:
       client.authenticate("user", "pass")
       # ... opérations ...
   # Credentials automatiquement effacés

Gestion d'erreurs
-----------------

Erreur d'authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from arzeka import ArzekaPayment, ArzekaAuthenticationError

   client = ArzekaPayment()

   try:
       client.authenticate("wrong_user", "wrong_pass")
   except ArzekaAuthenticationError as e:
       print(f"Authentification échouée: {e}")
       # Message: "Invalid credentials: username or password is incorrect"

Erreurs courantes
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from arzeka import (
       ArzekaAuthenticationError,
       ArzekaConnectionError,
       ArzekaAPIError
   )

   try:
       auth = client.authenticate(username, password)

   except ArzekaAuthenticationError as e:
       # Credentials invalides ou compte inactif
       print(f"Erreur auth: {e}")

   except ArzekaConnectionError as e:
       # Problème réseau
       print(f"Erreur connexion: {e}")

   except ArzekaAPIError as e:
       # Erreur API avec détails
       print(f"Erreur API: {e}")
       print(f"Code statut: {e.status_code}")
       print(f"Réponse: {e.response_data}")

Token expiré sans credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   client = ArzekaPayment()
   # Définir manuellement un token expiré
   client._token = "expired_token"
   client._expires_at = 0

   try:
       response = client.initiate_payment(...)
   except ArzekaAuthenticationError as e:
       print(e)
       # "Token expired and no credentials stored for automatic re-authentication"

.. warning::
   Toujours utiliser la méthode ``authenticate()`` pour définir le token.
   Ne jamais définir manuellement ``_token`` ou ``_expires_at``.

Bonnes pratiques
----------------

1. **Utiliser les variables d'environnement**

   .. code-block:: python

      username = os.getenv('ARZEKA_USERNAME')
      password = os.getenv('ARZEKA_PASSWORD')

2. **Utiliser le context manager**

   .. code-block:: python

      with ArzekaPayment() as client:
          client.authenticate(username, password)
          # ... opérations ...

3. **Vérifier la validité avant opérations longues**

   .. code-block:: python

      if client.is_token_valid(margin_seconds=300):
          # Au moins 5 minutes restantes
          long_operation()

4. **Gérer les erreurs spécifiquement**

   .. code-block:: python

      try:
          auth = client.authenticate(username, password)
      except ArzekaAuthenticationError:
          # Traiter erreur d'authentification
      except ArzekaConnectionError:
          # Traiter erreur réseau

5. **Activer le logging pour debug**

   .. code-block:: python

      import logging
      logging.basicConfig(level=logging.DEBUG)

Exemples avancés
----------------

Authentication avec retry personnalisé
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from arzeka import ArzekaPayment
   import time

   def authenticate_with_retry(client, username, password, max_retries=3):
       """Authentification avec retry manuel"""
       for attempt in range(max_retries):
           try:
               return client.authenticate(username, password)
           except ArzekaConnectionError as e:
               if attempt < max_retries - 1:
                   wait_time = 2 ** attempt  # Backoff exponentiel
                   print(f"Tentative {attempt + 1} échouée. Retry dans {wait_time}s...")
                   time.sleep(wait_time)
               else:
                   raise

   client = ArzekaPayment()
   auth = authenticate_with_retry(client, "user", "pass")

Vérification périodique du token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   from arzeka import ArzekaPayment

   client = ArzekaPayment()
   client.authenticate("username", "password")

   while True:
       # Opération longue durée
       info = client.get_token_expiry_info()

       if info['expires_in_minutes'] < 5:
           print("⚠️ Token expire bientôt, considérez la réauthentification")

       # Faire quelque chose
       process_batch()

       time.sleep(60)  # Attendre 1 minute

Prochaines étapes
-----------------

- Apprenez à effectuer des :doc:`payment_operations`
- Explorez la :doc:`error_handling`
- Consultez les :doc:`examples/authentication_examples`
