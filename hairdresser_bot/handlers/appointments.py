from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from ..config import SERVICES
from ..storage import cancel_appointment, user_appointments


async def my_appointments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    appointments = user_appointments(user_id)

    if not appointments:
        await update.message.reply_text("You have no upcoming appointments.")
        return

    lines = ["*Your upcoming appointments:*\n"]
    for a in sorted(appointments, key=lambda x: (x["date"], x["time"])):
        display_date = datetime.strptime(a["date"], "%Y-%m-%d").strftime("%a, %d %b %Y")
        lines.append(f"• {display_date} at {a['time']} — {SERVICES[a['service']]}")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cancel_appointment_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    appointments = user_appointments(user_id)

    if not appointments:
        await update.message.reply_text("You have no upcoming appointments to cancel.")
        return

    buttons = []
    for a in sorted(appointments, key=lambda x: (x["date"], x["time"])):
        display_date = datetime.strptime(a["date"], "%Y-%m-%d").strftime("%a, %d %b")
        label = f"{display_date} {a['time']} — {SERVICES[a['service']]}"
        data = f"del:{a['date']}:{a['time']}"
        buttons.append([InlineKeyboardButton(label, callback_data=data)])

    buttons.append([InlineKeyboardButton("Back", callback_data="del:back")])
    await update.message.reply_text(
        "Select the appointment to cancel:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def handle_cancel_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "del:back":
        await query.edit_message_text("No changes made.")
        return

    _, date, time_str = query.data.split(":", 2)
    user_id = query.from_user.id

    if cancel_appointment(user_id, date, time_str):
        display_date = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %d %B %Y")
        await query.edit_message_text(
            f"Appointment on *{display_date}* at *{time_str}* has been cancelled.",
            parse_mode="Markdown",
        )
    else:
        await query.edit_message_text("Appointment not found.")
