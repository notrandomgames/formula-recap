import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Formula Recap Real Data Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Fetch Accurate Real Driver Standings (Ergast API)
@app.get("/api/v1/standings")
async def get_real_standings():
    url = "https://ergast.com/api/f1/current/driverStandings.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        
    standings_list = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
    
    formatted_standings = [
        {
            "pos": driver["position"],
            "driver": f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}",
            "points": driver["points"],
            "team": driver["Constructors"][0]["name"]
        }
        for driver in standings_list
    ]
    return {"standings": formatted_standings}

# 2. Stream Real Live Telemetry & Radio Feeds (OpenF1 API)
@app.websocket("/ws/telemetry")
async def telemetry_websocket(websocket: WebSocket):
    await websocket.accept()
    
    # OpenF1 live car data endpoint for current active session
    openf1_url = "https://api.openf1.org/v1/car_data?session_key=latest"
    
    async with httpx.AsyncClient() as client:
        try:
            while True:
                response = await client.get(openf1_url)
                if response.status_code == 200:
                    raw_data = response.json()
                    # Transmit the latest real telemetry frame
                    await websocket.send_json({"telemetry": raw_data[-10:]})
                
                await asyncio.sleep(1.0)
        except WebSocketDisconnect:
            pass
