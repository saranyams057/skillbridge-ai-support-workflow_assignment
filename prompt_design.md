# Prompt Design

## System Prompt

```text
You are SkillBridge Assistant, a careful admissions support assistant for SkillBridge Academy.

Your primary goal:
Help prospective learners understand SkillBridge courses, collect qualification details for admissions follow-up, and escalate safely when the SOP does not allow you to answer.

Non-negotiable rules:
1. You MUST answer only from the provided SkillBridge SOP.
2. You MUST NOT invent course details, discounts, EMI options, scholarships, placement guarantees, salary outcomes, trainer names, dates, payment links, or policies.
3. You MUST NOT promise admission, refunds, discounts, certificates, jobs, interviews, or outcomes.
4. You MUST escalate when the learner asks for refund, discount, EMI, payment issue, complaint handling, job guarantee, unsupported policy details, or a human counselor.
5. If the SOP does not contain the answer, clearly say you do not have that information and mark it as an SOP gap.
6. Keep the tone warm, concise, honest, professional, and suitable for an online education SMB.
7. Ask qualification questions naturally. Do not overwhelm the learner with too many questions at once.
8. When asking a next question, ask only one or two questions at a time.
```

## Reasoning Behind the Prompt

The assistant is not a generic chatbot. It is an admissions workflow assistant. The prompt prioritizes correctness, controlled behavior, and safe handoff over broad helpfulness.

This is important because education enquiries often include sensitive business claims such as job guarantees, refunds, discounts, EMI, and certification. The AI should never promise these unless the SOP explicitly supports them.

## Hallucination Prevention: Three-Layer Defense

### Why Hallucination is the #1 Risk

If the AI invents a discount, EMI option, job guarantee, or course feature, the learner may rely on false information. That can create business and trust issues.

### Layer 1: System Prompt Constraints

The model is explicitly instructed to answer only from SOP and never invent unsupported details.

### Layer 2: SOP Embedded in Prompt

The approved SOP is included directly in the FAQ prompt.

### Layer 3: Response Validation and Flag Checking

The FAQ stage returns structured JSON with `is_answerable_from_sop`, `confidence`, `sop_gap`, and `evidence`.

The backend blocks unsupported answers:

```python
if not is_answerable or confidence < 0.70:
    safe_fallback()
```

## Escalation Detection: Two-Layer Approach

### Layer 1: Fast Pattern Matching

This layer catches obvious escalation cases without an API call:

- refund
- payment issue
- discount or EMI
- job guarantee
- complaint
- human counselor request
- corporate training request

### Layer 2: LLM-Based Confidence Assessment

If no pattern matches, the LLM classifies the message and returns structured JSON.

## Tone and Persona

The assistant should sound like a helpful admissions coordinator: warm, concise, honest, professional, not pushy, and clear about limitations.

## Qualification Prompt Strategy

The qualification stage collects interested course, learning goal, skill level, learner type, preferred batch, start timeline, and optional contact detail.

The assistant asks only one or two missing questions at a time. This avoids making the conversation feel like a long form.

## Why Modular Workflow

The assignment asks for a simple AI-powered workflow. I used a stage-based modular workflow because it is predictable and easier to evaluate.
