from fastapi import APIRouter
from models import SelectedBattery, SiteDetails, Dimensions
from db import BATTERIES, TRANSFORMER

router = APIRouter()


def getBatteryCost(batteryId: int) -> int:
    for battery in BATTERIES:
        if battery["id"] == batteryId:
            return battery["cost"]
    raise ValueError(f"Battery with id {batteryId} not found")


def calculateTotalCost(selectedBatteries: list[SelectedBattery]) -> int:
    return sum(
        getBatteryCost(battery.batteryId) * battery.quantity
        for battery in selectedBatteries
    )


def getBatteryEnergy(batteryId: int) -> float:
    for battery in BATTERIES:
        if battery["id"] == batteryId:
            return battery["energy"]
    raise ValueError(f"Battery with id {batteryId} not found")


def calculateTotalEnergy(selectedBatteries: list[SelectedBattery]) -> float:
    return sum(
        getBatteryEnergy(battery.batteryId) * battery.quantity
        for battery in selectedBatteries
    )


def calculateEnergyDensity(totalEnergy: float, area: float) -> float:
    return totalEnergy / area if area > 0 else 0


@router.post("/build")
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
