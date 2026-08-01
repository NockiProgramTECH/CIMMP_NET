# Documentation de l'API CIMPP (Spécifications JSON)

Cette API utilise le format JSON pour tous les échanges de données, sauf pour les uploads de fichiers qui nécessitent `multipart/form-data`.

## Informations Générales
- **URL de Base** : `http://<votre-domaine>/cimppApi/`
- **Authentification** : JWT (`Authorization: Bearer <access_token>`).

---

## 1. Authentification & Comptes (`/auth/`)

### Demande de code de vérification
- `POST /auth/request-code/`
    - **Entrée (JSON)** :
    ```json
    {
        "identifier": "01234567", // Numéro de téléphone ou Email
        "purpose": "REGISTER" // ou "PASSWORD_RESET"
    }
    ```
    - **Sortie (JSON - 200 OK)** :
    ```json
    {
        "message": "Code de vérification envoyé à 01234567.",
        "code": "123456" // Uniquement présent en mode test/dev
    }
    ```

### Vérification de code
- `POST /auth/verify-code/`
    - **Entrée (JSON)** :
    ```json
    {
        "identifier": "01234567",
        "code": "123456",
        "purpose": "REGISTER" // ou "PASSWORD_RESET"
    }
    ```
    - **Sortie (JSON - 200 OK)** :
    ```json
    {
        "message": "Code valide."
    }
    ```

### Inscription
- `POST /auth/register/`
    - **Entrée (JSON)** :
    ```json
    {
        "username": "01234567", // Numéro de téléphone
        "email": "user@example.com",
        "password": "password123",
        "first_name": "Jean",
        "last_name": "Dupont",
        "code": "123456" // Code de 6 chiffres reçu par email
    }
    ```
    - **Sortie (JSON - 201 Created)** :
    ```json
    {
        "user": {
            "id": 1,
            "username": "01234567",
            "email": "user@example.com",
            "first_name": "Jean",
            "last_name": "Dupont"
        },
        "tokens": {
            "refresh": "eyJhbG...",
            "access": "eyJhbG..."
        },
        "message": "Compte créé et connecté avec succès."
    }
    ```

### Réinitialisation de mot de passe (Demande)
- `POST /auth/forgot-password/`
    - **Entrée (JSON)** :
    ```json
    {
        "phone": "01234567"
    }
    ```
    - **Sortie (JSON - 200 OK)** :
    ```json
    {
        "message": "Un code de réinitialisation a été envoyé à l'adresse email associée.",
        "phone": "01234567"
    }
    ```

### Réinitialisation de mot de passe (Confirmation)
- `POST /auth/reset-password/`
    - **Entrée (JSON)** :
    ```json
    {
        "phone": "01234567",
        "code": "123456",
        "new_password": "new_password123"
    }
    ```
    - **Sortie (JSON - 200 OK)** :
    ```json
    {
        "message": "Mot de passe réinitialisé avec succès.",
        "tokens": {
            "refresh": "eyJhbG...",
            "access": "eyJhbG..."
        }
    }
    ```

### Connexion (Login)
- `POST /auth/token/`
    - **Entrée (JSON)** :
    ```json
    {
        "username": "01234567", // ou email
        "password": "password123"
    }
    ```
    - **Sortie (JSON - 200 OK)** :
    ```json
    {
        "access": "eyJhbG...",
        "refresh": "eyJhbG..."
    }
    ```

### Profil Utilisateur
- `GET /auth/profile/`
    - **Sortie (JSON - 200 OK)** :
    ```json
    {
        "id": 1,
        "username": "admin",
        "email": "admin@cimpp.org",
        "first_name": "Admin",
        "last_name": "CIMPP",
        "is_staff": true
    }
    ```

---

## 2. Événements (`/evenements/`)

### Liste & Détails
- `GET /evenements/` (Liste) ou `GET /evenements/{id}/` (Détails)
    - **Sortie (JSON)** :
    ```json
    [
        {
            "id": 1,
            "name": "Conférence Foi",
            "slug": "conference-foi",
            "description": "Description détaillée...",
            "date": "2026-05-15T18:00:00Z",
            "lieu": "Eglise CIMPP",
            "image": "http://127.0.0.1:8000/media/evenements/img.jpg",
            "created_at": "2026-04-19T10:00:00Z",
            "updated_at": "2026-04-19T10:00:00Z"
        }
    ]
    ```

### Création (Admin)
- `POST /evenements/`
    - **Type** : `multipart/form-data`
    - **Entrée** : `name` (string), `description` (text), `date` (datetime), `lieu` (string), `image` (file).

---

## 3. Prédications (`/predications/`)

