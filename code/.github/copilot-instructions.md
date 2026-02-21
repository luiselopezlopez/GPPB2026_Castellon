# Copilot instructions for this repository

## Project overview
- This repo is a **single-file CLI chat client** for an Azure AI Project agent: [capibaras.py](capibaras.py).
- The script opens one persistent conversation, streams assistant output token-by-token, and deletes the conversation on exit.
- Main dependency boundary:
  - Azure auth/session: `DefaultAzureCredential` + `AIProjectClient`
  - Chat runtime: `openai_client.conversations` + `openai_client.responses.create(..., stream=True)`

## Runtime and configuration
- Required env var: `AZURE_AI_PROJECT_ENDPOINT` (loaded via `.env` with `python-dotenv`).
- Authentication uses `DefaultAzureCredential`; local runs usually require `az login` or valid managed identity context.
- Current package set is intentionally minimal and pinned in [requirements.txt](requirements.txt):
  - `azure-ai-projects>=2.0.0b1`
  - `azure-identity`
  - `python-dotenv`

## Local developer workflow
- Create/activate virtual env, then install deps from [requirements.txt](requirements.txt).
- Run the app directly: `python capibaras.py`.
- Interactive loop conventions:
  - Exit keywords: `salir`, `exit`, `quit`
  - Empty input is ignored
  - Prompt/response labels are colorized ANSI strings (`Prompt>`, `Agente>`)

## Code patterns to preserve
- Keep streaming output behavior based on `ResponseStreamEventType`:
  - append text on `RESPONSE_OUTPUT_TEXT_DELTA`
  - fallback to `RESPONSE_OUTPUT_TEXT_DONE` when no delta was printed
- Keep one conversation per process and delete it before shutdown.
- Keep the explicit system message that forces plain-text, non-Markdown responses.
- Keep agent binding in `extra_body` using agent reference:
  - `{"agent": {"name": "Capibaras", "type": "agent_reference"}}`

## Repo-specific conventions
- User-facing copy is currently Spanish (`Escribe tu prompt...`, `Agente>`); keep language consistent unless requested otherwise.
- This is a script-style codebase (top-level execution in [capibaras.py](capibaras.py)); avoid introducing extra project structure unless necessary.
- If adding features, prefer extending the existing loop and event handling rather than replacing with a framework.

## Useful file references
- Main logic and streaming behavior: [capibaras.py](capibaras.py)
- Dependencies: [requirements.txt](requirements.txt)
- Local env template/example values: [.env](.env)
