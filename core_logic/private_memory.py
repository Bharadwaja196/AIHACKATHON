import os
import base64
import json
from cryptography.fernet import Fernet
from datetime import datetime


class PrivateMemoryVault:
    def __init__(self, user_id: str, vault_dir: str = "memory/vault"):
        self.user_id = user_id
        self.vault_dir = vault_dir
        os.makedirs(self.vault_dir, exist_ok=True)
        self.key_path = os.path.join(self.vault_dir, f"{self.user_id}_key.key")
        self.vault_path = os.path.join(self.vault_dir, f"{self.user_id}_vault.json")
        self.fernet = self._load_or_create_key()

    def _load_or_create_key(self) -> Fernet:
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
        return Fernet(key)

    def store_entry(self, entry: dict) -> None:
        """
        Stores a securely encrypted journal/memory entry.
        Entry should contain keys like: 'timestamp', 'emotion', 'content', etc.
        """
        entry.setdefault("timestamp", datetime.utcnow().isoformat())
        encrypted_entry = self.fernet.encrypt(json.dumps(entry).encode("utf-8"))

        if not os.path.exists(self.vault_path):
            with open(self.vault_path, "w") as f:
                json.dump([], f)

        with open(self.vault_path, "r") as f:
            entries = json.load(f)

        entries.append(base64.b64encode(encrypted_entry).decode("utf-8"))

        with open(self.vault_path, "w") as f:
            json.dump(entries, f, indent=2)

    def retrieve_entries(self) -> list:
        """
        Retrieves all securely stored entries for the user.
        Returns a list of decrypted dictionary entries.
        """
        if not os.path.exists(self.vault_path):
            return []

        with open(self.vault_path, "r") as f:
            encoded_entries = json.load(f)

        decrypted_entries = []
        for entry in encoded_entries:
            try:
                decrypted_data = self.fernet.decrypt(base64.b64decode(entry))
                decrypted_entries.append(json.loads(decrypted_data))
            except Exception as e:
                # Log or ignore corrupted entries
                continue

        return decrypted_entries
