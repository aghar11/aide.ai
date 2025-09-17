from fastapi import APIRouter
from ..api.schemas import PromptRequest, PromptResponse
from ..diagnostics.collector import collect_basic
from ..llm.orchestrator import generate_install_plan, generate_diagnose_plan
from ..executor.executor import dry_run_plan, execute_plan
import uuid

router = APIRouter()

@router.post("/api/v1/prompt", response_model=PromptResponse)
async def handle_prompt(req: PromptRequest):
    req_id = str(uuid.uuid4())
    snapshot = collect_basic()
    text = req.prompt.lower()
    if any(k in text for k in ("install", "setup", "setup")):
        llm_result = generate_install_plan(req.prompt, snapshot)
    elif any(k in text for k in ("slow", "sluggish", "virus", "malware", "diagnose")):
        llm_result = generate_diagnose_plan(req.prompt, snapshot)
    else:
        llm_result = generate_install_plan(req.prompt, snapshot)

    plan = llm_result.get("plan", [])
    explanation = llm_result.get("explanation", "")
    preview = dry_run_plan(plan)
    return {"id": req_id, "explanation": explanation, "plan": plan, "audit_entry": None}