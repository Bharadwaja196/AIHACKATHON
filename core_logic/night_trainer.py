import datetime
from memory_manager import MemoryManager
from journaling import Journal
from private_memory import PrivateMemoryVault
from feedback_learner import FeedbackLearner
from daily_summary import DailySummary
from llm.llm_with_lora import LoRATrainer
from utils.logger import logger

# Modular function that scheduler can call
def fine_tune_model(user_id, data=None, embeddings=None):
    logger.info(f"🌙 Night training started for {user_id}...")

    # Init trainers and tools
    memory = MemoryManager(user_id)
    journal = Journal(user_id)
    vault = PrivateMemoryVault(user_id)
    feedback = FeedbackLearner(user_id)
    summarizer = DailySummary(user_id)
    trainer = LoRATrainer(model_path="llm/11m", adapter_path="lora_adapters")

    if data is None:
        # Fallback to internal fetch if not provided
        memory_logs = memory.retrieve_all()
        private_entries = vault.retrieve_private_entries()
        feedback_entries = feedback.retrieve_all_feedback()

        combined_logs = memory_logs + private_entries

        high_quality = [
            {"input": e["user_input"], "output": e["soulmate_response"]}
            for e in feedback_entries
            if e.get("feedback_score", 0) == 1
        ]

        data = [
            {"input": e["user_input"], "output": e["soulmate_response"]}
            for e in combined_logs
            if e.get("user_input") and e.get("soulmate_response")
        ] + high_quality

    if not data:
        logger.warning(f"📭 No training data found for {user_id}, skipping...")
        return

    summary = summarizer.generate_summary()
    logger.info(f"🧠 Summary for {user_id}: {summary}")

    trainer.fine_tune(data, embeddings=embeddings)

    logger.info(f"✅ Soulmate for {user_id} has evolved overnight. 🌌🧠💖")

# CLI runner for manual mode
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("⚠️  Please provide user ID as a command-line argument.")
    else:
        fine_tune_model(sys.argv[1])
