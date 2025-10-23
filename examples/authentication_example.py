"""
Exemple complet d'authentification et de paiement avec Arzeka API
"""

from arzeka import ArzekaAuthenticationError, ArzekaPayment, ArzekaPaymentError, authenticate

# Configuration
BASE_URL = "https://pwg-test.fasoarzeka.com/"
USERNAME = "votre_nom_utilisateur"
PASSWORD = "votre_mot_de_passe"
MERCHANT_ID = "votre_merchant_id"


def workflow_complet_authentification_et_paiement():
    """
    Workflow complet : authentification puis paiement
    """
    print("=== Workflow complet : Authentification + Paiement ===\n")

    try:
        # Étape 1 : Authentification pour obtenir le token
        print("1. Authentification en cours...")
        auth_response = authenticate(
            username=USERNAME, password=PASSWORD, base_url=BASE_URL
        )

        print("✓ Authentification réussie!")
        print(
            f"   - Token obtenu (premiers caractères): {auth_response['access_token'][:30]}..."
        )
        print(f"   - Type de token: {auth_response['token_type']}")
        print(f"   - Expire dans: {auth_response['expires_in']} secondes")
        print(f"   - Soit {auth_response['expires_in'] / 60:.1f} minutes\n")

        # Récupérer le token d'accès
        access_token = auth_response["access_token"]

        # Étape 2 : Utiliser le token pour effectuer un paiement
        print("2. Initiation du paiement...")
        with ArzekaPayment(token=access_token, base_url=BASE_URL) as client:
            payment_response = client.initiate_payment(
                msisdn="22670123456",  # Numéro du client
                amount=1000,  # Montant en FCFA
                merchant_id=MERCHANT_ID,
                link_for_update_status="https://votresite.com/webhook/status",
                link_back_to_calling_website="https://votresite.com/success",
            )

            print("✓ Paiement initié avec succès!")
            print(f"   - ID de commande: {payment_response.get('mappedOrderId')}")
            print(f"   - Réponse complète: {payment_response}\n")

            # Étape 3 : Vérifier le statut du paiement
            order_id = payment_response.get("mappedOrderId")
            if order_id:
                print("3. Vérification du statut...")
                status_response = client.check_payment(mapped_order_id=order_id)
                print("✓ Statut récupéré!")
                print(f"   - Statut: {status_response}\n")

        print("=== Workflow terminé avec succès! ===")

    except ArzekaAuthenticationError as e:
        print(f"❌ Erreur d'authentification: {e}")
        print("   Vérifiez vos identifiants (username et password)")

    except ArzekaPaymentError as e:
        print(f"❌ Erreur de paiement: {e}")


def authentification_avec_gestion_token():
    """
    Exemple montrant comment gérer le token et sa durée de vie
    """
    print("\n=== Gestion du token d'authentification ===\n")

    try:
        # Méthode 1 : Authentification puis mise à jour du client
        print("Méthode 1 : Authentification intégrée au client\n")

        with ArzekaPayment(token="", base_url=BASE_URL) as client:
            # Authentification - le token du client sera automatiquement mis à jour
            auth = client.authenticate(username=USERNAME, password=PASSWORD)

            print(f"Token actif pendant {auth['expires_in']} secondes")
            print(f"Type de token: {auth['token_type']}\n")

            # Le client peut maintenant être utilisé directement
            # car son token interne a été mis à jour
            payment = client.initiate_payment(
                msisdn="22670123456", amount=500, merchant_id=MERCHANT_ID
            )
            print(f"✓ Paiement effectué: {payment.get('mappedOrderId')}\n")

        print("=" * 50)

        # Méthode 2 : Authentification séparée
        print("\nMéthode 2 : Authentification avec fonction séparée\n")

        # D'abord authentifier
        auth = authenticate(USERNAME, PASSWORD, BASE_URL)
        token = auth["access_token"]
        print(f"✓ Token récupéré (valide {auth['expires_in']}s)\n")

        # Puis créer un client avec le token
        with ArzekaPayment(token=token, base_url=BASE_URL) as client:
            payment = client.initiate_payment(
                msisdn="22670123456", amount=750, merchant_id=MERCHANT_ID
            )
            print(f"✓ Paiement effectué: {payment.get('mappedOrderId')}")

    except ArzekaAuthenticationError as e:
        print(f"❌ Échec de l'authentification: {e}")
    except ArzekaPaymentError as e:
        print(f"❌ Erreur: {e}")


def gestion_erreurs_authentification():
    """
    Exemples de gestion des différents types d'erreurs d'authentification
    """
    print("\n=== Gestion des erreurs d'authentification ===\n")

    # Cas 1 : Identifiants incorrects
    print("Test 1 : Identifiants incorrects")
    try:
        auth = authenticate("mauvais_user", "mauvais_pass", BASE_URL)
    except ArzekaAuthenticationError as e:
        print(f"✓ Erreur capturée correctement: {e}\n")

    # Cas 2 : Champs vides
    print("Test 2 : Validation des champs")
    try:
        with ArzekaPayment(token="", base_url=BASE_URL) as client:
            client.authenticate(username="", password="password")
    except Exception as e:
        print(f"✓ Erreur de validation capturée: {type(e).__name__}: {e}\n")

    # Cas 3 : Utilisation correcte
    print("Test 3 : Authentification correcte")
    try:
        # Remplacer par vos vrais identifiants pour tester
        # auth = authenticate(USERNAME, PASSWORD, BASE_URL)
        # print(f"✓ Authentification réussie!")
        print("   (Décommentez le code avec vos vrais identifiants)\n")
    except Exception as e:
        print(f"Erreur: {e}\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  EXEMPLES D'AUTHENTIFICATION ARZEKA PAYMENT API")
    print("=" * 60 + "\n")

    # Décommentez l'exemple que vous voulez exécuter

    # Exemple complet (authentification + paiement)
    # workflow_complet_authentification_et_paiement()

    # Gestion du token
    # authentification_avec_gestion_token()

    # Gestion des erreurs
    # gestion_erreurs_authentification()

    print("\n" + "=" * 60)
    print("NOTES IMPORTANTES:")
    print("=" * 60)
    print(
        """
1. Remplacez les variables suivantes par vos vraies valeurs :
   - USERNAME : votre nom d'utilisateur Arzeka
   - PASSWORD : votre mot de passe Arzeka
   - MERCHANT_ID : votre identifiant marchand

2. Le token obtenu a une durée de vie limitée (expires_in)
   Vous devez vous réauthentifier après expiration

3. La méthode authenticate() retourne :
   - access_token : le token JWT à utiliser
   - token_type : généralement "Bearer"
   - expires_in : durée de validité en secondes

4. Deux façons d'utiliser l'authentification :
   a) Appeler client.authenticate() qui met à jour le token du client
   b) Appeler authenticate() puis créer un client avec le token

5. Pour la production, utilisez l'URL de production au lieu de l'URL de test
"""
    )
