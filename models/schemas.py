from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    id: str
    name: str
    wallet_balance: float

class Station(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    charge_rate_kw: float
    cost_per_kwh: float
    status: str  # "Available" or "In Use"

class ChargingSession(BaseModel):
    id: str
    user_id: str
    station_id: str
    kwh_delivered: float = 0.0
    cost_incurred: float = 0.0
    status: str  # "ACTIVE", "COMPLETED", "INSUFFICIENT_FUNDS"

# Replace LocationInput with this:
class PlaceInput(BaseModel):
    place_name: str

class StationDistance(Station):
    distance_km: float

class CalculatorInput(BaseModel):
    battery_capacity_kwh: float
    current_percentage: float
    target_percentage: float
    charge_rate_kw: float
    cost_per_kwh: float

class CalculatorOutput(BaseModel):
    estimated_time_hours: float
    total_cost: float
    kwh_required: float