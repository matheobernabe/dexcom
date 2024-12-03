class GlucoseAnalyzer:
    def __init__(self, kafka_producer):
        self.hypo_threshold = 70
        self.hyper_threshold = 180
        self.kafka_producer = kafka_producer

    def analyze_glucose(self, glucose_level, timestamp):
        """Analyse le niveau de glucose et envoie des alertes si nécessaire"""
        if glucose_level <= self.hypo_threshold:
            alert = {
                'timestamp': timestamp,
                'type': 'HYPOGLYCEMIA',
                'level': 'URGENT',
                'glucose_level': glucose_level,
                'threshold': self.hypo_threshold,
                'message': 'Hypoglycémie détectée'
            }
            self.kafka_producer.send_message(self.kafka_producer.ALERT_TOPIC, alert)
            
        elif glucose_level >= self.hyper_threshold:
            alert = {
                'timestamp': timestamp,
                'type': 'HYPERGLYCEMIA',
                'level': 'WARNING',
                'glucose_level': glucose_level,
                'threshold': self.hyper_threshold,
                'message': 'Hyperglycémie détectée'
            }
            self.kafka_producer.send_message(self.kafka_producer.ALERT_TOPIC, alert)

    def set_thresholds(self, hypo=None, hyper=None):
        """Configure les seuils d'alerte"""
        if hypo is not None:
            self.hypo_threshold = hypo
        if hyper is not None:
            self.hyper_threshold = hyper