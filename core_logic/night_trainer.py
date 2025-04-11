import os
import pickle
from datetime import datetime
from journaling import Journal
from memory_manager import MemoryManager
from personality_manager import PersonalityManager


class NightTrainer:
    def __init__(self, user_id, output_dir="training_data"):
        self.user_id = user_id
        self.journal = Journal(user_id)
        self.memory = MemoryManager(user_id)
        self.personality = PersonalityManager(user_id)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def collect_training_data(self):
        today_str = datetime.now().strftime("%Y-%m-%d")
        logs = self.journal.get_logs_for_day(today_str)
        memory_data = self.memory.retrieve_global(limit=20)  # broader context

        training_samples = []

        for entry in logs:
            user_input = entry.get("user")
            ai_response = entry.get("ai")
            emotion = entry.get("emotion")
            tone_instruction = self.personality.get_personality_instruction()

            prompt = f"{tone_instruction}\nUser (feeling {emotion}): {user_input}\nSoulmate:"

            training_samples.append({
                "prompt": prompt,
                "response": ai_response,
                "emotion": emotion,
                "date": today_str
            })

        for memory in memory_data:
            training_samples.append({
                "prompt": memory["user"],
                "response": memory["ai"],
                "emotion": "contextual_memory",
                "date": memory.get("timestamp")
            })

        output_file = os.path.join(self.output_dir, f"{self.user_id}_daily_data.pkl")
        with open(output_file, "wb") as f:
            pickle.dump(training_samples, f)

        print(f"Collected {len(training_samples)} samples for training.")
        return output_file


# Example usage:
# trainer = NightTrainer(user_id="user123")
# data_path = trainer.collect_training_data()
