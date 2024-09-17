from fastapi import APIRouter
from models import SelectedBattery, SiteDetails, Dimensions
from db import BATTERIES, TRANSFORMER

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

    shapes.sort(key=lambda x: x["length"], reverse=True)

    shelves = []
    current_shelf = {"height": shapes[0]["length"], "shapes": [], "width_used": 0}
    shelves.append(current_shelf)

    for shape in shapes:
        width, length = shape["width"], shape["length"]
        if current_shelf["width_used"] + width <= max_width:
            current_shelf["shapes"].append((current_shelf["width_used"], shape))
            current_shelf["width_used"] += width
        else:
            current_shelf = {"height": length, "shapes": [], "width_used": 0}
            shelves.append(current_shelf)
            current_shelf["shapes"].append((0, shape))
            current_shelf["width_used"] += width

    total_height = sum(shelf["height"] for shelf in shelves)
    max_width_used = max(shelf["width_used"] for shelf in shelves)

    total_cost = calculate_total_cost(selected_batteries)
    total_energy = calculate_total_energy(selected_batteries)
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
