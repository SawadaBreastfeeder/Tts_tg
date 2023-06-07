import logging

from telegram import Update

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from gtts import gTTS

from io import BytesIO

# Set up logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Define your bot token

TOKEN = 'your_bot_token_here'

# Initialize the updater and dispatcher

updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

# Dictionary to store voice chat IDs and the corresponding text

vcs_text = {}

def start(update: Update, context: CallbackContext) -> None:

    """Handler for /start command."""

    update.message.reply_text('Welcome! Send me a message, and I will convert it into speech for the voice chat.')

def help_command(update: Update, context: CallbackContext) -> None:

    """Handler for /help command."""

    help_text = """

    Available commands:

    /start - Start the bot and display a welcome message.

    /help - Display this help message.

    /text <your_message> - Save your message for playback in the voice chat.

    /play - Play the saved message in the voice chat.

    """

    update.message.reply_text(help_text)

def text_to_speech(update: Update, context: CallbackContext) -> None:

    """Handler for text messages."""

    message = update.message

    chat_id = message.chat_id

    text = message.text

    # Save the text for the voice chat

    vcs_text[chat_id] = text

    message.reply_text('Your message has been saved. Use /play to play it in the voice chat.')

def play_text(update: Update, context: CallbackContext) -> None:

    """Handler for /play command to play the text in the voice chat."""

    chat_id = update.message.chat_id

    if chat_id in vcs_text:

        text = vcs_text[chat_id]

        # Generate speech from the text using gTTS

        speech = gTTS(text=text, lang='en')

        audio_file = BytesIO()

        speech.save(audio_file)

        audio_file.seek(0)

        # Send the audio file to the voice chat

        context.bot.send_voice(chat_id=chat_id, voice=audio_file)

    else:

        update.message.reply_text('No saved message found. Send me a message first using /text command.')

def main() -> None:

    """Main function to start the bot."""

    # Register handlers

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(CommandHandler("text", text_to_speech))

    dispatcher.add_handler(CommandHandler("play", play_text))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_to_speech))

    # Start the bot

    updater.start_polling()

    logger.info("Bot started.")

    updater.idle()

if __name__ == '__main__':

    main()

