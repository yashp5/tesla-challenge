from pydantic import BaseModel
from typing import Dict, List, Union


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
    color: str


class Transformer(BaseModel):
    id: int
    name: str
    dimensions: Dimensions
    energy: float
    energyUnit: str
    cost: int
    costCurrency: str
    releaseDate: str
    color: str


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
