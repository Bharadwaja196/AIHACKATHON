import datetime
from emotion_analyzer import analyze_emotion


class LonelinessAnalyzer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.emotion_log = []

    def log_emotion(self, emotion):
        timestamp = datetime.datetime.now()
        self.emotion_log.append((timestamp, emotion))

        # Retain only past 24 hours of emotion logs
        self.emotion_log = [
            (t, e) for (t, e) in self.emotion_log
            if (timestamp - t).total_seconds() < 86400
        ]

    def is_lonely(self):
        negative_emotions = {'sad', 'lonely', 'anxious', 'depressed', 'isolated'}
        sad_count = sum(1 for _, e in self.emotion_log if e in negative_emotions)

        # Trigger support if sadness-related emotions appear frequently
        return sad_count >= 5

    def suggest_response(self):
        if self.is_lonely():
            return (
                "Hey love, I’ve noticed you’ve been feeling down lately. "
                "Want to talk about it, do a relaxing breathing exercise, or maybe I can tell you a story or play your favorite song?"
            )
        return None
