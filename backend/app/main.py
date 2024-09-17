from typing import Dict, List, Union
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from db.data import BATTERIES, TRANSFORMER

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Dimensions(BaseModel):
    length: int
    width: int
    unit: str


class Battery(BaseModel):
    id: int
    name: str
    dimensions: Dimensions
    energy: float
    energyUnit: str
    cost: int
    costCurrency: str
    releaseDate: str
    weight: int
    weightUnit: str


class Transformer(BaseModel):
    id: int
    name: str
    dimensions: Dimensions
    energy: float
    energyUnit: str
    cost: int
    costCurrency: str
    releaseDate: str
    weight: int
    weightUnit: str


class SelectedBattery(BaseModel):
    batteryId: int
    quantity: int


class SiteDetails(BaseModel):
    cost: int
    costCurrency: str
    dimensions: Dimensions
    energy: float
    energyUnit: str
    energyDensity: float
    energyDensityUnit: str
    layout: List[List[Dict[str, Union[str, int]]]]


@app.get("/health")
async def health():
    return {"message": "Hello World"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Docs",
        oauth2_redirect_url="/docs/oauth2-redirect",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="API Docs",
        redoc_js_url="/static/redoc.standalone.js",
    )


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return get_openapi(title="API Docs", version="1.0.0", routes=app.routes)


@app.get("/data/batteries")
def get_data_batteries() -> list[Battery]:
    return [Battery(**battery) for battery in BATTERIES]


@app.get("/data/transformer")
def get_data_transformer() -> Transformer:
    return Transformer(**TRANSFORMER)


def getBatteryCost(batteryId: int) -> int:
    for battery in BATTERIES:
        if battery["id"] == batteryId:
            return battery["cost"]
    raise ValueError(f"Battery with id {batteryId} not found")


def calculateTotalCost(selectedBatteries: List[SelectedBattery]) -> int:
    return sum(
        getBatteryCost(battery.batteryId) * battery.quantity
        for battery in selectedBatteries
    )


def getBatteryEnergy(batteryId: int) -> float:
    for battery in BATTERIES:
        if battery["id"] == batteryId:
            return battery["energy"]
    raise ValueError(f"Battery with id {batteryId} not found")


def calculateTotalEnergy(selectedBatteries: List[SelectedBattery]) -> float:
    return sum(
        getBatteryEnergy(battery.batteryId) * battery.quantity
        for battery in selectedBatteries
    )


def calculateEnergyDensity(totalEnergy: float, area: float) -> float:
    return totalEnergy / area if area > 0 else 0


@app.post("/site/build")
def postSiteBuild(selectedBatteries: list[SelectedBattery]) -> SiteDetails:
    shapes = []
    batteryCount = 0
    transformerCount = 0

    for selectedBattery in selectedBatteries:
        battery = next(
            (b for b in BATTERIES if b["id"] == selectedBattery.batteryId), None
        )
        if battery:
            for _ in range(selectedBattery.quantity):
                shapes.append(
                    {
                        "type": "battery",
                        "id": battery["id"],
                        "width": battery["dimensions"]["width"],
                        "length": battery["dimensions"]["length"],
                        "name": battery["name"],
                    }
                )
                batteryCount += 1

                # Add a transformer for every four batteries
                if batteryCount % 4 == 0:
                    shapes.append(
                        {
                            "type": "transformer",
                            "id": TRANSFORMER["id"],
                            "width": TRANSFORMER["dimensions"]["width"],
                            "length": TRANSFORMER["dimensions"]["length"],
                            "name": TRANSFORMER["name"],
                        }
                    )
                    transformerCount += 1

    # Add one final transformer if there are remaining batteries
    if batteryCount % 4 != 0:
        shapes.append(
            {
                "type": "transformer",
                "id": TRANSFORMER["id"],
                "width": TRANSFORMER["dimensions"]["width"],
                "length": TRANSFORMER["dimensions"]["length"],
                "name": TRANSFORMER["name"],
            }
        )
        transformerCount += 1

    # Maximum grid width
    maxWidth = 100

    # Sort shapes by decreasing length
    shapes.sort(key=lambda x: x["length"], reverse=True)

    shelves = []
    currentShelf = {"height": shapes[0]["length"], "shapes": [], "widthUsed": 0}
    shelves.append(currentShelf)

    for shape in shapes:
        width, length = shape["width"], shape["length"]
        if currentShelf["widthUsed"] + width <= maxWidth:
            # Place on current shelf
            currentShelf["shapes"].append((currentShelf["widthUsed"], shape))
            currentShelf["widthUsed"] += width
        else:
            # Start new shelf
            currentShelf = {"height": length, "shapes": [], "widthUsed": 0}
            shelves.append(currentShelf)
            currentShelf["shapes"].append((0, shape))
            currentShelf["widthUsed"] += width

    # Calculate total grid height and maximum width used
    totalHeight = sum(shelf["height"] for shelf in shelves)
    maxWidthUsed = max(shelf["widthUsed"] for shelf in shelves)

    totalCost = calculateTotalCost(selectedBatteries)
    totalEnergy = calculateTotalEnergy(selectedBatteries)
    area = totalHeight * maxWidthUsed
    energyDensity = calculateEnergyDensity(totalEnergy, area)

    return SiteDetails(
        cost=totalCost,
        costCurrency="USD",
        dimensions=Dimensions(length=totalHeight, width=maxWidthUsed, unit="ft"),
        energy=totalEnergy,
        energyUnit="MWh",
        energyDensity=energyDensity,
        energyDensityUnit="MWh/sqft",
        layout=[[shape for _, shape in shelf["shapes"]] for shelf in shelves],
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
