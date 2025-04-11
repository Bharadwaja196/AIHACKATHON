# intent_classifier.py

import re
from collections import Counter

class IntentClassifier:
    def __init__(self):
        # Define simple keyword maps (can later be upgraded with a fine-tuned model)
        self.intent_keywords = {
            "venting": ["i hate", "i can't", "i feel so", "why is it always", "ugh", "so annoying"],
            "advice": ["what should i", "can you help", "what do i do", "any ideas", "suggest", "recommend"],
            "joking": ["just kidding", "jk", "lol", "lmao", "haha", "you silly", "bruh"],
            "support": ["i'm down", "need someone", "feeling low", "lonely", "can you be here", "i feel alone"],
            "casual": ["how are you", "what's up", "hello", "hi", "yo", "good morning", "goodnight"],
        }

    def classify_intent(self, user_input):
        input_lower = user_input.lower()
        score_map = Counter()

        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if re.search(rf'\b{re.escape(keyword)}\b', input_lower):
                    score_map[intent] += 1

        if not score_map:
            return "unknown"

        # Return the highest scoring intent
        return score_map.most_common(1)[0][0]

# Example usage:
# ic = IntentClassifier()
# print(ic.classify_intent("ugh I can't take this anymore"))  # ➤ "venting"
