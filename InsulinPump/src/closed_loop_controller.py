# src/closed_loop_controller.py

class ClosedLoopController:
    def __init__(self, target_glucose, pump, cgm):
        self.target_glucose = target_glucose
        self.pump = pump
        self.cgm = cgm

    def adjust_basal_rate(self, current_glucose):
        if current_glucose > self.target_glucose:
            return 1  # Augmenter la dose basale
        else:
            return 0.5  # Diminuer la dose
