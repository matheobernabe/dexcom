class Simulator:
    def __init__(self, patient, pump, cgm, controller, duration):
        self.patient = patient
        self.pump = pump
        self.cgm = cgm
        self.controller = controller
        self.duration = duration

    def run_simulation(self):
        for hour in range(self.duration):
            print(f"Heure {hour}: Glycémie actuelle: {self.patient.glucose_level} mg/dL")

            # Simulation d'un repas toutes les 6 heures
            if hour % 6 == 0:  # Un repas toutes les 6 heures
                carbs = 60  # 60g de glucides consommés à chaque repas
                bolus = self.pump.calculate_meal_bolus(carbs)
                print(f"Heure {hour}: Repas pris (60g de glucides), bolus calculé = {bolus} U.")
                self.patient.update_glucose_level(bolus, carbs)

            # Mesure de la glycémie
            glucose = self.cgm.measure_glucose(self.patient)

            # Ajustement du taux basal si la glycémie est correcte
            if glucose >= 70:
                basal_rate = self.controller.adjust_basal_rate(glucose)
                insulin_delivered = self.pump.deliver_basal(hour % 24) * basal_rate
                self.patient.update_glucose_level(insulin_delivered, 0)
            else:
                print(f"Heure {hour}: Glycémie trop basse, pas d'administration d'insuline.")
                print(f"Heure {hour}: Correction de l'hypoglycémie par ingestion de 15g de glucides.")
                self.patient.update_glucose_level(0, 15)  # Ajout de 15g de glucides pour corriger l'hypoglycémie

            # Affichage de la glycémie après correction
            print(f"Heure {hour + 1}: Glycémie après ajustement: {self.patient.glucose_level} mg/dL")
