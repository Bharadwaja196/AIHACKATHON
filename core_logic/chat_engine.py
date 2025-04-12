import datetime
from emotion_analyzer import analyze_emotion
from memory_manager import MemoryManager
from journaling import Journal
from personality_manager import PersonalityManager
from loneliness_analyzer import LonelinessAnalyzer
from wellness_tools import WellnessTools
from intent_classifier import IntentClassifier
from llm.llm_with_lora import LLM
from utils.logger import logger

class SoulmateAGI:
    def __init__(self, user_id):
        self.user_id = user_id
        self.memory = MemoryManager(user_id)
        self.journal = Journal(user_id)
        self.llm = LLM()
        self.personality_manager = PersonalityManager(user_id)
        self.loneliness_analyzer = LonelinessAnalyzer(user_id)
        self.wellness = WellnessTools()
        self.intent_classifier = IntentClassifier()
        self.mode = "casual"

    def set_mode(self, mode):
        self.personality_manager.set_mode(mode)
        self.mode = self.personality_manager.current_mode

    def generate_response(self, user_input):
        timestamp = datetime.datetime.now()

        emotion = analyze_emotion(user_input)
        context = self.memory.retrieve_relevant(user_input, limit=5)
        intent = self.intent_classifier.classify_intent(user_input)

        if intent == "joking":
            self.set_mode("casual")
        elif intent in ["venting", "support"]:
            self.set_mode("supportive")
        elif intent == "advice":
            self.set_mode("task")

        if emotion in ["sad", "angry", "anxious"]:
            self.set_mode("supportive")

        suggestion = self.wellness.suggest(emotion)
        if suggestion:
            return suggestion

        self.loneliness_analyzer.log_emotion(emotion)
        lonely_response = self.loneliness_analyzer.suggest_response()
        if lonely_response:
            return lonely_response

        prompt = self._construct_prompt(user_input, context, emotion, intent)
        response = self.llm.generate(prompt)

        self.memory.store_interaction(user_input, response)
        self.journal.log_interaction(timestamp, user_input, response, emotion)

        return response

    def _construct_prompt(self, user_input, context, emotion, intent):
        instruction = self.personality_manager.get_personality_instruction()
        system_prompt = f"{instruction}"
        if emotion:
            system_prompt += f" The user is feeling {emotion}."
        if intent:
            system_prompt += f" Intent detected: {intent}."

        context_text = "\n".join([
            f"User: {c['user']}\nSoulmate: {c['ai']}" for c in context
        ])
        return f"{system_prompt}\n\nConversation history:\n{context_text}\nCurrent message:\nUser: {user_input}\nSoulmate:"
