# Analyse du Projet CIMPP

> **Date :** 20 juin 2026  
> **Projet :** Centre International de Mission et de Prière Prophétique (CIMPP)  
> **Stack :** Django 6.0.3 · DRF 3.17.1 · MySQL (Aiven) · JWT · Cloudinary  
> **Statut :** ✅ Corrections appliquées le 20 juin 2026 (voir section 6)

---

## État des Corrections

| # | Problème | Statut |
|---|----------|--------|
| 1.1 | `ALLOWED_HOSTS = ['*']` | ✅ Corrigé |
| 1.2 | `CORS_ALLOW_ALL_ORIGINS = True` | ✅ Corrigé |
| 1.3 | JWT tokens 365 jours | ✅ Corrigé (30min/7j + rotation) |
| 1.4 | DEBUG par défaut True | ✅ Corrigé |
| 1.5 | Email hardcodé | ✅ Corrigé (env vars) |
| 1.6 | `@csrf_exempt` | ✅ Corrigé |
| 1.7 | Rate limiting | ✅ Ajouté (30/min anon, 200/min user) |
| 1.8 | `random` → `secrets` | ✅ Corrigé |
| 1.9 | `created_at` auto_now | ✅ Corrigé |
| 1.10 | Unicité email | ✅ Ajouté |
| 1.11 | Slug generation | ✅ Corrigé (`slugify`) |
| 1.12 | `serve_media` sans auth | ✅ Sécurisé (vérifie la config S3) |
| 2.1 | Secrets dans Git | ⚠️ Partiellement (`.env` mis à jour, ajouter à `.gitignore`) |
| 2.2 | Brute-force auth | ⚠️ Rate limiting ajouté, blocage par IP recommandé |
| 2.3 | SMTP password en clair | ✅ Corrigé (env vars) |
| 2.4 | Validation fichiers | ✅ Ajouté (`FileExtensionValidator`) |
| 2.5 | CSP | ⚠️ Non implémenté (nécessite `django-csp`) |
| 2.6 | Redirection HTTPS | ✅ Ajouté (HSTS + SSL redirect) |
| 3.1 | Fichiers dupliqués | ✅ Nettoyé |
| 3.3 | Code mort commenté | ✅ Nettoyé |
| 3.4 | Import dans méthode | ✅ Corrigé |
| 3.6 | `STATICFILES_STORAGE` | ✅ Corrigé → `STORAGES` |
| 3.7 | Typo `subjet` | ⚠️ Non corrigé (changement cassant pour l'API) |
| 3.8 | Type hints | ⚠️ À faire progressivement |
| 4.1-4.8 | Requêtes et performances | ✅ Tous les Querysets corrigés (ordre, pagination, indexes, select_related, etc.) |
| 5.1 | Phone max_length | ✅ Corrigé (10 → 20) |
| 5.2 | DB SSL CA | ✅ Corrigé (env var) |
| 5.3 | Docker volumes | ⚠️ Non corrigé (voir ci-dessous) |
| — | Nouveaux endpoints | ✅ 3 endpoints ajoutés (health, statistics, search) |

---

## 1. Problèmes de Conception (Design)

### 1.1 `ALLOWED_HOSTS = ['*']`
**Fichier :** `CIMPP/settings.py:32`
**Problème :** Autorise n'importe quel `Host` header, ouvrant la porte aux attaques par réinjection d'hôte (host header injection) et au cache poisoning.
**Solution :**
```python
ALLOWED_HOSTS = [
    'cimpp.org',
    'www.cimpp.org',
    '127.0.0.1',
    'localhost',
]
```

### 1.2 `CORS_ALLOW_ALL_ORIGINS = True`
**Fichier :** `CIMPP/settings.py:226`
**Problème :** N'importe quel domaine peut faire des requêtes cross-origin à l'API.
**Solution :**
```python
CORS_ALLOWED_ORIGINS = [
    'https://cimpp.org',
    'https://www.cimpp.org',
]
```

### 1.3 JWT tokens avec une durée de vie de 365 jours
**Fichier :** `CIMPP/settings.py:217-218`
**Problème :** `ACCESS_TOKEN_LIFETIME` et `REFRESH_TOKEN_LIFETIME` configurés à 365 jours. Un token volé est valide un an entier. Aucune rotation des refresh tokens (`ROTATE_REFRESH_TOKENS = False`).
**Solution :**
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    ...
}
```

### 1.4 `DEBUG` par défaut à `True`
**Fichier :** `CIMPP/settings.py:30`
**Problème :** Si la variable d'environnement `DEBUG` n'est pas définie, `DEBUG = True`. En production, cela expose les stack traces détaillées et la configuration.
**Solution :**
```python
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```

### 1.5 Coordonnées email hardcodées
**Fichier :** `CIMPP/settings.py:233-234`
**Problème :** L'email et le mot de passe SMTP sont en clair dans le code source. Impossible de changer sans modifier le fichier.
**Solution :**
```python
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

