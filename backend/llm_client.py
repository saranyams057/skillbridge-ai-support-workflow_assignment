import json
from typing import Any, Dict

from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL
from prompts import SYSTEM_PROMPT
from schemas import ConversationState
from utils import estimate_tokens

client = OpenAI(api_key=OPENAI_API_KEY)


def call_llm_json(
    prompt: str,
    state: ConversationState,
    system_prompt: str = SYSTEM_PROMPT,
) -> Dict[str, Any]:
    try:
        state.usage.model_calls += 1
        state.usage.estimated_input_tokens += estimate_tokens(system_prompt + prompt)

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
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
