# ⚡ EV Charging Hub

A full-stack mock application for Electric Vehicle (EV) charging. This project simulates finding nearby charging stations, estimating charge times and costs, and tracking a live charging session in real-time. 

Built with a **FastAPI** backend (using an in-memory database and the Controller-Service-Repository pattern) and a lightning-fast **React + Vite** frontend.

## ✨ Features

- **📍 Station Finder:** Search for nearby EV chargers using mock geocoding (supports: *Bengaluru, Mysuru, Chennai*). Calculates distances using the Haversine formula.
- **🔋 Live Charging Simulator:** Start and stop mock charging sessions. The frontend polls the backend in real-time as the background task increments energy delivered (kWh) and deducts wallet balance.
- **🧮 EV Calculator:** Input battery capacity, target charge percentage, and station charge rates to instantly calculate estimated time and total cost.

## 🛠️ Tech Stack

**Frontend:**
- React (via Vite)
- Vanilla JavaScript
- Inline CSS for zero-dependency styling

**Backend:**
- Python 3.x
- FastAPI (REST API framework)
- Uvicorn (ASGI server)
- Pydantic (Data validation and schemas)



    
    <img width="1865" height="852" alt="Screenshot 2026-04-15 114219" src="https://github.com/user-attachments/assets/e946ef3c-231a-4394-8220-766013e59e1e" />
    <img width="1245" height="747" alt="Screenshot 2026-04-15 114236" src="https://github.com/user-attachments/assets/6ef095a4-7355-4408-8376-5ddca153cfbe" />
    <img width="1638" height="786" alt="Screenshot 2026-04-15 114257" src="https://github.com/user-attachments/assets/29569a95-e822-43e9-9e7c-ac61cb96786b" />


