class Simulator:
    def run_simulation(self):
        for hour in range(self.duration):
            print(f"Heure {hour}: Glycémie actuelle: {self.patient.glucose_level} mg/dL")

            # Mesure de la glycémie
            glucose = self.cgm.measure_glucose(self.patient)

            # Ajustement du taux basal si la glycémie est correcte
            if glucose >= 70:  # Administrer de l'insuline seulement si la glycémie est suffisante
                basal_rate = self.controller.adjust_basal_rate(glucose)
                insulin_delivered = self.pump.deliver_basal(hour % 24) * basal_rate
                self.patient.update_glucose_level(insulin_delivered, 0)
            else:
                print(f"Heure {hour}: Glycémie trop basse, pas d'administration d'insuline.")

            # Si la glycémie est trop basse, on la corrige
            if self.patient.glucose_level < 70:
                print(f"Heure {hour}: Glycémie trop basse, ajustement nécessaire!")
                self.patient.glucose_level = 70

            # Si un repas est pris (exemple simplifié, repas toutes les 6 heures)
            if hour % 6 == 0:
                carbs = 60  # 60g de glucides consommés
                bolus = self.pump.calculate_meal_bolus(carbs)
                self.patient.update_glucose_level(bolus, carbs)

            # Bolus de correction si nécessaire
            if glucose > 150:  # Glycémie trop élevée
                correction_bolus = self.pump.calculate_correction_bolus(glucose, 100)
                self.patient.update_glucose_level(correction_bolus, 0)

            print(f"Heure {hour + 1}: Glycémie après ajustement: {self.patient.glucose_level} mg/dL")
