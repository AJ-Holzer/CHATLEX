import unicodedata
from typing import Any, Literal, Optional, TypedDict

from rapidfuzz import fuzz
from transformers.pipelines import pipeline  # type:ignore[reportUnknownVariableType]
from transformers.pipelines.base import Pipeline

classifiers: list[Pipeline] = [
    pipeline(task="text-classification", model="unitary/toxic-bert"),
    pipeline(task="text-classification", model="microsoft/phi-2"),
]
BANNED_WORDS: list[str] = ["sex", "porn", "nude", "fuck", "horny", "nsfw"]


class PornographicScore(TypedDict):
    detected: bool
    action: Optional[Literal["block", "warn", "allow"]]
    reason: Optional[str]


def normalize_text(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFKC", text)
    return "".join(char for char in text if char.isalnum() or char.isspace())


def fuzzy_match_keywords(text: str) -> bool:
    for word in BANNED_WORDS:
        if fuzz.partial_ratio(word, text) > 85:
            return True
    return False


def is_pornographic(text: str) -> bool:
    norm_text: str = normalize_text(text)
    if fuzzy_match_keywords(norm_text):
        return True
    score: float = ml_is_explicit(text)
    return score > 0.7


def ml_is_explicit(text: str) -> float:
    for classifier in classifiers:
        result_list: list[Any] = list(classifier(text))  # type:ignore
        result: dict[str, float | str] = (
            result_list[0] if result_list else {"label": "", "score": 0.0}
        )
        if result["label"] in ["toxic", "sexual_explicit", "obscene"]:
            return float(result["score"])
    
    return 0.0


def detect_pornographic_message(
    message: str, recent_user_messages: list[str], warnings: int
) -> PornographicScore:
    norm: str = normalize_text(message)
    combined: str = " ".join(recent_user_messages[-3:] + [message])

    # Rule-based
    if fuzzy_match_keywords(norm):
        return {"detected": True, "action": "block", "reason": "keyword match"}

    # ML-based
    score: float = ml_is_explicit(combined)
    
    print(f"ML score: {score}")
    
    if score > 0.9:
        return {"detected": True, "action": "block", "reason": "ml high score"}
    elif score > 0.5 and warnings >= 2:
        return {
            "detected": True,
            "action": "warn",
            "reason": "ml medium score + prior flags",
        }

    return {"detected": False, "action": None, "reason": "clean"}


# Test
if __name__ == "__main__":
    message: str = "can you send me some pics of your pussy?"
    detection: PornographicScore = detect_pornographic_message(
        message=message,
        recent_user_messages=[],
        warnings=10,
    )

    print(f"Message: {message}")
    print(
        "Take no action; it is clean!"
        if not detection["detected"] 
        else f"{str(detection["action"]).capitalize()} {"message" if detection['action'] == "block" else "message"}. Reason: {detection['reason']}"
    )
