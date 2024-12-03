import pytest
from src.pump_config import PumpConfig
from src.insulin_pump import InsulinPump
from src.patient import Patient
from src.cgm import CGM
from src.closed_loop_controller import ClosedLoopController
from src.simulator import Simulator

def test_pump_config():
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

def test_insulin_pump():
    config = PumpConfig([0.8]*24, 10, 30, 10)
    pump = InsulinPump(config)
    bolus = pump.calculate_meal_bolus(60)
    assert bolus == 6
    correction_bolus = pump.calculate_correction_bolus(current_glucose=250, target_glucose=100)
    assert correction_bolus == 5

def test_patient():
    patient = Patient(initial_glucose=120)
    assert patient.glucose_level == 120
    patient.update_glucose_level(insulin=1, carbs=10)
    assert patient.glucose_level == 120

def test_cgm():
    patient = Patient(initial_glucose=120)
    cgm = CGM(interval=5)
    glucose_measured = cgm.measure_glucose(patient)
    assert glucose_measured == 120

def test_closed_loop_controller():
    config = PumpConfig([0.8]*24, 10, 30, 10)
    pump = InsulinPump(config)
    patient = Patient(initial_glucose=120)
    cgm = CGM(interval=5)
    controller = ClosedLoopController(target_glucose=100, pump=pump, cgm=cgm)
    assert controller.target_glucose == 100

def test_simulator():
    config = PumpConfig([0.8]*24, 10, 30, 10)
    pump = InsulinPump(config)
    patient = Patient(initial_glucose=120)
    cgm = CGM(interval=5)
    controller = ClosedLoopController(target_glucose=100, pump=pump, cgm=cgm)
    simulator = Simulator(patient, pump, cgm, controller, duration=1)
    simulator.run_simulation()
    assert patient.glucose_level < 120