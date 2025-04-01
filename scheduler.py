import schedule
import time
from telegram import Bot
from config import load_config

# Load the configuration data
config_data = load_config()

# Example: Using the API key or any other config value for a scheduled task
api_key = config_data.get('api_key')

# Example of using the API key in a scheduled task
def scheduled_task():
    print(f"Running scheduled task with API Key: {api_key}")
    # Add your scheduled task logic here

class Scheduler:
    def __init__(self, bot_token):
        self.bot = Bot(token=bot_token)
        self.jobs = []
    
    def send_good_morning(self, chat_id):
        self.bot.send_message(chat_id, "Good morning, everyone! ☀️")
    
    def send_good_night(self, chat_id):
        self.bot.send_message(chat_id, "Good night, sleep well! 🌙")
    
    def schedule_messages(self, chat_id):
        job_morning = schedule.every().day.at("07:00").do(self.send_good_morning, chat_id=chat_id)
        job_night = schedule.every().day.at("22:00").do(self.send_good_night, chat_id=chat_id)
        self.jobs.append(job_morning)
        self.jobs.append(job_night)
    
    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(60)
