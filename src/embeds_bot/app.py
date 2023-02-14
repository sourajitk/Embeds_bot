""" Main application file. """
import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from embeds_bot.gimme_embeds import GimmeEmbeds

load_dotenv()
ge = GimmeEmbeds()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

# Use variables derived from custom API methods.
updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


def main():
    """Setup and run the bot."""
    # Handle the /start command.
    start_handler = CommandHandler("start", ge.start)
    dispatcher.add_handler(start_handler)
    # Handle the /source command.
    source_handler = CommandHandler("source", ge.source)
    dispatcher.add_handler(source_handler)
    # Main handler for links and hyperlinks.
    message_handler = MessageHandler(
        (Filters.entity("url") | Filters.entity("text_link")), ge.text_handler
    )
    dispatcher.add_handler(message_handler)
    # Handler to stop the bot
    dispatcher.add_handler(CommandHandler("r", ge.restart))

    # Handler to filter and embed a website
    dispatcher.add_handler(CommandHandler("embed", ge.filter_website))

    updater.start_polling()


if __name__ == "__main__":
    main()
