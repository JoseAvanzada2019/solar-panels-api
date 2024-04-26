from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from solver import fit_panels_in_rectangular_roof
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class BigRectangle(BaseModel):
    width: int
    height: int

class SmallRectangle(BaseModel):
    width: int
    height: int

class PanelsPlacementRequest(BaseModel):
    big_rectangle: BigRectangle = Field(..., example={"width": 100, "height": 200})
    small_rectangle: SmallRectangle = Field(..., example={"width": 100, "height": 200})

class PanelsPlacementResponse(BaseModel):
    total_small_rectangles: int
    arrangement: List[dict]

@app.post("/panels-placement", response_model=PanelsPlacementResponse)
async def panels_placement_api(request: PanelsPlacementRequest):
    big_rectangle_width = request.big_rectangle.width
    big_rectangle_height = request.big_rectangle.height
    small_rectangle_width = request.small_rectangle.width
    small_rectangle_height = request.small_rectangle.height

    total_small_rectangles, arrangement = fit_panels_in_rectangular_roof(
        big_rectangle_width, big_rectangle_height, small_rectangle_width, small_rectangle_height 
    )
    
    if total_small_rectangles is None or arrangement is None:
        raise HTTPException(status_code=500, detail="Failed to solve the panels placement problem")

    return PanelsPlacementResponse(total_small_rectangles=total_small_rectangles, arrangement=arrangement)