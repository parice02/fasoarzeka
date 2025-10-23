Exceptions
==========

Le module Arzeka Payment fournit plusieurs exceptions personnalisées pour une gestion d'erreurs précise.

Hiérarchie des exceptions
--------------------------

.. code-block:: text

   Exception
   └── ArzekaPaymentError (base)
       ├── ArzekaConnectionError
       ├── ArzekaValidationError
       ├── ArzekaAPIError
       └── ArzekaAuthenticationError

ArzekaPaymentError
------------------

Exception de base pour toutes les erreurs Arzeka.

.. autoexception:: arzeka.ArzekaPaymentError
   :members:
   :show-inheritance:

**Quand l'utiliser** : Pour capturer n'importe quelle erreur liée à Arzeka Payment.

.. code-block:: python

   from arzeka import ArzekaPayment, ArzekaPaymentError

   try:
       client = ArzekaPayment()
       # ... opérations ...
   except ArzekaPaymentError as e:
       print(f"Erreur Arzeka: {e}")

ArzekaConnectionError
---------------------

Exception levée en cas de problème de connexion réseau.

.. autoexception:: arzeka.ArzekaConnectionError
   :members:
   :show-inheritance:

**Causes courantes** :

- Pas de connexion internet
- Serveur Arzeka inaccessible
- Timeout de connexion
- Problèmes DNS

**Exemple** :

.. code-block:: python

   from arzeka import ArzekaConnectionError

   try:
       response = client.initiate_payment(...)
   except ArzekaConnectionError as e:
       print("Vérifiez votre connexion internet")
       # Réessayer plus tard ou utiliser un fallback

ArzekaValidationError
---------------------

Exception levée quand les données fournies sont invalides.

.. autoexception:: arzeka.ArzekaValidationError
   :members:
   :show-inheritance:

**Causes courantes** :

- Montant invalide (< 100 FCFA)
- Numéro de téléphone invalide
- Champs requis manquants
- Format de données incorrect

**Exemple** :

.. code-block:: python

   from arzeka import ArzekaValidationError

   try:
       response = client.initiate_payment(
           amount=50,  # Trop petit!
           merchant_id="MERCHANT_123",
           ...
       )
   except ArzekaValidationError as e:
       print(f"Données invalides: {e}")
       # Corriger les données et réessayer

ArzekaAPIError
--------------

Exception levée quand l'API Arzeka retourne une erreur.

.. autoexception:: arzeka.ArzekaAPIError
   :members:
   :show-inheritance:

**Attributs supplémentaires** :

- ``status_code`` : Code de statut HTTP
- ``response_data`` : Données de réponse de l'API

**Exemple** :

.. code-block:: python

   from arzeka import ArzekaAPIError

   try:
       response = client.initiate_payment(...)
   except ArzekaAPIError as e:
       print(f"Erreur API: {e}")
       print(f"Code statut: {e.status_code}")
       print(f"Réponse: {e.response_data}")

       if e.status_code == 400:
           print("Requête invalide")
       elif e.status_code == 500:
           print("Erreur serveur")

ArzekaAuthenticationError
-------------------------

Exception levée en cas de problème d'authentification.

.. autoexception:: arzeka.ArzekaAuthenticationError
   :members:
   :show-inheritance:

**Causes courantes** :

- Credentials invalides
- Token expiré sans credentials stockés
- Compte verrouillé ou inactif
- Réauthentification échouée

**Exemple** :

.. code-block:: python

   from arzeka import ArzekaAuthenticationError

   try:
       client.authenticate("user", "wrong_password")
   except ArzekaAuthenticationError as e:
       print(f"Authentification échouée: {e}")
       # Demander à l'utilisateur de réessayer

Gestion globale des erreurs
----------------------------

Exemple complet
~~~~~~~~~~~~~~~

.. code-block:: python

   from arzeka import (
       ArzekaPayment,
       ArzekaPaymentError,
       ArzekaConnectionError,
       ArzekaValidationError,
       ArzekaAPIError,
       ArzekaAuthenticationError
   )

   def safe_payment_process():
       """Traitement de paiement avec gestion complète d'erreurs"""

       try:
           with ArzekaPayment() as client:
               # Authentification
               client.authenticate("username", "password")

               # Paiement
               response = client.initiate_payment(...)

               return {'success': True, 'data': response}

       except ArzekaAuthenticationError as e:
           # Problème de credentials
           return {
               'success': False,
               'error_type': 'authentication',
               'message': str(e)
           }

       except ArzekaValidationError as e:
           # Données invalides
           return {
               'success': False,
               'error_type': 'validation',
               'message': str(e)
           }

       except ArzekaConnectionError as e:
           # Problème réseau
           return {
               'success': False,
               'error_type': 'connection',
               'message': 'Vérifiez votre connexion internet'
           }

       except ArzekaAPIError as e:
           # Erreur API
           return {
               'success': False,
               'error_type': 'api',
               'status_code': e.status_code,
               'message': str(e),
               'details': e.response_data
           }

       except ArzekaPaymentError as e:
           # Autre erreur Arzeka
           return {
               'success': False,
               'error_type': 'unknown',
               'message': str(e)
           }

       except Exception as e:
           # Erreur inattendue
           return {
               'success': False,
               'error_type': 'unexpected',
               'message': f'Erreur inattendue: {e}'
           }

Retry avec gestion d'erreurs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   from arzeka import ArzekaConnectionError

   def initiate_payment_with_retry(client, payment_data, max_retries=3):
       """Initialiser un paiement avec retry automatique"""

       for attempt in range(max_retries):
           try:
               return client.initiate_payment(**payment_data)

           except ArzekaConnectionError as e:
               if attempt < max_retries - 1:
                   wait_time = 2 ** attempt  # Backoff exponentiel
                   print(f"Tentative {attempt + 1} échouée. Retry dans {wait_time}s...")
                   time.sleep(wait_time)
               else:
                   # Dernière tentative échouée
                   raise

Logging des erreurs
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from arzeka import ArzekaPaymentError

   logger = logging.getLogger(__name__)

   try:
       response = client.initiate_payment(...)
   except ArzekaPaymentError as e:
       logger.error(f"Erreur paiement: {e}", exc_info=True)
       # exc_info=True ajoute la stack trace complète

Bonnes pratiques
----------------

1. **Capturer les exceptions spécifiques d'abord**

   .. code-block:: python

      try:
          ...
      except ArzekaAuthenticationError:
          # Spécifique
      except ArzekaPaymentError:
          # Général
      except Exception:
          # Tout le reste

2. **Fournir des messages d'erreur clairs**

   .. code-block:: python

      except ArzekaValidationError as e:
          return f"Veuillez vérifier vos données: {e}"

3. **Logger les erreurs en production**

   .. code-block:: python

      logger.error(f"Payment failed: {e}", extra={'order_id': order_id})

4. **Ne pas exposer les détails sensibles**

   .. code-block:: python

      # ❌ Mauvais
      print(f"Error: {e.response_data}")  # Peut contenir des infos sensibles

      # ✅ Bon
      logger.error(f"API error", extra={'status': e.status_code})
      return "Une erreur est survenue, veuillez réessayer"

5. **Implémenter des fallbacks**

   .. code-block:: python

      try:
          return primary_payment_method()
      except ArzekaConnectionError:
          return fallback_payment_method()

Prochaines étapes
-----------------

- Consultez les :doc:`../examples/error_handling_examples`
- Apprenez les :doc:`../advanced_features`
- Explorez le :doc:`../payment_operations`
