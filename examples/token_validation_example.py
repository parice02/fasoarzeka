"""
Exemple d'utilisation de la méthode is_token_valid() pour vérifier la validité du token
"""

import time
from arzeka import ArzekaPayment

# Configuration
BASE_URL = "https://pwg-test.fasoarzeka.com/"
USERNAME = "votre_username"
PASSWORD = "votre_password"


def exemple_verification_token():
    """
    Exemple basique de vérification de la validité du token
    """
    print("=== Exemple 1 : Vérification basique du token ===\n")

    with ArzekaPayment(base_url=BASE_URL) as client:
        # Vérifier avant authentification
        if client.is_token_valid():
            print("✓ Token valide")
        else:
            print("✗ Token invalide ou inexistant")
            print("  → Authentification nécessaire\n")

        # Authentification
        print("Authentification en cours...")
        try:
            auth = client.authenticate(USERNAME, PASSWORD)
            print(f"✓ Authentification réussie!")
            print(f"  Token expire dans: {auth['expires_in']} secondes\n")
        except Exception as e:
            print(f"✗ Échec: {e}")
            return

        # Vérifier après authentification
        if client.is_token_valid():
            print("✓ Token valide après authentification")
        else:
            print("✗ Token invalide après authentification")


def exemple_verification_avec_marge():
    """
    Exemple de vérification avec marge de sécurité personnalisée
    """
    print("\n=== Exemple 2 : Vérification avec marge de sécurité ===\n")

    with ArzekaPayment(base_url=BASE_URL) as client:
        # Authentifier
        try:
            client.authenticate(USERNAME, PASSWORD)
            print("✓ Authentification réussie\n")
        except Exception as e:
            print(f"✗ Échec: {e}")
            return

        # Vérifier avec différentes marges
        marges = [
            (60, "1 minute"),
            (300, "5 minutes"),
            (600, "10 minutes"),
            (1800, "30 minutes"),
        ]

        for seconds, description in marges:
            is_valid = client.is_token_valid(margin_seconds=seconds)
            status = "✓ Valide" if is_valid else "✗ Expiré ou proche expiration"
            print(f"{status} pour une marge de {description} ({seconds}s)")


def exemple_informations_expiration():
    """
    Exemple d'utilisation de get_token_expiry_info()
    """
    print("\n=== Exemple 3 : Informations détaillées sur l'expiration ===\n")

    with ArzekaPayment(base_url=BASE_URL) as client:
        # Avant authentification
        print("Avant authentification:")
        info = client.get_token_expiry_info()
        print(f"  Has token: {info['has_token']}")
        print(f"  Is valid: {info['is_valid']}")
        print(f"  Is expired: {info['is_expired']}\n")

        # Authentifier
        try:
            client.authenticate(USERNAME, PASSWORD)
            print("✓ Authentification réussie\n")
        except Exception as e:
            print(f"✗ Échec: {e}")
            return

        # Après authentification
        print("Après authentification:")
        info = client.get_token_expiry_info()
        print(f"  Has token: {info['has_token']}")
        print(f"  Is valid: {info['is_valid']}")
        print(f"  Is expired: {info['is_expired']}")
        print(f"  Expires at (timestamp): {info['expires_at']}")
        print(f"  Expires in: {info['expires_in_seconds']:.0f} secondes")
        print(f"  Expires in: {info['expires_in_minutes']:.1f} minutes")


def exemple_surveillance_expiration():
    """
    Exemple de surveillance de l'expiration du token en temps réel
    """
    print("\n=== Exemple 4 : Surveillance en temps réel ===\n")

    with ArzekaPayment(base_url=BASE_URL) as client:
        try:
            client.authenticate(USERNAME, PASSWORD)
            print("✓ Authentification réussie\n")
        except Exception as e:
            print(f"✗ Échec: {e}")
            return

        print("Surveillance du token (appuyez sur Ctrl+C pour arrêter):\n")

        try:
            for i in range(10):  # Surveiller pendant 10 secondes
                info = client.get_token_expiry_info()

                # Afficher l'état
                status = "✓ VALIDE" if info["is_valid"] else "✗ EXPIRÉ"
                minutes = info["expires_in_minutes"]

                print(f"[{i+1}] {status} - Expire dans {minutes:.2f} minutes")

                # Vérifier si proche de l'expiration
                if info["expires_in_seconds"] < 300:  # Moins de 5 minutes
                    print("    ⚠️  ATTENTION: Token expire bientôt!")

                time.sleep(1)  # Attendre 1 seconde

        except KeyboardInterrupt:
            print("\n\nSurveillance arrêtée.")


