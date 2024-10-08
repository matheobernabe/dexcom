# src/insulin_pump.py

class InsulinPump:
    def __init__(self, config):
        self.config = config

    def deliver_basal(self, hour):
        return self.config.basal_rates[hour]

    def calculate_meal_bolus(self, carbs):
        return carbs / self.config.insulin_to_carb_ratio

    def calculate_correction_bolus(self, current_glucose, target_glucose):
        diff = current_glucose - target_glucose
        return diff / self.config.insulin_sensitivity_factor
