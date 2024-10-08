# src/pump_config.py

class PumpConfig:
    def __init__(self, basal_rates, insulin_to_carb_ratio, insulin_sensitivity_factor, max_bolus):
        self.basal_rates = basal_rates
        self.insulin_to_carb_ratio = insulin_to_carb_ratio
        self.insulin_sensitivity_factor = insulin_sensitivity_factor
        self.max_bolus = max_bolus
    
    def validate(self):
        # Ici, tu peux ajouter des validations pour t'assurer que les valeurs sont correctes
        return True
