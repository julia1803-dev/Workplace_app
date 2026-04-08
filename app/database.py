from pathlib import Path
from sqlmodel import SQLModel, create_engine
from app import models

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)


def create_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
    print(f"Datenbank erstellt unter: {DATABASE_PATH}")