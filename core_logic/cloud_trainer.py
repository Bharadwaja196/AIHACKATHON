import os
import json
from utils.logger import logger

class CloudTrainer:
    def __init__(self, user_id, cloud_dir="cloud_data"):
        self.user_id = user_id
        self.cloud_dir = os.path.join(cloud_dir, user_id)
        os.makedirs(self.cloud_dir, exist_ok=True)
        logger.info(f"CloudTrainer initialized for user {self.user_id}.")

    def upload_training_data(self, data):
        """
        Uploads training data to the cloud directory for a specific user.
        """
        try:
            filepath = os.path.join(self.cloud_dir, "night_training_data.json")
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"☁️ Uploaded training data for user {self.user_id} to {filepath}")
        except Exception as e:
            logger.error(f"Error uploading training data for user {self.user_id}: {e}")
            raise  # Reraise the exception after logging

    def fetch_training_data(self):
        """
        Fetches training data from the cloud directory for a specific user.
        Returns an empty list if no data is found.
        """
        try:
            filepath = os.path.join(self.cloud_dir, "night_training_data.json")
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    data = json.load(f)
                logger.info(f"☁️ Fetched training data for user {self.user_id} from {filepath}")
                return data
            else:
                logger.warning(f"No training data found for user {self.user_id}. Returning empty list.")
                return []
        except Exception as e:
            logger.error(f"Error fetching training data for user {self.user_id}: {e}")
            raise  # Reraise the exception after logging

    def store_embeddings(self, embeddings):
        """
        Store the embeddings for the user to the cloud directory.
        """
        try:
            embeddings_filepath = os.path.join(self.cloud_dir, "user_embeddings.json")
            with open(embeddings_filepath, "w") as f:
                json.dump(embeddings, f, indent=2)
            logger.info(f"☁️ Stored embeddings for user {self.user_id} to {embeddings_filepath}")
        except Exception as e:
            logger.error(f"Error storing embeddings for user {self.user_id}: {e}")
            raise  # Reraise the exception after logging

    def fetch_embeddings(self):
        """
        Fetch the embeddings stored for the user.
        """
        try:
            embeddings_filepath = os.path.join(self.cloud_dir, "user_embeddings.json")
            if os.path.exists(embeddings_filepath):
                with open(embeddings_filepath, "r") as f:
                    embeddings = json.load(f)
                logger.info(f"☁️ Fetched embeddings for user {self.user_id} from {embeddings_filepath}")
                return embeddings
            else:
                logger.warning(f"No embeddings found for user {self.user_id}. Returning empty list.")
                return []
        except Exception as e:
            logger.error(f"Error fetching embeddings for user {self.user_id}: {e}")
            raise  # Reraise the exception after logging
