# 🔐 Authentification Arzeka Payment API

## Description

La méthode d'authentification permet d'obtenir un token d'accès (access token) à partir de vos identifiants Arzeka (nom d'utilisateur et mot de passe). Ce token est nécessaire pour effectuer des opérations de paiement.

## Fonctionnalités

### 1. Méthode `authenticate()` de la classe

```python
from arzeka import ArzekaPayment

with ArzekaPayment(token="", base_url=BASE_URL) as client:
    auth_response = client.authenticate(
        username="votre_username",
        password="votre_password"
    )

    print(f"Token: {auth_response['access_token']}")
    print(f"Type: {auth_response['token_type']}")
    print(f"Expire dans: {auth_response['expires_in']} secondes")
```

### 2. Fonction de commodité `authenticate()`

```python
from arzeka import authenticate

auth = authenticate(
    username="votre_username",
    password="votre_password",
    base_url="https://pwg-test.fasoarzeka.com/"
)

token = auth['access_token']
```

## Réponse d'authentification

La méthode retourne un dictionnaire contenant :

| Champ | Type | Description |
|-------|------|-------------|
| `access_token` | string | Token JWT pour authentifier les requêtes suivantes |
| `token_type` | string | Type de token, généralement "Bearer" |
| `expires_in` | int | Durée de validité du token en secondes |

## Exemples d'utilisation

### Exemple 1 : Workflow complet (Authentification + Paiement)

```python
from arzeka import authenticate, ArzekaPayment

# 1. Authentifier pour obtenir le token
auth = authenticate("user@example.com", "password123")
token = auth['access_token']

print(f"Token valide pendant {auth['expires_in']} secondes")

# 2. Utiliser le token pour initier un paiement
with ArzekaPayment(token=token) as client:
    response = client.initiate_payment(
        msisdn="22670123456",
        amount=1000,
        merchant_id="merchant123"
    )
    print(f"Paiement initié: {response}")
```

### Exemple 2 : Authentification intégrée

```python
from arzeka import ArzekaPayment

# Le client s'authentifie et met à jour son token automatiquement
with ArzekaPayment(token="") as client:
    # Authentifier
    auth = client.authenticate("user@example.com", "password123")

    # Le token du client est maintenant à jour
    # On peut directement faire des paiements
    payment = client.initiate_payment(
        msisdn="22670123456",
        amount=1000,
        merchant_id="merchant123"
    )
```

### Exemple 3 : Gestion des erreurs

```python
from arzeka import authenticate, ArzekaAuthenticationError

try:
    auth = authenticate("user@example.com", "wrong_password")
except ArzekaAuthenticationError as e:
    print(f"Échec de l'authentification: {e}")
    # Gérer l'erreur : afficher message, demander à nouveau, etc.
```

## Gestion des erreurs

La méthode d'authentification peut lever les exceptions suivantes :

### `ArzekaValidationError`
- Username ou password vide
- Paramètres invalides

```python
# Exemple d'erreur
client.authenticate(username="", password="pass")  # ❌ Username vide
```

### `ArzekaAuthenticationError`
- Identifiants incorrects (401)
- Compte verrouillé ou inactif (403)
- Problème d'authentification

```python
try:
    auth = client.authenticate("bad_user", "bad_pass")
except ArzekaAuthenticationError as e:
    if "Invalid credentials" in str(e):
        print("Identifiants incorrects")
    elif "forbidden" in str(e):
        print("Compte bloqué")
```

### `ArzekaConnectionError`
- Problème de connexion réseau
- Timeout

```python
try:
    auth = authenticate("user", "pass", timeout=5)
except ArzekaConnectionError as e:
    print(f"Impossible de se connecter: {e}")
```

## Durée de vie du token

⚠️ **Important** : Le token a une durée de vie limitée (indiquée par `expires_in`)

```python
auth = authenticate("user", "password")

expires_in = auth['expires_in']  # en secondes
expires_in_minutes = expires_in / 60

print(f"Token valide pendant {expires_in_minutes} minutes")

# Après expiration, vous devez vous réauthentifier
```

### Bonne pratique : Réauthentification automatique

```python
import time

class ArzekaClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None
        self.token_expires_at = 0

    def get_valid_token(self):
        # Vérifier si le token est encore valide
        if time.time() >= self.token_expires_at:
            # Token expiré, réauthentifier
            auth = authenticate(self.username, self.password)
            self.token = auth['access_token']
            self.token_expires_at = time.time() + auth['expires_in'] - 60  # -60s de marge

        return self.token

    def make_payment(self, msisdn, amount, merchant_id):
        token = self.get_valid_token()
        with ArzekaPayment(token=token) as client:
            return client.initiate_payment(msisdn, amount, merchant_id)
```

## Configuration de l'endpoint

L'endpoint d'authentification est défini dans les constantes :

```python
# Dans arzeka.py
AUTH_ENDPOINT = "AvepayPaymentGatewayUI/api/auth/login/"
```

Si l'API change, vous pouvez modifier cette constante ou l'endpoint peut être ajusté selon les besoins.

## Sécurité

### ⚠️ Bonnes pratiques

1. **Ne jamais hardcoder les identifiants**
```python
# ❌ MAL
auth = authenticate("user@example.com", "password123")

# ✅ BIEN
import os
username = os.getenv("ARZEKA_USERNAME")
password = os.getenv("ARZEKA_PASSWORD")
auth = authenticate(username, password)
```

2. **Stocker le token de manière sécurisée**
```python
# Ne pas logger le token complet
logger.info(f"Token obtenu: {token[:10]}...")  # Seulement les premiers caractères
```

3. **Gérer l'expiration du token**
```python
# Toujours vérifier la validité du token avant usage
if token_is_expired():
    auth = authenticate(username, password)
    token = auth['access_token']
```

## Tests

Voir `authentication_example.py` pour des exemples complets et des cas de test.

```bash
# Exécuter l'exemple
python authentication_example.py
```

## Questions fréquentes

### Q: Dois-je m'authentifier à chaque requête ?
**R:** Non, le token est valide pendant la durée indiquée par `expires_in`. Réutilisez-le pour plusieurs requêtes.

### Q: Que faire si le token expire pendant une opération ?
**R:** Réauthentifiez-vous et réessayez l'opération. Implémentez une logique de retry avec réauthentification.

### Q: Puis-je utiliser le même token pour plusieurs clients simultanés ?
**R:** Oui, le token peut être partagé entre plusieurs instances, mais attention aux limites de taux (rate limiting).

### Q: Comment savoir si mon token est expiré ?
**R:** Vous recevrez une erreur 401 lors de votre prochaine requête. Implémentez un système de vérification avec `expires_in`.

## Support

Pour plus d'exemples, consultez :
- `authentication_example.py` - Exemples détaillés
- `example.py` - Autres exemples d'utilisation
- `QUICKSTART.md` - Guide de démarrage rapide
