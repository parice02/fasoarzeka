Gestion d'erreurs
=================

Guide complet de gestion d'erreurs dans Arzeka Payment.

Types d'exceptions
------------------

Le client fournit 5 types d'exceptions :

- ``ArzekaPaymentError`` - Exception de base
- ``ArzekaConnectionError`` - Erreurs réseau
- ``ArzekaValidationError`` - Données invalides
- ``ArzekaAPIError`` - Erreurs API
- ``ArzekaAuthenticationError`` - Erreurs d'authentification

Exemple basique
---------------

.. code-block:: python

   from arzeka import ArzekaPayment, ArzekaPaymentError

   try:
       with ArzekaPayment() as client:
           client.authenticate("username", "password")
           response = client.initiate_payment(...)
   except ArzekaPaymentError as e:
       print(f"Erreur: {e}")

Pour plus de détails
---------------------

Consultez :doc:`api/exceptions` pour la référence complète des exceptions.
