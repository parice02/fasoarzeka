Opérations de paiement
======================

Ce guide détaille toutes les opérations de paiement disponibles.

Initialisation d'un paiement
-----------------------------

La méthode ``initiate_payment()`` permet d'initier un nouveau paiement.

Paramètres requis
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Paramètre
     - Type
     - Description
   * - amount
     - float
     - Montant en FCFA (minimum 100)
   * - merchant_id
     - str
     - Identifiant du marchand
   * - additional_info
     - dict
     - Informations client (first_name, last_name, mobile)
   * - hash_secret
     - str
     - Secret pour signature
   * - link_for_update_status
     - str
     - URL webhook pour notifications
   * - link_back_to_calling_website
     - str
     - URL de retour après paiement

Exemple simple
~~~~~~~~~~~~~~

.. code-block:: python

   from arzeka import authenticate, initiate_payment

   authenticate("username", "password")

   response = initiate_payment({
       "amount": 1000,
       "merchant_id": "MERCHANT_123",
       "additional_info": {
           "first_name": "Jean",
           "last_name": "Dupont",
           "mobile": "70123456"
       },
       "hash_secret": "secret",
       "link_for_update_status": "https://example.com/webhook",
       "link_back_to_calling_website": "https://example.com/return"
   })

Vérification de paiement
-------------------------

La méthode ``check_payment()`` permet de vérifier le statut d'un paiement.

.. code-block:: python

   from arzeka import check_payment

   status = check_payment("ORDER-2025-001")
   print(status)

Prochaines étapes
-----------------

- Explorez :doc:`advanced_features`
- Consultez :doc:`examples/payment_examples`
