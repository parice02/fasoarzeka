"""
Exemples d'utilisation des fonctions de commodité avec instance partagée
"""

from arzeka import (
    authenticate,
    initiate_payment,
    check_payment,
    get_shared_client,
    close_shared_client,
)

# Configuration
BASE_URL = "https://pwg-test.fasoarzeka.com/"
USERNAME = "votre_username"
PASSWORD = "votre_password"
MERCHANT_ID = "votre_merchant_id"
HASH_SECRET = "votre_hash_secret"


def exemple_workflow_simple():
    """
    Workflow simple : authentifier une fois, puis faire plusieurs opérations
    """
    print("=== Exemple 1 : Workflow Simple avec Instance Partagée ===\n")

    try:
        # Étape 1 : Authentifier (une seule fois)
        print("1. Authentification...")
        auth = authenticate(USERNAME, PASSWORD)
        print(f"✓ Authentification réussie!")
        print(f"   Token expire dans: {auth['expires_in']} secondes\n")

        # Étape 2 : Initier un paiement (utilise l'instance authentifiée)
        print("2. Initiation du paiement...")
        payment_data = {
            "amount": 1000,
            "merchant_id": MERCHANT_ID,
            "additional_info": {
                "first_name": "John",
                "last_name": "Doe",
                "mobile": "22670123456",
            },
            "hash_secret": HASH_SECRET,
            "link_for_update_status": "https://votresite.com/webhook",
            "link_back_to_calling_website": "https://votresite.com/success",
        }

        payment_response = initiate_payment(payment_data)
        print(f"✓ Paiement initié!")
        print(f"   Order ID: {payment_response.get('mappedOrderId')}\n")

        # Étape 3 : Vérifier le statut (même instance)
        print("3. Vérification du statut...")
        order_id = payment_response.get("mappedOrderId")
        if order_id:
            status = check_payment(order_id)
            print(f"✓ Statut récupéré: {status}\n")

        print("✓ Toutes les opérations réussies avec la même instance!\n")

    except Exception as e:
        print(f"✗ Erreur: {e}")
    finally:
        # Nettoyer à la fin
        close_shared_client()
        print("Instance partagée fermée.")


def exemple_verification_token_partage():
    """
    Vérifier le token de l'instance partagée
    """
    print("\n=== Exemple 2 : Vérification du Token Partagé ===\n")

    try:
        # Authentifier
        print("Authentification...")
        authenticate(USERNAME, PASSWORD)

        # Obtenir l'instance partagée
        client = get_shared_client()

        if client:
            print("✓ Instance partagée obtenue\n")

            # Vérifier le token
            if client.is_token_valid():
                info = client.get_token_expiry_info()
                print(f"✓ Token valide")
                print(f"   Expire dans: {info['expires_in_minutes']:.1f} minutes")
                print(f"   Timestamp expiration: {info['expires_at']}\n")
            else:
                print("✗ Token expiré ou invalide\n")

            # Faire des opérations
            print("Opérations avec instance partagée:")
            payment_data = {
                "amount": 500,
                "merchant_id": MERCHANT_ID,
                "additional_info": {
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "mobile": "22670987654",
                },
                "hash_secret": HASH_SECRET,
                "link_for_update_status": "https://votresite.com/webhook",
                "link_back_to_calling_website": "https://votresite.com/success",
            }

            response = initiate_payment(payment_data)
            print(f"✓ Paiement initié: {response.get('mappedOrderId')}")
        else:
            print("✗ Aucune instance partagée disponible")

    except Exception as e:
        print(f"✗ Erreur: {e}")
    finally:
        close_shared_client()


