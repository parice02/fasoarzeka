Exemples de gestion d'erreurs
==============================

Voir le guide complet: :doc:`../api/exceptions`

Gestion complète
----------------

.. code-block:: python

   from arzeka import (
       ArzekaPayment,
       ArzekaAuthenticationError,
       ArzekaValidationError,
       ArzekaConnectionError,
       ArzekaAPIError
   )

   try:
       with ArzekaPayment() as client:
           client.authenticate("user", "pass")
           response = client.initiate_payment(...)
   except ArzekaAuthenticationError:
       print("Erreur d'authentification")
   except ArzekaValidationError:
       print("Données invalides")
   except ArzekaConnectionError:
       print("Erreur réseau")
   except ArzekaAPIError as e:
       print(f"Erreur API: {e.status_code}")
