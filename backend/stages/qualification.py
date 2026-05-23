from typing import Any, Dict

from llm_client import call_llm_json
from prompts import QUALIFICATION_PROMPT
from schemas import ConversationState, LeadData
from utils import stringify_conversation


def merge_lead_data(existing: LeadData, updated: Dict[str, Any]) -> LeadData:
    current = existing.model_dump()
    for key, value in updated.items():
        if value not in [None, "", "null"]:
            current[key] = value
    return LeadData(**current)


def qualify_lead(message: str, state: ConversationState, sop: str) -> Dict[str, Any]:
    prompt = QUALIFICATION_PROMPT.format(
        SOP=sop,
        message=message,
        conversation=stringify_conversation(state),
        lead_data=state.lead_data.model_dump(),
    )
    return call_llm_json(prompt, state)
