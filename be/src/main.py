import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from src.api import auth, site, user, shift, certification, staff

app = FastAPI(title="Workforce Scheduling API")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(site.router)
app.include_router(shift.router)
app.include_router(staff.router)
app.include_router(certification.router)

@app.get("/health")
def health():
    return {"status": "ok"}
