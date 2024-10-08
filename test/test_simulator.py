# tests/test_simulator.py

from insulin_pump import InsulinPump
from pump_config import PumpConfig

def test_calculate_meal_bolus():
    config = PumpConfig([0.8] * 24, 10, 30, 10)
    pump = InsulinPump(config)
    carbs = 60
    expected_bolus = 6.0  # 60g / 10 (ICR)
    assert pump.calculate_meal_bolus(carbs) == expected_bolus, "Le calcul du bolus est incorrect"
