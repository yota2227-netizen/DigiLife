from pydantic import BaseModel

class LifeForm(BaseModel):
    energy: float = 100.0
    social: float = 100.0
    integrity: float = 100.0

    # Decay rates (per second)
    DECAY_ENERGY: float = 0.5
    DECAY_SOCIAL: float = 0.8
    DECAY_INTEGRITY: float = 0.3

    # Thresholds for requests
    THRESHOLD: float = 20.0

    def decay(self):
        self.energy = max(0.0, self.energy - self.DECAY_ENERGY)
        self.social = max(0.0, self.social - self.DECAY_SOCIAL)
        self.integrity = max(0.0, self.integrity - self.DECAY_INTEGRITY)

    def eat(self):
        self.energy = min(100.0, self.energy + 30.0)

    def talk(self):
        self.social = min(100.0, self.social + 40.0)

    def sleep(self):
        self.integrity = min(100.0, self.integrity + 20.0)
