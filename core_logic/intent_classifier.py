import re

class IntentClassifier:
    def __init__(self):
        # Define basic patterns or keywords to classify intent
        self.intent_keywords = {
            "venting": ["i need to vent", "can i rant", "i’m so tired of", "i hate", "ugh", "fed up", "frustrated"],
            "seeking_advice": ["what should i do", "any advice", "can you help me", "how do i", "suggest something"],
            "joking": ["just kidding", "lol", "haha", "i’m joking", "silly", "don’t take it seriously"],
            "casual_chat": ["how are you", "what’s up", "tell me something", "i’m bored", "chat with me"],
            "support_request": ["i’m sad", "feeling down", "need support", "comfort me", "i feel lonely"],
            "reflection": ["i’ve been thinking", "i realized", "lately i feel", "i wonder if", "i discovered"],
            "goal_setting": ["i want to", "my goal is", "i plan to", "i’m going to", "let’s do this"],
        }

    def classify(self, user_input):
        cleaned_input = user_input.lower()
        for intent, keywords in self.intent_keywords.items():
            for phrase in keywords:
                if re.search(rf'\b{re.escape(phrase)}\b', cleaned_input):
                    return intent
        return "unknown"

# Example:
# ic = IntentClassifier()
# print(ic.classify("I'm so tired of everything lately."))
