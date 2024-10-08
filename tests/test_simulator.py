import pytest
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

# Test 3: Programmation du Bolus Alimentaire
def test_meal_bolus():
    config = PumpConfig([0.8]*24, 10, 30, 10)
    pump = InsulinPump(config)
    bolus = pump.calculate_meal_bolus(60)  # 60g de glucides
    assert bolus == 6  # 60g / 10 = 6 unités d'insuline

# Test 4: Fourniture d'un Bolus de Correction
def test_correction_bolus():
    config = PumpConfig([0.8]*24, 10, 30, 10)
    pump = InsulinPump(config)
    bolus = pump.calculate_correction_bolus(current_glucose=250, target_glucose=100)  # Glycémie actuelle de 250 mg/dL
    assert bolus == 5  # (250 - 100) / 30 = 5 unités d'insuline

# Test 5: Mesure de la Glycémie en Continu
def test_cgm_measurement():
    patient = Patient(initial_glucose=120)
    cgm = CGM(interval=5)
    glucose_measured = cgm.measure_glucose(patient)
    assert glucose_measured == 120

# Test 6: Alerte des Patients par le PDM (Glycémie Hors Limites)
def test_alert_patient():
    patient = Patient(initial_glucose=300)  # Glycémie de 300 mg/dL
    assert patient.glucose_level > 250  # Une alerte devrait être déclenchée
