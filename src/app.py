from gimme_embeds import GimmeEmbeds
import os
import logging
from dotenv import load_dotenv
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

load_dotenv()
ge = GimmeEmbeds()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

# Use variables derived from custom API methods.
updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


def main():
    start_handler = CommandHandler("start", ge.start)
    dispatcher.add_handler(start_handler)
    message_handler = MessageHandler(Filters.text, ge.text_handler)
    dispatcher.add_handler(message_handler)
    # Handler to stop the bot
    dispatcher.add_handler(
        CommandHandler("r", restart, filters=Filters.user(username="@CompassNeedle, @zzkW35"))
    )

    updater.start_polling()


if __name__ == "__main__":
    main()
