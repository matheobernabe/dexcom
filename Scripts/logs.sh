#!/bin/bash

# Vérifie que le nom du service est fourni
if [ -z "$1" ]; then
  echo "Usage: ./scripts/logs.sh <service_name>"
  exit 1
fi

# Affiche les logs en temps réel pour un service
docker-compose logs -f $1
