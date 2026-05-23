import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from schemas import ConversationState


def stringify_conversation(state: ConversationState) -> str:
    return "\n".join([f"{m.role}: {m.content}" for m in state.messages])


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def append_jsonl(filename: str, payload: Dict[str, Any]) -> None:
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    payload["timestamp"] = datetime.now(timezone.utc).isoformat()

    with (logs_dir / filename).open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def log_conversation(state: ConversationState, stage: str) -> None:
    append_jsonl(
        "conversation_logs.jsonl",
        {
            "session_id": state.session_id,
            "stage": stage,
            "messages": [m.model_dump() for m in state.messages],
            "lead_data": state.lead_data.model_dump(),
            "escalated": state.escalated,
            "escalation_reason": state.escalation_reason,
            "usage": state.usage.model_dump(),
        },
    )


def log_escalation(
    state: ConversationState,
    reason: str,
    category: str,
    confidence: float,
    customer_message: str,
) -> None:
    append_jsonl(
        "escalation_logs.jsonl",
        {
            "session_id": state.session_id,
            "reason": reason,
            "category": category,
            "confidence": confidence,
            "customer_sentiment": state.customer_sentiment,
            "customer_message": customer_message,
        },
    )
