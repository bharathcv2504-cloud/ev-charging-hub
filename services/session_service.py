import asyncio
from repository.in_memory_db import UserRepository, StationRepository, SessionRepository

class SessionService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.station_repo = StationRepository()
        self.session_repo = SessionRepository()

    def start_session(self, user_id: str, station_id: str):
        # Mark station as In Use
        self.station_repo.update_status(station_id, "In Use")
        return self.session_repo.create_session(user_id, station_id)

    def stop_session(self, session_id: str):
        session = self.session_repo.get_session(session_id)
        if session:
            self.session_repo.complete_session(session_id)
            self.station_repo.update_status(session.station_id, "Available")
        return session

    async def simulate_charging(self, session_id: str):
        """Background task to simulate charging over time"""
        session = self.session_repo.get_session(session_id)
        if not session:
            return

        station = next((s for s in self.station_repo.get_all_stations() if s.id == session.station_id), None)
        user = self.user_repo.get_user(session.user_id)

        if not station or not user:
            return

        # Simulate update every 2 seconds
        # Let's say in 2 seconds, we deliver a fraction of the kW rate
        # (rate per hour / 1800 for a 2-second interval)
        kwh_per_tick = station.charge_rate_kw / 1800 
        cost_per_tick = kwh_per_tick * station.cost_per_kwh

        while True:
            # Refresh session and user state
            current_session = self.session_repo.get_session(session_id)
            current_user = self.user_repo.get_user(session.user_id)

            if current_session.status != "ACTIVE":
                break

            if current_user.wallet_balance < cost_per_tick:
                self.session_repo.complete_session(session_id, "INSUFFICIENT_FUNDS")
                self.station_repo.update_status(station.id, "Available")
                break

            # Process transaction
            self.user_repo.update_balance(user.id, -cost_per_tick)
            self.session_repo.update_session(session_id, kwh_per_tick, cost_per_tick)
            
            await asyncio.sleep(2)