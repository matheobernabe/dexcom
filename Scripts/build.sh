#!/bin/bash

# Vérifie que le nom du service est fourni
if [ -z "$1" ]; then
  echo "Usage: ./scripts/rebuild.sh <service_name>"
  exit 1
fi

# Reconstruit le service spécifique
docker-compose up --build -d $1

echo "Service $1 reconstruit et redémarré."
