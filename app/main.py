from fastapi import FastAPI
from sqlmodel import Session, select
from app.database import create_db, engine
from app.routers import router
from app.models import Team

app = FastAPI(title="Workplace Booking App")


def seed_data():
    with Session(engine) as session:
        existing_team = session.exec(select(Team)).first()
        if not existing_team:
            team = Team(name="IT Team")
            session.add(team)
            session.commit()
            print("Seed-Daten erstellt!")


@app.on_event("startup")
def on_startup():
    create_db()
    seed_data()


app.include_router(router)