from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import ChatRequest, ChatResponse, ConversationState
from sop_loader import load_sop
from workflow import run_workflow

app = FastAPI(title="SkillBridge AI Support Workflow")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SOP = load_sop()


@app.get("/")
def root():
    return {"message": "SkillBridge AI Support Workflow API is running"}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/state")
def initial_state():
    return ConversationState()


@app.get("/api/sop")
def get_sop():
    return {"sop": SOP}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = run_workflow(
        message=request.message,
        state=request.state,
        sop=SOP,
    )
    return ChatResponse(**result)
