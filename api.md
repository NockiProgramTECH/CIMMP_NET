# Documentation de l'API CIMPP (Mise à jour)

Cette API supporte désormais l'authentification JWT et la gestion des comptes utilisateurs pour l'application Flutter.

## Informations Générales
- **URL de Base** : `http://<votre-domaine>/cimppApi/`
- **Authentification** : JSON Web Token (JWT). Utilisez le header `Authorization: Bearer <access_token>`.

---

## 1. Authentification & Comptes (`/auth/`)

### Inscription
- `POST /auth/register/` : Créer un nouveau compte.
    - **Champs** : `username` (Téléphone), `email`, `password`, `first_name`, `last_name`.

### Connexion (Login)
- `POST /auth/token/` : Obtenir les jetons d'accès et de rafraîchissement.
    - **Champs** : `username` (Email ou Téléphone) et `password`.
    - **Retour** : `{ "access": "...", "refresh": "..." }`.

### Rafraîchissement du Jeton
- `POST /auth/token/refresh/` : Obtenir un nouveau jeton d'accès.
    - **Champs** : `refresh`.

### Profil Utilisateur
- `GET /auth/profile/` : Récupérer les informations de l'utilisateur connecté (nécessite d'être authentifié).
{
    "id": 1,
    "username": "admin",
    "email": "",
    "first_name": "",
    "last_name": "",
    "is_staff": true
}
---

## 2. Événements (`/evenements/`)

### Endpoints
- `GET /evenements/` : Liste publique.
 {
        "id": 1,
        "name": "lankoande",
        "slug": "mangue",
        "description": "uibjkj\r\nibj",
        "date": "2026-04-30T06:00:00Z",
        "lieu": "Eglise CIMPP",
        "image": "http://127.0.0.1:8000/media/evenements/WhatsApp_Image_2026-04-03_at_16.24.59.jpeg",
        "created_at": "2026-04-07T14:06:12.407217Z",
        "updated_at": "2026-04-07T14:06:12.407244Z"
    }

- `GET /evenements/{id}/` : Détails.
- `POST /evenements/` : **Admin uniquement**. Créer un événement.
 {
      
        "name": "lankoande",
        "slug": "mangue",
        "description": "uibjkj\r\nibj",
        "date": "2026-04-30T06:00:00Z",
        "lieu": "Eglise CIMPP",
        "image": "http://127.0.0.1:8000/media/evenements/WhatsApp_Image_2026-04-03_at_16.24.59.jpeg",
       
    }

- `PUT/PATCH /evenements/{id}/` : **Admin uniquement**. Modifier un événement.
- `DELETE /evenements/{id}/` : **Admin uniquement**. Supprimer un événement.

---

## 3. Prédications (`/predications/`)

### Endpoints
- `GET /predications/` : Liste publique.
[
   
    {
        "id": ,
        "img_couverture": "http://127.0.0.1:8000/media/predications/650203946_122126143605064169_5052247897823378937_n.jpg",
        "titre": "titre3",
        "slug": "titre3",
        "date": "2026-04-01T00:34:34Z",
        "url_video": "https://python.org",
        "audio": null,
        "resume": "djskddddsjskj\r\ndsjsdhdsjkds\r\ndsmidkdsds\r\ndopzeoezjklsd\r\nioirkeerismoenz\r\nezopdsnk\r\nd",
        "verset_principal": "dskdsjisdubdss^psdl",
        "contenu": "sdklsdçojçezpojqodj^r qqkdnqopjerqknqoieoqsj bdqojqo\r\ndqifçpqmjqkqdjq",
        "predicateur": "pasterur",
        "interprete": "pasteru",
        "theme": "pasteru",
        "created_at": "2026-04-01T00:35:34.637849Z",
        "updated_at": "2026-04-13T17:58:33.680574Z"
    },
    
]
- `GET /predications/{id}/` : Détails.
- `POST /predications/` : **Admin uniquement**. Ajouter une prédication.

  {
        "img_couverture": "http://127.0.0.1:8000/media/predications/650203946_122126143605064169_5052247897823378937_n.jpg",
        "titre": "titre3",
        "slug": "titre3",
        "date": "2026-04-01T00:34:34Z",
        "url_video": "https://python.org",
        "audio": null,
        "resume": "djskddddsjskj\r\ndsjsdhdsjkds\r\ndsmidkdsds\r\ndopzeoezjklsd\r\nioirkeerismoenz\r\nezopdsnk\r\nd",
        "verset_principal": "dskdsjisdubdss^psdl",
        "contenu": "sdklsdçojçezpojqodj^r qqkdnqopjerqknqoieoqsj bdqojqo\r\ndqifçpqmjqkqdjq",
        "predicateur": "pasterur",
        "interprete": "pasteru",
        "theme": "pasteru",
      
    },
    

- `PUT/PATCH /predications/{id}/` : **Admin uniquement**. Modifier.
- `DELETE /predications/{id}/` : **Admin uniquement**. Supprimer.

---

## 4. Témoignages (`/temoignages/`)

### Endpoints
- `GET /temoignages/` :
    - **Public** : Liste des témoignages publiés uniquement.
    - **Admin** : Liste de tous les témoignages (incluant ceux à modérer).

     {
        "id": 1,
        "first_name": "Albertine",
        "last_name": "Soubeiga",
        "full_name": "Albertine-Soubeiga",
        "phone": "24943687",
        "subjet": "guerison",
        "temoignage": "J'Y GjygNnd.gsuhsbbs\nSjsysns",
        "created_at": "2026-04-10T16:11:19.504381Z",
        "published": false
    }
- `POST /temoignages/` : Soumettre un témoignage (Public). Statut par défaut : `non publié`.
 {
       
        "first_name": "Albertine",
        "last_name": "Soubeiga",
        "full_name": "Albertine-Soubeiga",
        "phone": "24943687",
        "subjet": "guerison",
        "temoignage": "J'Y GjygNnd.gsuhsbbs\nSjsysns",
    }
- `PATCH /temoignages/{id}/` : **Admin uniquement**. Permet de changer `published: true` pour valider un témoignage.

---

## Gestion des Médias
Les fichiers (images et audio) sont servis via le préfixe `/media/`.
Pour uploader via l'API (POST), utilisez un `multipart/form-data`.

## Codes de Statut HTTP
- `200 OK` : Succès.
- `201 Created` : Création réussie.
- `401 Unauthorized` : Jeton manquant ou invalide.
- `403 Forbidden` : Droits insuffisants (tentative d'admin sans être staff).
- `400 Bad Request` : Erreur de validation des données.
