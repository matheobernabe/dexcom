# Simulateur de Pompe à Insuline

## Membres du groupe
Mathéo Bernabé
Valentin Gaillard
Tom Serayet

## Description

Ce projet simule une pompe à insuline pour gérer la glycémie d'un patient diabétique.

## Installation

1. Clonez le projet.
2. Créez un environnement virtuel avec Python.
3. Activez l'environnement virtuel.
4. Installez les dépendances.

```bash
pip install -r requirements.txt
pip install pytest 

## Pour simuler une journée
python src/main.py

## Pour les tests fonctionnel 
pytest -v -s tests/test_simulator.py

## Pour les tests unitaires 
pytest tests/tests_unitaires.py