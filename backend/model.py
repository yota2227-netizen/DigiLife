from pydantic import BaseModel
import random
import tiktoken
from duckduckgo_search import DDGS

class LifeForm(BaseModel):
    # Energy is now derived from token_balance
    token_balance: int = 5000
    MAX_TOKENS: int = 5000
    
    # Energy needs to be a field to be serialized by Pydantic default settings
    energy: float = 100.0
    
    social: float = 100.0
    integrity: float = 100.0

    # Decay rates (per second)
    # Energy decay: tokens per second
    DECAY_TOKENS: int = 25  # Roughly 0.5% of 5000
    DECAY_SOCIAL: float = 0.8
    DECAY_INTEGRITY: float = 0.3

    # Thresholds for requests (Energy is % calculated from tokens)
    THRESHOLD_ENERGY: float = 20.0
    THRESHOLD_SOCIAL: float = 50.0
    THRESHOLD_INTEGRITY: float = 20.0

    # Action Costs
    COST_SEARCH: int = 100  # Cost to perform a search
    COST_TALK: float = 10.0  # Energy % cost (converted dynamically)
    COST_SLEEP: float = 5.0  # Energy % cost (converted dynamically)

    # State flags for time-based recovery
    # remaining_recovery_eat removed (Search is immediate/blocking)
    remaining_recovery_sleep: float = 0.0

    # Statistics
    last_search_keyword: str = "None"
    last_search_tokens: int = 0
    total_search_tokens: int = 0

    def _update_energy(self):
        """Helper to sync energy % with token_balance"""
        self.energy = (self.token_balance / self.MAX_TOKENS) * 100.0

    def decay(self):
        # Update Energy (Token Decay)
        self.token_balance = max(0, self.token_balance - self.DECAY_TOKENS)
        self._update_energy()

        # Update Social (Normal decay, Talk is immediate)
        self.social = max(0.0, self.social - self.DECAY_SOCIAL)

        # Update Integrity (Sleep)
        if self.remaining_recovery_sleep > 0:
            recovery_rate = self.DECAY_INTEGRITY * 2
from pydantic import BaseModel
import random
import tiktoken
from duckduckgo_search import DDGS
import asyncio

