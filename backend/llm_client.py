import json
from typing import Any, Dict

from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL
from prompts import SYSTEM_PROMPT
from schemas import ConversationState
from utils import estimate_tokens

client = Groq(api_key=GROQ_API_KEY)


def call_llm_json(prompt: str, state: ConversationState) -> Dict[str, Any]:
    try:
        state.usage.model_calls += 1
        state.usage.estimated_input_tokens += estimate_tokens(SYSTEM_PROMPT + prompt)

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content or "{}"
        state.usage.estimated_output_tokens += estimate_tokens(content)

        return json.loads(content)

    except json.JSONDecodeError:
        return {
            "system_error": True,
            "should_escalate": True,
            "reason": "Invalid model JSON response. Human handoff required.",
            "category": "system_error",
            "confidence": 1.0,
            "customer_sentiment": "neutral",
        }

    except Exception:
        return {
            "system_error": True,
            "should_escalate": True,
            "reason": "LLM provider error. Human handoff required.",
            "category": "system_error",
            "confidence": 1.0,
            "customer_sentiment": "neutral",
        }
