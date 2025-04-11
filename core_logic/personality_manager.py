import datetime
from emotion_analyzer import analyze_emotion
from memory_manager import MemoryManager
from journaling import Journal
from some_llm_sdk import LLM
from personality_manager import PersonalityManager


class SoulmateAGI:
    def __init__(self, user_id):
        self.user_id = user_id
        self.memory = MemoryManager(user_id)
        self.journal = Journal(user_id)
        self.llm = LLM()
        self.personality_manager = PersonalityManager(user_id)
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

        # Step 3: Dynamic Persona Adjustment
        if emotion in ["sad", "angry", "anxious"]:
            self.set_mode("supportive")

        # Step 4: Prompt Construction
        prompt = self._construct_prompt(user_input, recent_context, emotion)

        # Step 5: LLM Response
        response = self.llm.generate(prompt)

        # Step 6: Memory & Journaling
        self.memory.store_interaction(user_input, response)
        self.journal.log_interaction(timestamp, user_input, response, emotion)

        return response

    def _construct_prompt(self, user_input, context, emotion):
        base_instruction = self.personality_manager.get_personality_instruction()
        system_prompt = f"{base_instruction}"
        if emotion:
            system_prompt += f" The user seems to be feeling {emotion}. Respond with appropriate empathy."

        context_text = "\n".join([
            f"User: {c['user']}\nSoulmate: {c['ai']}" for c in context
        ])

        full_prompt = f"{system_prompt}\nConversation history:\n{context_text}\nCurrent message:\nUser: {user_input}\nSoulmate:"
        return full_prompt


# Example usage:
# agi = SoulmateAGI(user_id="user123")
# response = agi.generate_response("I feel a bit down today...")
# print(response)