### Liste & Détails
- `GET /predications/`
    - **Sortie (JSON)** :
    ```json
    [
        {
            "id": 1,
            "img_couverture": "http://domain.com/media/predications/cover.jpg",
            "titre": "La Puissance de la Prière",
            "slug": "la-puissance-de-la-priere",
            "date": "2026-04-01T10:00:00Z",
            "url_video": "https://youtube.com/watch?v=...",
            "audio": "http://domain.com/media/audio/sermon.mp3",
            "resume": "Bref résumé...",
            "verset_principal": "Matthieu 21:22",
            "contenu": "Texte intégral...",
            "predicateur": "Pasteur Emmanuel",
            "interprete": "Frère Marc",
            "theme": "Foi",
            "created_at": "2026-04-01T10:00:00Z",
            "updated_at": "2026-04-19T10:00:00Z"
        }
    ]
    ```

### Création (Admin)
- `POST /predications/`
    - **Type** : `multipart/form-data`
    - **Entrée** : `titre`, `date`, `url_video` (optionnel), `resume`, `verset_principal`, `contenu`, `predicateur`, `interprete` (optionnel), `theme`, `img_couverture` (file), `audio` (file, optionnel).

---

## 4. Témoignages (`/temoignages/`)

### Liste (Public)
- `GET /temoignages/` : Retourne uniquement les témoignages avec `published: true`.
- **Sortie (JSON)** :
```json
[
    {
        "id": 1,
        "first_name": "Marie",
        "last_name": "Kaboré",
        "full_name": "Marie-Kaboré",
        "phone": "00000000",
        "subjet": "Guérison",
        "temoignage": "J'ai été guérie...",
        "created_at": "2026-04-10T16:00:00Z",
        "published": true
    }
]
```

### Soumission (Public)
- `POST /temoignages/`
    - **Entrée (JSON)** :
    ```json
    {
        "first_name": "Marie",
        "last_name": "Kaboré",
        "phone": "00000000",
        "subjet": "Guérison",
        "temoignage": "J'ai été guérie..."
    }
    ```

---

## 5. Programmes Hebdomadaires (`/programmes-hebdo/`)

### Liste
- `GET /programmes-hebdo/`
- **Sortie (JSON)** :
```json
[
    {
        "id": 1,
        "jour": "dimanche",
        "jour_display": "Dimanche",
        "horaire": "08:00 - 11:00",
        "activite": "Culte d'Adoration",
        "icone": "fa-solid fa-church",
        "badge_special": true,
        "salle": "Grand Temple",
        "responsable": "Pasteur Principal",
        "ordre": 1
    }
]
```

---

## 6. Direct (Live Stream) (`/live/`)

### Récupérer le lien actuel
- `GET /live/`
- **Sortie (JSON - 200 OK)** :
```json
{
    "id": 1,
    "titre": "Culte en Direct",
    "url": "https://www.youtube.com/live/xyz123",
    "is_live": true,
    "updated_at": "2026-04-19T14:30:00Z"
}
```

### Mise à jour (Admin)
- `PATCH /live/{id}/`
    - **Entrée (JSON)** :
    ```json
    {
        "url": "nouvelle_url",
        "is_live": false
    }
    ```

---

## Codes d'Erreurs
- `400 Bad Request` : Erreur de validation (ex: champ manquant).
- `401 Unauthorized` : Token JWT invalide ou expiré (durée : 30 min).
- `403 Forbidden` : Tentative d'action admin par un utilisateur standard.
- `404 Not Found` : Ressource introuvable.
- `429 Too Many Requests` : Trop de requêtes (limite : 30/min pour les anonymes, 200/min pour les authentifiés).
- `503 Service Unavailable` : Base de données indisponible.

---

## 7. Nouveaux Endpoints

### Santé de l'API
- `GET /health/` (Public)
    - **Sortie (JSON)** :
    ```json
    {
        "status": "ok",
        "database": "connected",
        "version": "1.0.0"
    }
    ```

### Statistiques
- `GET /statistics/` (Public)
    - **Sortie (JSON)** :
    ```json
    {
        "predications": 15,
        "evenements": 8,
        "temoignages_publics": 23
    }
    ```

### Recherche de Prédications
- `GET /predications/search/?q=mot&theme=&date_from=&date_to=` (Public)
    - **Paramètres (query string)** :
        - `q` : recherche full-text dans titre, résumé, contenu, prédicateur
        - `theme` : filtre par thème
        - `date_from` : date minimale (format YYYY-MM-DD)
        - `date_to` : date maximale (format YYYY-MM-DD)
    - **Sortie (JSON - liste paginée)** :
    ```json
    {
        "count": 3,
        "next": "?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "titre": "La foi qui déplace les montagnes",
                "slug": "la-foi-qui-deplace-les-montagnes",
                "predicateur": "Pasteur Jean",
                "date": "2026-06-15T10:00:00Z",
                "resume": "..."
            }
        ]
    }
    ```

---

## Notes de Version
**v1.0.0** — Première version stable de l'API avec authentification JWT, CRUD complet, et pagination automatique (20 éléments/page).
