import datetime
from memory_manager import MemoryManager
from journaling import Journal
from private_memory import PrivateMemoryVault
from feedback_learner import FeedbackLearner
from daily_summary import DailySummary
from llm.llm_with_lora import LoRATrainer
from utils.logger import logger

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
        )

    def run_training_job(self):
        logger.info(f"🌙 Night training started for {self.user_id}...")

        memory_logs = self.memory.retrieve_all()
        private_entries = self.vault.retrieve_private_entries()
        feedback_entries = self.feedback.retrieve_all_feedback()
        combined_logs = memory_logs + private_entries

        high_quality = [
            {"input": e["user_input"], "output": e["soulmate_response"]}
            for e in feedback_entries
            if e.get("feedback_score", 0) == 1
        ]

        all_data = [
            {"input": e["user_input"], "output": e["soulmate_response"]}
            for e in combined_logs
            if e.get("user_input") and e.get("soulmate_response")
        ] + high_quality

        if not all_data:
            logger.warning("📭 No data to train on tonight.")
            return

        summary = self.summarizer.generate_summary()
        logger.info(f"🧠 {summary}")

        self.trainer.fine_tune(all_data)

        logger.success("✅ Soulmate has evolved overnight. 🌌🧠💖")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("⚠️  Please provide user ID as a command-line argument.")
    else:
        trainer = NightTrainer(sys.argv[1])
        trainer.run_training_job()