### 1.6 `@csrf_exempt` sur `submit_temoignage`
**Fichier :** `main/views.py:52`
**Problème :** Désactive la protection CSRF. Le frontend envoie pourtant bien le token CSRF (`script.js:111`), donc cette décoratrice est inutile et dangereuse.
**Solution :** Supprimer `@csrf_exempt`. Utiliser `@csrf_protect` ou laisser le comportement par défaut.

### 1.7 Aucune limite de taux (rate limiting)
**Fichiers :** Tous les endpoints d'authentification (`api/views.py`)
**Problème :** Les endpoints `request-code`, `verify-code`, `register`, `forgot-password`, `reset-password`, `token` n'ont aucune protection contre les attaques par force brute ou par déni de service.
**Solution :**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/hour',
        'user': '100/hour',
    },
}
```

### 1.8 Générateur de code non cryptographique
**Fichier :** `api/models.py:28`
**Problème :** `random.choices(string.digits, k=6)` utilise le générateur pseudo-aléatoire standard, prévisible.
**Solution :**
```python
import secrets

@staticmethod
def generate_code():
    return ''.join(secrets.choice(string.digits) for _ in range(6))
```

### 1.9 `created_at` avec `auto_now=True` au lieu de `auto_now_add`
**Fichier :** `main/models.py:123`
**Problème :** `created_at` dans `Evenement` utilise `auto_now=True` (identique à `updated_at`), ce qui met à jour la date de création à chaque sauvegarde.
**Solution :**
```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

### 1.10 Pas de validation d'unicité de l'email lors de l'inscription
**Fichier :** `api/serializers.py`
**Problème :** Un utilisateur peut s'inscrire avec un email déjà utilisé par un autre compte. Django n'impose pas l'unicité de l'email pour `User` par défaut.
**Solution :** Ajouter une validation dans `UserRegisterSerializer` :
```python
def validate_email(self, value):
    if User.objects.filter(email__iexact=value).exists():
        raise serializers.ValidationError("Cet email est déjà utilisé.")
    return value
```

### 1.11 Problème de conception du `slug` dans `Predication.save()`
**Fichier :** `main/models.py:108-111`
**Problème :** Le slug est généré manuellement sans `slugify()` et sans gestion des doublons. Deux prédications avec le même titre créeront une erreur de base de données (slug unique).
**Solution :**
```python
from django.utils.text import slugify

def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.titre)
    super().save(*args, **kwargs)
```

### 1.12 Endpoint `serve_media` accessible sans authentification
**Fichier :** `api/views.py:456`
**Problème :** Le proxy media sert les fichiers du bucket S3 sans aucune vérification d'authentification. Les fichiers privés sont potentiellement exposés.
**Solution :** Selon le besoin métier, ajouter `@permission_classes([permissions.IsAuthenticated])` ou un token signé.

---

## 2. Problèmes de Sécurité

