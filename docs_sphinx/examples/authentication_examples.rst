Exemples d'authentification
===========================

Voir le guide complet: :doc:`../authentication`

Exemple avec retry
------------------

.. code-block:: python

   from arzeka import ArzekaPayment, ArzekaAuthenticationError
   import time

   def auth_with_retry(username, password, max_retries=3):
       client = ArzekaPayment()
       for attempt in range(max_retries):
           try:
               return client.authenticate(username, password)
           except ArzekaAuthenticationError as e:
               if attempt < max_retries - 1:
                   time.sleep(2 ** attempt)
               else:
                   raise

   auth = auth_with_retry("username", "password")
