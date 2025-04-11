import datetime
from memory_manager import MemoryManager
from journaling import Journal
from private_memory import PrivateMemoryVault
from some_llm_sdk import LoRATrainer  # Update if you have a specific LoRA SDK

class NightTrainer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.memory = MemoryManager(user_id)
        self.journal = Journal(user_id)
        self.vault = PrivateMemoryVault(user_id)
        self.trainer = LoRATrainer(model_path="llm/11m", adapter_path="lora_adapters")  # Adjust to your actual paths

    def run_training_job(self):
        print(f"🌙 Night training started for {self.user_id}...")

        # Step 1: Collect daytime memory logs
        memory_logs = self.memory.retrieve_all()

        # Step 2: Collect private emotional entries from the vault
        private_entries = self.vault.retrieve_private_entries()

        # Step 3: Merge both datasets
        combined_logs = memory_logs + private_entries

        if not combined_logs:
            print("📭 No data to train on tonight.")
            return

        # Step 4: Format for training (prompt-response pairs)
        formatted_data = [
            {
                "input": entry["user_input"],
                "output": entry["soulmate_response"]
            }
            for entry in combined_logs
            if entry.get("user_input") and entry.get("soulmate_response")
        ]

        # Step 5: Fine-tune with LoRA (or PEFT)
        self.trainer.fine_tune(formatted_data)

        print("✅ Soulmate has grown stronger tonight. 🌱💖")

# Example usage:
# trainer = NightTrainer("user123")
# trainer.run_training_job()
