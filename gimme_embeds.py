from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
import config # Contains our API key.

# Use variables derived from custom API methods.
updater = Updater(token=config.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def text_handler(update, context):
    """
    The primary handler that does all the replacement action through
    the API.
    """
    # Declare our list of to-be-replaced and new URLs.
    list_of_urls = ["https://twitter.com/", "https://www.tiktok.com/"]
    list_of_new_urls = ["https://vxtwitter.com/", "https://www.vxtiktok.com/"]

    # Use variables derived from custom API methods.
    message = update.message.text
    reply = update.message.reply_text

    # Setup conditionals for TikTok and Twitter.
    # For Twitter
    if message.startswith(list_of_urls[0]):
        url_id_0 = message.split(list_of_urls[0])
        reply(list_of_new_urls[0]+url_id_0[1])
    
    # For TikTok
    elif message.startswith(list_of_urls[1]):
        url_id_1 = message.split(list_of_urls[1])
        reply(list_of_new_urls[1]+url_id_1[1])

message_handler = MessageHandler(Filters.text, text_handler)
dispatcher.add_handler(message_handler)
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

updater.start_polling()
