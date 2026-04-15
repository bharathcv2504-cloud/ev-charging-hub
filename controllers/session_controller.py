from fastapi import APIRouter, BackgroundTasks, HTTPException
from services.session_service import SessionService
from repository.in_memory_db import sessions_db

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])
session_service = SessionService()

@router.post("/start")
async def start_charging(user_id: str, station_id: str, background_tasks: BackgroundTasks):
    session = session_service.start_session(user_id, station_id)
    # Trigger background async task
    background_tasks.add_task(session_service.simulate_charging, session.id)
    return {"message": "Charging started", "session": session}

@router.post("/stop/{session_id}")
def stop_charging(session_id: str):
    session = session_service.stop_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Charging stopped", "session": session}

@router.get("/{session_id}")
def get_session_status(session_id: str):
    session = sessions_db.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session