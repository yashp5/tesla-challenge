from fastapi import APIRouter
from models import Battery, Transformer, Dimensions
from db import BATTERIES, TRANSFORMER

router = APIRouter()


@router.get("/batteries")
def get_data_batteries() -> list[Battery]:
    return [
        Battery(
            id=battery["id"],
            name=battery["name"],
            dimensions=Dimensions(**battery["dimensions"]),
            energy=battery["energy"],
            energyUnit=battery["energy_unit"],
            cost=battery["cost"],
            costCurrency=battery["cost_currency"],
            releaseDate=battery["release_date"],
            weight=battery["weight"],
            weightUnit=battery["weight_unit"],
        )
        for battery in BATTERIES
    ]


@router.get("/transformer")
def get_data_transformer() -> Transformer:
    return Transformer(
        id=TRANSFORMER["id"],
        name=TRANSFORMER["name"],
        dimensions=Dimensions(**TRANSFORMER["dimensions"]),
        energy=TRANSFORMER["energy"],
        energyUnit=TRANSFORMER["energy_unit"],
        cost=TRANSFORMER["cost"],
        costCurrency=TRANSFORMER["cost_currency"],
        releaseDate=TRANSFORMER["release_date"],
        weight=TRANSFORMER["weight"],
        weightUnit=TRANSFORMER["weight_unit"],
    )
