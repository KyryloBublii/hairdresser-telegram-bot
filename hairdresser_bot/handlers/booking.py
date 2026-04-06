from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from ..config import CONFIRM, SELECT_DATE, SELECT_SERVICE, SELECT_TIME, SERVICES
from ..keyboards import confirm_keyboard, dates_keyboard, services_keyboard, times_keyboard
from ..storage import add_appointment, is_slot_taken


async def book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Choose a service:", reply_markup=services_keyboard()
    )
    return SELECT_SERVICE


async def select_service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "cancel":
        await query.edit_message_text("Booking cancelled.")
        return ConversationHandler.END

    service_key = query.data.split(":", 1)[1]
    context.user_data["service"] = service_key

    await query.edit_message_text(
        f"Service: *{SERVICES[service_key]}*\n\nChoose a date:",
        parse_mode="Markdown",
        reply_markup=dates_keyboard(),
    )
    return SELECT_DATE


async def select_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "cancel":
        await query.edit_message_text("Booking cancelled.")
        return ConversationHandler.END

    date = query.data.split(":", 1)[1]
    context.user_data["date"] = date
    display_date = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %d %B %Y")

    await query.edit_message_text(
        f"Date: *{display_date}*\n\nChoose a time (✖ = already booked):",
        parse_mode="Markdown",
        reply_markup=times_keyboard(date),
    )
    return SELECT_TIME


async def select_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "cancel":
        await query.edit_message_text("Booking cancelled.")
        return ConversationHandler.END

    if query.data == "taken":
        await query.answer("That slot is already taken. Pick another time.", show_alert=True)
        return SELECT_TIME

    time_str = query.data.split(":", 1)[1]
    context.user_data["time"] = time_str

    service = SERVICES[context.user_data["service"]]
    date = datetime.strptime(context.user_data["date"], "%Y-%m-%d").strftime("%A, %d %B %Y")

    await query.edit_message_text(
        f"*Booking summary*\n\n"
        f"Service: {service}\n"
        f"Date: {date}\n"
        f"Time: {time_str}\n\n"
        f"Confirm your appointment?",
        parse_mode="Markdown",
        reply_markup=confirm_keyboard(),
    )
    return CONFIRM


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "cancel":
        await query.edit_message_text("Booking cancelled.")
        return ConversationHandler.END

    user = query.from_user
    service_key = context.user_data["service"]
    date = context.user_data["date"]
    time_str = context.user_data["time"]

    if is_slot_taken(date, time_str):
        await query.edit_message_text(
            "Sorry, this slot was just taken. Please /book again."
        )
        return ConversationHandler.END

    add_appointment(user.id, user.username or user.first_name, service_key, date, time_str)

    display_date = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %d %B %Y")
    await query.edit_message_text(
        f"*Appointment confirmed!*\n\n"
        f"Service: {SERVICES[service_key]}\n"
        f"Date: {display_date}\n"
        f"Time: {time_str}\n\n"
        f"We'll see you then! Use /cancel\\_appointment to cancel if needed.",
        parse_mode="Markdown",
    )
    return ConversationHandler.END


async def cancel_conv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        await update.message.reply_text("Booking cancelled.")
    return ConversationHandler.END
