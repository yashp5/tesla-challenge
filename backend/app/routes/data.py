from fastapi import APIRouter
from models import Battery, Transformer
from db import BATTERIES, TRANSFORMER

router = APIRouter()

@router.get("/batteries")
def getDataBatteries() -> list[Battery]:
    return [Battery(**battery) for battery in BATTERIES]


@router.get("/transformer")
def getDataTransformer() -> Transformer:
    return Transformer(**TRANSFORMER)
