import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from configparser import ConfigParser
import subprocess

# read config.ini file
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)

TOKEN = config['heroku_bot']['TOKEN']
LINK = config['heroku_bot']['LINK']

# set port number to listen in for the webhook
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi! I'm a Mask detective. Send me a picture and I will tell you who's wearing a mask!!")

def object_detection(update, context):
    cid = update.message.chat.id
    image_id = context.bot.get_file(update.message.photo[-1].file_id)
    context.bot.send_message(cid, f'Analyzing image...')
    image_id.download('darknet/image.jpg')
    cwd = os.getcwd()
    os.chdir(cwd + '/darknet')
    subprocess.run(['chmod', 'a+x', 'darknet'])
    subprocess.run(['./darknet', 'detect', 'yolo-obj.cfg', 'yolo-obj_best_v2.weights', 'image.jpg', '-dont-show'])
    os.chdir(cwd)
    context.bot.send_photo(cid, open('darknet/predictions.jpg','rb'))

# def help(update, context):
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help!')

# def echo(update, context):
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    
    dp.add_handler(MessageHandler(Filters.photo, object_detection))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(LINK + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()