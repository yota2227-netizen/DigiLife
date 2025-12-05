from pydantic import BaseModel
import random

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

    # State flags for time-based recovery
    remaining_recovery_eat: float = 0.0
    remaining_recovery_sleep: float = 0.0

    def decay(self):
        # Update Energy (Eat)
        if self.remaining_recovery_eat > 0:
            recovery_rate = self.DECAY_ENERGY * 2
            amount = min(self.remaining_recovery_eat, recovery_rate)
            self.energy = min(100.0, self.energy + amount)
            self.remaining_recovery_eat -= amount
        else:
            self.energy = max(0.0, self.energy - self.DECAY_ENERGY)

        # Update Social (Normal decay, Talk is immediate)
        self.social = max(0.0, self.social - self.DECAY_SOCIAL)

        # Update Integrity (Sleep)
        if self.remaining_recovery_sleep > 0:
            recovery_rate = self.DECAY_INTEGRITY * 2
            amount = min(self.remaining_recovery_sleep, recovery_rate)
            self.integrity = min(100.0, self.integrity + amount)
            self.remaining_recovery_sleep -= amount
        else:
            self.integrity = max(0.0, self.integrity - self.DECAY_INTEGRITY)

    def eat(self):
        # Don't start if already eating
        if self.remaining_recovery_eat > 0:
            return
            
        # Cost is paid immediately
        self.energy = max(0.0, self.energy - self.COST_EAT)
        # Set recovery target (+30 total)
        self.remaining_recovery_eat = 30.0

    def talk(self):
        # Gain random social (15-30), cost 10 energy
        gain = random.uniform(15.0, 30.0)
        self.social = min(100.0, self.social + gain)
        self.energy = max(0.0, self.energy - self.COST_TALK)

    def sleep(self):
        # Don't start if already sleeping
        if self.remaining_recovery_sleep > 0:
            return

        # Cost is paid immediately
        self.energy = max(0.0, self.energy - self.COST_SLEEP)
        # Set recovery target (+20 total)
        self.remaining_recovery_sleep = 20.0

    def check_and_recover(self):
        # If currently recovering (busy), do not initiate new actions
        if self.remaining_recovery_eat > 0 or self.remaining_recovery_sleep > 0:
            return

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
