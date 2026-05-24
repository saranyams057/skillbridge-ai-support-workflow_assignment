import re
from typing import Optional

from llm_client import call_llm_json
from prompts import ESCALATION_ASSESSMENT_PROMPT
from utils import stringify_conversation

# Layer 1: Fast pattern matching (no API call)
ESCALATION_PATTERNS = {
    "refund_or_cancellation": [
        r"refund",
        r"cancel",
        r"money back",
        r"return",
        r"not happy",
        r"unsatisfied",
    ],
    "payment_issue": [
        r"payment fail",
        r"payment error",
        r"duplicate payment",
        r"transaction fail",
        r"billing issue",
    ],
    "complaint": [
        r"complain",
        r"poor quality",
        r"trainer quality",
        r"certificate delay",
        r"access issue",
        r"recording missing",
        r"bad experience",
    ],
    "placement_guarantee": [
        r"guaranteed job",
        r"guarantee.*job",
        r"job placement guarantee",
        r"guaranteed interview",
        r"salary promise",
        r"salary guarantee",
    ],
    "pricing_exception": [
        r"discount",
        r"scholarship",
        r"emi",
        r"installment",
        r"payment plan",
        r"cheaper",
        r"negotiat",
    ],
    "explicit_human_request": [
        r"speak.*counselor",
        r"speak.*human",
        r"speak.*manager",
        r"speak.*trainer",
        r"call me",
        r"contact.*human",
    ],
    "corporate_training": [
        r"corporate training",
        r"custom training",
        r"enterprise solution",
        r"bulk order",
    ],
}


def detect_sentiment(message: str):
    """Simple sentiment detection based on keywords"""
    message_lower = message.lower()

    if re.search(r"angry|furious|hate|horrible|terrible|worst", message_lower):
        return "angry"
    elif re.search(r"frustrated|annoyed|upset|disappointed|upset", message_lower):
        return "frustrated"
    elif re.search(r"not happy|unhappy|dissatisfied", message_lower):
        return "frustrated"
    elif re.search(r"urgent|asap|immediately|help|please", message_lower):
        return "urgent"
    elif re.search(r"interested|want|curious|considering|maybe", message_lower):
        return "interested"
    elif re.search(r"confused|not sure|unclear|don't know|what's", message_lower):
        return "confused"
    else:
        return "neutral"


def layer_1_pattern_matching(message: str):
    """Layer 1: Fast pattern matching without API call"""
    message_lower = message.lower()

    for category, patterns in ESCALATION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, message_lower):
                return {
                    "matched": True,
                    "should_escalate": True,
                    "reason": f"Pattern matched: {category.replace('_', ' ')}",
                    "category": category,
                    "confidence": 0.95,
                    "customer_sentiment": detect_sentiment(message),
                    "layer": "pattern_match"
                }

    return {
        "matched": False,
        "layer": "pattern_match"
    }


def layer_2_llm_assessment(message: str, state, conversation_str: str):
    """Layer 2: LLM-based sentiment and context analysis"""
    prompt = ESCALATION_ASSESSMENT_PROMPT.format(
        message=message,
        conversation=conversation_str
    )

    result = call_llm_json(prompt, state)

    # Handle system errors
    if result.get("system_error"):
        return result

    result["layer"] = "llm_assessment"
    return result


def detect_escalation(message: str, state, sop: Optional[str] = None):
    """
    Two-layer escalation detection:
    Layer 1: Fast pattern matching (no API call)
    Layer 2: LLM assessment (only if Layer 1 doesn't match)
    """
    # Layer 1: Pattern matching
    layer1_result = layer_1_pattern_matching(message)

    if layer1_result["matched"]:
        return layer1_result

    # Layer 2: LLM assessment
    conversation_str = stringify_conversation(state)
    layer2_result = layer_2_llm_assessment(message, state, conversation_str)

    return layer2_result
