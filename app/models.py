from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Zone(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Desk(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str
    zone_id: Optional[int] = Field(default=None, foreign_key="zone.id")


class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    desk_id: int = Field(foreign_key="desk.id")
    booking_date: date


class BookingCreate(SQLModel):
    user_id: int
    desk_id: int
    booking_date: date