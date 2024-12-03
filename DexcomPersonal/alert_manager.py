import json
from datetime import datetime

class AlertManager:
    def __init__(self):
        self.alert_settings = {
            'hypo_threshold': 70,
            'hyper_threshold': 180,
            'rate_of_change_threshold': 2,  # mg/dL/min
            'notification_enabled': True,
            'sound_enabled': True
        }

    def process_alert(self, alert_data):
        """Traite une alerte reçue"""
        if not self._should_process_alert(alert_data):
            return

        if alert_data['type'] == 'HYPOGLYCEMIA':
            self._handle_hypo_alert(alert_data)
        elif alert_data['type'] == 'HYPERGLYCEMIA':
            self._handle_hyper_alert(alert_data)

    def update_settings(self, new_settings):
        """Met à jour les paramètres d'alerte"""
        self.alert_settings.update(new_settings)

    def _should_process_alert(self, alert_data):
        """Vérifie si l'alerte doit être traitée"""
        if not self.alert_settings['notification_enabled']:
            return False

        if alert_data['type'] == 'HYPOGLYCEMIA':
            return alert_data['glucose_level'] <= self.alert_settings['hypo_threshold']
        elif alert_data['type'] == 'HYPERGLYCEMIA':
            return alert_data['glucose_level'] >= self.alert_settings['hyper_threshold']

        return True

    def _handle_hypo_alert(self, alert_data):
        """Gère une alerte d'hypoglycémie"""
        self._notify(
            "URGENCE Hypoglycémie",
            f"Glucose: {alert_data['glucose_level']} mg/dL",
            urgent=True
        )

    def _handle_hyper_alert(self, alert_data):
        """Gère une alerte d'hyperglycémie"""
        self._notify(
            "Attention Hyperglycémie",
            f"Glucose: {alert_data['glucose_level']} mg/dL",
            urgent=False
        )

    def _notify(self, title, message, urgent=False):
        """Envoie une notification"""
        # Ici, implémenter le système de notification réel
        # (notifications système, sons, vibrations, etc.)
        print(f"{title}: {message}")
        if self.alert_settings['sound_enabled'] and urgent:
            # Jouer un son d'alerte
            pass