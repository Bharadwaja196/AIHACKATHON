import os
import json
from datetime import datetime

class FeedbackLearner:
    def __init__(self, user_id, base_dir="memory/feedback"):
        self.user_id = user_id
        self.feedback_dir = os.path.join(base_dir, user_id)
        os.makedirs(self.feedback_dir, exist_ok=True)

    def log_feedback(self, user_input, response, feedback_score):
        """
        Stores feedback entry with a score:
        +1 for positive, 0 for neutral, -1 for negative
        """
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "user_input": user_input,
            "soulmate_response": response,
            "feedback_score": feedback_score
        }
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(self.feedback_dir, f"{date_str}.json")

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(entry)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    def retrieve_all_feedback(self):
        all_entries = []
        for file in os.listdir(self.feedback_dir):
            if file.endswith(".json"):
                with open(os.path.join(self.feedback_dir, file), "r") as f:
                    all_entries.extend(json.load(f))
        return all_entries

    def get_feedback_summary(self):
        entries = self.retrieve_all_feedback()
        if not entries:
            return "No feedback received yet."

        total = len(entries)
        positives = sum(1 for e in entries if e["feedback_score"] == 1)
        negatives = sum(1 for e in entries if e["feedback_score"] == -1)
        neutral = total - positives - negatives

        return f"👍 Positive: {positives} | 😐 Neutral: {neutral} | 👎 Negative: {negatives}"

# Example usage:
# fl = FeedbackLearner("user123")
# fl.log_feedback("I'm feeling weird", "Want to talk about it?", 1)
# print(fl.get_feedback_summary())
