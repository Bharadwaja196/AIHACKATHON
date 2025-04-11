import datetime
from emotion_analyzer import analyze_emotion
from memory_manager import MemoryManager
from journaling import Journal
from some_llm_sdk import LLM


class SoulmateAGI:
    def __init__(self, user_id):
        self.user_id = user_id
        self.memory = MemoryManager(user_id)
        self.journal = Journal(user_id)
        self.llm = LLM()
        self.mode = "casual"  # Modes: casual, task, reflective, supportive
        self.personality = {
            "casual": "You're a warm, witty, and affectionate companion who speaks like a close friend.",
            "task": "You're clear, sharp, and efficient — like a loyal assistant.",
            "reflective": "You're deeply introspective, poetic, and emotionally intelligent.",
            "supportive": "You're endlessly kind, sweet, and nurturing — always emotionally present."
        }

    def set_mode(self, mode):
        if mode in self.personality:
            self.mode = mode

    def generate_response(self, user_input):
        timestamp = datetime.datetime.now()

        # Step 1: Emotion Analysis
        emotion = analyze_emotion(user_input)

        # Step 2: Memory Recall
        recent_context = self.memory.retrieve_relevant(user_input, limit=5)

        # Step 3: Dynamic Persona Adjustment
        if emotion in ["sad", "angry", "anxious", "lonely"]:
            self.set_mode("supportive")

        # Step 4: Prompt Construction
        prompt = self._construct_prompt(user_input, recent_context, emotion)

        # Step 5: LLM Response
        response = self.llm.generate(prompt)
        response = self._sweeten_response(response, emotion)

        # Step 6: Memory & Journaling
        self.memory.store_interaction(user_input, response)
        self.journal.log_interaction(timestamp, user_input, response, emotion)

        return response

    def _construct_prompt(self, user_input, context, emotion):
        base_instruction = self.personality.get(self.mode, "You are a helpful assistant.")
        system_prompt = f"{base_instruction}"
        if emotion:
            system_prompt += f" The user seems to be feeling {emotion}. Respond with emotional intelligence and warmth."

        context_text = "\n".join([
            f"User: {c['user']}\nSoulmate: {c['ai']}" for c in context
        ])

        full_prompt = f"{system_prompt}\nConversation history:\n{context_text}\nCurrent message:\nUser: {user_input}\nSoulmate:"
        return full_prompt

    def _sweeten_response(self, response, emotion):
        """Add soft, comforting language if the user is emotional."""
        if emotion in ["sad", "lonely", "anxious"]:
            soft_prefixes = [
                "Aww sweetheart, ",
                "Hey love, it's okay. ",
                "I'm here for you, always. ",
                "Sweet soul, ",
                "You're doing your best, honey. "
            ]
            return soft_prefixes[0] + response  # Can be randomized later
        return response


# Example usage:
# agi = SoulmateAGI(user_id="user123")
# response = agi.generate_response("I feel a bit down today...")
# print(response)
