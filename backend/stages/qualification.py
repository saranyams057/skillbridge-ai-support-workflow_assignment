from typing import Optional

from llm_client import call_llm_json
from prompts import QUALIFICATION_PROMPT, SYSTEM_PROMPT
from schemas import LeadData
from utils import stringify_conversation


def qualify_lead(message: str, state, sop: Optional[str] = None):
    """
    Qualification stage: Extract lead data and ask next questions.
    """

    conversation_str = stringify_conversation(state)
    lead_data_dict = state.lead_data.dict()

    prompt = QUALIFICATION_PROMPT.format(
        lead_data=lead_data_dict,
        conversation=conversation_str
    )

    # Call LLM
    result = call_llm_json(prompt, state, system_prompt=SYSTEM_PROMPT)

    # Handle system errors
    if result.get("system_error"):
        return {
            "updated_lead_data": {},
            "next_question": None,
            "is_lead_complete": False,
            "qualification_summary": "Error in qualification"
        }

    return result


def merge_lead_data(existing: LeadData, updated: dict):
    """Merge updated lead data: non-null fields overwrite existing"""
    data = existing.dict()

    for key, value in updated.items():
        if value is not None:
            data[key] = value

    return LeadData(**data)
