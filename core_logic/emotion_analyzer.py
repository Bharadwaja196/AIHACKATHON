import torch
import json
import yaml
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

class EmotionAnalyzer:
    def __init__(self, config_path='emotion/config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.labels = self.config['labels']
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = AutoModelForSequenceClassification.from_pretrained("emotion/", local_files_only=True).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained("emotion/", use_fast=True)

    def analyze(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(self.device)
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = F.softmax(logits, dim=1).cpu().numpy()[0]
            top_idx = probs.argmax()
        return self.labels[top_idx], float(probs[top_idx])

# Global instance for use
emotion_model = EmotionAnalyzer()

def analyze_emotion(text):
    label, confidence = emotion_model.analyze(text)
    return label  # or return (label, confidence) if needed
