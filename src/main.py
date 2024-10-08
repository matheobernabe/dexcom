# src/main.py

from pump_config import PumpConfig
from insulin_pump import InsulinPump
from patient import Patient
from cgm import CGM
from closed_loop_controller import ClosedLoopController
from simulator import Simulator

if __name__ == "__main__":
    config = PumpConfig(
        basal_rates=[0.8, 0.6, 0.5, 0.7, 1.0, 1.2, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4], 
        insulin_to_carb_ratio=10, 
        insulin_sensitivity_factor=30, 
        max_bolus=10
    )

    pump = InsulinPump(config)
    patient = Patient(initial_glucose=120)
    cgm = CGM(interval=5)
    controller = ClosedLoopController(target_glucose=100, pump=pump, cgm=cgm)

    simulator = Simulator(patient, pump, cgm, controller, duration=24)
    simulator.run_simulation()
