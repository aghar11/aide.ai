# aide.ai — CLI-first AI OS Agent (Prototype)

This repository is a **prototype** for an AI-first OSagent daemon + CLI branded as **aide.ai**. It demonstrates prompt-based installs, environment setup, and basic diagnostics on Linux (Ubuntu-friendly).

**Important:** this is a minimal prototype for experimentation. DO NOT run `--apply` commands on production machines without auditing the generated plan.

## Quick start (dev)

1. Create a Python virtual env:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   # edit .env and set OPENAI_API_KEY=sk-...
   ```

3. Start the daemon:
   ```bash
   python -m src.ai_agent.main
   ```

4. In another terminal, run the CLI:
   ```bash
   python -m src.cli.cli ask "Install docker and python3-pip with numpy"
   ```

5. By default the agent uses **dry-run**. To actually apply generated commands (use with care):
   ```bash
   python -m src.cli.cli ask "Install docker and python3-pip with numpy" --apply --no-dry-run
   ```

## Branding

This prototype is branded as **aide.ai**. The CLI command is `aide` (a launcher script is included at the repo root).

## Project layout (important files)

```
aide-ai/
├── requirements.txt
├── .env.example
├── systemd/aide-agent.service
├── src/
│   ├── ai_agent/    # daemon service
│   └── cli/         # CLI client
└── tests/           # simple unit test stubs
```

## Safety & notes

- The prototype **calls OpenAI** by default. Do not commit API keys to git.
- The executor in this prototype is intentionally simple. It may run shell commands using `shell=True` — **this is unsafe for production**.
- Default behavior is `dry-run`. Always review generated plans before applying.
- This is targeted at Ubuntu/Debian for package commands (apt).

## License & attribution

Prototype code provided for educational purposes. Extend/improve responsibly.

## Installing via pip (developer / local)

To install the `aide` command globally (or in your virtualenv), run:

```bash
# from the repository root
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
# 'aide' should now be available as a console command:
aide --help
```

This creates a console script `aide` that points to the CLI. The repository already includes a lightweight launcher `./aide` at the repo root for quick demos, but installing with pip is the recommended developer flow.

Note: the package is a prototype. Review code and `.env` before running the daemon.
