from datetime import datetime, timedelta

class SensorMonitor:
    def __init__(self, kafka_producer):
        self.installation_time = datetime.now()
        self.expiration_time = self.installation_time + timedelta(days=10)
        self.kafka_producer = kafka_producer

    def check_sensor_lifetime(self):
        """Vérifie si le capteur est encore dans sa durée de vie"""
        current_time = datetime.now()
        
        if current_time >= self.expiration_time:
            status_message = {
                'timestamp': current_time.isoformat(),
                'status': 'EXPIRED',
                'message': 'Capteur expiré - Remplacement nécessaire'
            }
            self.kafka_producer.send_message(self.kafka_producer.STATUS_TOPIC, status_message)
            return False
            
        days_remaining = (self.expiration_time - current_time).days
        if days_remaining <= 2:
            status_message = {
                'timestamp': current_time.isoformat(),
                'status': 'WARNING',
                'message': f'Capteur expire dans {days_remaining} jours'
            }
            self.kafka_producer.send_message(self.kafka_producer.STATUS_TOPIC, status_message)
            
        return True