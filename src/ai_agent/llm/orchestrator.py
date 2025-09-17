import os, re, json
from typing import Dict, Any
from ..config import settings
from ..llm.prompts import build_prompt_for_install, build_prompt_for_diagnose
from ..utils.logger import get_logger

logger = get_logger(__name__)

try:
    import openai
    if settings.OPENAI_API_KEY:
        openai.api_key = settings.OPENAI_API_KEY
except Exception:
    openai = None
    logger.warning("openai package not available or API key not set; LLM calls will fail without config.")

def call_openai(prompt: str, max_tokens=512) -> str:
    logger.debug("Calling LLM with prompt length %d", len(prompt))
    if openai is None:
        return json.dumps({"plan": [], "notes": "OpenAI not configured in prototype."})
    resp = openai.Completion.create(
        engine="gpt-4o" if False else "gpt-4o-mini",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.1
    )
    txt = resp.choices[0].text.strip()
    return txt

def generate_install_plan(request_prompt: str, system_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    prompt = build_prompt_for_install(request_prompt, system_snapshot)
    raw = call_openai(prompt)
    # attempt to extract JSON blob
    m = re.search(r"(\{.*\})", raw, re.S)
    if not m:
        return {"explanation": raw, "plan": []}
    try:
        parsed = json.loads(m.group(1))
        return {"explanation": raw, "plan": parsed.get("plan", [])}
    except Exception:
        logger.exception("Failed to parse LLM JSON")
        return {"explanation": raw, "plan": []}

def generate_diagnose_plan(request_prompt: str, system_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    prompt = build_prompt_for_diagnose(request_prompt, system_snapshot)
    raw = call_openai(prompt)
    m = re.search(r"(\{.*\})", raw, re.S)
    if not m:
        return {"explanation": raw, "plan": []}
    try:
        parsed = json.loads(m.group(1))
        return {"explanation": raw, "plan": parsed.get("recommendations", [])}
    except Exception:
        logger.exception("Failed to parse LLM JSON")
        return {"explanation": raw, "plan": []}