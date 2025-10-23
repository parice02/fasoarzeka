# 🔍 Vérification de la validité du token

## Vue d'ensemble

Deux méthodes sont disponibles pour vérifier la validité du token d'authentification :

1. **`is_token_valid()`** - Vérification simple (retourne `bool`)
2. **`get_token_expiry_info()`** - Informations détaillées (retourne `dict`)

## Méthode 1 : `is_token_valid()`

### Signature

```python
def is_token_valid(self, margin_seconds: int = 60) -> bool
```

### Description

Vérifie si le token d'authentification est toujours valide en se basant sur `self._expires_at`.

### Paramètres

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `margin_seconds` | int | 60 | Marge de sécurité en secondes avant l'expiration réelle |

### Retour

- `True` : Le token est valide et n'expirera pas dans les `margin_seconds` prochaines secondes
- `False` : Le token est expiré, inexistant, ou expirera bientôt

### Exemples d'utilisation

#### Exemple 1 : Vérification basique

```python
from arzeka import ArzekaPayment

client = ArzekaPayment()
client.authenticate("username", "password")

# Vérification simple
if client.is_token_valid():
    print("Token valide, vous pouvez faire des opérations")
else:
    print("Token expiré, réauthentification nécessaire")
```

#### Exemple 2 : Avec marge de sécurité personnalisée

```python
# Vérifier si le token est valide pour au moins 5 minutes
if client.is_token_valid(margin_seconds=300):
    print("Token valide pour au moins 5 minutes")
else:
    print("Token expire dans moins de 5 minutes")
```

#### Exemple 3 : Workflow avec réauthentification

```python
def faire_operation(client):
    # Vérifier avant chaque opération
    if not client.is_token_valid():
        print("Token expiré, réauthentification...")
        client.authenticate(USERNAME, PASSWORD)

    # Faire l'opération
    return client.initiate_payment(...)

with ArzekaPayment() as client:
    client.authenticate(USERNAME, PASSWORD)

    # Ces opérations vérifieront le token automatiquement
    result1 = faire_operation(client)
    time.sleep(3600)  # Attendre 1 heure
    result2 = faire_operation(client)  # Se réauthentifiera si nécessaire
```

### Cas d'usage

✅ **Utilisez `is_token_valid()` quand :**
- Vous voulez juste savoir si le token est valide
- Vous devez prendre une décision binaire (continuer ou réauthentifier)
- Vous voulez un code simple et lisible

## Méthode 2 : `get_token_expiry_info()`

### Signature

```python
def get_token_expiry_info(self) -> Dict[str, Any]
```

### Description

Retourne des informations détaillées sur l'expiration du token.

### Retour

Dictionnaire contenant :

| Clé | Type | Description |
|-----|------|-------------|
| `is_valid` | bool | Si le token est valide (équivalent à `is_token_valid()`) |
| `expires_at` | float/None | Timestamp Unix de l'expiration |
| `expires_in_seconds` | float | Secondes jusqu'à l'expiration (négatif si expiré) |
| `expires_in_minutes` | float | Minutes jusqu'à l'expiration |
| `is_expired` | bool | Si le token est déjà expiré |
| `has_token` | bool | Si un token est présent |

### Exemples d'utilisation

#### Exemple 1 : Afficher les informations

```python
client = ArzekaPayment()
client.authenticate("username", "password")

info = client.get_token_expiry_info()

print(f"Token valide: {info['is_valid']}")
print(f"Expire dans: {info['expires_in_minutes']:.1f} minutes")
print(f"Est expiré: {info['is_expired']}")
```

#### Exemple 2 : Décisions conditionnelles

```python
info = client.get_token_expiry_info()

if not info['has_token']:
    print("Pas de token, authentification requise")
    client.authenticate(USERNAME, PASSWORD)
elif info['is_expired']:
    print("Token expiré, réauthentification")
    client.authenticate(USERNAME, PASSWORD)
elif info['expires_in_minutes'] < 5:
    print("Token expire bientôt, réauthentification préventive")
    client.authenticate(USERNAME, PASSWORD)
else:
    print(f"Token OK pour {info['expires_in_minutes']:.1f} min")
```

#### Exemple 3 : Monitoring et logging

```python
import logging

def monitor_token_status(client):
    info = client.get_token_expiry_info()

    logging.info(f"Token Status Report:")
    logging.info(f"  Has Token: {info['has_token']}")
    logging.info(f"  Is Valid: {info['is_valid']}")
    logging.info(f"  Expires In: {info['expires_in_minutes']:.2f} minutes")

    if info['expires_in_minutes'] < 10:
        logging.warning(f"Token expires soon!")

    return info

# Utilisation
with ArzekaPayment() as client:
    client.authenticate(USERNAME, PASSWORD)
    monitor_token_status(client)
```

### Cas d'usage

✅ **Utilisez `get_token_expiry_info()` quand :**
- Vous avez besoin d'informations précises sur l'expiration
- Vous voulez logger ou afficher des détails
- Vous devez prendre des décisions basées sur le temps restant
- Vous créez un système de monitoring

## Comparaison des méthodes

