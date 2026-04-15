from fastapi import APIRouter
from models.schemas import PlaceInput, CalculatorInput
from services.charger_service import ChargerService

router = APIRouter(prefix="/api/chargers", tags=["Chargers"])
charger_service = ChargerService()

@router.post("/nearby")
def get_nearby_stations(location: PlaceInput): # <-- Updated here
    return charger_service.find_nearby_stations(location.place_name) # <-- Updated here

@router.post("/calculate")
def calculate_estimates(calc_input: CalculatorInput):
    return charger_service.calculate_charging_estimates(calc_input)