import datetime
from memory_manager import MemoryManager
from journaling import Journal
from private_memory import PrivateMemoryVault
from daily_summary import DailySummary
from feedback_learner import FeedbackLearner
from some_llm_sdk import LoRATrainer  # Replace with your actual LoRA SDK

class NightTrainer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.memory = MemoryManager(user_id)
        self.journal = Journal(user_id)
        self.vault = PrivateMemoryVault(user_id)
        self.summary = DailySummary(user_id)
        self.feedback = FeedbackLearner(user_id)
        self.trainer = LoRATrainer(model_path="llm/11m", adapter_path="lora_adapters")

    def run_training_job(self):
        print(f"🌙 Night training started for {self.user_id}...")

        # Step 1: Collect memory logs from the day
        memory_logs = self.memory.retrieve_all()

        # Step 2: Collect private emotional entries
        private_entries = self.vault.retrieve_private_entries()

        # Step 3: Collect feedback learning examples
        feedback_examples = self.feedback.retrieve_feedback_samples()

        # Step 4: Merge all sources
        combined_logs = memory_logs + private_entries + feedback_examples

        if not combined_logs:
            print("📭 No data to train on tonight.")
            return

        # Step 5: Format into prompt-response pairs
        formatted_data = [
            {
                "input": entry["user_input"],
                "output": entry["soulmate_response"]
            }
            for entry in combined_logs
            if entry.get("user_input") and entry.get("soulmate_response")
        ]

        # Step 6: Perform LoRA fine-tuning
        self.trainer.fine_tune(formatted_data)

        # Step 7: Generate daily thought summary
        summary = self.journal.get_daily_summary()
        self.summary.save_summary(summary)

        print("✅ SoulMate has evolved with love, insight, and empathy tonight. 🌌💞")

# Example usage:
# trainer = NightTrainer("user123")
# trainer.run_training_job()
