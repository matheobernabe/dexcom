#!/bin/bash

# Supprime les conteneurs, images et volumes inutilisés
docker system prune -f
docker volume prune -f

echo "Nettoyage terminé."
