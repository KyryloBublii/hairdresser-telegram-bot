import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
APPOINTMENTS_FILE = "appointments.json"

SERVICES = {
    "haircut": "Haircut — 45 min",
    "coloring": "Coloring — 2 h",
    "styling": "Styling — 30 min",
    "highlights": "Highlights — 2.5 h",
    "trim": "Trim & Blowout — 1 h",
}

WORKING_HOURS = list(range(9, 19))  # 9:00–18:00

# Conversation states
SELECT_SERVICE, SELECT_DATE, SELECT_TIME, CONFIRM = range(4)
