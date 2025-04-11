import os
import json
from datetime import datetime
from collections import Counter

class DailyThoughtSummary:
    def __init__(self, user_id, journal_dir="memory/journals"):
        self.user_id = user_id
        self.journal_dir = os.path.join(journal_dir, user_id)

    def generate_summary(self, date=None):
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        journal_path = os.path.join(self.journal_dir, f"{date}.json")
        if not os.path.exists(journal_path):
            return "No journal data available to summarize."

        with open(journal_path, "r") as f:
            entries = json.load(f)

        if not entries:
            return "No entries recorded today."

        # Extract emotions
        emotions = [entry.get("emotion", "neutral") for entry in entries]
        most_common_emotion = Counter(emotions).most_common(1)[0][0]

        # Extract recurring thoughts
        thought_fragments = [entry["user_input"] for entry in entries if entry["user_input"]]
        thoughts = " ".join(thought_fragments).lower()

        common_keywords = [word for word in thoughts.split() if len(word) > 4]
        frequent_words = Counter(common_keywords).most_common(5)

        summary = f"🧠 **Daily Thought Summary** for {date}:\n"
        summary += f"- Dominant Emotion: **{most_common_emotion}**\n"
        if frequent_words:
            summary += "- Frequent topics: " + ", ".join([word for word, count in frequent_words]) + "\n"
        summary += "- You had " + str(len(entries)) + " key reflections today.\n"

        return summary

# Example usage:
# summarizer = DailyThoughtSummary(user_id="user123")
# print(summarizer.generate_summary())
