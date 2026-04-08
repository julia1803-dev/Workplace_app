from sqlmodel import Session
from app.database import engine, create_db
from app.models import Team, User, Zone, Desk


def seed():
    create_db()

    with Session(engine) as session:

        # 🔹 TEAMS
        team_names = [
            "Eiger", "Gurten", "Titlis", "Matterhorn", "Mönch",
            "Weisshorn", "Dom", "Rothorn", "Niesen",
            "Niederhorn", "Pilatus", "Stockhorn", "Brisen"
        ]

        teams = []
        for name in team_names:
            team = Team(name=name)
            session.add(team)
            teams.append(team)

        session.commit()

        # 🔹 USERS (pro Team mehrere)
        for team in teams:
            for i in range(1, 4):  # 3 User pro Team
                user = User(name=f"{team.name}_User{i}", team_id=team.id)
                session.add(user)

        session.commit()

        # 🔹 ZONEN
        zone_names = [
            "Emme", "Aare", "Brinzersee", "Thunersee",
            "Rhein", "Rhone", "Saane", "Inn"
        ]

        zones = []
        for name in zone_names:
            zone = Zone(name=name)
            session.add(zone)
            zones.append(zone)

        session.commit()

        # 🔹 DESKS (WICHTIG 🔥 viele Arbeitsplätze)
        desk_counter = 1

        for zone in zones:
            for i in range(1, 21):  # 👉 20 Desks pro Zone
                desk = Desk(
                    code=f"{zone.name[:2].upper()}{i}",  # z.B. EM1, AA2
                    zone_id=zone.id
                )
                session.add(desk)
                desk_counter += 1

        session.commit()

        print("✅ Realistische Testdaten erstellt!")


if __name__ == "__main__":
    seed()