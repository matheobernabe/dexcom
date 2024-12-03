import json
from typing import Dict, Any
from dataclasses import dataclass
from datetime import time

@dataclass
class UserSettings:
    hypo_threshold: float = 70.0
    hyper_threshold: float = 180.0
    target_glucose: float = 120.0
    insulin_sensitivity: float = 50.0  # mg/dL par unité d'insuline
    carb_ratio: float = 10.0  # grammes de glucides par unité d'insuline
    quiet_hours_start: time = time(22, 0)  # 22h00
    quiet_hours_end: time = time(7, 0)    # 07h00
    notifications_enabled: bool = True
    sound_enabled: bool = True
    vibration_enabled: bool = True
    auto_sync_enabled: bool = True

class SettingsManager:
    def __init__(self, settings_file: str = "user_settings.json"):
        self.settings_file = settings_file
        self.settings = self._load_settings()

    def _load_settings(self) -> UserSettings:
        """Charge les paramètres depuis le fichier"""
        try:
            with open(self.settings_file, 'r') as f:
                data = json.load(f)
                # Convertir les heures en objets time
                data['quiet_hours_start'] = time.fromisoformat(data['quiet_hours_start'])
                data['quiet_hours_end'] = time.fromisoformat(data['quiet_hours_end'])
                return UserSettings(**data)
        except FileNotFoundError:
            return UserSettings()

    def save_settings(self) -> bool:
        """Sauvegarde les paramètres dans le fichier"""
        try:
            data = self.settings.__dict__
            # Convertir les objets time en strings
            data['quiet_hours_start'] = data['quiet_hours_start'].isoformat()
            data['quiet_hours_end'] = data['quiet_hours_end'].isoformat()
            
            with open(self.settings_file, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des paramètres: {e}")
            return False

    def update_settings(self, new_settings: Dict[str, Any]) -> bool:
        """Met à jour les paramètres utilisateur"""
        try:
            for key, value in new_settings.items():
                if hasattr(self.settings, key):
                    # Conversion spéciale pour les heures
                    if key in ['quiet_hours_start', 'quiet_hours_end'] and isinstance(value, str):
                        value = time.fromisoformat(value)
                    setattr(self.settings, key, value)
            return self.save_settings()
        except Exception as e:
            print(f"Erreur lors de la mise à jour des paramètres: {e}")
            return False

    def validate_settings(self) -> bool:
        """Valide les paramètres utilisateur"""
        try:
            assert 40 <= self.settings.hypo_threshold <= 80, "Seuil hypo invalide"
            assert 160 <= self.settings.hyper_threshold <= 300, "Seuil hyper invalide"
            assert self.settings.hypo_threshold < self.settings.target_glucose < self.settings.hyper_threshold, "Cible invalide"
            assert 20 <= self.settings.insulin_sensitivity <= 100, "Sensibilité insuline invalide"
            assert 3 <= self.settings.carb_ratio <= 50, "Ratio glucides invalide"
            return True
        except AssertionError as e:
            print(f"Validation des paramètres échouée: {e}")
            return False