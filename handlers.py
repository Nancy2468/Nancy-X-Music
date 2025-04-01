from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from database import Database
import random

db = Database()

def start(update: Update, context: CallbackContext):
    chat_type = update.message.chat.type
    if chat_type == "private":
        update.message.reply_text("Welcome to the Music Bot! Use /help to see commands.")
    else:
        update.message.reply_text("Hello! Add me as admin to use music features!")

def help_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    admins = db.get_admins(chat_id)
    
    user_commands = """
    /play - Play music
    /stop - Stop music
    /resume - Resume music
    /skip - Skip current song
    /seek [seconds] - Seek in song
    /playlist or /pl - View playlist
    /downloadmp3 - Download MP3
    /downloadmp4 - Download MP4
    /Nancy - Ask the bot anything
    """
    
    admin_commands = """
    /addplaylist or /ap - Add playlist
    /removeplaylist or /rp - Remove playlist
    /addsong or /as - Add song to playlist
    /removesong or /rs - Remove song from playlist
    /queue - Manage queue
    """
    
    if user_id in admins:
        update.message.reply_text(f"Admin Commands:
{admin_commands}")
    else:
        update.message.reply_text(f"User Commands:
{user_commands}")

def playlist(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    playlists = db.get_all_playlists(chat_id)
    
    if not playlists:
        update.message.reply_text("No playlists found!")
        return
    
    keyboard = [[InlineKeyboardButton(name, callback_data=f"view_playlist_{name}")] for name in playlists]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose a playlist:", reply_markup=reply_markup)

def handle_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    data = query.data.split("_")
    action = data[0]
    
    if action == "view":
        playlist_name = data[2]
        chat_id = query.message.chat.id
        songs = db.get_playlist(chat_id, playlist_name)
        
        if not songs:
            query.message.reply_text("No songs in this playlist.")
            return
        
        song_buttons = [[InlineKeyboardButton(song, callback_data=f"play_{song}")] for song in songs]
        reply_markup = InlineKeyboardMarkup(song_buttons)
        query.message.reply_text(f"Songs in {playlist_name}:", reply_markup=reply_markup)

def add_playlist(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id

    # Check if user is admin
    if not db.is_admin(chat_id, user_id):
        update.message.reply_text("❌ Only admins can add playlists.")
        return
    
    # Get playlist name
    if not context.args:
        update.message.reply_text("⚠️ Please provide a playlist name. Usage: /addplaylist <playlist_name>")
        return
    
    playlist_name = " ".join(context.args).strip()

    # Add playlist to database
    try:
        db.add_playlist(chat_id, playlist_name)
        update.message.reply_text(f"✅ Playlist '{playlist_name}' added successfully!")
    except Exception as e:
        update.message.reply_text(f"⚠️ Error: {str(e)}")

def remove_playlist(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    if not db.is_admin(chat_id, user_id):
        update.message.reply_text("Only admins can remove playlists.")
        return
    
    playlists = db.get_all_playlists(chat_id)
    keyboard = [[InlineKeyboardButton(name, callback_data=f"remove_playlist_{name}")] for name in playlists]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Select a playlist to remove:", reply_markup=reply_markup)

def add_song(update: Update, context: CallbackContext):
    update.message.reply_text("Adding song to playlist...")

def remove_song(update: Update, context: CallbackContext):
    update.message.reply_text("Removing song from playlist...")

def play(update: Update, context: CallbackContext):
    update.message.reply_text("Playing music...")

def stop(update: Update, context: CallbackContext):
    update.message.reply_text("Music stopped.")

def resume(update: Update, context: CallbackContext):
    update.message.reply_text("Resuming music...")

def seek(update: Update, context: CallbackContext):
    args = context.args
    if args:
        update.message.reply_text(f"Seeking to {args[0]} seconds...")
    else:
        update.message.reply_text("Please provide a number of seconds.")

def skip(update: Update, context: CallbackContext):
    update.message.reply_text("Skipping song...")

def download_mp3(update: Update, context: CallbackContext):
    update.message.reply_text("Downloading MP3...")

def download_mp4(update: Update, context: CallbackContext):
    update.message.reply_text("Downloading MP4...")

def nancy(update: Update, context: CallbackContext):
    responses = ["I'm here! How can I help?", "What do you want to ask?", "Yes, tell me your question!"]
    update.message.reply_text(random.choice(responses))

def queue(update: Update, context: CallbackContext):
    update.message.reply_text("Managing queue...")

def get_songs_from_playlist(group_id, playlist_name):
    cursor.execute("SELECT song_name, song_url FROM songs WHERE playlist_id = (SELECT id FROM playlists WHERE group_id = ? AND name = ?)",
                   (group_id, playlist_name))
    return cursor.fetchall()

# Register handlers in bot.py
