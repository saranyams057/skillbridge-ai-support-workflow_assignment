from typing import Any, Dict

from llm_client import call_llm_json
from prompts import SUMMARY_PROMPT
from schemas import ConversationState
from utils import stringify_conversation


def generate_summary(state: ConversationState, sop: str) -> Dict[str, Any]:
    prompt = SUMMARY_PROMPT.format(
        SOP=sop,
        conversation=stringify_conversation(state),
        lead_data=state.lead_data.model_dump(),
        sop_gaps=state.sop_gaps,
        escalated=state.escalated,
        escalation_reason=state.escalation_reason,
    )
    return call_llm_json(prompt, state)


def format_summary(summary: Dict[str, Any]) -> str:
    details = summary.get("key_details_collected", [])
    gaps = summary.get("sop_gaps_identified", [])

    details_text = "\n".join([f"- {item}" for item in details]) if details else "- None"
    gaps_text = "\n".join([f"- {item}" for item in gaps]) if gaps else "- None"

    return (
        "Here is the conversation summary:\n\n"
        f"Customer Intent: {summary.get('customer_intent', 'Not identified')}\n\n"
        f"Key Details Collected:\n{details_text}\n\n"
        f"SOP Gaps Identified:\n{gaps_text}\n\n"
        f"Recommended Next Action: {summary.get('recommended_next_action', 'Admissions team follow-up recommended')}"
    )
