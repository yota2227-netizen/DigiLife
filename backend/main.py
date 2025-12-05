from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
from model import LifeForm
from simulation import Simulation

life_form = LifeForm()
simulation = Simulation(life_form)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start simulation on startup
    asyncio.create_task(simulation.start())
    yield
    # Stop simulation on shutdown
    simulation.stop()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "DigiLife Backend Running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await simulation.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for any client messages if needed
            await websocket.receive_text()
    except WebSocketDisconnect:
        simulation.disconnect(websocket)

@app.post("/action/{action_type}")
async def perform_action(action_type: str):
    if action_type == "eat":
        life_form.eat()
    elif action_type == "talk":
        life_form.talk()
    elif action_type == "sleep":
        life_form.sleep()
    else:
        return {"error": "Invalid action"}
    
    # Broadcast update immediately after action
    await simulation.broadcast()
    return life_form