def exemple_multiples_operations():
    """
    Exemple de multiples opérations consécutives sans réauthentification
    """
    print("\n=== Exemple 3 : Multiples Opérations ===\n")

    try:
        # Une seule authentification
        print("Authentification initiale...")
        auth = authenticate(USERNAME, PASSWORD)
        print(f"✓ Token obtenu (expire dans {auth['expires_in']}s)\n")

        # Faire plusieurs paiements
        print("Initiation de plusieurs paiements:")
        for i in range(3):
            print(f"\n  Paiement {i+1}:")

            payment_data = {
                "amount": 1000 + (i * 500),
                "merchant_id": MERCHANT_ID,
                "additional_info": {
                    "first_name": f"User{i+1}",
                    "last_name": "Test",
                    "mobile": f"2267012345{i}",
                },
                "hash_secret": HASH_SECRET,
                "link_for_update_status": f"https://votresite.com/webhook/{i}",
                "link_back_to_calling_website": "https://votresite.com/success",
            }

            try:
                response = initiate_payment(payment_data)
                print(f"    ✓ Paiement {i+1} initié: {response.get('mappedOrderId')}")
            except Exception as e:
                print(f"    ✗ Échec du paiement {i+1}: {e}")

        print("\n✓ Tous les paiements traités avec la même session!")

    except Exception as e:
        print(f"✗ Erreur: {e}")
    finally:
        close_shared_client()


def exemple_gestion_expiration():
    """
    Gestion de l'expiration du token avec réauthentification
    """
    print("\n=== Exemple 4 : Gestion de l'Expiration ===\n")

    try:
        # Authentifier
        print("1. Authentification initiale...")
        authenticate(USERNAME, PASSWORD)
        print("✓ Authentifié\n")

        # Obtenir le client partagé
        client = get_shared_client()

        if client:
            # Vérifier le token avant chaque opération
            def faire_operation(operation_name):
                print(f"--- {operation_name} ---")

                # Vérifier le token
                if not client.is_token_valid():
                    print("⚠️  Token expiré, réauthentification...")
                    authenticate(USERNAME, PASSWORD)
                    print("✓ Réauthentifié")
                else:
                    info = client.get_token_expiry_info()
                    print(
                        f"✓ Token valide ({info['expires_in_minutes']:.1f} min restantes)"
                    )

                # Faire l'opération (simulé)
                print(f"✓ {operation_name} exécutée\n")

            # Faire plusieurs opérations
            faire_operation("Opération 1")
            faire_operation("Opération 2")
            faire_operation("Opération 3")

    except Exception as e:
        print(f"✗ Erreur: {e}")
    finally:
        close_shared_client()


def exemple_comparaison_approches():
    """
    Comparaison entre l'ancienne et la nouvelle approche
    """
    print("\n=== Exemple 5 : Comparaison des Approches ===\n")

    print("ANCIENNE APPROCHE (sans instance partagée):")
    print("=" * 50)
    print(
        """
from arzeka import ArzekaPayment

# Créer une nouvelle instance pour chaque opération
with ArzekaPayment() as client1:
    client1.authenticate("user", "pass")
    payment1 = client1.initiate_payment(...)

with ArzekaPayment() as client2:
    client2.authenticate("user", "pass")  # Ré-authentification!
    status = client2.check_payment(...)

# Problèmes:
# - Multiples instances créées
# - Authentification répétée
# - Plus de requêtes réseau
# - Moins efficace
"""
    )

    print("\nNOUVELLE APPROCHE (avec instance partagée):")
    print("=" * 50)
    print(
        """
from arzeka import authenticate, initiate_payment, check_payment

# Authentifier une seule fois
authenticate("user", "pass")

# Utiliser la même instance pour toutes les opérations
payment1 = initiate_payment(payment_data1)
payment2 = initiate_payment(payment_data2)
status1 = check_payment(order_id1)
status2 = check_payment(order_id2)

# Avantages:
# ✓ Une seule instance
# ✓ Authentification unique
# ✓ Moins de requêtes réseau
# ✓ Plus efficace
# ✓ Code plus simple
"""
    )

    print("\nDÉMONSTRATION:")
    print("=" * 50)

    try:
        # Nouvelle approche en action
        print("\n1. Authentification unique...")
        auth = authenticate(USERNAME, PASSWORD)
        print(f"   ✓ Token obtenu\n")

        print("2. Plusieurs opérations sans réauthentification...")

        # Opération 1
        client = get_shared_client()
        print(f"   - Instance partagée: {id(client)}")

        # Opération 2 (même instance)
        client2 = get_shared_client()
        print(f"   - Instance partagée: {id(client2)}")

        if id(client) == id(client2):
            print(f"   ✓ Les deux appels retournent la MÊME instance!\n")

        print("3. Vérification du token partagé...")
        if client.is_token_valid():
            print("   ✓ Token toujours valide sur l'instance partagée")

    except Exception as e:
        print(f"✗ Erreur: {e}")
    finally:
        close_shared_client()


