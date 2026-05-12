# Utiliser une image Python officielle légère
FROM python:3.12-slim

# Définir des variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires pour mysqlclient et psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    libpq-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . /app/

# Collecter les fichiers statiques (nécessaire pour la production avec Whitenoise)
RUN python manage.py collectstatic --noinput

# Exposer le port sur lequel Django va tourner
EXPOSE 8000

# Commande par défaut pour démarrer le serveur via Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "CIMPP.wsgi:application"]
