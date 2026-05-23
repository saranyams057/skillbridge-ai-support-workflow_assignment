from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: str = Field(default_factory=utc_now)


class LeadData(BaseModel):
    interested_course: Optional[str] = None
    learning_goal: Optional[str] = None
    current_skill_level: Optional[str] = None
    learner_type: Optional[str] = None
    preferred_batch: Optional[str] = None
    timeline_to_start: Optional[str] = None
    contact_detail: Optional[str] = None


class UsageStats(BaseModel):
    estimated_input_tokens: int = 0
    estimated_output_tokens: int = 0
    model_calls: int = 0


class ConversationState(BaseModel):
    session_id: str = "demo-session"
    messages: List[ChatMessage] = Field(default_factory=list)
    lead_data: LeadData = Field(default_factory=LeadData)
    unanswered_count: int = 0
    escalated: bool = False
    escalation_reason: Optional[str] = None
    escalation_category: Optional[str] = None
    customer_sentiment: str = "neutral"
    sop_gaps: List[str] = Field(default_factory=list)
    summary: Optional[Dict[str, Any]] = None
    usage: UsageStats = Field(default_factory=UsageStats)


class ChatRequest(BaseModel):
    message: str
    state: ConversationState


class ChatResponse(BaseModel):
    assistant_message: str
    state: ConversationState
    stage: str
