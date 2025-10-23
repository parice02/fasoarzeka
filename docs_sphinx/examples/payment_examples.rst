Exemples de paiement
====================

Voir le guide complet: :doc:`../payment_operations`

Paiement avec reçu
------------------

.. code-block:: python

   from arzeka import initiate_payment

   response = initiate_payment({
       "amount": 5000,
       "merchant_id": "MERCHANT_123",
       "additional_info": {
           "first_name": "Marie",
           "last_name": "Kaboré",
           "mobile": "70987654",
           "generateReceipt": True,
           "paymentDescription": "Facture N°12345",
           "accountingOffice": "Bureau Principal",
           "accountantName": "Jean Traoré"
       },
       "hash_secret": "secret",
       "link_for_update_status": "https://...",
       "link_back_to_calling_website": "https://..."
   })
