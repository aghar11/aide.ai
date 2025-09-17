def build_prompt_for_install(user_request: str, snapshot: dict) -> str:
    sys_summary = []
    if snapshot.get("processes_top"):
        top = snapshot["processes_top"][:5]
        sys_summary.append("Top processes: " + ", ".join(f'{p.get("name")}(CPU={p.get("cpu_percent")})' for p in top))
    if snapshot.get("df"):
        sys_summary.append("Disk usage snapshot (df -h):\n" + snapshot["df"][:1000])

    prompt = f"""You are a careful system assistant. The user requested: "{user_request}"

System snapshot:
{chr(10).join(sys_summary)}

Instructions:
* Output a JSON object ONLY with keys "plan" (array of steps) and "notes" (explanation).
* Each plan step must be an object with "type" ("shell"|"note"), "command" for shell steps, and "backup" = true|false where applicable.
* Provide a minimal, safe plan. Use apt for Debian/Ubuntu. Do not attempt to modify system files other than configs inside the user's home without explicit confirmation.

Example:
{{
  "plan": [
    {{ "type": "shell", "command": "sudo apt update", "backup": false }},
    {{ "type": "shell", "command": "sudo apt install -y docker.io", "backup": false }}
  ],
  "notes": "Explanation of steps"
}}

Now produce the JSON for the user's request."""
    return prompt

def build_prompt_for_diagnose(user_request: str, snapshot: dict) -> str:
    prompt = f"""You are a cautious system diagnostics expert. The user said: "{user_request}"

System snapshot:
- top processes (first lines):
{snapshot.get('processes_top')}

- disk usage:
{snapshot.get('df')[:1000]}

- last journal entries (short):
{snapshot.get('journal')[:1000]}

Instructions:
* Output a JSON object with keys: "diagnosis" (string), "confidence" (0-1), "recommendations" (array of objects).
* Each recommendation should have "description", "command" (optional), and "risk" ("low"|"medium"|"high").

Return only JSON."""
    return prompt