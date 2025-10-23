Fonctionnalités avancées
========================

Guide des fonctionnalités avancées d'Arzeka Payment.

Réauthentification automatique
-------------------------------

Le client se réauthentifie automatiquement quand le token expire.

.. code-block:: python

   from arzeka import ArzekaPayment

   client = ArzekaPayment()
   client.authenticate("username", "password")

   # Faites plusieurs requêtes sur une longue période
   # La réauthentification est AUTOMATIQUE
   for i in range(10):
       response = client.initiate_payment(...)

Instance partagée
-----------------

Les fonctions de convenance utilisent une instance partagée.

.. code-block:: python

   from arzeka import authenticate, get_shared_client

   authenticate("username", "password")

   # Accès à l'instance partagée
   client = get_shared_client()
   print(client.is_token_valid())

Retry automatique
-----------------

Le client réessaie automatiquement en cas d'erreur réseau (max 3 fois).

Session persistante
-------------------

Les connexions HTTP sont réutilisées pour de meilleures performances.

Context manager
---------------

Utilisation recommandée pour gestion automatique des ressources.

.. code-block:: python

   with ArzekaPayment() as client:
       client.authenticate("user", "pass")
       # ... opérations ...
   # Fermeture automatique

Prochaines étapes
-----------------

- Consultez les :doc:`examples/basic_usage`
- Explorez l':doc:`api/arzeka`
