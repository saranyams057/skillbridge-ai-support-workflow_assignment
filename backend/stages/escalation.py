from typing import Any, Dict

from llm_client import call_llm_json
from prompts import ESCALATION_ASSESSMENT_PROMPT
from schemas import ConversationState
from utils import stringify_conversation


COMPLAINT_PATTERNS = [
    "angry", "frustrated", "upset", "disappointed", "complaint",
    "bad experience", "not happy", "poor support", "trainer was bad",
    "certificate not received", "recording not available", "access issue"
]

HUMAN_REQUEST_PATTERNS = [
    "human", "counselor", "counsellor", "manager", "trainer",
    "admissions team", "talk to someone", "speak to someone", "call me"
]

PRICING_EXCEPTION_PATTERNS = [
    "discount", "scholarship", "emi", "installment", "instalment",
    "lower price", "reduce fee", "fee waiver", "coupon"
]

REFUND_PAYMENT_PATTERNS = [
    "refund", "cancel my enrollment", "cancellation", "payment failed",
    "duplicate payment", "paid twice", "money deducted", "receipt not received"
]

PLACEMENT_GUARANTEE_PATTERNS = [
    "guaranteed job", "job guarantee", "guaranteed placement",
    "sure placement", "salary guarantee", "guaranteed interview",
    "100% placement", "assured job"
]

CORPORATE_PATTERNS = [
    "corporate training", "train my team", "company training",
    "bulk training", "custom training for employees"
]


def layer1_fast_pattern_match(message: str) -> Dict[str, Any]:
    text = message.lower()

    if any(p in text for p in REFUND_PAYMENT_PATTERNS):
        return {
            "matched": True,
            "should_escalate": True,
            "reason": "Refund, cancellation, or payment issue requires admissions team review.",
            "category": "refund_or_cancellation",
            "confidence": 0.97,
            "customer_sentiment": "urgent",
            "layer": "pattern_match",
        }

    if any(p in text for p in COMPLAINT_PATTERNS):
        return {
            "matched": True,
            "should_escalate": True,
            "reason": "Learner complaint or dissatisfaction detected.",
            "category": "complaint",
            "confidence": 0.95,
            "customer_sentiment": "frustrated",
            "layer": "pattern_match",
        }

    if any(p in text for p in PLACEMENT_GUARANTEE_PATTERNS):
        return {
            "matched": True,
            "should_escalate": True,
            "reason": "Placement or job guarantee request requires human counselor clarification.",
            "category": "placement_guarantee",
            "confidence": 0.96,
            "customer_sentiment": "neutral",
            "layer": "pattern_match",
        }

    if any(p in text for p in PRICING_EXCEPTION_PATTERNS):
        return {
            "matched": True,
            "should_escalate": True,
            "reason": "Discount, scholarship, EMI, or pricing exception request detected.",
            "category": "pricing_exception",
            "confidence": 0.94,
            "customer_sentiment": "neutral",
            "layer": "pattern_match",
        }

    if any(p in text for p in HUMAN_REQUEST_PATTERNS):
        return {
            "matched": True,
            "should_escalate": True,
            "reason": "Learner requested human admissions support.",
            "category": "explicit_human_request",
            "confidence": 0.95,
            "customer_sentiment": "neutral",
            "layer": "pattern_match",
        }

    if any(p in text for p in CORPORATE_PATTERNS):
        return {
            "matched": True,
            "should_escalate": True,
            "reason": "Corporate or custom training request is outside standard SOP handling.",
            "category": "corporate_training",
            "confidence": 0.93,
            "customer_sentiment": "neutral",
            "layer": "pattern_match",
        }

    return {"matched": False, "layer": "pattern_match"}


def detect_escalation(message: str, state: ConversationState, sop: str) -> Dict[str, Any]:
    layer1 = layer1_fast_pattern_match(message)
    if layer1["matched"]:
        return layer1

    prompt = ESCALATION_ASSESSMENT_PROMPT.format(
        SOP=sop,
        message=message,
        conversation=stringify_conversation(state),
    )
    result = call_llm_json(prompt, state)
    result["layer"] = "llm_assessment"
    return result
