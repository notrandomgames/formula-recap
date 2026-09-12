from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import random

app = FastAPI(title="Formula Recap Unlocked Data Stream")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

drivers = [
    {"number": 1, "code": "VER", "team": "Red Bull Racing", "speed": 315, "throttle": 100, "gear": 8},
    {"number": 4, "code": "NOR", "team": "McLaren", "speed": 312, "throttle": 98, "gear": 8},
    {"number": 16, "code": "LEC", "team": "Ferrari", "speed": 310, "throttle": 95, "gear": 8},
]

@app.websocket("/ws/telemetry")
async def telemetry_websocket(websocket: WebSocket):
    """Broadcasting live telemetry feed freely to all connected devices."""
    await websocket.accept()
    try:
        while True:
            for driver in drivers:
                driver["speed"] = max(80, min(350, driver["speed"] + random.randint(-15, 15)))
                driver["throttle"] = max(0, min(100, driver["throttle"] + random.randint(-10, 10)))
            
            payload = {
                "timestamp": asyncio.get_event_loop().time(),
                "telemetry": drivers
            }
            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(0.25)
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
