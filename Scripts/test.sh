#!/bin/bash

# Vérifie que le conteneur existe
container_name="GlucoseSensor"

if ! docker ps | grep -q $container_name; then
  echo "Le conteneur $container_name n'est pas en cours d'exécution."
  exit 1
fi

# Exécute les tests
docker exec -it $container_name pytest tests/

echo "Tests exécutés."