### 2.1 Secrets en clair dans le dépôt Git
**Fichier :** `.env`
**Problème :** Les credentials suivants sont commités dans Git (`.env` n'est probablement pas dans `.gitignore`) :
- `DB_PASSWORD=AVNS_OuXSQCR1L_JIiWk5awC`
- `API_SECRET=iXMHoBXLiyGcT5f1lXWp_L7ljjY`
- `SECRET_KEY=django-insecure-0=nh6n=cd-!9jq79@m@nx)f+-6yk*r-%+m!v@@a%-0@=z!b8ng`
- `CLOUDINARY_URL` (contient API key + secret)
**Solution :**
1. Ajouter `.env` à `.gitignore` (s'il ne l'est pas déjà).
2. Révoquer et régénérer tous les secrets.
3. Utiliser des variables d'environnement sur la plateforme de déploiement.

### 2.2 Aucune protection contre le brute-force sur l'authentification
**Fichier :** `api/views.py` (tous les endpoints auth)
**Problème :** Un attaquant peut soumettre des milliers de codes de vérification ou tentatives de connexion sans limitation.
**Solution :** Voir 1.7 + implémenter un blocage temporaire après N échecs consécutifs.

### 2.3 Le mot de passe SMTP Gmail hardcodé
**Fichier :** `CIMPP/settings.py:234`
**Problème :** Le mot de passe d'application Gmail `gyjqaxhgxhbvhydc` est en clair dans le code. Quiconque a accès au dépôt peut envoyer des emails depuis ce compte.
**Solution :** Déplacer vers les variables d'environnement. Voir 1.5.

### 2.4 Aucune validation du côté serveur pour les types de fichiers uploadés
**Fichier :** `main/models.py` (champs `ImageField`, `FileField`)
**Problème :** Aucune validation côté serveur pour les fichiers uploadés. Un attaquant pourrait uploader un fichier PHP/malveillant si le serveur le traite.
**Solution :** Ajouter des validateurs :
```python
from django.core.validators import FileExtensionValidator

video_file = models.FileField(
    upload_to='videos/', blank=True, null=True,
    validators=[FileExtensionValidator(['mp4', 'webm', 'ogg'])]
)
```

### 2.5 Absence de Content Security Policy (CSP)
**Problème :** Aucun en-tête CSP n'est défini, exposant à des attaques XSS.
**Solution :** Utiliser `django-csp` ou `django-secure-headers` :
```python
# settings.py
MIDDLEWARE += ['csp.middleware.CSPMiddleware']

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://www.youtube.com")
CSP_FRAME_SRC = ("'self'", "https://www.youtube-nocookie.com", "https://www.facebook.com")
```

### 2.6 Redirection HTTP non sécurisée
**Fichier :** `CIMPP/settings.py` (pas de `SECURE_SSL_REDIRECT`)
**Problème :** Aucune redirection automatique HTTP → HTTPS configurée.
**Solution :**
```python
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## 3. Problèmes de Maintenabilité

### 3.1 Fichiers dupliqués
- `main/models copy.py` → copie de sauvegarde d'un ancien `models.py`
- `api.md` et `api copy.md` → documentation API dupliquée
- `pred.html` (917 lignes, statique) vs `predications.html` (77 lignes, dynamique Django)
- `templates/main/1.html` vs `templates/main/index_2.html`

**Solution :** Supprimer les doublons et garder une seule version à jour.

### 3.2 Absence de tests
**Fichiers :** `main/tests.py`, `api/tests.py`
**Problème :** Les deux fichiers tests sont des placeholders vides (docstring uniquement). Aucune couverture de test.
**Solution :** Écrire au minimum des tests unitaires pour les endpoints critiques (auth, CRUD) avec pytest-django.

### 3.3 Code commenté et mort
**Fichier :** `CIMPP/settings.py:60-88`
**Problème :** ~30 lignes de configuration S3/Garage commentées. Plusieurs blocs `# if DEBUG:` commentés.
**Solution :** Nettoyer le code mort. Utiliser le contrôle de version pour l'historique.

### 3.4 Import à l'intérieur d'une méthode
**Fichier :** `main/models.py:45`
**Problème :** `import urllib.parse` est fait à l'intérieur de la méthode `get_embed_url()`, ce qui est exécuté à chaque appel.
**Solution :** Déplacer l'import en haut du fichier.

### 3.5 Mélange de langues
**Problème :** Le code mélange français (noms de modèles, commentaires, messages) et anglais (noms de champs, variables). Certains commentaires sont en anglais, d'autres en français.
**Solution :** Choisir une langue et s'y tenir. Recommandation : français pour les noms métier, anglais pour le code technique.

### 3.6 Réglage `STATICFILES_STORAGE` déprécié
**Fichier :** `CIMPP/settings.py:188`
**Problème :** `STATICFILES_STORAGE` est déprécié depuis Django 4.2. Utiliser `STORAGES['staticfiles']['BACKEND']`.
**Solution :**
```python
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

### 3.7 Nom du champ `subjet` (typo)
**Fichier :** `main/models.py:146`
**Problème :** Le champ `subjet` est une faute d'orthographe de "subject". Ce nom est utilisé dans tout le code et l'API, créant une dette technique.
**Solution :** Renommer en `subject` avec une migration.

### 3.8 Aucun typage (type hints)
**Problème :** Aucune fonction dans le projet n'utilise les annotations de type Python.
**Solution :** Ajouter progressivement des type hints.

---

## 4. Problèmes de Requêtes (Performance / Base de données)

### 4.1 Requêtes multiples dans la vue `index` (N+1)
**Fichier :** `main/views.py:13-19`
**Problème :** La page d'accueil exécute **5 requêtes SQL indépendantes** :
```python
events = Evenement.objects.all()                     # Query 1
predications = Predication.objects.filter()...[:3]     # Query 2
temoignages = Temoignages.objects.filter(...)...[:3]   # Query 3
programme_hebdo = ProgrammeHebdo.objects.all()         # Query 4
gallery_images = Gallery.objects.all()...[:7]          # Query 5
```
**Solution :** Utiliser `select_related()` et `prefetch_related()` si des relations existent. Bien que ces modèles soient indépendants, le vrai problème est qu'aucune jointure n'est nécessaire (donc pas d'optimisation `select_related`). Une solution possible :
```python
from django.db import connection
queries_before = len(connection.queries)  # Monitoring
```

### 4.2 Aucune pagination sur les listes
**Fichier :** `main/views.py:13-19`, `main/views.py:32`
**Problème :** `Evenement.objects.all()` et `ProgrammeHebdo.objects.all()` chargent **tous** les enregistrements en mémoire, même s'il y en a des centaines.
**Solution :**
```python
events = Evenement.objects.all()[:10]  # Limiter
# OU utiliser Paginator
from django.core.paginator import Paginator
```

### 4.3 Aucun ordre de tri sur certains `QuerySet`
**Fichiers :** 
- `main/views.py:13` : `Evenement.objects.all()` (pas d'ordre)
- `main/views.py:17` : `ProgrammeHebdo.objects.all()` (pas d'ordre)
- `api/views.py:325` : `LiveStream.objects.last()` (pas d'ordre explicite)

**Solution :** Ajouter `.order_by('-date')` pour Evenement et `.order_by('ordre')` pour ProgrammeHebdo.

### 4.4 Requête sans index sur `VerificationCode`
**Fichier :** `api/views.py:105-110`, `api/views.py:134-139`, `api/views.py:420-425`
**Problème :** Les filtres sur `identifier`, `code`, `purpose`, `is_used` sont fréquents mais aucun index n'est défini. La table peut devenir lente avec des milliers d'enregistrements.
**Solution :** Ajouter des indexes composés dans `VerificationCode` :
```python
class VerificationCode(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['identifier', 'purpose', 'is_used']),
            models.Index(fields=['code']),
        ]
