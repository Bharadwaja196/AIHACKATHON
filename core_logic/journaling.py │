import os
import json
from private_memory import PrivateMemoryVault
from datetime import datetime

class Journal:
    def __init__(self, user_id, base_dir="memory/journals"):
        self.user_id = user_id
        self.journal_dir = os.path.join(base_dir, user_id)
        os.makedirs(self.journal_dir, exist_ok=True)
        self.vault = PrivateMemoryVault(user_id)

    def log_interaction(self, timestamp, user_input, response, emotion):
        # 🛡️ Store private emotional memory
        if emotion in ["sad", "lonely", "anxious", "depressed"]:
            self.vault.store_private_entry(timestamp, user_input, response, emotion)

        # 📖 Standard journaling
        entry = {
            "timestamp": timestamp.isoformat(),
            "user_input": user_input,
            "soulmate_response": response,
            "emotion": emotion
        }
        date_str = timestamp.strftime("%Y-%m-%d")
        file_path = os.path.join(self.journal_dir, f"{date_str}.json")

        # Load existing entries or start fresh
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(entry)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    def get_daily_summary(self, date=None):
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(self.journal_dir, f"{date}.json")

        if not os.path.exists(file_path):
            return "No journal entries found for today."

        with open(file_path, "r") as f:
            data = json.load(f)

        emotions = [entry["emotion"] for entry in data]
        most_common = max(set(emotions), key=emotions.count) if emotions else "neutral"

        return f"🧠 Daily Mood Summary: You mostly felt **{most_common}** today."

    def read_journal(self, date=None):
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(self.journal_dir, f"{date}.json")

        if not os.path.exists(file_path):
            return []

        with open(file_path, "r") as f:
            return json.load(f)
