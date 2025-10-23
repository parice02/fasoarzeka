Module arzeka
=============

.. automodule:: arzeka
   :members:
   :undoc-members:
   :show-inheritance:

Classes principales
-------------------

ArzekaPayment
~~~~~~~~~~~~~

.. autoclass:: arzeka.ArzekaPayment
   :members:
   :undoc-members:
   :show-inheritance:

BasePayment
~~~~~~~~~~~

.. autoclass:: arzeka.BasePayment
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions
----------

ArzekaPaymentError
~~~~~~~~~~~~~~~~~~

.. autoexception:: arzeka.ArzekaPaymentError
   :members:
   :show-inheritance:

ArzekaConnectionError
~~~~~~~~~~~~~~~~~~~~~

.. autoexception:: arzeka.ArzekaConnectionError
   :members:
   :show-inheritance:

ArzekaValidationError
~~~~~~~~~~~~~~~~~~~~~

.. autoexception:: arzeka.ArzekaValidationError
   :members:
   :show-inheritance:

ArzekaAPIError
~~~~~~~~~~~~~~

.. autoexception:: arzeka.ArzekaAPIError
   :members:
   :show-inheritance:

ArzekaAuthenticationError
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoexception:: arzeka.ArzekaAuthenticationError
   :members:
   :show-inheritance:

Fonctions de convenance
-----------------------

authenticate
~~~~~~~~~~~~

.. autofunction:: arzeka.authenticate

initiate_payment
~~~~~~~~~~~~~~~~

.. autofunction:: arzeka.initiate_payment

check_payment
~~~~~~~~~~~~~

.. autofunction:: arzeka.check_payment

get_shared_client
~~~~~~~~~~~~~~~~~

.. autofunction:: arzeka.get_shared_client

close_shared_client
~~~~~~~~~~~~~~~~~~~

.. autofunction:: arzeka.close_shared_client
