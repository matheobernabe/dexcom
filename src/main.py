from pump_config import PumpConfig
from insulin_pump import InsulinPump
from patient import Patient
from cgm import CGM
from closed_loop_controller import ClosedLoopController
from simulator import Simulator

if __name__ == "__main__":
    # Configuration de base de la pompe
    config = PumpConfig(
        basal_rates=[0.8]*24,  # Exemple : taux basal constant de 0,8 U/h pour 24 heures
        insulin_to_carb_ratio=10,  # Ratio insuline/glucides
        insulin_sensitivity_factor=30,  # Sensibilité à l'insuline
        max_bolus=10  # Bolus maximum de 10 unités
    )

    # Création de la pompe, du patient, du CGM et du contrôleur
    pump = InsulinPump(config)
    patient = Patient(initial_glucose=120)
    cgm = CGM(interval=5)
    controller = ClosedLoopController(target_glucose=100, pump=pump, cgm=cgm)

    # Exécution de la simulation pour 24 heures
    simulator = Simulator(patient, pump, cgm, controller, duration=24)
    simulator.run_simulation()

    print("Simulation terminée.")
