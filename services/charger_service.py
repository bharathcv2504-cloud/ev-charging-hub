import math
from models.schemas import CalculatorInput, CalculatorOutput
from repository.in_memory_db import StationRepository

# Mock Geocoder to translate names to coordinates
MOCK_GEOCODING = {
    "bengaluru": {"lat": 12.9716, "lng": 77.5946},
    "mysuru": {"lat": 12.2958, "lng": 76.6394},
    "chennai": {"lat": 13.0827, "lng": 80.2707},
}

class ChargerService:
    def __init__(self):
        self.station_repo = StationRepository()

    def _haversine(self, lat1, lon1, lat2, lon2):
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    # Updated method to accept place_name
    def find_nearby_stations(self, place_name: str):
        # Default to Bengaluru if the place isn't in our mock dictionary
        coords = MOCK_GEOCODING.get(place_name.lower().strip(), MOCK_GEOCODING["bengaluru"])
        
        stations = self.station_repo.get_all_stations()
        nearby = []
        for station in stations:
            dist = self._haversine(coords["lat"], coords["lng"], station.lat, station.lng)
            station_dict = station.model_dump()
            station_dict['distance_km'] = round(dist, 2)
            nearby.append(station_dict)
        
        return sorted(nearby, key=lambda x: x['distance_km'])

    # ... keep your existing calculate_charging_estimates method below ...
    def calculate_charging_estimates(self, calc_input: CalculatorInput) -> CalculatorOutput:
        percentage_needed = calc_input.target_percentage - calc_input.current_percentage
        if percentage_needed <= 0:
            return CalculatorOutput(estimated_time_hours=0, total_cost=0, kwh_required=0)

        kwh_required = (percentage_needed / 100) * calc_input.battery_capacity_kwh
        estimated_time = kwh_required / calc_input.charge_rate_kw
        total_cost = kwh_required * calc_input.cost_per_kwh

        return CalculatorOutput(
            estimated_time_hours=round(estimated_time, 2),
            total_cost=round(total_cost, 2),
            kwh_required=round(kwh_required, 2)
        )