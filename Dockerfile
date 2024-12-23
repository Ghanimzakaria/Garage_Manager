FROM python:3.10-slim

# Installer les dépendances système nécessaires pour mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    gcc \
    build-essential && \
    apt-get clean

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ /app/src

# Exposer le port
EXPOSE 80

# Commande pour démarrer le serveur Django
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
