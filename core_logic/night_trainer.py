import datetime
from memory_manager import MemoryManager
from journaling import Journal
from private_memory import PrivateMemoryVault
from feedback_learner import FeedbackLearner
from daily_summary import DailySummary
from some_llm_sdk import LoRATrainer  # Replace with your actual fine-tuning SDK


class NightTrainer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.memory = MemoryManager(user_id)
        self.journal = Journal(user_id)
        self.vault = PrivateMemoryVault(user_id)
        self.feedback = FeedbackLearner(user_id)
        self.summarizer = DailySummary(user_id)
        self.trainer = LoRATrainer(
            model_path="llm/11m", adapter_path="lora_adapters"
        )  # Adjust these paths to your setup

    def run_training_job(self):
        print(f"🌙 Night training started for {self.user_id}...")

        # Step 1: Retrieve interaction logs
        memory_logs = self.memory.retrieve_all()
        private_entries = self.vault.retrieve_private_entries()
        feedback_entries = self.feedback.retrieve_all_feedback()

        # Step 2: Merge all for training
        combined_logs = memory_logs + private_entries

        # Optionally filter feedback-rated entries as higher quality
        high_quality = [
            {"input": e["user_input"], "output": e["soulmate_response"]}
            for e in feedback_entries
            if e.get("feedback_score", 0) == 1
        ]

        # Final data to train
        all_training_data = [
            {
                "input": entry["user_input"],
                "output": entry["soulmate_response"]
            }
            for entry in combined_logs
            if entry.get("user_input") and entry.get("soulmate_response")
        ] + high_quality

        if not all_training_data:
            print("📭 No data to train on tonight.")
            return

        # Step 3: Generate daily summary
        summary = self.summarizer.generate_summary()
        print(f"🧠 {summary}")

        # Step 4: Train using LoRA
        self.trainer.fine_tune(all_training_data)

        print("✅ Soulmate has evolved overnight. 🌌🧠💖")

# Example (Manual Run):
# trainer = NightTrainer("user123")
# trainer.run_training_job()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("⚠️  Please provide user ID as a command-line argument.")
    else:
        user_id = sys.argv[1]
        trainer = NightTrainer(user_id)
        trainer.run_training_job()
