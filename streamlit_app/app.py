import streamlit as st
import requests
from datetime import date

API_URL = "https://workplace-app-aqsv.onrender.com"

st.set_page_config(page_title="Büro Anwesenheit", layout="wide")

st.title("🏢 Büro Anwesenheit und Arbeitsplatzbuchung")
st.write("Wähle Team, Mitarbeiter, Zone und Datum aus, prüfe die Verfügbarkeit und buche einen Arbeitsplatz.")


# -----------------------------
# Hilfsfunktionen
# -----------------------------
def load_teams():
    response = requests.get(f"{API_URL}/teams/")
    if response.status_code == 200:
        return response.json()
    return []


def load_users(team_id):
    response = requests.get(f"{API_URL}/users/by-team/{team_id}")
    if response.status_code == 200:
        return response.json()
    return []


def load_zones():
    response = requests.get(f"{API_URL}/zones/")
    if response.status_code == 200:
        return response.json()
    return []


def load_desks(zone_id):
    response = requests.get(f"{API_URL}/desks/{zone_id}")
    if response.status_code == 200:
        return response.json()
    return []


def load_zone_status(zone_id, booking_date):
    response = requests.get(
        f"{API_URL}/zone-status/",
        params={"zone_id": zone_id, "booking_date": str(booking_date)}
    )
    if response.status_code == 200:
        return response.json()
    return None


def load_zone_desks_status(zone_id, booking_date):
    response = requests.get(
        f"{API_URL}/zone-desks-status/",
        params={"zone_id": zone_id, "booking_date": str(booking_date)}
    )
    if response.status_code == 200:
        return response.json()
    return None


def create_booking(user_id, desk_id, booking_date):
    response = requests.post(
        f"{API_URL}/bookings/",
        json={
            "user_id": user_id,
            "desk_id": desk_id,
            "booking_date": str(booking_date)
        }
    )
    return response


# -----------------------------
# Daten laden
# -----------------------------
teams = load_teams()
zones = load_zones()

if not teams:
    st.error("Keine Teams gefunden. Bitte zuerst Seed-Daten laden.")
    st.stop()

if not zones:
    st.error("Keine Zonen gefunden. Bitte zuerst Seed-Daten laden.")
    st.stop()


# -----------------------------
# Auswahlbereich
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    team_names = [team["name"] for team in teams]
    selected_team_name = st.selectbox("Team", team_names)

selected_team = next(team for team in teams if team["name"] == selected_team_name)
team_id = selected_team["id"]

users = load_users(team_id)

if not users:
    st.error("Keine Benutzer für dieses Team gefunden.")
    st.stop()

with col2:
    user_names = [user["name"] for user in users]
    selected_user_name = st.selectbox("Mitarbeiter", user_names)

with col3:
    selected_date = st.date_input("Datum", value=date.today())

selected_user = next(user for user in users if user["name"] == selected_user_name)
user_id = selected_user["id"]


# -----------------------------
# Zone separat auswählen
# -----------------------------
selected_zone_name = st.selectbox("Zone", [zone["name"] for zone in zones])
selected_zone = next(zone for zone in zones if zone["name"] == selected_zone_name)
zone_id = selected_zone["id"]


# -----------------------------
# Status laden
# -----------------------------
status_data = load_zone_status(zone_id, selected_date)
details_data = load_zone_desks_status(zone_id, selected_date)
desks = load_desks(zone_id)

if status_data:
    st.subheader("📊 Belegung der Zone")

    c1, c2, c3 = st.columns(3)
    c1.metric("Gesamtplätze", status_data["total_desks"])
    c2.metric("Besetzt", status_data["occupied_desks"])
    c3.metric("Frei", status_data["free_desks"])

if details_data:
    col_free, col_occupied = st.columns(2)

    with col_free:
        st.subheader("✅ Freie Arbeitsplätze")
        if details_data["free_desks"]:
            free_codes = [desk["code"] for desk in details_data["free_desks"]]
            st.write(", ".join(free_codes))
        else:
            st.warning("Keine freien Arbeitsplätze")

    with col_occupied:
        st.subheader("❌ Besetzte Arbeitsplätze")
        if details_data["occupied_desks"]:
            occupied_codes = [desk["code"] for desk in details_data["occupied_desks"]]
            st.write(", ".join(occupied_codes))
        else:
            st.info("Keine besetzten Arbeitsplätze")


# -----------------------------
# Nur freie Desks zur Buchung anbieten
# -----------------------------
free_desk_options = []
if details_data:
    free_desk_options = details_data["free_desks"]

st.subheader("🪑 Arbeitsplatz buchen")

if free_desk_options:
    free_desk_map = {desk["code"]: desk["id"] for desk in free_desk_options}
    selected_desk_code = st.selectbox("Freien Arbeitsplatz auswählen", list(free_desk_map.keys()))
    selected_desk_id = free_desk_map[selected_desk_code]

    if st.button("Buchen"):
        response = create_booking(user_id, selected_desk_id, selected_date)

        if response.status_code == 200:
            st.success("Buchung erfolgreich!")
            st.json(response.json())
        else:
            try:
                st.error(response.json().get("detail", "Fehler bei der Buchung"))
            except Exception:
                st.error("Fehler bei der Buchung")
else:
    st.warning("Für diese Zone sind an diesem Datum keine freien Arbeitsplätze verfügbar.")