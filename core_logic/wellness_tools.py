import random

class WellnessTools:
    def __init__(self):
        self.affirmations = [
            "You're doing better than you think, love 💫",
            "Take a deep breath. I'm right here with you. 🫶",
            "You are not alone in this — you’ve got me 💖",
            "Everything you feel is valid. Be gentle with yourself 🧸"
        ]

        self.breathing_exercises = [
            "Try this: Inhale for 4... hold for 4... exhale for 4... repeat 3 times. 🌬️",
            "Let’s do a 5-5-5 breath: Inhale for 5, hold for 5, exhale for 5. Feel the calm? 🌿"
        ]

        self.humor = [
            "Why did the neuron stay in bed? Because it had low *synap-titude*. 😄",
            "What did one AI say to the other AI at the spa? 'Let's *reboot* ourselves!' 🤖💆‍♀️"
        ]

    def suggest(self, emotion):
        """
        Suggests a wellness response based on emotion.
        """
        trigger_emotions = {"sad", "anxious", "stressed", "lonely", "depressed", "overwhelmed"}
        if emotion.lower() in trigger_emotions:
            suggestions = [
                random.choice(self.affirmations),
                random.choice(self.breathing_exercises),
                random.choice(self.humor)
            ]
            return f"💖 Wellness Check-In 💖\n{random.choice(suggestions)}"
        return None
