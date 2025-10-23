Changelog
=========

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Version 1.0.0 - 2025-10-23
--------------------------

Première version stable

Ajouts
~~~~~~

**Authentification**

- ✅ Méthode ``authenticate()`` avec username/password
- ✅ Gestion automatique des tokens
- ✅ Stockage sécurisé des credentials
- ✅ Validation de token avec ``is_token_valid()``
- ✅ Informations détaillées avec ``get_token_expiry_info()``

**Réauthentification automatique**

- ✅ Vérification automatique de la validité du token
- ✅ Réauthentification transparente quand le token expire
- ✅ Méthode privée ``_ensure_valid_token()``
- ✅ Pas besoin de gérer manuellement l'expiration

**Opérations de paiement**

- ✅ ``initiate_payment()`` - Initialiser un paiement
- ✅ ``check_payment()`` - Vérifier le statut d'un paiement
- ✅ Support des reçus avec ``generateReceipt``
- ✅ Génération automatique d'ID de transaction

**Gestion d'erreurs**

- ✅ ``ArzekaPaymentError`` - Exception de base
- ✅ ``ArzekaConnectionError`` - Erreurs de connexion
- ✅ ``ArzekaValidationError`` - Erreurs de validation
- ✅ ``ArzekaAPIError`` - Erreurs API avec détails
- ✅ ``ArzekaAuthenticationError`` - Erreurs d'authentification

**Architecture robuste**

- ✅ Retry automatique avec backoff exponentiel (3 tentatives max)
- ✅ Session HTTP persistante avec connection pooling
- ✅ Context manager pour gestion automatique des ressources
- ✅ Logging intégré pour traçabilité complète
- ✅ Type hints complets pour meilleure auto-complétion

**Fonctions utilitaires**

- ✅ ``get_reference()`` - Générer un ID unique
- ✅ ``get_uuid_reference()`` - ID basé sur UUID
- ✅ ``format_msisdn()`` - Formater numéro de téléphone
- ✅ ``validate_phone_number()`` - Valider numéro burkinabè
- ✅ ``generate_hash_signature()`` - Signature de sécurité

**Instance partagée**

- ✅ Fonctions de convenance utilisant une instance partagée
- ✅ ``get_shared_client()`` - Accès à l'instance partagée
- ✅ ``close_shared_client()`` - Nettoyage de l'instance

**Tests et qualité**

- ✅ Tests unitaires complets avec pytest
- ✅ Couverture >90%
- ✅ Tests pour toutes les fonctionnalités
- ✅ Mocks pour isolation

**Documentation**

- ✅ Documentation complète style ReadTheDocs
- ✅ Guide d'installation
- ✅ Guide de démarrage rapide
- ✅ Guide d'authentification
- ✅ Référence API complète
- ✅ Exemples de code
- ✅ Guide de contribution
- ✅ README détaillé

Améliorations
~~~~~~~~~~~~~

- Performances optimisées avec session persistante
- Sécurité renforcée avec validation stricte
- Logs détaillés pour debugging
- Messages d'erreur clairs et actionnables

Correctifs
~~~~~~~~~~

- Correction de l'import urllib3
- Gestion correcte de l'expiration des tokens
- Validation des numéros de téléphone burkinabès

Documentation
~~~~~~~~~~~~~

- 4 guides détaillés
- Référence API complète
- 20+ exemples de code
- Documentation des exceptions
- Guide de contribution

Version 0.1.0 - 2025-10-22
--------------------------

Version initiale (avant améliorations)

- Fonctionnalités de base
- API simple
- Documentation minimale
