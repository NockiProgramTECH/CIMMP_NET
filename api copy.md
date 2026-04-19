# Documentation de l'API CIMPP (Mise à jour)

Cette API supporte désormais l'authentification JWT et la gestion des comptes utilisateurs pour l'application Flutter.

## Informations Générales
- **URL de Base** : `http://<votre-domaine>/cimppApi/`
- **Authentification** : JSON Web Token (JWT). Utilisez le header `Authorization: Bearer <access_token>`.
- **Note sur les types de requêtes** :
    - Utilisez `application/json` pour les requêtes sans fichiers.
    - Utilisez `multipart/form-data` impérativement pour toute requête incluant des fichiers (images, audio).

---

## 1. Authentification & Comptes (`/auth/`)

### Inscription
- `POST /auth/register/` : Créer un nouveau compte.
    - **Type de requête** : `application/json`
    - **Champs** : `username` (Téléphone), `email`, `password`, `first_name`, `last_name`.

### Connexion (Login)
- `POST /auth/token/` : Obtenir les jetons d'accès et de rafraîchissement.
    - **Type de requête** : `application/json`
    - **Champs** : `username` (Email ou Téléphone) et `password`.
    - **Retour** : `{ "access": "...", "refresh": "..." }`.

### Rafraîchissement du Jeton
- `POST /auth/token/refresh/` : Obtenir un nouveau jeton d'accès.
    - **Type de requête** : `application/json`
    - **Champs** : `refresh`.

### Profil Utilisateur
- `GET /auth/profile/` : Récupérer les informations de l'utilisateur connecté (nécessite d'être authentifié).
```json
{
    "id": 1,
    "username": "admin",
    "email": "",
    "first_name": "",
    "last_name": "",
    "is_staff": true
}
```
---

## 2. Événements (`/evenements/`)

### Endpoints
- `GET /evenements/` : Liste publique.
- `GET /evenements/{id}/` : Détails.
- `POST /evenements/` : **Admin uniquement**. Créer un événement.
    - **Type de requête** : `multipart/form-data` (Requis pour l'image)
    - **Champs** : `name`, `description`, `date`, `lieu`, `image` (Fichier).
- `PUT/PATCH /evenements/{id}/` : **Admin uniquement**. Modifier un événement.
    - **Type de requête** : `multipart/form-data` (Si l'image est modifiée)
- `DELETE /evenements/{id}/` : **Admin uniquement**. Supprimer un événement.

---

## 3. Prédications (`/predications/`)

### Endpoints
- `GET /predications/` : Liste publique.
- `GET /predications/{id}/` : Détails.
- `POST /predications/` : **Admin uniquement**. Ajouter une prédication.
    - **Type de requête** : `multipart/form-data` (Requis pour `img_couverture` et `audio`)
    - **Champs** : `titre`, `slug`, `date`, `url_video`, `resume`, `verset_principal`, `contenu`, `predicateur`, `interprete`, `theme`, `img_couverture` (Fichier), `audio` (Fichier).
- `PUT/PATCH /predications/{id}/` : **Admin uniquement**. Modifier.
    - **Type de requête** : `multipart/form-data`
- `DELETE /predications/{id}/` : **Admin uniquement**. Supprimer.

---

## 4. Témoignages (`/temoignages/`)

### Endpoints
- `GET /temoignages/` :
    - **Public** : Liste des témoignages publiés uniquement.
    - **Admin** : Liste de tous les témoignages (incluant ceux à modérer).
- `POST /temoignages/` : Soumettre un témoignage (Public).
    - **Type de requête** : `application/json`
    - **Champs** : `first_name`, `last_name`, `phone`, `subjet`, `temoignage`.
- `PATCH /temoignages/{id}/` : **Admin uniquement**. Permet de changer `published: true` pour valider un témoignage.
    - **Type de requête** : `application/json`

---

## 5. Programmes Hebdomadaires (`/programmes-hebdo/`)

### Endpoints
- `GET /programmes-hebdo/` : Liste complète des activités hebdomadaires triées par ordre.
- `GET /programmes-hebdo/{id}/` : Détails d'une activité.
- `POST /programmes-hebdo/` : **Admin uniquement**. Ajouter une activité au programme.
    - **Type de requête** : `application/json`
    - **Champs** : 
        - `jour` : `lundi`, `mardi`, `mercredi`, `jeudi`, `vendredi`, `samedi`, `dimanche`
        - `horaire` : ex "18h30 - 20h00"
        - `activite` : nom de l'activité
        - `icone` : classe FontAwesome (ex: "fa-solid fa-hands-praying")
        - `badge_special` : boolean
        - `salle` : nom de la salle
        - `responsable` : nom du responsable
        - `ordre` : entier pour le tri
- `PUT/PATCH /programmes-hebdo/{id}/` : **Admin uniquement**. Modifier une activité.
    - **Type de requête** : `application/json`
- `DELETE /programmes-hebdo/{id}/` : **Admin uniquement**. Supprimer une activité.

---

## Gestion des Médias
Les fichiers (images et audio) sont servis via le préfixe `/media/`.
Pour uploader via l'API (POST/PUT/PATCH), utilisez impérativement un `multipart/form-data` dès qu'un champ de type fichier est présent.

## Codes de Statut HTTP
- `200 OK` : Succès.
- `201 Created` : Création réussie.
- `401 Unauthorized` : Jeton manquant ou invalide.
- `403 Forbidden` : Droits insuffisants (tentative d'admin sans être staff).
- `400 Bad Request` : Erreur de validation des données.
