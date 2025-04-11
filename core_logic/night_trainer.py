import os
from datetime import datetime
from memory_manager import MemoryManager
from private_memory import PrivateMemoryVault
from daily_summary import DailySummarizer
from llm.llm_with_lora import FineTuner  # Assuming you're using your LoRA-based fine-tuner

class NightTrainer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.memory_manager = MemoryManager(user_id)
        self.vault = PrivateMemoryVault(user_id)
        self.summarizer = DailySummarizer(user_id)
        self.trainer = FineTuner(user_id)  # your fine-tuner class using LoRA/PEFT

    def gather_training_data(self):
        print("[🌙] Gathering training data for nightly learning...")

        # Daily conversation logs & embeddings
        memory_logs = self.memory_manager.retrieve_recent_memories()

        # Private Vault entries (emotions, thoughts, sensitive moments)
        private_entries = self.vault.retrieve_private_entries()

        # Daily Summary (mood + thought patterns)
        summary_text = self.summarizer.get_summary_text()

        training_corpus = []

        # Add memory logs
        for log in memory_logs:
            training_corpus.append(f"[Memory] {log['user_input']} => {log['response']} (emotion: {log.get('emotion', 'neutral')})")

        # Add private entries
        for entry in private_entries:
            training_corpus.append(f"[Private] {entry['user_input']} => {entry['response']} (emotion: {entry.get('emotion', 'unknown')})")

        # Add summary if available
        if summary_text:
            training_corpus.append(f"[Summary] {summary_text}")

        return training_corpus

    def run_training_job(self):
        print(f"[🚀] Starting nightly training for user: {self.user_id}")
        training_data = self.gather_training_data()

        if not training_data:
            print("[⚠️] No data found for today. Skipping training.")
            return

        # Launch fine-tuning via LoRA or PEFT
        self.trainer.fine_tune(training_data)
        print(f"[✅] Nightly training complete for {self.user_id} at {datetime.now()}")


# Optional: Run when this file is executed directly
if __name__ == "__main__":
    user_id = "demo_user"
    trainer = NightTrainer(user_id)
    trainer.run_training_job()
