FROM python:3.9-slim

# Installer les dépendances nécessaires et les outils réseau
WORKDIR /DexcomCloud
ENV PYTHONPATH=/DexcomCloud

# Copier les fichiers du projet dans le conteneur
COPY . /DexcomCloud

# Mettre à jour les paquets et installer telnet et netcat
RUN apt-get update && \
    apt-get install -y telnet  && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Définir le point d'entrée de l'application
CMD ["python", "main.py"]
