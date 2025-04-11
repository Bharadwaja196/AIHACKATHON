import datetime
from emotion_analyzer import analyze_emotion
from memory_manager import MemoryManager
from journaling import Journal
from personality_manager import PersonalityManager
from loneliness_analyzer import LonelinessAnalyzer
from wellness_tools import WellnessTools
from some_llm_sdk import LLM  # Replace with your actual LLM interface

class SoulmateAGI:
    def __init__(self, user_id):
        self.user_id = user_id
        self.memory = MemoryManager(user_id)
        self.journal = Journal(user_id)
        self.llm = LLM()
        self.personality_manager = PersonalityManager(user_id)
        self.loneliness_analyzer = LonelinessAnalyzer(user_id)
        self.wellness = WellnessTools()
        self.mode = "casual"  # Modes: casual, task, reflective, supportive

    def set_mode(self, mode):
        self.personality_manager.set_mode(mode)
        self.mode = self.personality_manager.current_mode

    def generate_response(self, user_input):
        timestamp = datetime.datetime.now()

        # Step 1: Emotion Analysis
        emotion = analyze_emotion(user_input)

        # Step 2: Memory Recall
        recent_context = self.memory.retrieve_relevant(user_input, limit=5)

        # Step 3: Adjust Personality Mode
        if emotion in ["sad", "angry", "anxious", "lonely", "depressed"]:
            self.set_mode("supportive")

        # Step 4: Check Wellness Tools
        wellness_suggestion = self.wellness.suggest(emotion)
        if wellness_suggestion:
            self.journal.log_entry(timestamp, user_input, wellness_suggestion, emotion)
            return wellness_suggestion

        # Step 5: Check Loneliness Analyzer
        self.loneliness_analyzer.log_emotion(emotion)
        lonely_response = self.loneliness_analyzer.suggest_response()
        if lonely_response:
            self.journal.log_entry(timestamp, user_input, lonely_response, emotion)
            return lonely_response

        # Step 6: Construct prompt
        prompt = self._construct_prompt(user_input, recent_context, emotion)

        # Step 7: LLM response
        response = self.llm.generate(prompt)

        # Step 8: Store interaction
        self.memory.store_interaction(user_input, response)
        self.journal.log_entry(timestamp, user_input, response, emotion)

        return response

    def _construct_prompt(self, user_input, context, emotion):
        base_instruction = self.personality_manager.get_personality_instruction()
        system_prompt = f"{base_instruction}"
        if emotion:
            system_prompt += f" The user seems to be feeling {emotion}. Respond with empathy and emotional awareness."

        context_text = "\n".join([
            f"User: {c['user']}\nSoulmate: {c['ai']}" for c in context
        ])

        full_prompt = (
            f"{system_prompt}\n\n"
            f"Conversation history:\n{context_text}\n"
            f"Current message:\nUser: {user_input}\nSoulmate:"
        )
        return full_prompt
