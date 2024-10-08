# src/simulator.py

class Simulator:
    def __init__(self, patient, pump, cgm, controller, duration):
        self.patient = patient
        self.pump = pump
        self.cgm = cgm
        self.controller = controller
        self.duration = duration

    def run_simulation(self):
        for hour in range(self.duration):
            glucose = self.cgm.measure_glucose(self.patient)
            basal_rate = self.controller.adjust_basal_rate(glucose)
            insulin_delivered = self.pump.deliver_basal(hour) * basal_rate
            self.patient.update_glucose_level(insulin_delivered, 0)

            if hour % 6 == 0:  # Simule un repas toutes les 6 heures
                carbs = 60  # Ex : 60g de glucides
                bolus = self.pump.calculate_meal_bolus(carbs)
                self.patient.update_glucose_level(bolus, carbs)

            print(f"Heure {hour}: Glycémie actuelle: {self.patient.glucose_level} mg/dL")
