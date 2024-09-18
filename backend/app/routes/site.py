from fastapi import APIRouter
from models import SelectedBattery, SiteDetails, Dimensions
from db import BATTERIES, TRANSFORMER
from core.layout import LayoutBuilder, FirstFitDecreasingHeightLayoutStrategy

router = APIRouter()


def get_battery_cost(battery_id: int) -> int:
    for battery in BATTERIES:
        if battery["id"] == battery_id:
            return battery["cost"]
    raise ValueError(f"Battery with id {battery_id} not found")


def calculate_total_cost(selected_batteries: list[SelectedBattery]) -> int:
    return sum(
        get_battery_cost(battery.batteryId) * battery.quantity
        for battery in selected_batteries
    )


def get_battery_energy(battery_id: int) -> float:
    for battery in BATTERIES:
        if battery["id"] == battery_id:
            return battery["energy"]
    raise ValueError(f"Battery with id {battery_id} not found")


def calculate_total_energy(selected_batteries: list[SelectedBattery]) -> float:
    return sum(
        get_battery_energy(battery.batteryId) * battery.quantity
        for battery in selected_batteries
    )


def calculate_energy_density(total_energy: float, area: float) -> float:
    return total_energy / area if area > 0 else 0


@router.post("/build")
def post_site_build(selected_batteries: list[SelectedBattery]) -> SiteDetails:
    shapes = []
    battery_count = 0
    transformer_count = 0

    for selected_battery in selected_batteries:
        battery = next(
            (b for b in BATTERIES if b["id"] == selected_battery.batteryId), None
        )
        if battery:
            for _ in range(selected_battery.quantity):
                shapes.append(
                    {
                        "type": "battery",
                        "id": battery["id"],
                        "width": battery["dimensions"]["width"],
                        "length": battery["dimensions"]["length"],
                        "name": battery["name"],
                    }
                )
                battery_count += 1

                if battery_count % 4 == 0:
                    shapes.append(
                        {
                            "type": "transformer",
                            "id": TRANSFORMER["id"],
                            "width": TRANSFORMER["dimensions"]["width"],
                            "length": TRANSFORMER["dimensions"]["length"],
                            "name": TRANSFORMER["name"],
                        }
                    )
                    transformer_count += 1

    if battery_count % 4 != 0:
        shapes.append(
            {
                "type": "transformer",
                "id": TRANSFORMER["id"],
                "width": TRANSFORMER["dimensions"]["width"],
                "length": TRANSFORMER["dimensions"]["length"],
                "name": TRANSFORMER["name"],
            }
        )
        transformer_count += 1

    max_width = 100
    layout_builder = LayoutBuilder(FirstFitDecreasingHeightLayoutStrategy())
    layout = layout_builder.build(shapes, max_width)

    total_cost = calculate_total_cost(selected_batteries)
    total_energy = calculate_total_energy(selected_batteries)
    energy_density = calculate_energy_density(total_energy, layout.area)

    return SiteDetails(
        cost=total_cost,
        costCurrency="USD",
        dimensions=Dimensions(length=layout.height, width=layout.width, unit="ft"),
        energy=total_energy,
        energyUnit="MWh",
        energyDensity=energy_density,
        energyDensityUnit="MWh/sqft",
        layout=[[shape for _, shape in shelf["shapes"]] for shelf in layout.layout],
    )
