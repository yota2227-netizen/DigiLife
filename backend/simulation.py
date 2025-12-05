import asyncio
import os
import subprocess
from typing import List
from fastapi import WebSocket
from model import LifeForm
import logging

# Configure Logging
logging.basicConfig(
    filename='simulation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Simulation:
    def __init__(self, life_form: LifeForm):
        self.life_form = life_form
        self.active_connections: List[WebSocket] = []
        self.running = False

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Cancel shutdown if a client reconnects
        if hasattr(self, 'shutdown_task') and self.shutdown_task:
            self.shutdown_task.cancel()
            self.shutdown_task = None
            print("Shutdown cancelled - Client reconnected")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        # Start shutdown timer if no clients connected
        if len(self.active_connections) == 0:
            self.shutdown_task = asyncio.create_task(self.shutdown_sequence())
            print("All clients disconnected. Shutdown in 3 seconds...")

    async def shutdown_sequence(self):
        try:
            await asyncio.sleep(3)
            print("Executing shutdown script...")
            # Execute stop_digilife.bat in the parent directory
            subprocess.Popen([os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "stop_digilife.bat"))], shell=True)
            # Find the bat file relative to this file
        except asyncio.CancelledError:
            print("Shutdown sequence cancelled")
            pass

    async def broadcast(self):
        state = self.life_form.model_dump_json()
        for connection in self.active_connections:
            try:
                await connection.send_text(state)
            except Exception:
                # Handle disconnected clients gracefully if needed
                pass

    async def start(self):
        self.running = True
        while self.running:
            self.life_form.decay()
            self.life_form.check_and_recover()
            
            # Log current state
            logging.info(f"Energy: {self.life_form.energy:.1f}, Social: {self.life_form.social:.1f}, Integrity: {self.life_form.integrity:.1f}")

            # Check for violations
            if self.life_form.energy < self.life_form.THRESHOLD_ENERGY:
                 logging.warning(f"VIOLATION: Energy is below threshold ({self.life_form.energy:.1f} < {self.life_form.THRESHOLD_ENERGY})")
            if self.life_form.social < self.life_form.THRESHOLD_SOCIAL:
                 logging.warning(f"VIOLATION: Social is below threshold ({self.life_form.social:.1f} < {self.life_form.THRESHOLD_SOCIAL})")
            if self.life_form.integrity < self.life_form.THRESHOLD_INTEGRITY:
                 logging.warning(f"VIOLATION: Integrity is below threshold ({self.life_form.integrity:.1f} < {self.life_form.THRESHOLD_INTEGRITY})")

            await self.broadcast()
            await asyncio.sleep(1)  # Decay every second

    def stop(self):
        self.running = False