def exemple_bonnes_pratiques():
    """
    Bonnes pratiques pour utiliser l'instance partagée
    """
    print("\n=== Exemple 6 : Bonnes Pratiques ===\n")

    print("BONNE PRATIQUE 1 : Toujours fermer à la fin")
    print("-" * 50)
    print(
        """
try:
    authenticate("user", "pass")
    # ... opérations ...
finally:
    close_shared_client()  # Toujours nettoyer!
"""
    )

    print("\nBONNE PRATIQUE 2 : Vérifier le token avant opérations longues")
    print("-" * 50)
    print(
        """
client = get_shared_client()
if client and client.is_token_valid(margin_seconds=300):
    # Token valide pour au moins 5 minutes
    faire_operation_longue()
else:
    authenticate(username, password)
"""
    )

    print("\nBONNE PRATIQUE 3 : Gérer les erreurs d'authentification")
    print("-" * 50)
    print(
        """
try:
    result = initiate_payment(payment_data)
except ArzekaAuthenticationError:
    # Token expiré, réauthentifier
    authenticate(username, password)
    result = initiate_payment(payment_data)
"""
    )

    print("\nBONNE PRATIQUE 4 : Utiliser get_shared_client() pour accès avancé")
    print("-" * 50)
    print(
        """
# Pour accès direct aux méthodes du client
client = get_shared_client()
if client:
    info = client.get_token_expiry_info()
    if info['expires_in_minutes'] < 5:
        # Réauthentifier de manière préventive
        authenticate(username, password)
"""
    )


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  EXEMPLES D'UTILISATION DES FONCTIONS AVEC INSTANCE PARTAGÉE")
    print("=" * 70)

    print("\nREMARQUE: Remplacez les variables de configuration par vos valeurs.\n")

    # Décommentez l'exemple que vous voulez exécuter

    # exemple_workflow_simple()
    # exemple_verification_token_partage()
    # exemple_multiples_operations()
    # exemple_gestion_expiration()
    # exemple_comparaison_approches()
    # exemple_bonnes_pratiques()

    print("\n" + "=" * 70)
    print("RÉSUMÉ DES NOUVELLES FONCTIONNALITÉS:")
    print("=" * 70)
    print(
        """
1. INSTANCE PARTAGÉE
   ✓ Une seule instance ArzekaPayment pour toutes les opérations
   ✓ Authentification unique réutilisée
   ✓ Plus efficace et moins de requêtes réseau

2. FONCTIONS DISPONIBLES
   - authenticate(username, password) → Authentifie et crée l'instance
   - initiate_payment(payment_data) → Utilise l'instance partagée
   - check_payment(order_id) → Utilise l'instance partagée
   - get_shared_client() → Obtient l'instance partagée
   - close_shared_client() → Ferme et nettoie l'instance

3. AVANTAGES
   ✓ Code plus simple et lisible
   ✓ Pas besoin de gérer les instances manuellement
   ✓ Token automatiquement partagé entre les appels
   ✓ Réduction du nombre d'authentifications
   ✓ Meilleure performance

4. UTILISATION TYPIQUE
   authenticate("user", "pass")      # Une fois
   payment1 = initiate_payment(...)  # Plusieurs fois
   payment2 = initiate_payment(...)  # Sans réauthentifier
   status = check_payment(...)       # Même token
   close_shared_client()             # À la fin

5. COMPATIBILITÉ
   ✓ Les anciennes méthodes avec context manager fonctionnent toujours
   ✓ Vous pouvez mélanger les deux approches si nécessaire
   ✓ Pas de breaking changes
"""
    )
