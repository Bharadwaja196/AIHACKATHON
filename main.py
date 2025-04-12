# main.py

from chat_engine import ChatEngine
from journaling import JournalHandler
from emotion_analyzer import EmotionAnalyzer
from intent_classifier import IntentClassifier
from memory_manager import MemoryManager
from feedback_learner import FeedbackLearner
from personality_manager import PersonalityManager
from daily_summary import DailySummary
from cloud_trainer import CloudTrainer
from private_memory import PrivateMemory
from wellness_tools import WellnessTools
from loneliness_analyzer import LonelinessAnalyzer

import datetime

class SoulMateAGI:
    def __init__(self, user_id):
        self.user_id = user_id
        self.chat_engine = ChatEngine(user_id)
        self.journal = JournalHandler(user_id)
        self.emotion = EmotionAnalyzer()
        self.intent = IntentClassifier()
        self.memory = MemoryManager(user_id)
        self.feedback = FeedbackLearner(user_id)
        self.personality = PersonalityManager(user_id)
        self.summary = DailySummary(user_id)
        self.trainer = CloudTrainer(user_id)
        self.vault = PrivateMemory(user_id)
        self.wellness = WellnessTools()
        self.loneliness = LonelinessAnalyzer(user_id)

    def handle_user_input(self, input_text):
        emotion_state = self.emotion.analyze(input_text)
        user_intent = self.intent.classify(input_text)
        response = self.chat_engine.respond(input_text, emotion_state, user_intent)
        
        self.memory.store_conversation(input_text, response, emotion_state)
        self.personality.update_with_input(input_text)
        self.feedback.learn_from_response_quality(input_text, response)

        if self.loneliness.check_trigger(emotion_state):
            self.wellness.offer_grounding_technique()
        
        return response

    def summarize_day(self):
        return self.summary.generate()

    def nightly_training(self):
        self.trainer.run_nightly_update()

if __name__ == "__main__":
    user_id = "default_user"  # this can come from an auth layer later
    soulmate = SoulMateAGI(user_id)

    print("SoulMate.AGI is now running.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "bye"]:
            print("Goodnight! 🌙")
            soulmate.nightly_training()
            break

        response = soulmate.handle_user_input(user_input)
        print("SoulMate 💬:", response)