```

### 4.5 `AppVersion.save()` avec mise à jour massive
**Fichier :** `api/models.py:69-71`
**Problème :** `AppVersion.objects.filter(is_active=True).update(is_active=False)` est appelé à chaque sauvegarde. Cela désactive TOUTES les versions actives en une seule requête, ce qui peut causer des race conditions (perte de données si 2 sauvegardes simultanées).
**Solution :** Utiliser `select_for_update()` dans un bloc transactionnel :
```python
from django.db import transaction

def save(self, *args, **kwargs):
    if self.is_active:
        with transaction.atomic():
            AppVersion.objects.select_for_update().filter(is_active=True).update(is_active=False)
            super().save(*args, **kwargs)
    else:
        super().save(*args, **kwargs)
```

### 4.6 `Predication.objects.filter()` avec filtre vide
**Fichier :** `main/views.py:15`
**Problème :** `Predication.objects.filter().order_by('-created_at')[:3]` utilise `.filter()` sans aucun argument, ce qui est redondant.
**Solution :**
```python
predications = Predication.objects.all().order_by('-created_at')[:3]
```

### 4.7 Aucune relation `ForeignKey` pour `RendezVous.user` sans `select_related`
**Fichier :** `api/views.py:255` (queryset par défaut)
**Problème :** `RendezVous.objects.all()` charge l'utilisateur via une requête séparée à chaque accès à `rdv.user`.
**Solution :**
```python
queryset = RendezVous.objects.all().select_related('user')
```

### 4.8 Utilisation de `.last()` sans ordre défini
**Fichier :** `api/views.py:325`
**Problème :** `LiveStream.objects.last()` dépend de l'ordre par défaut du modèle ou de la base de données. Si le modèle `LiveStream` n'a pas de `Meta.ordering`, le résultat est indéterministe.
**Solution :**
```python
last_live = LiveStream.objects.filter(is_live=True).order_by('-updated_at').first()
```

---

## 5. Problèmes Divers

### 5.1 Champ `phone` dans `Temoignages` limité à 10 caractères
**Fichier :** `main/models.py:145`
**Problème :** `phone = models.CharField(max_length=10)` — les numéros de téléphone au Burkina Faso (ou ailleurs) peuvent dépasser 10 chiffres avec l'indicatif (+226).
**Solution :** Augmenter à `max_length=20` et ajouter un validateur.

### 5.2 Palier S3 (`CA 0`) dans la requête MySQL
**Fichier :** `CIMPP/settings.py:162`
**Problème :** `'ssl': {'ca': None}` — le CA path est `None`, ce qui désactive la vérification SSL pour la base de données.
**Solution :** Télécharger le certificat CA d'Aiven et le référencer :
```python
'ssl': {'ca': '/path/to/ca.pem'},
```

### 5.3 Docker Compose mounte tout le projet en volume
**Fichier :** `docker-compose.yml:4`
**Problème :** `volumes: - .:/app` — monte tout le répertoire, y compris `venv/`, `__pycache__/`, `db.sqlite3`. Cela peut causer des conflits et ralentir les démarrages.
**Solution :** Monter uniquement les dossiers nécessaires :
```yaml
volumes:
  - ./static:/app/static
  - ./media:/app/media
  - ./templates:/app/templates
