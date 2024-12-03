class InsulinPump:
    def __init__(self, config):
        self.config = config

    def deliver_basal(self, hour):
        return self.config.basal_rates[hour]

    def calculate_meal_bolus(self, carbs):
        bolus = carbs / self.config.insulin_to_carb_ratio
        return min(bolus, self.config.max_bolus)  # Limiter le bolus à la dose maximale

    def calculate_correction_bolus(self, current_glucose, target_glucose):
        diff = current_glucose - target_glucose
        bolus = diff / self.config.insulin_sensitivity_factor
        return min(bolus, self.config.max_bolus)  # Limiter le bolus de correction
    def update_isf(self, new_isf):
        self.config.insulin_sensitivity_factor = new_isf