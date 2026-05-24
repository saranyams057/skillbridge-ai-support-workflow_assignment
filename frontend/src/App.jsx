import React, { useEffect, useState } from "react";
import {
  AlertTriangle,
  Bot,
  CheckCircle2,
  ClipboardList,
  GraduationCap,
  RefreshCcw,
  Send,
  ShieldCheck,
  User,
} from "lucide-react";
import { getInitialState, sendMessage } from "./api";

export default function App() {
  const [state, setState] = useState(null);
  const [input, setInput] = useState("");
  const [stage, setStage] = useState("not_started");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getInitialState().then(setState);
  }, []);

  async function handleSend() {
    if (!input.trim() || !state || loading) return;

    const userMessage = input;
    setInput("");
    setLoading(true);

    const optimistic = {
      ...state,
      messages: [...state.messages, { role: "user", content: userMessage, timestamp: new Date().toISOString() }],
    };
    setState(optimistic);

    try {
      const data = await sendMessage(userMessage, state);
      setState(data.state);
      setStage(data.stage);
    } catch (error) {
      console.error(error);
      alert("Request failed. Check backend server and OPENAI_API_KEY.");
    } finally {
      setLoading(false);
    }
  }

  async function resetChat() {
    const initial = await getInitialState();
    setState(initial);
    setStage("not_started");
    setInput("");
  }

  if (!state) return <div className="loading-screen">Loading SkillBridge Assistant...</div>;

  const lead = state.lead_data || {};
  const usage = state.usage || {};

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><GraduationCap size={26} /></div>
          <div>
            <h1>SkillBridge AI</h1>
            <p>Course Enrollment Support Workflow</p>
          </div>
        </div>

        <div className="panel">
          <h2>Current Stage</h2>
          <span className="stage-pill">{stage.replaceAll("_", " ")}</span>
        </div>

        <div className="panel guardrails">
          <div className="panel-title">
            <ShieldCheck size={18} />
            <h2>Production Guardrails</h2>
          </div>
          <Guardrail text="Two-layer escalation detection" />
          <Guardrail text="Three-layer hallucination defense" />
          <Guardrail text="Confidence threshold: 0.70" />
          <Guardrail text="Conversation limit: 12 messages" />
        </div>

        {state.escalated && (
          <div className="panel danger">
            <div className="panel-title">
              <AlertTriangle size={18} />
              <h2>Escalation Triggered</h2>
            </div>
            <p>{state.escalation_reason}</p>
            <small>Category: {state.escalation_category || "unknown"}</small>
          </div>
        )}

        <div className="panel">
          <div className="panel-title">
            <ClipboardList size={18} />
            <h2>Lead Details</h2>
          </div>
          <Info label="Course" value={lead.interested_course} />
          <Info label="Goal" value={lead.learning_goal} />
          <Info label="Skill Level" value={lead.current_skill_level} />
          <Info label="Learner Type" value={lead.learner_type} />
          <Info label="Batch" value={lead.preferred_batch} />
          <Info label="Start Timeline" value={lead.timeline_to_start} />
          <Info label="Contact" value={lead.contact_detail} />
        </div>

        <div className="panel">
          <h2>Usage Estimate</h2>
          <Info label="Model Calls" value={usage.model_calls} />
          <Info label="Input Tokens" value={usage.estimated_input_tokens} />
          <Info label="Output Tokens" value={usage.estimated_output_tokens} />
        </div>

        <button className="reset-btn" onClick={resetChat}>
          <RefreshCcw size={16} />
          Reset Session
        </button>
      </aside>

      <main className="chat-section">
        <header className="chat-header">
          <div>
            <h2>SkillBridge Academy Assistant</h2>
            <p>Demo SOP-grounded AI workflow for course enquiries, lead qualification, escalation, and summaries.</p>
          </div>
        </header>

        <div className="chat-box">
          {state.messages.length === 0 && (
            <div className="empty-state">
              <GraduationCap size={50} />
              <h3>Start a course enquiry</h3>
              <p>Try course fee, duration, batch timing, certificate, placement support, or enrollment questions.</p>
            </div>
          )}

          {state.messages.map((msg, index) => (
            <div key={index} className={`message-row ${msg.role}`}>
              <div className="avatar">{msg.role === "user" ? <User size={18} /> : <Bot size={18} />}</div>
              <div className="message-bubble">
                {msg.content.split("\n").map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="avatar"><Bot size={18} /></div>
              <div className="message-bubble typing">Thinking safely...</div>
            </div>
          )}
        </div>

        <footer className="chat-input-area">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Type learner message..."
          />
          <button onClick={handleSend} disabled={loading}>
            <Send size={18} />
          </button>
        </footer>

        <div className="quick-actions">
          <button onClick={() => setInput("What is the fee and duration for the Generative AI Basics course?")}>In-SOP FAQ</button>
          <button onClick={() => setInput("I want to learn AI but I only know basic Python. Which course should I choose?")}>Lead Qualification</button>
          <button onClick={() => setInput("Do you provide a guaranteed job after the course?")}>Escalation</button>
          <button onClick={() => setInput("Do you have EMI options?")}>Unsupported Policy</button>
          <button onClick={() => setInput("Can I get a refund? I am not happy with the course.")}>Complaint</button>
          <button onClick={() => setInput("summary")}>Generate Summary</button>
        </div>
      </main>
    </div>
  );
}

function Info({ label, value }) {
  return (
    <div className="info-row">
      <span>{label}</span>
      <strong>{value || "Not collected"}</strong>
    </div>
  );
}

function Guardrail({ text }) {
  return (
    <div className="guardrail-item">
      <CheckCircle2 size={15} />
      <span>{text}</span>
    </div>
  );
}
