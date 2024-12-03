FROM python:3.9-slim

# Installer les dépendances nécessaires
WORKDIR /DexcomCloud
ENV PYTHONPATH=/DexcomCloud
COPY . /DexcomCloud

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Définir le point d'entrée de l'application
CMD ["python", "main.py"]
