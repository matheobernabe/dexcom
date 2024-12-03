import json
from datetime import datetime
import requests
from typing import Dict, Any

class CloudSync:
    def __init__(self, api_url: str, user_id: str):
        self.api_url = api_url
        self.user_id = user_id
        self.sync_queue = []
        self.last_sync = datetime.now()

    def sync_glucose_data(self, glucose_data: Dict[str, Any]) -> bool:
        """Synchronise les données de glucose avec le cloud"""
        endpoint = f"{self.api_url}/glucose/{self.user_id}"
        
        try:
            response = requests.post(
                endpoint,
                json={
                    "timestamp": glucose_data["timestamp"].isoformat(),
                    "glucose_level": glucose_data["glucose_level"],
                    "device_id": "dexcom_personal_1"
                }
            )
            return response.status_code == 200
        except Exception as e:
            self.sync_queue.append(("glucose", glucose_data))
            print(f"Erreur de synchronisation: {e}")
            return False

    def sync_insulin_data(self, insulin_data: Dict[str, Any]) -> bool:
        """Synchronise les données d'insuline avec le cloud"""
        endpoint = f"{self.api_url}/insulin/{self.user_id}"
        
        try:
            response = requests.post(
                endpoint,
                json={
                    "timestamp": insulin_data["timestamp"].isoformat(),
                    "units": insulin_data["units"],
                    "type": insulin_data["type"]
                }
            )
            return response.status_code == 200
        except Exception as e:
            self.sync_queue.append(("insulin", insulin_data))
            print(f"Erreur de synchronisation: {e}")
            return False

    def process_sync_queue(self) -> None:
        """Traite la file d'attente de synchronisation"""
        successful_syncs = []
        
        for idx, (data_type, data) in enumerate(self.sync_queue):
            if data_type == "glucose":
                if self.sync_glucose_data(data):
                    successful_syncs.append(idx)
            elif data_type == "insulin":
                if self.sync_insulin_data(data):
                    successful_syncs.append(idx)
        
        # Supprime les éléments synchronisés avec succès
        for idx in reversed(successful_syncs):
            self.sync_queue.pop(idx)