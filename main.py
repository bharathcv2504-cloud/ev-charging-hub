from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import charger_controller, session_controller

app = FastAPI(title="EV Charging API Mock")

# --- UPDATED CORS TO FIX 405 ERRORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------

app.include_router(charger_controller.router)
app.include_router(session_controller.router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "EV Charging Backend is running"}