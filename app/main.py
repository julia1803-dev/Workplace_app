from fastapi import FastAPI
from app.database import create_db
from app.routers import router

app = FastAPI(title="Workplace Booking App")


@app.on_event("startup")
def on_startup():
    create_db()


app.include_router(router)