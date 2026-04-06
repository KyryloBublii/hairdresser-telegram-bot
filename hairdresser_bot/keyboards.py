from datetime import datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .config import SERVICES, WORKING_HOURS
from .storage import is_slot_taken


def services_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(label, callback_data=f"svc:{key}")]
        for key, label in SERVICES.items()
    ]
    buttons.append([InlineKeyboardButton("Cancel", callback_data="cancel")])
    return InlineKeyboardMarkup(buttons)


def dates_keyboard() -> InlineKeyboardMarkup:
    today = datetime.now()
    buttons = []
    for i in range(1, 8):
        day = today + timedelta(days=i)
        label = day.strftime("%a, %d %b")
        data = day.strftime("%Y-%m-%d")
        buttons.append([InlineKeyboardButton(label, callback_data=f"date:{data}")])
    buttons.append([InlineKeyboardButton("Cancel", callback_data="cancel")])
    return InlineKeyboardMarkup(buttons)


def times_keyboard(date: str) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for hour in WORKING_HOURS:
        time_str = f"{hour:02d}:00"
        if is_slot_taken(date, time_str):
            label = f"✖ {time_str}"
            data = "taken"
        else:
            label = time_str
            data = f"time:{time_str}"
        row.append(InlineKeyboardButton(label, callback_data=data))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("Cancel", callback_data="cancel")])
    return InlineKeyboardMarkup(buttons)


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Confirm", callback_data="confirm"),
            InlineKeyboardButton("Cancel", callback_data="cancel"),
        ]
    ])
