from datetime import datetime
import json

class InsulinManager:
    def __init__(self, insulin_pump, data_manager, cloud_sync):
        self.insulin_pump = insulin_pump
        self.data_manager = data_manager
        self.cloud_sync = cloud_sync
        self.last_bolus_time = None

    def deliver_bolus(self, units):
        """Administre un bolus d'insuline"""
        if not self._check_safety_constraints(units):
            raise ValueError("Dose d'insuline non sécurisée")

        # Enregistre l'administration
        timestamp = datetime.now()
        bolus_record = {
            'timestamp': timestamp,
            'units': units,
            'type': 'bolus'
        }
        
        # Administre via la pompe
        self.insulin_pump.calculate_meal_bolus(units)
        
        # Enregistre dans l'historique
        self.data_manager.add_insulin_record(bolus_record)
        
        # Synchronise avec le cloud
        self.cloud_sync.sync_insulin_data(bolus_record)
        
        self.last_bolus_time = timestamp

    def _check_safety_constraints(self, units):
        """Vérifie les contraintes de sécurité pour l'administration d'insuline"""
        # Vérifie le temps depuis le dernier bolus
        if (self.last_bolus_time and 
            (datetime.now() - self.last_bolus_time).seconds < 3600):
            return False
            
        # Vérifie la dose maximale
        if units > self.insulin_pump.config.max_bolus:
            return False
            
        return True