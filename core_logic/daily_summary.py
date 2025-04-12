import os
import json
from datetime import datetime
from collections import Counter
from intent_classifier import IntentClassifier
from emotion_analyzer import analyze_emotion

class DailySummary:
    def __init__(self, user_id, memory_dir="memory/interactions"):
        self.user_id = user_id
        self.memory_path = os.path.join(memory_dir, user_id)
        self.intent_classifier = IntentClassifier()

    def _load_today_entries(self):
        """Loads the user interactions for today from memory."""
        today_str = datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(self.memory_path, f"{today_str}.json")
        if not os.path.exists(filepath):
            return []
        with open(filepath, "r") as f:
            return json.load(f)

    def generate_summary(self):
        """Generates a daily summary of user interactions including emotions, intents, and topics."""
        entries = self._load_today_entries()
        if not entries:
            return "📭 No conversations logged today."

        emotions = []
        intents = []
        topics = []

        # Loop through each entry and extract emotions, intents, and topics
        for entry in entries:
            user_input = entry.get("user_input", "")
            emotion = analyze_emotion(user_input)
            intent = self.intent_classifier.classify_intent(user_input)

            emotions.append(emotion)
            intents.append(intent)

            # Check if the entry contains a topic (optional, depends on how topics are tracked)
            topic = entry.get("topic")
            if topic:
                topics.append(topic)

        # Summarize emotions, intents, and topics using Counter
        emotion_summary = Counter(emotions).most_common()
        intent_summary = Counter(intents).most_common()
        topic_summary = Counter(topics).most_common()

        # Construct the report string
        report = f"📝 **Daily Summary for {self.user_id}**\n\n"

        if emotion_summary:
            report += "💬 Emotions:\n"
            for emotion, count in emotion_summary:
                report += f" - {emotion}: {count} times\n"

        if intent_summary:
            report += "\n🎯 Intents:\n"
            for intent, count in intent_summary:
                report += f" - {intent}: {count} times\n"

        if topic_summary:
            report += "\n🧠 Topics (if tracked):\n"
            for topic, count in topic_summary:
                report += f" - {topic}: {count} times\n"

        return report.strip()

