# Guide de Démarrage Rapide - Arzeka Payment API

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/parice02/arzeka-payment.git
cd arzeka-payment

# Installer les dépendances
pip install -r requirements.txt
```

## Configuration

1. Obtenez vos identifiants API auprès de Faso Arzeka:
   - Token d'authentification
   - Merchant ID
   - URL de l'API (test ou production)

2. Configurez vos variables d'environnement (optionnel):
```bash
export ARZEKA_TOKEN="votre_token"
export ARZEKA_MERCHANT_ID="votre_merchant_id"
export ARZEKA_BASE_URL="https://pwg-test.fasoarzeka.com/"
```

## Utilisation Basique

### 1. Initier un paiement

```python
from arzeka import ArzekaPayment

# Créer une instance du client
with ArzekaPayment(token="votre_token") as client:
    # Initier le paiement
    response = client.initiate_payment(
        msisdn="22670123456",      # Numéro sans le '+'
        amount=1000,                # Montant en FCFA
        merchant_id="votre_merchant_id",
        link_for_update_status="https://votresite.com/webhook",
        link_back_to_calling_website="https://votresite.com/success"
    )

    print(f"Paiement initié: {response}")
    order_id = response.get('mappedOrderId')
```

### 2. Vérifier le statut d'un paiement

```python
from arzeka import ArzekaPayment

with ArzekaPayment(token="votre_token") as client:
    status = client.check_payment(mapped_order_id="order-123")
    print(f"Statut: {status}")
```

### 3. Gestion des erreurs

```python
from arzeka import (
    ArzekaPayment,
    ArzekaValidationError,
    ArzekaAPIError,
    ArzekaConnectionError
)

try:
    with ArzekaPayment(token="votre_token") as client:
        response = client.initiate_payment(
            msisdn="22670123456",
            amount=1000,
            merchant_id="merchant123"
        )
        print("Succès!")

except ArzekaValidationError as e:
    print(f"Erreur de validation: {e}")

except ArzekaAPIError as e:
    print(f"Erreur API (code {e.status_code}): {e}")
    print(f"Détails: {e.response_data}")

except ArzekaConnectionError as e:
    print(f"Erreur de connexion: {e}")
```

## Fonctionnalités Avancées

### Utilisation des utilitaires

```python
from arzeka.utils import format_msisdn, validate_phone_number

# Formater un numéro de téléphone
phone = format_msisdn("+226 70 12 34 56")  # => "22670123456"

# Valider un numéro
is_valid = validate_phone_number("22670123456")  # => True
```

### Configuration du timeout

```python
# Timeout personnalisé (en secondes)
client = ArzekaPayment(token="votre_token", timeout=60)
```

### Utilisation avec différents environnements

```python
# Environnement de test
client_test = ArzekaPayment(
    token="test_token",
    base_url="https://pwg-test.fasoarzeka.com/"
)

# Environnement de production
client_prod = ArzekaPayment(
    token="prod_token",
    base_url="https://pwg.fasoarzeka.com/"
)
```

## Tests

```bash
# Exécuter tous les tests
python -m pytest test/

# Exécuter un test spécifique
python -m pytest test/test_arzeka.py::TestArzekaPayment

# Avec couverture de code
python -m pytest --cov=arzeka test/
```

## Exemples Complets

Consultez le fichier `example.py` pour des exemples détaillés incluant:
- Initiation de paiement avec tous les paramètres
- Vérification de statut
- Gestion complète des erreurs
- Utilisation avec context manager
- Fonctions de commodité

## Support

Pour plus d'informations, consultez:
- `README.md` - Documentation complète
- `CHANGELOG.md` - Liste des améliorations
- `example.py` - Exemples d'utilisation

## Notes Importantes

1. **Numéros de téléphone**: Utilisez le format international sans '+' (ex: 22670123456)
2. **Montants**: En FCFA, nombres entiers ou décimaux positifs
3. **IDs de transaction**: Générés automatiquement si non fournis
4. **Environnement**: Testez d'abord en environnement de test avant la production
5. **Sécurité**: Ne commitez jamais vos tokens dans le code source

## Contribution

Les contributions sont les bienvenues! Consultez le fichier CONTRIBUTING.md pour les guidelines.
