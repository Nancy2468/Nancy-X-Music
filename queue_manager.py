from collections import deque
from config import load_config

# Load the configuration data
config_data = load_config()

# Access the necessary configuration for the queue system (e.g., Redis URL)
queue_url = config_data.get('queue_url')

# Example usage: Connecting to a queue system
print(f"Connecting to queue system at: {queue_url}")

# Queue setup and operations here...

class QueueManager:
    def __init__(self):
        self.queues = {}  # Stores queues per group
    
    def add_to_queue(self, chat_id, song):
        if chat_id not in self.queues:
            self.queues[chat_id] = deque()
        self.queues[chat_id].append(song)
    
    def get_queue(self, chat_id):
        return list(self.queues.get(chat_id, []))
    
    def remove_from_queue(self, chat_id, index):
        if chat_id in self.queues and 0 <= index < len(self.queues[chat_id]):
            self.queues[chat_id].remove(self.queues[chat_id][index])
    
    def clear_queue(self, chat_id):
        if chat_id in self.queues:
            self.queues[chat_id].clear()
    
    def move_in_queue(self, chat_id, old_index, new_index):
        if chat_id in self.queues and 0 <= old_index < len(self.queues[chat_id]) and 0 <= new_index < len(self.queues[chat_id]):
            song = self.queues[chat_id].pop(old_index)
            self.queues[chat_id].insert(new_index, song)
