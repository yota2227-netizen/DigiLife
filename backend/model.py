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
        # Gain 30 energy, but cost 5 energy to perform action (Net +25)
        self.energy = min(100.0, self.energy + 30.0 - 5.0)

    def talk(self):
        # Gain 40 social, cost 10 energy
        self.social = min(100.0, self.social + 40.0)
        self.energy = max(0.0, self.energy - 10.0)

    def sleep(self):
        # Gain 20 integrity, cost 5 energy
        self.integrity = min(100.0, self.integrity + 20.0)
        self.energy = max(0.0, self.energy - 5.0)

    def check_and_recover(self):
        if self.energy < self.THRESHOLD:
            self.eat()
        if self.social < self.THRESHOLD:
            self.talk()
        if self.integrity < self.THRESHOLD:
            self.sleep()
