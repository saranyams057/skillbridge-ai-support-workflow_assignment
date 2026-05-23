# SkillBridge AI Support Workflow

A full-stack SOP-grounded AI customer support workflow for a fictional online course academy: **SkillBridge Academy**.

This project demonstrates a safe, modular AI workflow for course enquiries, lead qualification, escalation detection, hallucination prevention, logging, and structured conversation summaries.

## Why This Use Case

The previous appliance repair use case created too many natural complaint and safety escalations. SkillBridge Academy is a better fit because most customer messages are normal course enquiries, while still having realistic escalation cases such as refunds, payment issues, complaints, discounts, and job guarantee requests.

## Core Problem

Build an AI-powered customer support workflow that can:

1. Answer FAQs only from SOP
2. Qualify course leads
3. Detect when a human admissions counselor is needed
4. Summarize the session for follow-up

## Architecture

```text
React Frontend
   ↓
FastAPI Backend
   ↓
Workflow Controller
   ↓
Escalation Detection
   ↓
FAQ Answering from SOP
   ↓
Lead Qualification
   ↓
Conversation Summary
   ↓
Logs + Updated State
```

## Framework and Tools

- Frontend: React + Vite
- Backend: FastAPI
- LLM Provider: Groq
- Model: `llama-3.3-70b-versatile`
- State Validation: Pydantic
- Workflow Orchestration: Modular Python workflow
- Logs: JSONL
- SOP: Plain text

## Why Simple Modular Workflow Instead of Agents

This project uses a deterministic stage-based workflow instead of autonomous agents.

The reason is that admissions support needs predictable behavior. The system should always check escalation first, answer from SOP only, qualify the lead, and summarize when needed.

This design is easier to test, debug, and evaluate than fully autonomous agents.

## Escalation Detection: Two-Layer Approach

### Layer 1: Fast Pattern Matching

No API call is made. The backend checks for obvious escalation phrases:

- refund or cancellation
- payment failure
- complaint
- certificate issue
- discount, EMI, scholarship
- job guarantee
- human counselor request

### Layer 2: LLM-Based Confidence Assessment

If Layer 1 does not match, the model classifies the message and returns structured JSON.

## Hallucination Prevention: Three-Layer Defense

### Layer 1: System Prompt Constraints

The prompt explicitly says answer only from SOP and do not invent unsupported course, payment, certificate, or placement details.

### Layer 2: SOP Embedded in Prompt

The full SOP is included inside the FAQ prompt so the model has the approved business knowledge.

### Layer 3: Response Validation and Flag Checking

The FAQ stage must return `is_answerable_from_sop`, `confidence`, `sop_gap`, and `evidence`.

If confidence is below `0.70` or the answer is unsupported, the backend blocks the answer and uses a safe fallback.

## Production-Ready Elements Implemented

- SOP-only answering
- confidence-based fallback
- escalation-first workflow
- conversation limit
- structured outputs
- no unsupported promises
- conversation logs
- escalation logs
- error handling
- token/model-call estimate tracking

## How to Run

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your Groq API key to `.env`.

```bash
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.
Backend runs at `http://localhost:8000`.

## Demo Scenarios

1. In-SOP FAQ: What is the fee and duration for the Generative AI Basics course?
2. Lead qualification: I want to learn AI but I only know basic Python. Which course should I choose?
3. Escalation: Do you provide a guaranteed job after the course?
4. Unsupported policy: Do you have EMI options?
5. Complaint: Can I get a refund? I am not happy with the course.
6. Summary: summary

## Known Limitations

This is a production-style prototype, not a full enterprise deployment. Future improvements include database persistence, authentication, WhatsApp integration, CRM ticket creation, automated evaluation tests, PII masking, and an admin SOP editor.
