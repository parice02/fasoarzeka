Exemples d'utilisation basique
===============================

Ce guide présente des exemples simples pour commencer avec Arzeka Payment.

Exemple 1 : Paiement simple
----------------------------

Le scénario le plus basique : authentification et paiement.

.. code-block:: python

   from arzeka import authenticate, initiate_payment

   # S'authentifier
   auth = authenticate("username", "password")
   print(f"✅ Authentifié! Token expire dans {auth['expires_in']}s")

   # Préparer les données de paiement
   payment_data = {
       "amount": 1000,
       "merchant_id": "MERCHANT_123",
       "additional_info": {
           "first_name": "Jean",
           "last_name": "Dupont",
           "mobile": "70123456"
       },
       "hash_secret": "your_secret",
       "link_for_update_status": "https://example.com/webhook",
       "link_back_to_calling_website": "https://example.com/return"
   }

   # Initier le paiement
   response = initiate_payment(payment_data)
   print(f"💳 Paiement initié: {response['mappedOrderId']}")

Exemple 2 : Vérification de statut
-----------------------------------

Comment vérifier le statut d'un paiement.

.. code-block:: python

   from arzeka import authenticate, check_payment

   # S'authentifier
   authenticate("username", "password")

   # Vérifier le statut
   order_id = "ORDER-2025-001"
   status = check_payment(order_id)

   print(f"📊 Statut du paiement {order_id}:")
   print(status)

Exemple 3 : Context manager
----------------------------

Utilisation recommandée avec context manager.

.. code-block:: python

   from arzeka import ArzekaPayment

   with ArzekaPayment() as client:
       # Authentification
       client.authenticate("username", "password")

       # Opérations
       response = client.initiate_payment(
           amount=2000,
           merchant_id="MERCHANT_123",
           additional_info={
               "first_name": "Marie",
               "last_name": "Kaboré",
               "mobile": "70987654"
           },
           hash_secret="secret",
           link_for_update_status="https://...",
           link_back_to_calling_website="https://..."
       )

       print(f"Paiement: {response['mappedOrderId']}")

   # Client automatiquement fermé

Exemple 4 : Variables d'environnement
--------------------------------------

Utiliser des variables d'environnement pour les credentials.

.. code-block:: python

   import os
   from arzeka import authenticate, initiate_payment

   # Charger depuis l'environnement
   username = os.getenv('ARZEKA_USERNAME')
   password = os.getenv('ARZEKA_PASSWORD')
   merchant_id = os.getenv('ARZEKA_MERCHANT_ID')
   hash_secret = os.getenv('ARZEKA_HASH_SECRET')

   # Authentifier
   authenticate(username, password)

   # Utiliser les credentials
   payment_data = {
       "amount": 1500,
       "merchant_id": merchant_id,
       "additional_info": {...},
       "hash_secret": hash_secret,
       "link_for_update_status": "https://...",
       "link_back_to_calling_website": "https://..."
   }

   response = initiate_payment(payment_data)

Exemple 5 : Fonctions utilitaires
----------------------------------

Utilisation des fonctions helper.

.. code-block:: python

   from arzeka import (
       get_reference,
       format_msisdn,
       validate_phone_number,
       initiate_payment
   )

   # Générer un ID unique
   order_id = get_reference()
   print(f"ID généré: {order_id}")  # REF-20251023-123456

   # Formater un numéro
   phone = "70 12 34 56"
   msisdn = format_msisdn(phone)
   print(f"Formaté: {msisdn}")  # 22670123456

   # Valider un numéro
   if validate_phone_number("70123456"):
       print("✅ Numéro valide")

   # Utiliser dans le paiement
   payment_data = {
       "amount": 1000,
       "merchant_id": "MERCHANT_123",
       "additional_info": {
           "first_name": "Jean",
           "last_name": "Dupont",
           "mobile": msisdn
       },
       "hash_secret": "secret",
       "link_for_update_status": "https://...",
       "link_back_to_calling_website": "https://...",
       "mapped_order_id": order_id
   }

Exemple 6 : Vérification du token
----------------------------------

Vérifier la validité du token avant une opération.

.. code-block:: python

   from arzeka import ArzekaPayment

   client = ArzekaPayment()
   client.authenticate("username", "password")

   # Vérification simple
   if client.is_token_valid():
       print("✅ Token valide")
       response = client.initiate_payment(...)
   else:
       print("❌ Token expiré")

   # Informations détaillées
   info = client.get_token_expiry_info()
   print(f"Expire dans: {info['expires_in_minutes']:.1f} minutes")

   # Vérifier avec marge
   if client.is_token_valid(margin_seconds=300):  # 5 minutes
       print("Token valide pour au moins 5 minutes")

Prochaines étapes
-----------------

- Consultez :doc:`authentication_examples` pour plus sur l'authentification
- Explorez :doc:`payment_examples` pour des cas avancés
- Apprenez la gestion d'erreurs avec :doc:`error_handling_examples`
