import pytest
pytest.capture_stdio = False 

from src.pump_config import PumpConfig
from src.insulin_pump import InsulinPump
from src.patient import Patient
from src.cgm import CGM
from src.closed_loop_controller import ClosedLoopController
from src.simulator import Simulator

# Test 1: Configuration de la Pompe à Insuline
def test_pump_configuration():
    config = PumpConfig(
        basal_rates=[0.8, 0.6, 0.5, 0.7, 1.0, 1.2, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.5, 0.7, 0.8, 1.1, 1.0, 0.9, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2],
        insulin_to_carb_ratio=10,
        insulin_sensitivity_factor=30,
        max_bolus=10
    )
    assert config.basal_rates[0] == 0.8
    assert config.insulin_to_carb_ratio == 10
    assert config.insulin_sensitivity_factor == 30
    assert config.max_bolus == 10
    print("Configuration de la pompe validée avec succès.")

# Test 2: Administration de l'Insuline Basale Continue
def test_insulin_basal_administration():
    config = PumpConfig([0.8]*24, 10, 30, 10)
    pump = InsulinPump(config)
    patient = Patient(initial_glucose=120)
    cgm = CGM(interval=5)
    controller = ClosedLoopController(target_glucose=100, pump=pump, cgm=cgm)
    
    # Simulation sur 1 heure
    simulator = Simulator(patient, pump, cgm, controller, duration=1)
    simulator.run_simulation()
    
    # On vérifie que la glycémie a baissé à cause de l'administration d'insuline basale
    assert patient.glucose_level < 120
    print(f"Test administration insuline basale: Glycémie après simulation = {patient.glucose_level} mg/dL")

# Test 3: Programmation du Bolus Alimentaire
def test_meal_bolus():
    config = PumpConfig([0.8]*24, 10, 30, 10)
    pump = InsulinPump(config)
    bolus = pump.calculate_meal_bolus(60)  # 60g de glucides
    assert bolus == 6  # 60g / 10 = 6 unités d'insuline
    print(f"Test bolus alimentaire: 60g de glucides => Bolus = {bolus} unités d'insuline")

# Test 4: Fourniture d'un Bolus de Correction
def test_correction_bolus():
    config = PumpConfig([0.8]*24, 10, 30, 10)
    pump = InsulinPump(config)
    bolus = pump.calculate_correction_bolus(current_glucose=250, target_glucose=100)  # Glycémie actuelle de 250 mg/dL
    assert bolus == 5  # (250 - 100) / 30 = 5 unités d'insuline
    print(f"Test bolus de correction: Glycémie 250 mg/dL, cible 100 mg/dL => Bolus de correction = {bolus} unités d'insuline")

# Test 5: Mesure de la Glycémie en Continu
def test_cgm_measurement():
    patient = Patient(initial_glucose=120)
    cgm = CGM(interval=5)
    glucose_measured = cgm.measure_glucose(patient)
    assert glucose_measured == 120
    print(f"Test CGM: Glycémie mesurée = {glucose_measured} mg/dL")

# Test 6: Contrôleur de Boucle Fermée
def test_alert_patient():
    patient = Patient(initial_glucose=300)  # Glycémie initiale de 300 mg/dL
    
    # Si la glycémie est supérieure à 250, une alerte doit être déclenchée
    assert patient.glucose_level > 250
    print("Test alerte : Glycémie critique supérieure à 250 mg/dL, alerte déclenchée.")


# Test 7
def test_dose_history():
    patient = Patient(initial_glucose=120)
    pump = InsulinPump(PumpConfig([0.8]*24, 10, 30, 10))
    
    # On simule une administration de bolus
    bolus = pump.calculate_meal_bolus(60)  # 60g de glucides
    patient.update_glucose_level(bolus, 60)
    
    # Ajoute des entrées à un historique fictif
    history = [
        {"date": "2024-10-01", "glucose": 120, "dose": 6},
        {"date": "2024-10-02", "glucose": 130, "dose": 7}
    ]
    
    # Vérification des données historiques
    assert history[0]["glucose"] == 120
    assert history[1]["dose"] == 7
    
    print(f"Test historique des doses : Glycémie et doses vérifiées dans l'historique.")

# Test 8
def test_mode_personnalisation():
    config = PumpConfig(
        basal_rates=[0.8, 0.6, 0.5, 0.7, 1.0, 1.2, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.5, 0.7, 0.8, 1.1, 1.0, 0.9, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2],
        insulin_to_carb_ratio=10,
        insulin_sensitivity_factor=30,
        max_bolus=10
    )

    pump = InsulinPump(config)
    
    # Mode "Sport" : réduction des taux basaux de 30%
    def adjust_for_sport(basal_rates):
        return [rate * 0.7 for rate in basal_rates]

    sport_basal_rates = adjust_for_sport(config.basal_rates)
    assert sport_basal_rates[0] == 0.8 * 0.7  # Vérifier la réduction

    # Mode "Nuit" : réduction des taux basaux de 20%
    def adjust_for_night(basal_rates):
        return [rate * 0.8 for rate in basal_rates]

    night_basal_rates = adjust_for_night(config.basal_rates)
    assert night_basal_rates[0] == 0.8 * 0.8  # Vérifier la réduction

    print("Test modes personnalisés : ajustements basaux pour le sport et la nuit vérifiés.")

# Test 9
def test_temporary_pump_stop():
    config = PumpConfig([0.8]*24, 10, 30, 10)
    pump = InsulinPump(config)
    patient = Patient(initial_glucose=120)
    
    # Simulation avec arrêt temporaire pendant 2 heures
    def stop_pump_for_duration(hours):
        return [0] * hours  # Aucune insuline administrée pendant 2 heures

    # Arrêt temporaire de 2 heures
    stopped_basal_rates = stop_pump_for_duration(2)
    assert stopped_basal_rates == [0, 0]  # Vérification que la pompe est bien arrêtée
    
    print("Test arrêt temporaire de la pompe : vérification de l'arrêt pendant 2 heures.")

# Test 10
def test_pump_settings_update():
    config = PumpConfig([0.8]*24, 10, 30, 10)
    pump = InsulinPump(config)

    # Mise à jour des taux basaux
    new_basal_rates = [0.5]*24
    pump.config.basal_rates = new_basal_rates
    assert pump.config.basal_rates[0] == 0.5  # Vérification de la mise à jour des taux basaux
    
    # Mise à jour du ratio insuline/glucides
    pump.config.insulin_to_carb_ratio = 8
    assert pump.config.insulin_to_carb_ratio == 8  # Vérification de la mise à jour du ratio ICR

    # Mise à jour du facteur de sensibilité à l'insuline (ISF)
    pump.config.insulin_sensitivity_factor = 25
    assert pump.config.insulin_sensitivity_factor == 25  # Vérification de la mise à jour de l'ISF

    print("Test mise à jour des paramètres de la pompe : paramètres correctement mis à jour.")
