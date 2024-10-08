# Utiliser une image de base Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt (si nécessaire) ou tout autre fichier dépendances
COPY requirements.txt .

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source dans le conteneur
COPY src/ ./src
COPY tests/ ./tests

# Exposer le port (si tu prévois une interface utilisateur plus tard, sinon tu peux l'ignorer)
# EXPOSE 5000

# Commande pour exécuter le programme
CMD ["python", "src/main.py"]
