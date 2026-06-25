# Utiliser une image Python officielle comme base
FROM python:3.11-slim

# Exposer le port que Streamlit va utiliser
EXPOSE 8501

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script de l'application
COPY demo_multiagent.py .

# Définir le point d'entrée pour exécuter l'application
# Utilise la commande de Streamlit pour lancer l'application
ENTRYPOINT ["streamlit", "run", "demo_multiagent.py", "--server.port=8501", "--server.address=0.0.0.0"]