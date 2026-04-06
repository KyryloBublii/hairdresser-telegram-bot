import json
import os
from datetime import datetime

from .config import APPOINTMENTS_FILE


def load_appointments() -> list:
    if os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE) as f:
            return json.load(f)
    return []


def save_appointments(appointments: list) -> None:
    with open(APPOINTMENTS_FILE, "w") as f:
        json.dump(appointments, f, indent=2)


def is_slot_taken(date: str, time: str) -> bool:
    return any(a["date"] == date and a["time"] == time for a in load_appointments())


def add_appointment(user_id: int, username: str, service: str, date: str, time: str) -> None:
    appointments = load_appointments()
    appointments.append(
        {
            "user_id": user_id,
            "username": username,
            "service": service,
            "date": date,
            "time": time,
            "booked_at": datetime.now().isoformat(),
        }
    )
    save_appointments(appointments)


def user_appointments(user_id: int) -> list:
    today = datetime.now().strftime("%Y-%m-%d")
    return [
        a
        for a in load_appointments()
        if a["user_id"] == user_id and a["date"] >= today
    ]


def cancel_appointment(user_id: int, date: str, time: str) -> bool:
    appointments = load_appointments()
    new_list = [
        a for a in appointments
        if not (a["user_id"] == user_id and a["date"] == date and a["time"] == time)
    ]
    if len(new_list) < len(appointments):
        save_appointments(new_list)
        return True
    return False
