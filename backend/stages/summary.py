from typing import Optional

from llm_client import call_llm_json
from prompts import SUMMARY_PROMPT, SYSTEM_PROMPT
from utils import stringify_conversation


def generate_summary(state, sop: Optional[str] = None):
    """
    Summary stage: Generate structured summary for admissions team.
    """

    conversation_str = stringify_conversation(state)
    lead_data_dict = state.lead_data.dict()
    sop_gaps = state.sop_gaps

    prompt = SUMMARY_PROMPT.format(
        conversation=conversation_str,
        lead_data=lead_data_dict,
        sop_gaps=sop_gaps
    )

    # Call LLM
    result = call_llm_json(prompt, state, system_prompt=SYSTEM_PROMPT)

    # Handle system errors
    if result.get("system_error"):
        return {
            "customer_intent": "Error generating summary",
            "key_details_collected": [],
            "sop_gaps_identified": sop_gaps,
            "recommended_next_action": "Manual review required"
        }

    return result


def format_summary(summary: dict):
    """Format summary for display"""
    formatted = []

    if summary.get("customer_intent"):
        formatted.append(f"**Customer Intent**: {summary['customer_intent']}")

    if summary.get("key_details_collected"):
        formatted.append("**Key Details Collected**:")
        for detail in summary["key_details_collected"]:
            formatted.append(f"• {detail}")

    if summary.get("sop_gaps_identified"):
        formatted.append("**SOP Gaps Identified**:")
        for gap in summary["sop_gaps_identified"]:
            formatted.append(f"• {gap}")

    if summary.get("recommended_next_action"):
        formatted.append(f"**Recommended Next Action**: {summary['recommended_next_action']}")

    return "\n".join(formatted)
