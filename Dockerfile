# Utiliser une image Python officielle comme base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script de l'application
COPY demo_multiagent.py .

# Définir le point d'entrée pour exécuter l'application en CLI
ENTRYPOINT ["python", "demo_multiagent.py"]