# src/cgm.py

class CGM:
    def __init__(self, interval):
        self.measurement_interval = interval

    def measure_glucose(self, patient):
        return patient.glucose_level
