from sqlmodel import Session, select
from app.models import Booking, BookingCreate, User, Desk


class BookingService:
    @staticmethod
    def create_booking(session: Session, booking_data: BookingCreate):
        user = session.get(User, booking_data.user_id)
        if not user:
            raise ValueError("User wurde nicht gefunden.")

        desk = session.get(Desk, booking_data.desk_id)
        if not desk:
            raise ValueError("Arbeitsplatz wurde nicht gefunden.")

        existing = session.exec(
            select(Booking).where(
                Booking.desk_id == booking_data.desk_id,
                Booking.booking_date == booking_data.booking_date
            )
        ).first()

        if existing:
            raise ValueError("Arbeitsplatz ist an diesem Datum bereits gebucht.")

        booking = Booking(
            user_id=booking_data.user_id,
            desk_id=booking_data.desk_id,
            booking_date=booking_data.booking_date
        )

        session.add(booking)
        session.commit()
        session.refresh(booking)
        return booking

    @staticmethod
    def delete_booking(session: Session, booking_id: int):
        booking = session.get(Booking, booking_id)
        if not booking:
            raise ValueError("Buchung wurde nicht gefunden.")

        session.delete(booking)
        session.commit()