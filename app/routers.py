from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import date
from app.database import engine
from app.models import BookingCreate, Team, Zone, Desk, Booking, User
from app.services import BookingService
import traceback

router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


# 🔹 CREATE BOOKING
@router.post("/bookings/")
def create_booking(booking: BookingCreate, session: Session = Depends(get_session)):
    try:
        return BookingService.create_booking(session, booking)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# 🔹 DELETE BOOKING
@router.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, session: Session = Depends(get_session)):
    try:
        BookingService.delete_booking(session, booking_id)
        return {"message": "Buchung gelöscht."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# 🔹 TEAMS
@router.get("/teams/")
def get_teams(session: Session = Depends(get_session)):
    return session.exec(select(Team)).all()


# 🔹 ZONES
@router.get("/zones/")
def get_zones(session: Session = Depends(get_session)):
    return session.exec(select(Zone)).all()


# 🔹 DESKS PER ZONE
@router.get("/desks/{zone_id}")
def get_desks(zone_id: int, session: Session = Depends(get_session)):
    return session.exec(
        select(Desk).where(Desk.zone_id == zone_id)
    ).all()


# 🔹 ZONE STATUS (gesamt)
@router.get("/zone-status/")
def get_zone_status(zone_id: int, booking_date: date, session: Session = Depends(get_session)):
    desks = session.exec(
        select(Desk).where(Desk.zone_id == zone_id)
    ).all()

    total_desks = len(desks)
    desk_ids = [desk.id for desk in desks]

    if not desk_ids:
        return {
            "zone_id": zone_id,
            "booking_date": booking_date,
            "total_desks": 0,
            "occupied_desks": 0,
            "free_desks": 0
        }

    bookings = session.exec(
        select(Booking).where(
            Booking.booking_date == booking_date,
            Booking.desk_id.in_(desk_ids)
        )
    ).all()

    occupied_desks = len(bookings)
    free_desks = total_desks - occupied_desks

    return {
        "zone_id": zone_id,
        "booking_date": booking_date,
        "total_desks": total_desks,
        "occupied_desks": occupied_desks,
        "free_desks": free_desks
    }


# 🔹 ZONE DETAIL (freie + besetzte desks)
@router.get("/zone-desks-status/")
def get_zone_desks_status(zone_id: int, booking_date: date, session: Session = Depends(get_session)):
    desks = session.exec(
        select(Desk).where(Desk.zone_id == zone_id)
    ).all()

    desk_ids = [desk.id for desk in desks]

    if not desk_ids:
        return {
            "zone_id": zone_id,
            "booking_date": booking_date,
            "free_desks": [],
            "occupied_desks": []
        }

    bookings = session.exec(
        select(Booking).where(
            Booking.booking_date == booking_date,
            Booking.desk_id.in_(desk_ids)
        )
    ).all()

    occupied_ids = {booking.desk_id for booking in bookings}

    free_desks = []
    occupied_desks = []

    for desk in desks:
        if desk.id in occupied_ids:
            occupied_desks.append({"id": desk.id, "code": desk.code})
        else:
            free_desks.append({"id": desk.id, "code": desk.code})

        return {
        "zone_id": zone_id,
        "booking_date": booking_date,
        "free_desks": free_desks,
        "occupied_desks": occupied_desks
    }


@router.get("/users/by-team/{team_id}")
def get_users_by_team(team_id: int, session: Session = Depends(get_session)):
    return session.exec(
        select(User).where(User.team_id == team_id)
    ).all()