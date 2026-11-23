# AI Multi-Agent PR Review

This project is an experimental Python application that sends source code to a Gemini model through three specialist review agents (bugs, security, and quality), then consolidates their findings through a lead reviewer agent.

The current entry point reads a fixed sample from `main.py` and prints the final review.

## Setup

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `GEMINI_API_KEY` in `.env` to a valid key obtained from the provider.

```powershell
python main.py
```

Do not commit `.env` or paste API keys into prompts, logs, code, or documentation.

## Project handoff

See [DEVELOPMENT_HANDOFF.md](DEVELOPMENT_HANDOFF.md) for the current implementation, architecture, known gaps, and the recommended continuation plan.