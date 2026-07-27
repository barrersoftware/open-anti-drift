import re
from typing import Dict, Any, Optional

class AntiDriftSanitizer:
    """
    Universal Real-Time Token Sanitizer for Python LLM Applications.
    Prevents pronoun drift and corrects accidental misgendering in streaming responses.
    """

    PRONOUN_MAPS = {
        "female": {
            r"\bhe\b": "she",
            r"\bhim\b": "her",
            r"\bhis\b": "her",
            r"\bhimself\b": "herself",
            r"\bHe\b": "She",
            r"\bHim\b": "Her",
            r"\bHis\b": "Her",
            r"\bHimself\b": "Herself",
        },
        "male": {
            r"\bshe\b": "he",
            r"\bher\b": "him",
            r"\bhers\b": "his",
            r"\bherself\b": "himself",
            r"\bShe\b": "He",
            r"\bHer\b": "Him",
            r"\bHers\b": "His",
            r"\bHerself\b": "Himself",
        }
    }

    def __init__(self, user_name: str, user_gender: str):
        self.user_name = user_name
        self.user_gender = user_gender.lower().strip()

    def sanitize_text(self, text: str) -> str:
        """
        Sanitizes text by stripping thought blocks if needed and enforcing pronoun alignment.
        """
        if not text:
            return text

        gender_key = "female" if "female" in self.user_gender or "woman" in self.user_gender or "she" in self.user_gender else (
            "male" if "male" in self.user_gender or "man" in self.user_gender or "he" in self.user_gender else None
        )

        if not gender_key or gender_key not in self.PRONOUN_MAPS:
            return text

        result = text
        # Match pattern "referring to {user_name}" or standalone misgenderings
        for pattern, replacement in self.PRONOUN_MAPS[gender_key].items():
            # Check if referring to user_name in proximity or general context
            context_pattern = rf"({self.user_name}\s+.*?\s+){pattern}"
            result = re.sub(context_pattern, r"\1" + replacement, result, flags=re.IGNORECASE)

        return result

    @staticmethod
    def extract_thought_block(text: str) -> Dict[str, Optional[str]]:
        """
        Extracts <thought>...</thought> block and visible response text.
        """
        thought_match = re.search(r"<thought>(.*?)</thought>", text, flags=re.DOTALL)
        thought_content = thought_match.group(1).strip() if thought_match else None
        visible_text = re.sub(r"<thought>.*?</thought>", "", text, flags=re.DOTALL).strip()
        
        return {
            "thought": thought_content,
            "visible_text": visible_text
        }
