# src/slot_manager.py

# src/slot_manager.py
import re
class SlotManager:
    def __init__(self):
        self.slots = {
            "genre": None,
            "topic": None,
            "emotion": None,
            "length": None
        }

        # 预设的合法值
        self.allowed_genres = ["pop", "hiphop"]
        self.allowed_topics = [
            "Heartbreak & Loss", "Love & Intimacy", "Persona & Performance",
            "Hope & Reflection", "Urban Party Life", "Street & Conflict",
            "Personal Change", "Voice & Identity", "Life & Mortality", "Faith & Religion"
        ]

        self.allowed_emotions = [
            "admiration", "amusement", "anger", "annoyance", "approval", "caring",
            "confusion", "curiosity", "desire", "disappointment", "disapproval",
            "embarrassment", "excitement", "fear", "gratitude", "grief", "joy",
            "love", "nervousness", "optimism", "pride", "realization", "relief",
            "remorse", "sadness", "surprise", "neutral"
        ]

    def is_filled(self):
        return all(value is not None for value in self.slots.values())

    def next_unfilled_slot(self):
        for slot, value in self.slots.items():
            if value is None:
                return slot
        return None

    def update_slot(self, slot, value):
        if slot not in self.slots:
            raise ValueError(f"Unknown slot: {slot}")

        
           # ========== genre ==========
        if slot == "genre":
            value = value.lower().strip()
            genre_map = {
                "pop": ["pop", "pop music", "popular", "pops"],
                "hiphop": ["hiphop", "hip-hop", "hip hop", "rap", "rap music"]
            }

            matched = None
            for genre, aliases in genre_map.items():
                for alias in aliases:
                    if value == alias or alias in value:
                        matched = genre
                        break
                if matched:
                    break

            if matched:
                value = matched
            else:
                raise ValueError(f"Invalid genre: {value}. Please choose from {self.allowed_genres}")

        # ========== topic ==========
        if slot == "topic":
            if self.allowed_topics and value not in self.allowed_topics:
                raise ValueError(f"Invalid topic: {value}. Please try other topics.")

        # ========== emotion ==========
        GOEMOTIONS_28 = [
                        "admiration", "amusement", "anger", "annoyance", "approval",
                        "caring", "confusion", "curiosity", "desire", "disappointment",
                        "disapproval", "disgust", "embarrassment", "excitement", "fear",
                        "gratitude", "grief", "joy", "love", "nervousness",
                        "optimism", "pride", "realization", "relief", "remorse",
                        "sadness", "surprise", "neutral"
                    ]
        if slot == "emotion":
            if value.lower() not in GOEMOTIONS_28:
                raise ValueError(
                    f"❌ Invalid emotion: '{value}'.\n\n"
                    f"Please choose one of the following supported emotions:\n\n"
                    f"{', '.join(GOEMOTIONS_28)}"
                )
        # ========== length ==========
        if slot == "length":
            if not (200 <= value <= 1200):
                raise ValueError(f"Invalid length: {value}. Please enter a number between 200 and 1200.")

        self.slots[slot] = value

    def get_slots(self):
        return self.slots
