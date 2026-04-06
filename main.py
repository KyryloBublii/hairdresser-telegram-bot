import logging

from telegram import BotCommand
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from hairdresser_bot.config import (
    BOT_TOKEN,
    CONFIRM,
    SELECT_DATE,
    SELECT_SERVICE,
    SELECT_TIME,
)
from hairdresser_bot.handlers.appointments import (
    cancel_appointment_cmd,
    handle_cancel_appointment,
    my_appointments,
)
from hairdresser_bot.handlers.booking import (
    book,
    cancel_conv,
    confirm,
    select_date,
    select_service,
    select_time,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    booking_conv = ConversationHandler(
        entry_points=[CommandHandler("book", book)],
        states={
            SELECT_SERVICE: [CallbackQueryHandler(select_service)],
            SELECT_DATE: [CallbackQueryHandler(select_date)],
            SELECT_TIME: [CallbackQueryHandler(select_time)],
            CONFIRM: [CallbackQueryHandler(confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conv)],
    )

    app.add_handler(booking_conv)
    app.add_handler(CommandHandler("my_appointments", my_appointments))
    app.add_handler(CommandHandler("cancel_appointment", cancel_appointment_cmd))
    app.add_handler(CallbackQueryHandler(handle_cancel_appointment, pattern=r"^del:"))

    app.bot_data["commands"] = [
        BotCommand("book", "Make an appointment"),
        BotCommand("my_appointments", "View your bookings"),
        BotCommand("cancel_appointment", "Cancel a booking"),
    ]

    async def set_commands(application: Application) -> None:
        await application.bot.set_my_commands(application.bot_data["commands"])

    app.post_init = set_commands

    logger.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
