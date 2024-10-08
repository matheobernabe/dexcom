class PumpConfig:
    def __init__(self, basal_rates, insulin_to_carb_ratio, insulin_sensitivity_factor, max_bolus):
        self.basal_rates = basal_rates  # Liste des taux basaux par heure
        self.insulin_to_carb_ratio = insulin_to_carb_ratio  # Ratio insuline/glucides
        self.insulin_sensitivity_factor = insulin_sensitivity_factor  # Sensibilité à l'insuline
        self.max_bolus = max_bolus  # Dose maximale de bolus
    
    def validate_basal_rates(self):
        # Lissage des variations abruptes dans les taux basaux
        for i in range(1, len(self.basal_rates)):
            if abs(self.basal_rates[i] - self.basal_rates[i-1]) > 0.3:  # Par exemple, limite à 0,3 U/h
                self.basal_rates[i] = (self.basal_rates[i] + self.basal_rates[i-1]) / 2  # Lissage
    def adjust_for_mode(self, mode):
        if mode == "Sport":
            # Réduction de 20 % des taux basaux
            self.basal_rates = [rate * 0.8 for rate in self.basal_rates]
        elif mode == "Nuit":
            # Réduction de 15 % des taux basaux
            self.basal_rates = [rate * 0.85 for rate in self.basal_rates]
        elif mode == "Jour":
            # Augmentation de 10 % des taux basaux pendant la journée (6h - 22h)
            for i in range(6, 22):
                self.basal_rates[i] *= 1.1