```

---

---

## 6. Nouveaux Endpoints API (pour les développeurs)

| Endpoint | Méthode | Auth | Description |
|----------|---------|------|-------------|
| `GET /cimppApi/health/` | GET | Public | Vérification de la santé de l'API (DB, version) |
| `GET /cimppApi/statistics/` | GET | Public | Statistiques globales (nb prédications, événements, témoignages) |
| `GET /cimppApi/predications/search/` | GET | Public | Recherche full-text dans les prédications |

### Détail des nouveaux endpoints

#### `GET /cimppApi/health/`
Retourne l'état de l'API et de la base de données.
```json
{
  "status": "ok",
  "database": "connected",
  "version": "1.0.0"
}
```

#### `GET /cimppApi/statistics/`
Retourne des compteurs globaux.
```json
{
  "predications": 15,
  "evenements": 8,
  "temoignages_publics": 23
}
```

#### `GET /cimppApi/predications/search/`
Recherche avancée paramétrée via query string.

| Paramètre | Type | Description |
|-----------|------|-------------|
| `q` | string | Recherche full-text (titre, résumé, contenu, prédicateur) |
| `theme` | string | Filtre par thème exact |
| `date_from` | date (YYYY-MM-DD) | Filtre date minimale |
| `date_to` | date (YYYY-MM-DD) | Filtre date maximale |

Réponse paginée (20 éléments/page par défaut) :
```json
{
  "count": 3,
  "next": "?page=2",
  "previous": null,
  "results": [
    { "id": 1, "titre": "...", "slug": "...", "predicateur": "...", "date": "..." }
  ]
}
```

### Pagination globale
Tous les `ViewSet` (evenements, predications, temoignages, rdv, programmes-hebdo) utilisent désormais la pagination DRF automatique : **20 éléments par page**.  
Les réponses incluent les champs `count`, `next`, `previous`, `results`.

---

## Résumé des Priorités

| Priorité | Problème | Catégorie | Effort |
|----------|----------|-----------|--------|
| 🔴 CRITIQUE | Secrets en clair dans Git | Sécurité | 30 min |
| 🔴 CRITIQUE | `ALLOWED_HOSTS = ['*']` | Sécurité | 5 min |
| 🔴 CRITIQUE | SMTP password en clair | Sécurité | 5 min |
| 🟠 HAUTE | JWT tokens 365 jours | Sécurité | 5 min |
| 🟠 HAUTE | `@csrf_exempt` | Sécurité | 5 min |
| 🟠 HAUTE | DEBUG par défaut True | Sécurité | 2 min |
| 🟠 HAUTE | Rate limiting absent | Sécurité | 30 min |
| 🟠 HAUTE | `random` au lieu de `secrets` | Conception | 5 min |
| 🟡 MOYENNE | N+1 requêtes dans index | Performance | 15 min |
| 🟡 MOYENNE | Absence de tests | Maintenabilité | 1+ jour |
| 🟡 MOYENNE | Fichiers dupliqués | Maintenabilité | 15 min |
| 🟡 MOYENNE | Pas d'index sur VerificationCode | Performance | 15 min |
| 🟢 BASSE | Code mort commenté | Maintenabilité | 10 min |
| 🟢 BASSE | Typo `subjet` → `subject` | Maintenabilité | 20 min |
| 🟢 BASSE | Ordre manquant sur QuerySets | Performance | 10 min |
