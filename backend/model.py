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
    THRESHOLD_ENERGY: float = 20.0
    THRESHOLD_SOCIAL: float = 50.0  # Changed to 50%
    THRESHOLD_INTEGRITY: float = 20.0

    # Action Costs
    COST_EAT: float = 5.0
    COST_TALK: float = 10.0
    COST_SLEEP: float = 5.0

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
        # 1. Critical Energy Check (Highest Priority)
        if self.energy < self.THRESHOLD_ENERGY:
            self.eat()
            return

        # 2. Critical Parameter Check (Immediate Action required)
        # Check if we can perform action without dropping energy below threshold immediately
        if self.social < self.THRESHOLD_SOCIAL:
            if self.energy - self.COST_TALK >= self.THRESHOLD_ENERGY:
                self.talk()
                return
            else:
                self.eat() # Emergency eat to enable talking
                return

        if self.integrity < self.THRESHOLD_INTEGRITY:
            if self.energy - self.COST_SLEEP >= self.THRESHOLD_ENERGY:
                self.sleep()
                return
            else:
                self.eat() # Emergency eat to enable sleeping
                return

        # 3. Predictive Safety Check (Time To Critical)
        
        # Predict Social Criticality
        if self.social > self.THRESHOLD_SOCIAL:
            ttc_social = (self.social - self.THRESHOLD_SOCIAL) / self.DECAY_SOCIAL
            # Only predict if critical time is relatively close (e.g., within 60 seconds)
            # Otherwise we rely on normal energy management
            if ttc_social < 60:
                predicted_energy_at_social_criticalParams = self.energy - (self.DECAY_ENERGY * ttc_social)
                if predicted_energy_at_social_criticalParams - self.COST_TALK < self.THRESHOLD_ENERGY:
                    # We won't have enough energy when social hits 20%, so eat now
                    self.eat()
                    return

        # Predict Integrity Criticality
        if self.integrity > self.THRESHOLD_INTEGRITY:
            ttc_integrity = (self.integrity - self.THRESHOLD_INTEGRITY) / self.DECAY_INTEGRITY
            if ttc_integrity < 60:
                predicted_energy_at_integrity_critical = self.energy - (self.DECAY_ENERGY * ttc_integrity)
                if predicted_energy_at_integrity_critical - self.COST_SLEEP < self.THRESHOLD_ENERGY:
                    # We won't have enough energy when integrity hits 20%, so eat now
                    self.eat()
                    return
