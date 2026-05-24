from config import CONFIDENCE_THRESHOLD
from llm_client import call_llm_json
from prompts import FAQ_PROMPT, SYSTEM_PROMPT
from utils import stringify_conversation


def answer_faq(message: str, state, sop: str):
    """
    FAQ answering stage with hallucination validation.
    Returns answer from SOP only, blocks if confidence too low.
    """

    conversation_str = stringify_conversation(state)

    prompt = FAQ_PROMPT.format(
        sop=sop,
        message=message,
        conversation=conversation_str
    )

    # Call LLM
    result = call_llm_json(prompt, state, system_prompt=SYSTEM_PROMPT)

    # Handle system errors
    if result.get("system_error"):
        return {
            "answer": "I encountered a technical issue. Let me connect you with a human counselor.",
            "confidence": 0.0,
            "is_answerable_from_sop": False,
            "sop_gap": "system_error",
            "evidence": None,
            "blocked_by_validation": True
        }

    # Extract response
    answer = result.get("answer", "")
    confidence = result.get("confidence", 0.0)
    is_answerable = result.get("is_answerable_from_sop", False)
    sop_gap = result.get("sop_gap")
    evidence = result.get("evidence")

    # Hallucination validation: block if not answerable from SOP or low confidence
    blocked_by_validation = False
    if not is_answerable or confidence < CONFIDENCE_THRESHOLD:
        blocked_by_validation = True
        safe_fallback = "I don't have that information in the current SkillBridge SOP, so I don't want to guess. Let me connect you with a human admissions counselor who can help you better."

        return {
            "answer": safe_fallback,
            "confidence": 0.0,
            "is_answerable_from_sop": False,
            "sop_gap": sop_gap or "unknown",
            "evidence": None,
            "blocked_by_validation": blocked_by_validation
        }

    # Return successful FAQ answer
    return {
        "answer": answer,
        "confidence": confidence,
        "is_answerable_from_sop": True,
        "sop_gap": None,
        "evidence": evidence,
        "blocked_by_validation": False
    }