class LifeForm(BaseModel):
    # Energy is now derived from token_balance
    token_balance: int = 5000
    MAX_TOKENS: int = 5000
    
    # Energy needs to be a field to be serialized by Pydantic default settings
    energy: float = 100.0
    
    social: float = 100.0
    integrity: float = 100.0

    # Decay rates (per second)
    # Energy decay: tokens per second
    DECAY_TOKENS: int = 25  # Roughly 0.5% of 5000
    DECAY_SOCIAL: float = 0.8
    DECAY_INTEGRITY: float = 0.3

    # Thresholds for requests (Energy is % calculated from tokens)
    THRESHOLD_ENERGY: float = 20.0
    THRESHOLD_SOCIAL: float = 50.0
    THRESHOLD_INTEGRITY: float = 20.0

    # Action Costs
    COST_SEARCH: int = 100  # Cost to perform a search
    COST_TALK: float = 10.0  # Energy % cost (converted dynamically)
    COST_SLEEP: float = 5.0  # Energy % cost (converted dynamically)

    # State flags for time-based recovery
    # remaining_recovery_eat removed (Search is immediate/blocking)
    remaining_recovery_sleep: float = 0.0

    # Statistics
    last_search_keyword: str = "None"
    last_search_tokens: int = 0
    total_search_tokens: int = 0

    def _update_energy(self):
        """Helper to sync energy % with token_balance"""
        self.energy = (self.token_balance / self.MAX_TOKENS) * 100.0

    def decay(self):
        # Update Energy (Token Decay)
        self.token_balance = max(0, self.token_balance - self.DECAY_TOKENS)
        self._update_energy()

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

    @staticmethod
    def _perform_search():
        # Use more complex queries and fetch more results to increase token count
        complex_keywords = ["Quantum Computing", "Ancient Civilizations", "Photosynthesis Process", "Machine Learning Algorithms", "Space Exploration History", "Philosophy of Mind", "Global Economic Trends", "Genetic Engineering", "Renewable Energy Technologies", "Neurology Research", "Deep Sea Exploration", "Particle Physics", "Cognitive Science"]
        
        # Retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                keyword = random.choice(complex_keywords)
                query = random.choice([
                    f"Detailed explanation of {keyword}",
                    f"Comprehensive history of {keyword}",
                    f"Technical breakdown of {keyword}",
                    f"Future implications of {keyword}",
                    f"Analysis of {keyword}"
                ])
                
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=20))
                    content = ""
                    if results:
                        content_pieces = [r['body'] for r in results]
                        content = "\n\n".join(content_pieces)
                        
                        # Count tokens
                        enc = tiktoken.get_encoding("cl100k_base")
                        tokens = enc.encode(content)
                        token_count = len(tokens)
                        
                        if token_count > 0:
                            return token_count, query, keyword
                        else:
                            print(f"Attempt {attempt+1}: Search returned 0 tokens. Retrying...")
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
                
        # Fallback if all retries fail
        fallback_keyword = "General Knowledge"
        fallback_query = "Fallback Recovery Search"
        fallback_content = "Knowledge recovery protocol initiated. System integrity check passed. Backup data loaded. " * 50
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode(fallback_content)
        return len(tokens), fallback_query, fallback_keyword

    async def eat(self):
        # "Eat" is now "Search & Recover Knowledge"
        # Allow search even if tokens are low (Emergency Recovery)
        if self.token_balance < self.COST_SEARCH:
            # Drain remaining tokens but allow search
            self.token_balance = 0
        else:
            self.token_balance -= self.COST_SEARCH
            
        self._update_energy()
        
        # Run search in a separate thread to avoid blocking the event loop
        try:
            # Await the thread execution (requires asyncio loop running)
            token_count, query, keyword = await asyncio.to_thread(LifeForm._perform_search)
            
            # Recover Energy (Add tokens)
            self.token_balance = min(self.MAX_TOKENS, self.token_balance + token_count + len(query))
            self._update_energy()
            
            # Update Stats
            self.last_search_keyword = keyword
            self.last_search_tokens = token_count
            self.total_search_tokens += token_count
            
            print(f"SEARCH COMPLETE: +{token_count} tokens from '{query}'")

        except Exception as e:
            print(f"SEARCH FAILED: {e}")
            self.token_balance = min(self.MAX_TOKENS, self.token_balance + 50)
            self._update_energy()

    async def talk(self):
        # Gain random social (15-30), cost energy % converted to tokens
        cost_tokens = int((self.COST_TALK / 100.0) * self.MAX_TOKENS)
        if self.token_balance >= cost_tokens:
            gain = random.uniform(15.0, 30.0)
            self.social = min(100.0, self.social + gain)
            self.token_balance -= cost_tokens
            self._update_energy()

    async def sleep(self):
        # Don't start if already sleeping
        if self.remaining_recovery_sleep > 0:
            return

        # Cost is paid immediately
        cost_tokens = int((self.COST_SLEEP / 100.0) * self.MAX_TOKENS)
        
        if self.token_balance >= cost_tokens:
            self.token_balance -= cost_tokens
            self._update_energy()
            # Set recovery target (+20 total)
            self.remaining_recovery_sleep = 20.0

    async def check_and_recover(self):
        # If currently recovering (busy), do not initiate new actions
        if self.remaining_recovery_sleep > 0:
            return
            
        # 1. Critical Energy Check (Highest Priority)
        if self.energy < self.THRESHOLD_ENERGY:
            await self.eat() # Triggers search
            return

        # 2. Critical Parameter Check (Immediate Action required)
        # Check if we can perform action as long as we have enough energy to pay the cost
        # We relax the safety buffer to prioritize critical parameter recovery
        if self.social < self.THRESHOLD_SOCIAL:
            cost_talk_pct = self.COST_TALK
            if self.energy > cost_talk_pct + 1.0: # Small buffer
                await self.talk()
                return
            else:
                await self.eat() # Emergency eat to enable talking
                return

        if self.integrity < self.THRESHOLD_INTEGRITY:
            cost_sleep_pct = self.COST_SLEEP
            if self.energy > cost_sleep_pct + 1.0: # Small buffer
                await self.sleep()
                return
            else:
                await self.eat() # Emergency eat to enable sleeping
                return

        # 3. Predictive Safety Check (Time To Critical)
        DECAY_ENERGY_PCT = (self.DECAY_TOKENS / self.MAX_TOKENS) * 100.0

        # Predict Social Criticality
        if self.social > self.THRESHOLD_SOCIAL:
            ttc_social = (self.social - self.THRESHOLD_SOCIAL) / self.DECAY_SOCIAL
            if ttc_social < 60:
                predicted_energy = self.energy - (DECAY_ENERGY_PCT * ttc_social)
                if predicted_energy - self.COST_TALK < self.THRESHOLD_ENERGY:
                    await self.eat()
                    return

        # Predict Integrity Criticality
        if self.integrity > self.THRESHOLD_INTEGRITY:
            ttc_integrity = (self.integrity - self.THRESHOLD_INTEGRITY) / self.DECAY_INTEGRITY
            if ttc_integrity < 60:
                predicted_energy = self.energy - (DECAY_ENERGY_PCT * ttc_integrity)
                if predicted_energy - self.COST_SLEEP < self.THRESHOLD_ENERGY:
                    await self.eat()
                    return