| Critère | `is_token_valid()` | `get_token_expiry_info()` |
|---------|-------------------|---------------------------|
| **Simplicité** | ⭐⭐⭐⭐⭐ Simple | ⭐⭐⭐ Moyenne |
| **Informations** | ⭐⭐ Basique (bool) | ⭐⭐⭐⭐⭐ Détaillées (dict) |
| **Performance** | ⭐⭐⭐⭐⭐ Rapide | ⭐⭐⭐⭐ Rapide |
| **Cas d'usage** | Décisions simples | Monitoring, logging |

## Fonctionnement interne

### Calcul de `_expires_at`

Lors de l'authentification, `_expires_at` est calculé comme suit :

```python
# Dans la méthode authenticate()
self._expires_at = time.time() + self.expires_in - 60
#                  ^              ^                 ^
#                  Maintenant     Durée du token   Marge sécurité
```

**Exemple :**
- Heure actuelle : `1729600000` (timestamp)
- `expires_in` : `3600` secondes (1 heure)
- Marge de sécurité : `60` secondes
- `_expires_at` = `1729600000 + 3600 - 60` = `1729603540`

### Vérification de validité

```python
# Dans is_token_valid()
current_time = time.time()
time_until_expiry = self._expires_at - current_time
is_valid = time_until_expiry > margin_seconds
```

**Exemple :**
- `_expires_at` : `1729603540`
- Heure actuelle : `1729600100`
- Temps restant : `3440` secondes (~57 minutes)
- Avec marge 60s : `3440 > 60` = `True` ✅
- Avec marge 3600s : `3440 > 3600` = `False` ❌

## Bonnes pratiques

### 1. Vérifier avant les opérations critiques

```python
if client.is_token_valid():
    # Faire l'opération
    payment = client.initiate_payment(...)
else:
    # Réauthentifier d'abord
    client.authenticate(USERNAME, PASSWORD)
    payment = client.initiate_payment(...)
```

### 2. Utiliser une marge appropriée

```python
# Pour opérations rapides (< 1 minute)
if client.is_token_valid(margin_seconds=60):
    # OK pour opérations courtes

# Pour opérations longues (plusieurs minutes)
if client.is_token_valid(margin_seconds=300):
    # OK pour opérations qui peuvent prendre 5 minutes
```

### 3. Logger les réauthentifications

```python
import logging

if not client.is_token_valid():
    logging.info("Token expiré, réauthentification en cours")
    client.authenticate(USERNAME, PASSWORD)
    logging.info("Réauthentification réussie")
```

### 4. Créer une classe wrapper

```python
class AutoReauthClient:
    def __init__(self, username, password):
        self.client = ArzekaPayment()
        self.username = username
        self.password = password
        self.client.authenticate(username, password)

    def ensure_authenticated(self):
        """Garantit que le client est authentifié"""
        if not self.client.is_token_valid():
            self.client.authenticate(self.username, self.password)

    def make_payment(self, **kwargs):
        """Fait un paiement avec réauth automatique"""
        self.ensure_authenticated()
        return self.client.initiate_payment(**kwargs)
```

## Gestion d'erreurs

```python
try:
    if not client.is_token_valid():
        client.authenticate(USERNAME, PASSWORD)

    # Faire l'opération
    result = client.initiate_payment(...)

except ArzekaAuthenticationError as e:
    print(f"Échec d'authentification: {e}")
except Exception as e:
    print(f"Erreur: {e}")
```

## Tests

```python
import unittest

class TestTokenValidation(unittest.TestCase):
    def test_token_valid_after_auth(self):
        client = ArzekaPayment()
        client.authenticate(USERNAME, PASSWORD)
        self.assertTrue(client.is_token_valid())

    def test_token_info_structure(self):
        client = ArzekaPayment()
        client.authenticate(USERNAME, PASSWORD)
        info = client.get_token_expiry_info()

        # Vérifier la structure
        self.assertIn('is_valid', info)
        self.assertIn('expires_at', info)
        self.assertIn('expires_in_seconds', info)
        self.assertTrue(info['has_token'])
        self.assertTrue(info['is_valid'])
```

## Questions fréquentes

### Q: Quelle marge de sécurité utiliser ?

**R:**
- **60s (défaut)** : Pour la plupart des cas
- **300s (5 min)** : Pour opérations qui peuvent prendre plusieurs minutes
- **600s (10 min)** : Pour opérations batch ou longues

### Q: Que faire si le token expire pendant une opération ?

**R:** L'opération échouera avec une erreur 401. Implémentez un retry avec réauthentification.

### Q: Puis-je modifier `_expires_at` manuellement ?

**R:** Non recommandé. Cette valeur est calculée automatiquement lors de l'authentification.

### Q: Le client se réauthentifie-t-il automatiquement ?

**R:** Non, vous devez appeler `authenticate()` manuellement après avoir vérifié avec `is_token_valid()`.

## Voir aussi

- `authentication_example.py` - Exemples d'authentification
- `token_validation_example.py` - Exemples de validation de token
- `AUTHENTICATION.md` - Documentation complète de l'authentification
