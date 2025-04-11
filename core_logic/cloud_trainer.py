# core_logic/cloud_trainer.py

import os
import pickle
from datetime import datetime
from memory_manager import MemoryManager
from journaling import Journal
from emotion_analyzer import analyze_emotion
from llm_with_lora import LLMWithLoRA  # Assuming your LoRA loader is named like this
import torch

class CloudTrainer:
    def __init__(self, user_id, embeddings_path="embeddings/", save_dir="llm"):
        self.user_id = user_id
        self.memory = MemoryManager(user_id)
        self.journal = Journal(user_id)
        self.llm = LLMWithLoRA(base_model_dir=save_dir)
        self.embeddings_path = embeddings_path
        self.save_dir = save_dir

    def collect_training_data(self):
        print("🔍 Collecting memory and journaling data...")
        context = self.memory.get_all_interactions()
        journal_logs = self.journal.get_all_logs()

        training_data = []
        for entry in context:
            prompt = f"User: {entry['user']}\nSoulmate: {entry['ai']}"
            training_data.append((prompt, entry["ai"]))

        for log in journal_logs:
            emotion = analyze_emotion(log["user_input"])
            prompt = f"[Mood: {emotion}] {log['user_input']}"
            training_data.append((prompt, log["ai_response"]))

        return training_data

    def fine_tune_model(self, training_data):
        print(f"📡 Starting nightly fine-tuning for user {self.user_id}...")

        # NOTE: You should be using a proper Trainer like HuggingFace's for real fine-tuning.
        # This is just pseudo-logic
        self.llm.train(training_data)

        # Save the adapted model (usually LoRA adapter only)
        adapter_path = os.path.join(self.save_dir, "nightly_adapter.pt")
        torch.save(self.llm.get_adapter_state(), adapter_path)

        print(f"✅ Fine-tuning completed and saved to: {adapter_path}")

    def run_nightly_training(self):
        print(f"🌙 Nightly training started at {datetime.now().isoformat()}")
        training_data = self.collect_training_data()
        self.fine_tune_model(training_data)
        print(f"🌟 Soulmate upgraded for tomorrow ❤️")


# Example usage (manual trigger)
# trainer = CloudTrainer(user_id="user123")
# trainer.run_nightly_training()
