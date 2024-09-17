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
    energy_unit: str
    cost: int
    cost_currency: str
    releaseDate: str
    weight: int
    weight_unit: str


class Transformer(BaseModel):
    id: int
    name: str
    dimensions: Dimensions
    energy: float
    energy_unit: str
    cost: int
    cost_currency: str
    releaseDate: str
    weight: int
    weight_unit: str


class SelectedBattery(BaseModel):
    battery_id: int
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


def get_battery_cost(battery_id: int) -> int:
    for battery in BATTERIES:
        if battery["id"] == battery_id:
            return battery["cost"]
    raise ValueError(f"Battery with id {battery_id} not found")


def calculate_total_cost(selected_batteries: List[SelectedBattery]) -> int:
    return sum(
        get_battery_cost(battery.battery_id) * battery.quantity
        for battery in selected_batteries
    )


def get_battery_energy(battery_id: int) -> float:
    for battery in BATTERIES:
        if battery["id"] == battery_id:
            return battery["energy"]
    raise ValueError(f"Battery with id {battery_id} not found")


def calculate_total_energy(selected_batteries: List[SelectedBattery]) -> float:
    return sum(
        get_battery_energy(battery.battery_id) * battery.quantity
        for battery in selected_batteries
    )


def calculate_energy_density(total_energy: float, area: float) -> float:
    return total_energy / area if area > 0 else 0


@app.post("/site/build")
def post_site_build(selectedBatteries: list[SelectedBattery]) -> SiteDetails:
    shapes = [
        {"type": "battery", "id": 4, "width": 10, "length": 10},
        {"type": "battery", "id": 2, "width": 30, "length": 10},
        {"type": "battery", "id": 1, "width": 40, "length": 10},
        {"type": "battery", "id": 1, "width": 40, "length": 10},
        {"type": "battery", "id": 1, "width": 40, "length": 10},
        {"type": "battery", "id": 1, "width": 40, "length": 10},
        {"type": "battery", "id": 2, "width": 30, "length": 10},
        {"type": "battery", "id": 3, "width": 30, "length": 10},
        {"type": "battery", "id": 3, "width": 30, "length": 10},
        {"type": "transformer", "id": 1, "width": 10, "length": 10},
        {"type": "transformer", "id": 1, "width": 10, "length": 10},
    ]

    # Maximum grid width
    max_width = 100

    # Sort shapes by decreasing length
    shapes.sort(key=lambda x: x["length"], reverse=True)

    shelves = []
    current_shelf = {"height": shapes[0]["length"], "shapes": [], "width_used": 0}
    shelves.append(current_shelf)

    for shape in shapes:
        width, length = shape["width"], shape["length"]
        if current_shelf["width_used"] + width <= max_width:
            # Place on current shelf
            current_shelf["shapes"].append((current_shelf["width_used"], shape))
            current_shelf["width_used"] += width
        else:
            # Start new shelf
            current_shelf = {"height": length, "shapes": [], "width_used": 0}
            shelves.append(current_shelf)
            current_shelf["shapes"].append((0, shape))
            current_shelf["width_used"] += width

    # Calculate total grid height and maximum width used
    total_height = sum(shelf["height"] for shelf in shelves)
    max_width_used = max(shelf["width_used"] for shelf in shelves)

    total_cost = calculate_total_cost(selectedBatteries)
    total_energy = calculate_total_energy(selectedBatteries)
    area = total_height * max_width_used
    energy_density = calculate_energy_density(total_energy, area)

    return SiteDetails(
        cost=total_cost,
        costCurrency="USD",
        dimensions=Dimensions(length=total_height, width=max_width_used, unit="ft"),
        energy=total_energy,
        energyUnit="MWh",
        energyDensity=energy_density,
        energyDensityUnit="MWh/sqft",
        layout=[[shape for _, shape in shelf["shapes"]] for shelf in shelves],
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
