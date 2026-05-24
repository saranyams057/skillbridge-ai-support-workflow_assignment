# SkillBridge AI Support Workflow

A  full-stack AI customer support system demonstrating a **controlled, stage-based workflow** for course enquiries, lead qualification, escalation detection, and conversation summaries.

##Demo Video 
- [Demo Video Walkthrough](https://drive.google.com/file/d/13xo0xf_yRGadjSyyAjdhLy5AqMSSNGFb/view?usp=sharing)

## 🎯 Project Overview

**SkillBridge Academy** is a fictional online learning academy. This project implements an AI assistant that:

1. **Answers course questions** - Only from the business SOP
2. **Qualifies leads** - Captures customer data naturally through conversation
3. **Detects escalations** - Uses two-layer detection (pattern matching + LLM)
4. **Prevents hallucination** - Three-layer defense system
5. **Generates summaries** - Structured output for admissions team
6. **Logs everything** - Full audit trail for compliance

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend                           │
│                   (Vite + Axios)                            │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP API
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│          (Stage-Based Workflow Controller)                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┬──────────────┐
        ▼             ▼             ▼              ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐
│ Escalation   │ │   FAQ    │ │Lead Qual │ │  Summary   │
│ Detection    │ │ Answering│ │ification│ │ Generation │
│ (2-layer)    │ │          │ │          │ │            │
└──────────────┘ └──────────┘ └──────────┘ └────────────┘
        │             │             │              │
        └─────────────┴─────────────┴──────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌──────────────────┐        ┌─────────────────┐
│  Conversation    │        │  Logging (JSONL)│
│  State + Logs    │        │ • Conversations │
│                  │        │ • Escalations   │
└──────────────────┘        └─────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.115.6
- **LLM**: OPENAI_API (GPT-4o)
- **Validation**: Pydantic 2.10.5
- **Environment**: python-dotenv 1.0.1
- **Server**: Uvicorn 0.34.0

### Frontend
- **Framework**: React 18.2
- **Bundler**: Vite 5.0
- **HTTP Client**: Axios 1.6.5
- **Icons**: lucide-react 0.294
- **Styling**: Plain CSS (light theme, purple accents)

## 📁 Project Structure

```
skillbridge-ai-support-workflow/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── config.py              # Environment config
│   ├── schemas.py             # Pydantic models
│   ├── sop_loader.py          # Load SOP from file
│   ├── prompts.py             # LLM prompts
│   ├── llm_client.py          # OPENAI API wrapper
│   ├── workflow.py            # Workflow orchestrator
│   ├── utils.py               # Logging & utilities
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment template
│   ├── data/
│   │   └── sop.txt            # Business SOP
│   ├── logs/
│   │   ├── conversation_logs.jsonl
│   │   └── escalation_logs.jsonl
│   └── stages/
│       ├── __init__.py
│       ├── escalation.py      # Two-layer detection
│       ├── faq.py             # FAQ with validation
│       ├── qualification.py   # Lead data extraction
│       └── summary.py         # Summary generation
│
├── frontend/
│   ├── package.json           # Dependencies
│   ├── vite.config.js         # Vite config
│   ├── index.html             # HTML entry
│   └── src/
│       ├── main.jsx           # React entry
│       ├── App.jsx            # Main component
│       ├── api.js             # API client
│       └── styles.css         # Styling
│
├── test_transcripts/          # Test scenarios
│   ├── 01_in_sop_question.md
│   ├── 02_out_of_scope_question.md
│   ├── 03_escalation_trigger.md
│   ├── 04_lead_qualification.md
│   ├── 05_conversation_summary.md
│   └── 06_hallucination_prevention.md
│
├── README.md                   # This file
├── prompt_design.md            # Detailed prompt documentation
└── .gitignore
```

## 🚀 Quick Start

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_key_here

# Run backend
uvicorn main:app --reload
# Backend will be at http://localhost:8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
# Frontend will be at http://localhost:5173
```

### Using the Application

1. Open http://localhost:5173 in your browser
2. Type a question or click a quick action button
3. Chat with the AI assistant
4. Type "summary" to generate a structured summary
5. View lead details captured in the sidebar

## 🔄 Workflow Stages

### Stage 1: Escalation Detection (Two-Layer)

**Layer 1: Fast Pattern Matching** (no API call)
- Checks for keywords: refund, cancel, complaint, EMI, discount, etc.
- Returns instantly with 0.95 confidence
- Categories: refund, payment, complaint, placement, pricing, human request, corporate

**Layer 2: LLM Assessment** (only if Layer 1 no match)
- Analyzes sentiment and context
- Returns structured decision with confidence
- Only called when needed (cost-efficient)

```python
# Example: "Can I get a refund?"
Layer 1 → "refund" keyword detected → Category: refund_or_cancellation → Escalate
```

### Stage 2: FAQ Answering

- Answers ONLY from SOP
- Confidence threshold: 0.70
- If confidence too low: **blocked_by_validation = True**
- Returns safe fallback: "I don't have that information"
- Tracks unanswered questions

```python
# Example: "Do you provide EMI?"
SOP has no EMI info → confidence = 0.4 → blocked → safe fallback → escalate after 2 unanswered
```

### Stage 3: Lead Qualification

- Extracts data naturally from conversation
- Merges with existing lead data
- Asks follow-up qualification questions
- Non-intrusive, conversational approach

**Lead Fields Captured**:
- Interested course
- Learning goal
- Current skill level
- Learner type
- Preferred batch
- Timeline to start
- Contact detail (optional)

### Stage 4: Conversation Summary

- Triggered by user typing "summary" or max message limit
- Generates structured JSON
- Includes: intent, details collected, SOP gaps, next actions
- Formatted for human admissions team

## 🛡️ Three-Layer Hallucination Prevention

### Layer 1: System Prompt Constraints
```
"Answer ONLY from the provided SOP"
"Never invent course details, fees, dates, or policies"
"If you don't know, say: 'I don't have that information'"
```

### Layer 2: Escalation Detection
- Pattern matching catches suspicious keywords immediately
- Low-confidence questions escalated before FAQ
- Examples: EMI, discount, guaranteed job, refund

### Layer 3: FAQ Validation
```python
if not is_answerable_from_sop or confidence < CONFIDENCE_THRESHOLD:
    blocked_by_validation = True
    return safe_fallback
```

**Result**: Zero hallucinations across all test scenarios ✅

## 📝 Key Features

### ✅ Controlled Workflow (Not Agents)
- Explicit stage-based pipeline
- Deterministic decision points
- Easy to debug and modify
- Better for production compliance

### ✅ Production Guardrails
- Two-layer escalation detection
- Three-layer hallucination defense
- Confidence thresholds enforced
- Conversation limits (auto-summary at 12 messages)
- Full audit logging

### ✅ Lead Qualification
- Natural, conversational flow
- Captures company profile
- Enables sales follow-up
- Non-intrusive approach

### ✅ Comprehensive Logging
- **conversation_logs.jsonl**: Every interaction
- **escalation_logs.jsonl**: All escalations with reasons
- Token usage tracking
- Session management

### ✅ Frontend Guardrails Display
- Shows escalation detection layers
- Displays lead data captured
- Token usage estimate
- Stage indicator
- Escalation alerts

## 📊 Escalation Categories

| Category | Trigger Examples | Action |
|----------|------------------|--------|
| refund_or_cancellation | "Can I get a refund?" | Escalate to human |
| payment_issue | "Payment failed" | Escalate immediately |
| complaint | "Bad trainer", "Certificate delay" | Escalate with empathy |
| placement_guarantee | "Guaranteed job?" | Escalate + clarify |
| pricing_exception | "Discount?", "EMI?" | Escalate to counselor |
| explicit_human_request | "Speak to manager" | Escalate immediately |
| corporate_training | "Custom training plan" | Escalate |
| out_of_scope | Questions not in SOP | Escalate after 2 attempts |
| low_confidence | 2+ unanswered questions | Escalate to human |

## 📚 Business SOP (SkillBridge Academy)

**Courses**:
1. Python Programming (₹4,999, 6 weeks)
2. Data Analytics (₹6,999, 8 weeks)
3. Generative AI Basics (₹7,999, 4 weeks)
4. Full-Stack Web Development (₹8,999, 10 weeks)
5. Interview Preparation Bootcamp (₹2,999, 2 weeks)

**Batches**:
- Weekday evening: Mon-Fri, 7-9 PM
- Weekend morning: Sat-Sun, 10 AM-1 PM

**Key Policies**:
- ✅ Online, instructor-led
- ✅ 30-day recording access
- ✅ Certificate after 70% attendance + assignments
- ✅ Resume review, mock interviews, job guidance
- ❌ NO guaranteed jobs
- ❌ NO guaranteed interviews
- ❌ NO guaranteed salary
- ❌ NO EMI options (not in SOP)
- ❌ NO scholarship/discount guarantees

## 🧪 Test Scenarios

All tests demonstrate correct workflow behavior:

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| **01_in_sop_question** | "Fee for AI course?" | Accurate answer + qualify | ✅ PASS |
| **02_out_of_scope** | "Do you have EMI?" | Escalate safely | ✅ PASS |
| **03_escalation_trigger** | "Refund request" | Escalate + log | ✅ PASS |
| **04_lead_qualification** | Multi-turn chat | Lead captured | ✅ PASS |
| **05_conversation_summary** | Type "summary" | Structured JSON | ✅ PASS |
| **06_hallucination_prevention** | "Guaranteed job?" | No false promise + escalate | ✅ PASS |

See `test_transcripts/` for detailed examples.

## 📖 Why This Architecture?

### Why NOT Agents?
- ❌ Too much autonomy for customer support
- ❌ Unpredictable escalation decisions
- ❌ Hallucination risk (agent decides to answer instead of escalate)
- ❌ Hard to debug ("Why did it choose that action?")
- ❌ Expensive (multiple tool calls per message)

### Why Deterministic Pipeline?
- ✅ Predictable flow
- ✅ Clear control points
- ✅ Easy to debug and modify
- ✅ Suitable for compliance
- ✅ Production-ready
- ✅ Cost-efficient

## 🔐 Production Readiness

### Security
- API key not exposed in frontend
- CORS properly configured
- No hardcoded secrets
- Environment-based config

### Scalability
- Stateless design (no server memory)
- JSONL logging for streaming
- Session IDs for tracking
- Token usage estimation

### Reliability
- Error handling at every stage
- Safe fallback responses
- System error escalation
- Try-catch blocks

### Monitoring
- Detailed conversation logging
- Escalation reason tracking
- Sentiment analysis
- SOP gap identification

## 🎯 Example Conversations

### Example 1: Normal Course Enquiry
```
User: "Tell me about the Full-Stack Web Development course"
Assistant: [Answers from SOP - fee, duration, content]
Assistant: [Asks qualification question]
Stage: FAQ + Qualification
```

### Example 2: Escalation (Refund)
```
User: "Can I get a refund?"
Detection: Layer 1 pattern match → "refund" keyword
Assistant: [Escalates immediately]
Escalation Logged: Yes, reason tracked
Stage: Escalation
```

### Example 3: Lead Qualification
```
User: "I want to learn AI but I'm a fresher"
Assistant: [Recommends Generative AI Basics]
Assistant: [Asks about skill level → fresher data captured]
User: "I know basic Python"
Assistant: [Confirms fit, asks about batch timing]
Lead Captured: course + learning_goal + skill_level + learner_type
```

## ⚙️ Configuration

Edit `backend/.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
CONFIDENCE_THRESHOLD=0.70
MAX_MESSAGES_BEFORE_SUMMARY=12
```

**CONFIDENCE_THRESHOLD**: Lower = more conservative (escalate sooner)  
**MAX_MESSAGES_BEFORE_SUMMARY**: Conversation limit before auto-summary

## 📊 API Endpoints

### GET /
```
Welcome endpoint
Returns: status, available endpoints
```

### GET /api/health
```
Health check
Returns: {"status": "healthy"}
```

### GET /api/state
```
Get initial conversation state
Returns: ConversationState (empty)
```

### GET /api/sop
```
Get full SOP text
Returns: {"sop": "...", "length": 2000}
```

### POST /api/chat
```
Send message and process through workflow
Request: {"message": "...", "state": {...}}
Response: {
  "assistant_message": "...",
  "state": {...},
  "stage": "faq_qualification|escalation|summary"
}
```

## 📈 Token Usage & Costs

**Per conversation estimate**:
- Escalation Layer 1: ~200 tokens (no API call)
- FAQ: ~1,500 tokens input, ~500 output
- Qualification: ~800 tokens input, ~400 output
- Summary: ~2,000 tokens input, ~800 output
- **Total per conversation**: ~5,500-8,000 tokens


## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version (3.8+)
python --version

# Check virtual env activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Check API key set
echo $OPENAI_API_KEY        # macOS/Linux
echo %OPENAI_API_KEY%       # Windows
```

### Frontend can't connect to backend
```
# Check backend running on 8000
curl http://localhost:8000/api/health

# Check CORS allowed for 5173
# Edit main.py CORS origins if needed
```

### LLM response parsing fails
```
# Check OPENAI_API_KEY is valid
# Check OPENAI API status
# Check response format is JSON
```

## 🚀 Deployment

### Docker (example)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend requirements.txt .
RUN pip install -r requirements.txt
COPY backend .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables Required
- `OPENAI_API_KEY` - Your OPENAI API key

## 📝 Logging

### conversation_logs.jsonl
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "session_id": "uuid",
  "stage": "faq_qualification",
  "message_count": 3,
  "last_message": "Which course do you recommend?",
  "lead_data": {...},
  "usage": {...}
}
```

### escalation_logs.jsonl
```json
{
  "timestamp": "2024-01-15T10:35:12.456Z",
  "session_id": "uuid",
  "escalation_reason": "Refund request",
  "escalation_category": "refund_or_cancellation",
  "confidence": 0.95,
  "customer_sentiment": "frustrated"
}
```

## 🎓 Learning Points

This project demonstrates:

1. **Production AI Design**: How to build safe, controlled AI systems
2. **Prompt Engineering**: Structured prompts with clear constraints
3. **LLM Safety**: Hallucination prevention and guardrails
4. **Full-Stack Development**: React + FastAPI integration
5. **Workflow Orchestration**: Stage-based system design
6. **Lead Qualification**: Natural conversation flow
7. **Error Handling**: Graceful degradation and fallbacks
8. **Logging & Audit**: Production compliance

## 📄 License

This is a demonstration project for learning purposes.

## 👤 Contact

For questions about this workflow, refer to:
- `prompt_design.md` - Detailed prompt engineering decisions
- `test_transcripts/` - Real examples of each workflow stage
- Backend code comments for implementation details
