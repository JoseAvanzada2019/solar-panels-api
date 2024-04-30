from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from placement_handler import PlacementHandler
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class Roof(BaseModel):
    width: int
    height: int

class SolarPanel(BaseModel):
    width: int
    height: int

class PanelsPlacementRequest(BaseModel):
    type: str =  Field(..., example="rectangular")
    roof: Roof = Field(..., example={"width": 100, "height": 200})
    solar_panel: SolarPanel = Field(..., example={"width": 100, "height": 200})

class PanelsPlacementResponse(BaseModel):
    total_panels: int
    arrangement: List[dict]

@app.post("/panels-placement", response_model=PanelsPlacementResponse)
async def panels_placement_api(request: PanelsPlacementRequest):
    roof = {
                "width": request.roof.width,
                "height": request.roof.height
            }
    solar_panel = {
                "width": request.solar_panel.width,
                "height": request.solar_panel.height
            }
    type = request.type
    handler = PlacementHandler(type)
    arrangement = handler.place_solar_panels(roof, solar_panel)
    if arrangement is None:
        raise HTTPException(status_code=500, detail="Failed to solve the panels placement problem")
    return PanelsPlacementResponse(total_panels=len(arrangement), arrangement=arrangement)