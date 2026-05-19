# Guide Complet : Garage S3 + Django Storage
> Stockage de fichiers media (images, vidéos) avec Garage S3 auto-hébergé et Django

---

## Prérequis

| Composant | Version testée |
|---|---|
| Ubuntu Server | 22.04 LTS |
| Docker | 24+ |
| Python | 3.10+ |
| Django | 4.x / 5.x |
| django-storages | 1.14+ |
| boto3 | 1.34+ |

---

## PARTIE 1 — Installation de Garage sur le serveur Linux

### 1.1 Préparer les dossiers

```bash
sudo mkdir -p /data/garage/meta
sudo mkdir -p /data/garage/data
sudo mkdir -p /etc/garage
```

### 1.2 Créer le fichier de configuration

```bash
sudo nano /etc/garage/garage.toml
```

Contenu :

```toml
metadata_dir = "/data/meta"
data_dir = "/data/data"
db_engine = "lmdb"
replication_factor = 1
rpc_bind_addr = "0.0.0.0:3901"
rpc_secret = "GENERER_AVEC_openssl_rand_-hex_32"

[s3_api]
s3_region = "garage"
api_bind_addr = "0.0.0.0:3900"

[s3_web]
bind_addr = "0.0.0.0:3902"
root_domain = ".web.garage"
index = "index.html"

[admin]
api_bind_addr = "0.0.0.0:3903"
admin_token = "GENERER_AVEC_openssl_rand_-hex_32"
```

> Génère les secrets avec : `openssl rand -hex 32`

### 1.3 Lancer Garage avec Docker

```bash
sudo docker run -d \
  --name garage \
  --restart unless-stopped \
  -p 3900:3900 \
  -p 3901:3901 \
  -p 3902:3902 \
  -p 3903:3903 \
  -v /etc/garage/garage.toml:/etc/garage.toml \
  -v /data/garage:/data \
  dxflrs/garage:v1.0.1 /garage server
```

Vérifier que ça tourne :

```bash
sudo docker ps
# Tu dois voir le container "garage" avec status "Up"
```

---

## PARTIE 2 — Configuration de Garage (clés + bucket)

### 2.1 Initialiser le nœud

```bash
# Voir l'ID du nœud
sudo docker exec garage /garage node list

# Assigner le layout (remplace NODE_ID par l'ID affiché)
sudo docker exec garage /garage layout assign -z dc1 -c 1G NODE_ID
sudo docker exec garage /garage layout apply --version 1
```

### 2.2 Créer une clé d'accès

```bash
sudo docker exec garage /garage key create mon-projet-key
```

Note bien le `Key ID` et le `Secret key` affichés — ils ne seront plus montrés.

### 2.3 Créer un bucket

```bash
sudo docker exec garage /garage bucket create mon-bucket
```

### 2.4 Donner accès à la clé sur le bucket

```bash
sudo docker exec garage /garage bucket allow \
  --read --write \
  --key KEY_ID \
  mon-bucket
```

### 2.5 Activer le mode website sur le bucket (accès public)

Crée un fichier Python `activate_website.py` sur ta machine de dev :

```python
import requests

GARAGE_ADMIN_URL = "http://IP_SERVEUR:3903"
ADMIN_TOKEN = "TON_ADMIN_TOKEN"
BUCKET_NAME = "mon-bucket"

# Trouver l'ID du bucket
r = requests.get(
    f"{GARAGE_ADMIN_URL}/v1/bucket?list",
    headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
)
buckets = r.json()
print("Buckets disponibles :", buckets)

# Trouver l'ID correspondant au nom
bucket_id = None
for b in buckets:
    if BUCKET_NAME in b.get('globalAliases', []):
        bucket_id = b['id']
        break

print(f"Bucket ID : {bucket_id}")

# Activer le website access
if bucket_id:
    r2 = requests.put(
        f"{GARAGE_ADMIN_URL}/v1/bucket?id={bucket_id}",
        headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
        json={
            "bucketId": bucket_id,
            "websiteAccess": {
                "enabled": True,
                "indexDocument": "index.html",
                "errorDocument": "error.html"
            }
        }
    )
    print(f"Status : {r2.status_code}")
    print(r2.json())
```

```bash
python activate_website.py
```

---

## PARTIE 3 — Proxy Django pour servir les fichiers publiquement

> Garage v1.x ne supporte pas l'accès anonyme S3 natif.
> La solution : Django récupère le fichier depuis Garage et le sert au client.

### 3.1 Ajouter la vue proxy dans `api/views.py`

