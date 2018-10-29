from main import units

class inductor:
    inductance = 0 * units.henry
    resistance = 0 * units.ohm
    drawnCurrent = 0 * units.amp
    def __init__(self, inductance, resistance):
        self.inductance = inductance
        self.resistance = resistance

    def update(self, voltage, dt=1):
        di = (voltage/self.resistance - self.drawnCurrent).m / self.inductance.m
        self.drawnCurrent += di * units.amp * dt
