# ⛪ CIMPP - Centre International de Mission et de Prière Prophétique

CIMPP est une plateforme web moderne et complète conçue pour gérer les activités d'une organisation religieuse. Elle permet la diffusion de messages (prédications), la gestion d'événements, le suivi des témoignages, la programmation hebdomadaire et le streaming en direct.

---

## 🚀 Technologies Utilisées

### Backend & API
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

### Frontend
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

### Base de Données & Stockage
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=Cloudinary&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Garage](https://img.shields.io/badge/Garage_S3-E24329?style=for-the-badge&logo=S3&logoColor=white)

### DevOps & Déploiement
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%23499848.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![WhiteNoise](https://img.shields.io/badge/WhiteNoise-blue?style=for-the-badge)

---

## ✨ Fonctionnalités Clés

- **🎤 Gestion des Prédications** : Publication de sermons avec support audio, vidéo (YouTube) et résumé textuel.
- **📅 Événements** : Système complet de gestion et d'affichage des événements à venir.
- **🙏 Témoignages** : Soumission publique de témoignages et modération par les administrateurs.
- **⏰ Programme Hebdo** : Affichage dynamique des activités régulières de la semaine.
- **📽️ Live Stream** : Intégration de flux en direct pour les cultes en ligne.
- **🔢 Vérification par Code** : Système de validation par code à 6 chiffres pour l'inscription et la réinitialisation de mot de passe.
- **🔐 Authentification Sécurisée** : Système robuste via JWT pour l'accès aux fonctionnalités restreintes.
- **📱 API RESTful** : Documentation complète sous Swagger/OpenAPI pour l'intégration mobile.
- **📦 Stockage Hybride** : Support de Cloudinary (production) et Garage S3 (développement local).

---

## 🛠️ Installation et Configuration

### Prérequis
- Python 3.10+
- Docker & Docker Compose (Recommandé pour Garage S3)
- MySQL ou PostgreSQL

### Stockage Local (Garage S3)
Pour le développement local, ce projet utilise **Garage**, un service S3 open-source.
1. Consultez le guide détaillé : [garage_integration.md](./garage_integration.md).
2. Lancez le container Garage via Docker.
3. Configurez vos clés dans le fichier `.env`.

### Installation Locale
1. **Cloner le dépôt**
   ```bash
   git clone <url-du-depot>
   cd CIMPP
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration de l'environnement**
   Créez un fichier `.env` à la racine et configurez vos variables (DB, Cloudinary, Secret Key, etc.).

5. **Migrations et Lancement**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Via Docker
```bash
docker-compose up --build
```

---

## 📖 Documentation de l'API
L'API est documentée de manière interactive. Une fois le serveur lancé, accédez à :
- **Swagger UI** : `/api/schema/swagger-ui/`
- **Redoc** : `/api/schema/redoc/`

---

## 🤝 Contribution
Les contributions sont les bienvenues ! Pour des changements majeurs, veuillez d'abord ouvrir une discussion pour discuter de ce que vous aimeriez changer.

---

## 📄 Licence
Ce projet est sous licence propriétaire. Tous droits réservés à CIMPP.
