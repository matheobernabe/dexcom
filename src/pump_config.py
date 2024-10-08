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
                
                
    def adjust_for_mode(self, mode, adjustments):
        if mode in adjustments:
            adjustment = adjustments[mode]
            if isinstance(adjustment, list):
                for i in range(len(self.basal_rates)):
                    self.basal_rates[i] *= adjustment[i]
            else:
                self.basal_rates = [rate * adjustment for rate in self.basal_rates]