def exemple_workflow_complet():
    """
    Workflow complet avec vérification automatique avant chaque opération
    """
    print("\n=== Exemple 5 : Workflow avec vérification automatique ===\n")

    with ArzekaPayment(base_url=BASE_URL) as client:
        # Authentifier initialement
        try:
            client.authenticate(USERNAME, PASSWORD)
            print("✓ Authentification initiale réussie\n")
        except Exception as e:
            print(f"✗ Échec: {e}")
            return

        # Simuler plusieurs opérations
        for i in range(3):
            print(f"--- Opération {i+1} ---")

            # Vérifier la validité avant l'opération
            if not client.is_token_valid():
                print("⚠️  Token expiré, réauthentification nécessaire...")
                try:
                    client.authenticate(USERNAME, PASSWORD)
                    print("✓ Réauthentification réussie")
                except Exception as e:
                    print(f"✗ Échec de réauthentification: {e}")
                    break
            else:
                info = client.get_token_expiry_info()
                print(
                    f"✓ Token valide (expire dans {info['expires_in_minutes']:.1f} min)"
                )

            # Effectuer l'opération (simulé)
            print(f"  → Exécution de l'opération {i+1}...")
            print(f"  ✓ Opération {i+1} terminée\n")

            # Attendre avant la prochaine opération
            if i < 2:
                time.sleep(1)


def exemple_comparaison_methodes():
    """
    Comparaison entre is_token_valid() et get_token_expiry_info()
    """
    print("\n=== Exemple 6 : Comparaison des méthodes ===\n")

    with ArzekaPayment(base_url=BASE_URL) as client:
        try:
            client.authenticate(USERNAME, PASSWORD)
            print("✓ Authentification réussie\n")
        except Exception as e:
            print(f"✗ Échec: {e}")
            return

        print("Méthode 1 - is_token_valid():")
        print("  Usage simple, retourne bool")
        is_valid = client.is_token_valid()
        print(f"  Résultat: {is_valid}\n")

        print("Méthode 2 - get_token_expiry_info():")
        print("  Informations détaillées, retourne dict")
        info = client.get_token_expiry_info()
        print("  Résultat:")
        for key, value in info.items():
            if isinstance(value, float) and key != "expires_at":
                print(f"    {key}: {value:.2f}")
            else:
                print(f"    {key}: {value}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  EXEMPLES DE VÉRIFICATION DE VALIDITÉ DU TOKEN")
    print("=" * 70 + "\n")

    print("REMARQUE: Ces exemples nécessitent des identifiants valides.")
    print("Remplacez USERNAME et PASSWORD par vos vraies valeurs.\n")

    # Décommentez l'exemple que vous voulez exécuter

    # exemple_verification_token()
    # exemple_verification_avec_marge()
    # exemple_informations_expiration()
    # exemple_surveillance_expiration()
    # exemple_workflow_complet()
    # exemple_comparaison_methodes()

    print("\n" + "=" * 70)
    print("RÉSUMÉ DES MÉTHODES DISPONIBLES:")
    print("=" * 70)
    print(
        """
1. is_token_valid(margin_seconds=60) -> bool
   ✓ Vérification simple de la validité du token
   ✓ Marge de sécurité configurable (défaut: 60s)
   ✓ Retourne True si valide, False sinon

2. get_token_expiry_info() -> Dict[str, Any]
   ✓ Informations détaillées sur l'expiration
   ✓ Retourne un dictionnaire avec:
     - is_valid: bool
     - expires_at: timestamp
     - expires_in_seconds: float
     - expires_in_minutes: float
     - is_expired: bool
     - has_token: bool

BONNES PRATIQUES:
- Vérifier la validité avant chaque opération critique
- Utiliser une marge de sécurité appropriée (60-300s)
- Réauthentifier automatiquement si token expiré
- Logger les réauthentifications pour audit
"""
    )
