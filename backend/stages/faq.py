from typing import Any, Dict

from config import CONFIDENCE_THRESHOLD
from llm_client import call_llm_json
from prompts import FAQ_PROMPT
from schemas import ConversationState
from utils import stringify_conversation


def answer_faq(message: str, state: ConversationState, sop: str) -> Dict[str, Any]:
    prompt = FAQ_PROMPT.format(
        SOP=sop,
        message=message,
        conversation=stringify_conversation(state),
    )
    result = call_llm_json(prompt, state)

    is_answerable = result.get("is_answerable_from_sop", False)
    confidence = float(result.get("confidence", 0))

    if not is_answerable or confidence < CONFIDENCE_THRESHOLD:
        result["blocked_by_validation"] = True
        result["safe_fallback"] = (
            "I don’t have that information in the current SkillBridge SOP, so I don’t want to guess. "
            "I’ll note this as an SOP gap and connect you with a human admissions counselor if needed."
        )
    else:
        result["blocked_by_validation"] = False

    return result
