import subprocess, shlex, json
from pathlib import Path
from typing import List, Dict, Any
from ..utils.logger import get_logger

logger = get_logger(__name__)
AUDIT_DIR = Path.home() / ".aide_ai" / "audit"
BACKUP_DIR = Path.home() / ".aide_ai" / "backups"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def dry_run_plan(plan: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"would_execute": [step for step in plan if step.get("type") == "shell"]}

def execute_plan(plan: List[Dict[str, Any]], apply: bool = False) -> Dict[str, Any]:
    results = []
    rollback_commands = []
    for step in plan:
        if step.get("type") != "shell":
            results.append({"step": step, "skipped": True})
            continue
        cmd = step.get("command")
        if not apply:
            results.append({"step": step, "executed": False})
            continue
        logger.info("Running command: %s", cmd)
        try:
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            results.append({"step": step, "executed": True, "returncode": proc.returncode, "stdout": proc.stdout[:2000], "stderr": proc.stderr[:2000]})
            if "apt install" in cmd or "apt-get install" in cmd:
                pkgs = _extract_pkgs_from_apt(cmd)
                for p in pkgs:
                    rollback_commands.append(f"sudo apt remove -y {p} && sudo apt autoremove -y")
        except Exception as e:
            logger.exception("command failed")
            results.append({"step": step, "executed": True, "error": str(e)})

    rb_path = BACKUP_DIR / f"rollback-{len(list(BACKUP_DIR.iterdir()))+1}.sh"
    if rollback_commands:
        rb_path.write_text("\n".join(["#!/usr/bin/env bash"] + rollback_commands))
        rb_path.chmod(0o700)

    audit_path = AUDIT_DIR / f"audit-{len(list(AUDIT_DIR.iterdir()))+1}.json"
    audit_path.write_text(json.dumps({"plan": plan, "results": results, "rollback": str(rb_path)}, indent=2))
    return {"results": results, "rollback_script": str(rb_path)}

def _extract_pkgs_from_apt(cmd: str):
    parts = shlex.split(cmd)
    if "install" in parts:
        try:
            idx = parts.index("install")
            return [p for p in parts[idx+1:] if not p.startswith("-")]
        except ValueError:
            return []
    return []