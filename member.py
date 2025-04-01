from pyrogram import Client, filters
from pyrogram.types import Message

def is_admin(client, chat_id, user_id):
    """Check if a user is an admin in a group."""
    chat_member = client.get_chat_member(chat_id, user_id)
    return chat_member.status in ["administrator", "creator"]

@Client.on_message(filters.command("tagall") & filters.group)
def tag_all(client: Client, message: Message):
    """Tags all members in the group."""
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not is_admin(client, chat_id, user_id):
        message.reply_text("❌ Only admins can use this command.")
        return
    
    members = client.get_chat_members(chat_id)
    text = "👥 **Tagging all members:**\n"
    
    for member in members:
        if not member.user.is_bot:
            text += f"@{member.user.username} " if member.user.username else f"[{member.user.first_name}](tg://user?id={member.user.id}) "
    
    message.reply_text(text, disable_web_page_preview=True)

@Client.on_message(filters.command("welcome") & filters.group)
def welcome_message(client: Client, message: Message):
    """Sends a welcome message when a new user joins."""
    message.reply_text("👋 Welcome to the group! Have a great time here.")

@Client.on_message(filters.command("leave") & filters.group)
def leave_message(client: Client, message: Message):
    """Sends a leave message when a user leaves the group."""
    message.reply_text("😢 A user has left the group. We'll miss you!")
