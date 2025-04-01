import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

from handlers import play, stop, resume, seek, skip, view_playlist, add_playlist, remove_playlist, add_song, remove_song, view_queue, ask_chatgpt, help_command
from queue_manager import add_to_queue, remove_from_queue, view_queue, rearrange_queue, clear_queue

from database import init_db, add_playlist_db, remove_playlist_db, add_song_db, remove_song_db, get_playlist_songs, get_all_playlists
from members import handle_new_members, handle_member_leave  # Join/leave messages
from schedulers import schedule_messages  # Auto Good Morning/Night messages
from config import TOKEN  # Bot token from config file
from config import load_config
from member import is_admin, tag_all, welcome_message, leave_message
from pyrogram import Client
from handlers import new_chat_member, left_chat_member

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the configuration data
config_data = load_config()

# Access the necessary values
api_key = config_data.get('api_key')

# Now use this API key where needed in your bot logic
print(f"Bot is using API Key: {api_key}")

# Example of how you might use the api_key in your bot:
# bot = YourBotLibrary(api_key=api_key)

def start(update: Update, context: CallbackContext):
    """Handles /start command differently in DM and group."""
    if update.message.chat.type == 'private':
        update.message.reply_text("👋 Hi! I am Nancy’s Music Bot. Use /help to see my features.")
    else:
        update.message.reply_text("🎶 Ready to play music! Use /play to start.")

def error(update: Update, context: CallbackContext):
    """Logs errors."""
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    """Starts the bot and initializes handlers."""
    init_db()  # Initialize the database
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Core Commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("play", play))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("resume", resume))
    dp.add_handler(CommandHandler("seek", seek))
    dp.add_handler(CommandHandler("skip", skip))
    dp.add_handler(CommandHandler("playlist", view_playlist))
    dp.add_handler(CommandHandler("pl", view_playlist))
    dp.add_handler(CommandHandler("downloadmp3", ask_download_preference))
    dp.add_handler(CommandHandler("downloadmp4", ask_download_preference))
    dp.add_handler(CommandHandler("nancy", ask_chatgpt))
    
    # Admin Commands
    dp.add_handler(CommandHandler("addplaylist", add_playlist))
    dp.add_handler(CommandHandler("ap", add_playlist))
    dp.add_handler(CommandHandler("removeplaylist", remove_playlist))
    dp.add_handler(CommandHandler("rp", remove_playlist))
    dp.add_handler(CommandHandler("addsong", add_song))
    dp.add_handler(CommandHandler("as", add_song))
    dp.add_handler(CommandHandler("removesongs", remove_song))
    dp.add_handler(CommandHandler("rs", remove_song))
    dp.add_handler(CommandHandler("queue", view_queue))
    
    # Callback Query Handlers
    dp.add_handler(CallbackQueryHandler(handle_download_choice))
    dp.add_handler(CallbackQueryHandler(handle_playlist_action))
    
    # Message Handlers
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, handle_new_members))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, handle_member_leave))
    
    # Error Handling
    dp.add_error_handler(error)
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_chat_member))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, left_chat_member))

    # Schedule automatic messages
    schedule_messages(updater)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


This is the bot.py file, which is the main entry point for your Telegram bot. It:
✔ Starts the bot and loads handlers
✔ Manages all user & admin commands
✔ Handles queue, playlists, and downloads
✔ Schedules Good Morning/Night messages
✔ Handles errors and logs issues

Next, I'll send the queue_manager.py file! 🚀

