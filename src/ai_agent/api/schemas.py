from pydantic import BaseModel
from typing import List, Dict, Any

class PromptRequest(BaseModel):
    prompt: str
    apply: bool = False
    dry_run: bool = True
    user_context: Dict[str, Any] = {}

class PlanStep(BaseModel):
    type: str
    command: str | None = None
    backup: bool = False

class PromptResponse(BaseModel):
    id: str
    explanation: str
    plan: List[PlanStep]
    audit_entry: str | None = None