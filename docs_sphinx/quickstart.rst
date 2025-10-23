Guide de démarrage rapide
=========================

Ce guide vous permet de commencer à utiliser Arzeka Payment en quelques minutes.

Deux approches principales
---------------------------

Il existe deux façons d'utiliser le client :

1. **Fonctions de convenance** (recommandé pour simplicité)
2. **Instance de classe** (recommandé pour contrôle fin)

Approche 1 : Fonctions de convenance
-------------------------------------

C'est l'approche la plus simple pour commencer :

.. code-block:: python

   from arzeka import authenticate, initiate_payment, check_payment

   # Étape 1 : Authentification
   auth = authenticate("your_username", "your_password")
   print(f"Token expires in: {auth['expires_in']} seconds")

   # Étape 2 : Initialisation d'un paiement
   payment_data = {
       "amount": 1000,  # Montant en FCFA (minimum 100)
       "merchant_id": "MERCHANT_123",
       "additional_info": {
           "first_name": "Jean",
           "last_name": "Dupont",
           "mobile": "70123456"  # Numéro sans indicatif
       },
       "hash_secret": "your_hash_secret",
       "link_for_update_status": "https://example.com/webhook",
       "link_back_to_calling_website": "https://example.com/return"
   }

   response = initiate_payment(payment_data)
   print(f"Payment initiated: {response['mappedOrderId']}")

   # Étape 3 : Vérification du statut
   status = check_payment(response['mappedOrderId'])
   print(f"Payment status: {status}")

Approche 2 : Instance de classe
--------------------------------

Pour un contrôle plus fin et des opérations avancées :

.. code-block:: python

   from arzeka import ArzekaPayment

   # Utilisation du context manager (recommandé)
   with ArzekaPayment() as client:
       # Authentification
       auth = client.authenticate("your_username", "your_password")

       # Vérification du token
       if client.is_token_valid():
           print("Token is valid")

       # Initialisation du paiement
       response = client.initiate_payment(
           amount=1000,
           merchant_id="MERCHANT_123",
           additional_info={
               "first_name": "Jean",
               "last_name": "Dupont",
               "mobile": "70123456"
           },
           hash_secret="your_hash_secret",
           link_for_update_status="https://example.com/webhook",
           link_back_to_calling_website="https://example.com/return"
       )

       # Vérification du statut
       status = client.check_payment(response['mappedOrderId'])
       print(f"Status: {status}")

   # Le client est automatiquement fermé

Workflow complet
----------------

Voici un exemple de workflow complet avec gestion d'erreurs :

.. code-block:: python

   from arzeka import (
       ArzekaPayment,
       ArzekaAuthenticationError,
       ArzekaValidationError,
       ArzekaAPIError
   )

   def process_payment(username, password, amount, customer_info):
       """Traitement complet d'un paiement"""

       try:
           # Créer le client
           with ArzekaPayment() as client:
               # S'authentifier
               print("🔐 Authentication en cours...")
               auth = client.authenticate(username, password)
               print(f"✅ Authentifié! Token expire dans {auth['expires_in']}s")

               # Préparer les données
               payment_data = {
                   "amount": amount,
                   "merchant_id": "MERCHANT_123",
                   "additional_info": customer_info,
                   "hash_secret": "your_secret",
                   "link_for_update_status": "https://example.com/webhook",
                   "link_back_to_calling_website": "https://example.com/return"
               }

               # Initier le paiement
               print("💳 Initialisation du paiement...")
               response = client.initiate_payment(**payment_data)
               order_id = response['mappedOrderId']
               print(f"✅ Paiement initié: {order_id}")

               # Vérifier le statut
               print("🔍 Vérification du statut...")
               status = client.check_payment(order_id)
               print(f"📊 Statut: {status}")

               return {
                   'success': True,
                   'order_id': order_id,
                   'status': status
               }

       except ArzekaAuthenticationError as e:
           print(f"❌ Erreur d'authentification: {e}")
           return {'success': False, 'error': 'authentication_failed'}

       except ArzekaValidationError as e:
           print(f"❌ Données invalides: {e}")
           return {'success': False, 'error': 'validation_failed'}

       except ArzekaAPIError as e:
           print(f"❌ Erreur API: {e}")
           return {'success': False, 'error': 'api_error'}

   # Utilisation
   result = process_payment(
       username="user@example.com",
       password="password123",
       amount=5000,
       customer_info={
           "first_name": "Marie",
           "last_name": "Kaboré",
           "mobile": "70987654"
       }
   )

   if result['success']:
       print(f"🎉 Paiement traité avec succès: {result['order_id']}")
   else:
       print(f"💥 Échec du paiement: {result['error']}")

Fonctionnalités clés
---------------------

Réauthentification automatique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le client se réauthentifie automatiquement quand le token expire :

.. code-block:: python

   from arzeka import ArzekaPayment

   client = ArzekaPayment()
   client.authenticate("username", "password")

   # Faites plusieurs requêtes sur une longue période
   # La réauthentification est AUTOMATIQUE
   for i in range(10):
       response = client.initiate_payment(...)
       print(f"Payment {i+1}: {response['mappedOrderId']}")

Validation du token
~~~~~~~~~~~~~~~~~~~

Vérifiez si le token est encore valide :

.. code-block:: python

   # Vérification simple
   if client.is_token_valid():
       print("Token valide")

   # Informations détaillées
   info = client.get_token_expiry_info()
   print(f"Expire dans {info['expires_in_minutes']:.1f} minutes")

Fonctions utilitaires
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from arzeka import get_reference, format_msisdn, validate_phone_number

   # Générer un ID unique
   ref = get_reference()  # REF-20251023-123456

   # Formater un numéro
   msisdn = format_msisdn("70 12 34 56")  # 22670123456

   # Valider un numéro burkinabè
   is_valid = validate_phone_number("70123456")  # True

Exemples rapides
----------------

Paiement avec reçu
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   payment_data = {
       "amount": 5000,
       "merchant_id": "MERCHANT_123",
       "additional_info": {
           "first_name": "Marie",
           "last_name": "Kaboré",
           "mobile": "70987654",
           "generateReceipt": True,
           "paymentDescription": "Facture N°12345",
           "accountingOffice": "Bureau Principal",
           "accountantName": "Jean Traoré",
           "address": "Ouagadougou, Burkina Faso"
       },
       "hash_secret": "secret",
       "link_for_update_status": "https://...",
       "link_back_to_calling_website": "https://...",
       "mapped_order_id": "ORDER-2025-001"
   }

   response = initiate_payment(payment_data)

Vérification avec transaction ID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   status = check_payment(
       mapped_order_id="ORDER-2025-001",
       transaction_id="TXN-12345"
   )

Prochaines étapes
-----------------

- Approfondissez avec le guide :doc:`authentication`
- Explorez les :doc:`payment_operations`
- Consultez les :doc:`examples/basic_usage`
- Apprenez la :doc:`error_handling`
