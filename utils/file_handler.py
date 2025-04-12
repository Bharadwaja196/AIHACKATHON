import os
import json

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_json(path, data):
    ensure_dir(os.path.dirname(path))
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return None
