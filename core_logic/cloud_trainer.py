import os
import json
from utils.logger import logger

class CloudTrainer:
    def __init__(self, user_id, cloud_dir="cloud_data"):
        self.user_id = user_id
        self.cloud_dir = os.path.join(cloud_dir, user_id)
        os.makedirs(self.cloud_dir, exist_ok=True)

    def upload_training_data(self, data):
        filepath = os.path.join(self.cloud_dir, "night_training_data.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"☁️ Uploaded training data for {self.user_id} to {filepath}")

    def fetch_training_data(self):
        filepath = os.path.join(self.cloud_dir, "night_training_data.json")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return json.load(f)
        return []