```python
import boto3
from django.http import HttpResponse, Http404

def serve_media(request, path):
    s3 = boto3.client(
        's3',
        endpoint_url='http://IP_SERVEUR:3900',
        aws_access_key_id='TON_KEY_ID',
        aws_secret_access_key='TON_SECRET_KEY',
        region_name='garage',
        config=boto3.session.Config(signature_version='s3v4')
    )
    try:
        obj = s3.get_object(Bucket='mon-bucket', Key=path)
        content_type = obj.get('ContentType', 'application/octet-stream')
        response = HttpResponse(obj['Body'].read(), content_type=content_type)
        response['Cache-Control'] = 'public, max-age=86400'
        return response
    except Exception:
        raise Http404
```

### 3.2 Ajouter l'URL dans `CIMPP/urls.py`

```python
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from api.views import serve_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path("cimppApi/", include('api.urls')),
    path("api-auth/", include("rest_framework.urls")),
    re_path(r'^media/(?P<path>.+)$', serve_media, name='serve_media'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## PARTIE 4 — Configuration Django (settings.py)

### 4.1 Installer les dépendances

```bash
pip install django-storages boto3
```

### 4.2 Ajouter dans `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'storages',
]
```

### 4.3 Configuration du storage

```python
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Connexion Garage S3
AWS_ACCESS_KEY_ID = 'TON_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'TON_SECRET_KEY'
AWS_STORAGE_BUCKET_NAME = 'mon-bucket'
AWS_S3_ENDPOINT_URL = 'http://IP_SERVEUR:3900'
AWS_S3_REGION_NAME = 'garage'
AWS_S3_ADDRESSING_STYLE = 'path'

# URLs publiques via proxy Django
AWS_S3_CUSTOM_DOMAIN = 'IP_MACHINE_DJANGO:8000/media'
AWS_S3_URL_PROTOCOL = 'http:'
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SECURE_URLS = False
AWS_S3_CUSTOM_DOMAIN = None
```

---

## PARTIE 5 — Variables d'environnement (.env)

Mets les secrets dans un fichier `.env` à la racine du projet :

```env
SECRET_KEY=django-secret-key-ici
DEBUG=True

DB_NAME=nom_base
DB_USER=utilisateur
DB_PASSWORD=mot_de_passe
DB_HOST=host_base
DB_PORT=3306

GARAGE_KEY_ID=GKxxxxxxxxxxxxxxxxxxxxxxxx
GARAGE_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GARAGE_ENDPOINT=http://192.168.1.X:3900
GARAGE_BUCKET=mon-bucket
```

Et dans `settings.py` :

```python
AWS_ACCESS_KEY_ID = os.getenv('GARAGE_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('GARAGE_SECRET_KEY')
AWS_S3_ENDPOINT_URL = os.getenv('GARAGE_ENDPOINT')
AWS_STORAGE_BUCKET_NAME = os.getenv('GARAGE_BUCKET')
```

---

## PARTIE 6 — Résumé des ports Garage

| Port | Rôle |
|---|---|
| 3900 | API S3 (upload/download avec auth) |
| 3901 | RPC interne (cluster) |
| 3902 | Web public (website mode) |
| 3903 | API Admin (gestion buckets/clés) |

---

## PARTIE 7 — Commandes utiles

```bash
# Voir les buckets
sudo docker exec garage /garage bucket list

# Voir les clés
sudo docker exec garage /garage key list

# Voir l'état du cluster
sudo docker exec garage /garage status

# Redémarrer Garage
sudo docker restart garage

# Voir les logs
sudo docker logs garage -f
```

---

## PARTIE 8 — Problèmes connus

### ❌ `AccessDenied: Garage does not support anonymous access yet`
→ Garage v1.x ne supporte pas les bucket policies S3 ni l'accès anonyme.
→ **Solution :** utiliser le proxy Django (Partie 3) ou le mode website (port 3902).

### ❌ `PutBucketPolicy: NotImplemented`
→ Garage ne supporte pas cette API S3.
→ **Solution :** utiliser l'API Admin Garage (port 3903).

### ❌ Kernel panic sur VM VirtualBox
→ Conflit entre VirtualBox Guest Additions et le kernel Linux.
→ **Solution :**
```bash
sudo apt remove virtualbox-guest-utils virtualbox-guest-dkms -y
sudo reboot
```

### ❌ `circular import` avec un fichier nommé `re.py` ou `requests.py`
→ Ne jamais nommer un fichier Python comme un module standard.
→ Utilise des noms explicites : `garage_setup.py`, `activate_bucket.py`, etc.

---

*Guide rédigé suite à une installation réelle sur Ubuntu Server 22.04 + VirtualBox + Django CIMPP — Mai 2026*