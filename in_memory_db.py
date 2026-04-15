from models.schemas import User, Station, ChargingSession
import uuid

# --- In-Memory State ---
users_db = {
    "u1": User(id="u1", name="Alice", wallet_balance=50.0)
}

stations_db = {
    "s1": Station(id="s1", name="Downtown Fast Charger", lat=12.9716, lng=77.5946, charge_rate_kw=50.0, cost_per_kwh=0.50, status="Available"),
    "s2": Station(id="s2", name="Tech Park Charger", lat=12.9850, lng=77.6050, charge_rate_kw=22.0, cost_per_kwh=0.30, status="Available"),
    "s3": Station(id="s3", name="Mall Slow Charger", lat=12.9352, lng=77.6245, charge_rate_kw=7.4, cost_per_kwh=0.15, status="In Use"),
}

sessions_db = {}

# --- Repository Classes ---
class UserRepository:
    def get_user(self, user_id: str):
        return users_db.get(user_id)

    def update_balance(self, user_id: str, amount: float):
        if user_id in users_db:
            users_db[user_id].wallet_balance += amount

class StationRepository:
    def get_all_stations(self):
        return list(stations_db.values())

    def update_status(self, station_id: str, status: str):
        if station_id in stations_db:
            stations_db[station_id].status = status

class SessionRepository:
    def create_session(self, user_id: str, station_id: str) -> ChargingSession:
        session_id = str(uuid.uuid4())
        session = ChargingSession(id=session_id, user_id=user_id, station_id=station_id, status="ACTIVE")
        sessions_db[session_id] = session
        return session

    def get_session(self, session_id: str):
        return sessions_db.get(session_id)

    def update_session(self, session_id: str, kwh_added: float, cost_added: float):
        if session_id in sessions_db:
            sessions_db[session_id].kwh_delivered += kwh_added
            sessions_db[session_id].cost_incurred += cost_added

    def complete_session(self, session_id: str, status: str = "COMPLETED"):
        if session_id in sessions_db:
            sessions_db[session_id].status = status