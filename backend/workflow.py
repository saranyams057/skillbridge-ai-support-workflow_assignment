from config import MAX_MESSAGES_BEFORE_SUMMARY
from schemas import ChatMessage, ConversationState
from stages.escalation import detect_escalation
from stages.faq import answer_faq
from stages.qualification import merge_lead_data, qualify_lead
from stages.summary import format_summary, generate_summary
from utils import log_conversation, log_escalation


def run_workflow(message: str, state: ConversationState, sop: str):
    state.messages.append(ChatMessage(role="user", content=message))

    normalized = message.lower().strip()
    if normalized in ["summary", "end", "end session", "finish", "generate summary"]:
        return _summary_response(state, sop)

    if len(state.messages) > MAX_MESSAGES_BEFORE_SUMMARY:
        summary = generate_summary(state, sop)
        state.summary = summary
        assistant_message = (
            "We’ve reached the safe conversation limit for this session, so I’ll summarize the conversation now.\n\n"
            + format_summary(summary)
        )
        state.messages.append(ChatMessage(role="assistant", content=assistant_message))
        log_conversation(state, "auto_summary_conversation_limit")
        return {"assistant_message": assistant_message, "state": state, "stage": "auto_summary"}

    escalation = detect_escalation(message, state, sop)
    if escalation.get("should_escalate") is True:
        state.escalated = True
        state.escalation_reason = escalation.get("reason", "Human admissions counselor handoff required.")
        state.escalation_category = escalation.get("category", "unknown")
        state.customer_sentiment = escalation.get("customer_sentiment", state.customer_sentiment)

        log_escalation(
            state=state,
            reason=state.escalation_reason,
            category=state.escalation_category or "unknown",
            confidence=float(escalation.get("confidence", 1.0)),
            customer_message=message,
        )

        assistant_message = (
            "I’ll connect this to a human admissions counselor so they can assist you accurately.\n\n"
            f"Escalation reason: {state.escalation_reason}"
        )
        state.messages.append(ChatMessage(role="assistant", content=assistant_message))
        log_conversation(state, "escalation_detection")
        return {"assistant_message": assistant_message, "state": state, "stage": "escalation_detection"}

    faq = answer_faq(message, state, sop)
    if faq.get("blocked_by_validation"):
        state.unanswered_count += 1
        sop_gap = faq.get("sop_gap") or message
        state.sop_gaps.append(sop_gap)

        if state.unanswered_count > 2:
            state.escalated = True
            state.escalation_reason = "More than two unanswered SOP questions."
            state.escalation_category = "low_confidence"

            log_escalation(
                state=state,
                reason=state.escalation_reason,
                category="low_confidence",
                confidence=float(faq.get("confidence", 0)),
                customer_message=message,
            )

            assistant_message = (
                "I don’t have enough information in the SOP to answer that accurately. "
                "I’ll connect you with a human admissions counselor."
            )
            stage = "escalation_detection"
        else:
            assistant_message = faq.get("safe_fallback")
            stage = "faq_answering_sop_gap"

        state.messages.append(ChatMessage(role="assistant", content=assistant_message))
        log_conversation(state, stage)
        return {"assistant_message": assistant_message, "state": state, "stage": stage}

    qualification = qualify_lead(message, state, sop)
    state.lead_data = merge_lead_data(
        state.lead_data,
        qualification.get("updated_lead_data", {}),
    )

    faq_answer = faq.get("answer", "")
    next_question = qualification.get("next_question")
    is_lead_complete = qualification.get("is_lead_complete", False)

    if next_question and not is_lead_complete:
        assistant_message = f"{faq_answer}\n\nTo guide you better, {next_question}"
        stage = "lead_qualification"
    else:
        assistant_message = faq_answer
        stage = "faq_answering"

    state.messages.append(ChatMessage(role="assistant", content=assistant_message))
    log_conversation(state, stage)
    return {"assistant_message": assistant_message, "state": state, "stage": stage}


def _summary_response(state: ConversationState, sop: str):
    summary = generate_summary(state, sop)
    state.summary = summary
    assistant_message = format_summary(summary)
    state.messages.append(ChatMessage(role="assistant", content=assistant_message))
    log_conversation(state, "conversation_summary")
    return {"assistant_message": assistant_message, "state": state, "stage": "conversation_summary"}
