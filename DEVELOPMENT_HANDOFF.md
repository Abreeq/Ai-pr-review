# Development Handoff

Last assessed: 2026-11-23

## Purpose

AI Multi-Agent PR Review is an experimental Python CLI that:

1. Accepts source code as a string.
2. Runs bug, security, and code-quality reviews concurrently.
3. Sends the three reports to a lead-reviewer prompt.
4. Produces one consolidated Markdown PR review.

The implemented application is a proof of concept. It is not yet a usable PR-review service or GitHub integration.

## Current State

### Implemented

- Gemini integration using `google-genai`.
- Environment-based API key loading with `python-dotenv`.
- Three specialist review prompts:
  - bug review
  - security review
  - code-quality review
- Lead-reviewer prompt that consolidates and prioritizes findings.
- Parallel execution of specialist agents with `ThreadPoolExecutor`.
- Fixed demo entry point in `main.py`.
- Basic console output.
- `.env` and virtual-environment exclusions in `.gitignore`.

### Not Implemented

- Real PR or Git diff collection.
- GitHub webhook, CLI flags, or API endpoints.
- File and line-aware structured review data.
- Retry policy for model calls.
- Tests.
- Configuration for model name or timeouts.
- Graceful handling of partial agent failures.
- Model-response validation.
- Cost, latency, and token reporting.
- Caching or rate limiting.
- Packaging and release configuration.

## Repository Layout

```text
main.py                    Fixed demo entry point
core/llm.py                Gemini client and environment loading
core/orchestrator.py       Parallel specialist execution and aggregation
agents/bug_agent.py        Bug-review prompt and agent
agents/security_agent.py   Security-review prompt and agent
agents/quality_agent.py    Maintainability-review prompt and agent
agents/reviewer_agent.py   Lead-reviewer consolidation prompt
utils/git_diff.py          Empty placeholder; intended for Git diff input
requirements.txt           Python dependencies
.env                       Local Gemini API key; ignored by Git
.gitignore                Ignores .env, venv, caches, and bytecode
```

## Runtime Flow

```text
main.py
  |
  v
review_code(code)
  |
  +--> bug agent --------+
  +--> security agent ---+--> ThreadPoolExecutor
  +--> quality agent ---+
                         |
                         v
              specialist reports
                         |
                         v
              lead reviewer agent
                         |
                         v
                 consolidated report
                         |
                         v
                  console output
```

There are four separate Gemini calls per review:

1. Bug review
2. Security review
3. Quality review
4. Lead-reviewer aggregation

The specialist calls run concurrently. The aggregation call runs only after all three reports are available.

## Key Modules

### `main.py`

Defines a hard-coded Python sample containing:

- a fake secret
- an average-calculation function
- a string-built SQL query
- an undefined database name

It calls `review_code(sample_code)` and prints the result.

This file will need to become a thin CLI or application entry point rather than owning demo input.

### `core/llm.py`

- Calls `load_dotenv()`.
- Reads `GEMINI_API_KEY`.
- Raises `ValueError` during module import when the key is missing.
- Creates one Gemini client at module import time.
- Uses `gemini-2.5-flash`.
- Uses `errors.APIError` for error handling.
- Handles HTTP 503 specially and returns `None` for failures.

Current consequences:

- Importing any agent fails before normal CLI argument handling if the key is missing.
- API/model configuration is not centralized.
- A model failure is converted to `None`, so callers lose error details.
- There is no timeout or retry configuration.

### `core/orchestrator.py`

- Creates a `ThreadPoolExecutor` with three workers.
- Submits exactly three specialist functions.
- Waits for all reports through `future.result()`.
- Calls the lead reviewer after specialist completion.

Current consequences:

- It is synchronous from the caller's perspective.
- One exception or hanging request can block or fail the whole review.
- `bug_report`, `security_report`, or `quality_report` may be `None`.
- The lead reviewer is not given the original code, only the agent summaries.

### `agents/bug_agent.py`

Prompts Gemini to find:

- logical errors
- runtime errors
- incorrect conditions
- missing edge cases
- possible crashes

The expected report fields are `BUG`, `LINE`, `SEVERITY`, `EXPLANATION`, and `SUGGESTED FIX`.

### `agents/security_agent.py`

Prompts Gemini to find:

- SQL injection
- hardcoded secrets
- unsafe input handling
- authentication or authorization weaknesses
- insecure data processing

The expected report fields are `VULNERABILITY`, `LINE`, `SEVERITY`, `EXPLANATION`, and `SUGGESTED FIX`.

### `agents/quality_agent.py`

Prompts Gemini to find meaningful maintainability issues and avoid reporting personal style preferences.

The expected report fields are `ISSUE`, `LINE`, `IMPORTANCE`, `EXPLANATION`, and `SUGGESTED IMPROVEMENT`.

### `agents/reviewer_agent.py`

Combines specialist reports into:

- overall summary
- critical issues
- high-priority issues
- medium-priority issues
- low-priority suggestions
- final recommendation

The lead prompt permits `APPROVE`, `REQUEST CHANGES`, or `NEEDS MANUAL REVIEW`.

### `utils/git_diff.py`

The file is empty. It does not yet collect Git changes or convert diff hunks into review input.

## Setup

The project was created with Python 3.12.4 and includes a local `venv`.

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Create `.env`:

```text
GEMINI_API_KEY=replace-with-a-new-local-key
```

Run:

```powershell
python main.py
```

Before continuing, rotate the existing Gemini key. Do not reuse or publish the previous value.

## Known Risks and Defects

### Security

- An API key is currently stored in the local ignored `.env` file. It must be rotated and removed from any shared shell, chat, export, or screenshot.
- The code reviewed by the model may contain proprietary or sensitive data. Define redaction and privacy behavior before production use.
- `.env.example` should be added with a placeholder, and `.env` must remain ignored.

### Reliability

- API failures become `None`; the lead reviewer can receive missing data.
- There is no timeout or retry loop beyond SDK defaults.
- There is no structured exception model.
- No tests exercise orchestration or prompts.

### Accuracy

- Results depend on free-form model text rather than typed review objects.
- The lead reviewer receives no original source, only specialist reports.
- Line numbers are not independently verified.
- Duplicate and contradictory findings are not deduplicated deterministically.

### Scope

- The application reviews pasted code, not a real pull request.
- `git_diff.py` is only a placeholder.
- It is currently not integrated with GitHub, CI, or developer tooling.

## Recommended Development Plan

### Phase 1: Stabilize the Core

1. Add a typed review schema with:
   - category
   - severity
   - file
   - start/end line
   - title
   - explanation
   - suggested fix
   - confidence
   - status
2. Make Gemini calls return structured JSON and validate it.
3. Centralize model configuration.
4. Replace import-time API-key validation with explicit startup validation.
5. Add retry, timeout, and cancellation behavior.
6. Preserve partial-failure information instead of silently returning `None`.
7. Remove hard-coded demo code from `main.py`.

### Phase 2: Add Real Diff Input

1. Implement `utils/git_diff.py` with an API such as:

```python
get_git_diff(repo_path: str, base: str, head: str) -> list[DiffFile]
```

2. Parse changed files and hunks.
3. Add file paths and line numbers to review prompts.
4. Limit review input to changed lines plus sufficient context.
5. Support commits, local branches, staged files, and pull request refs.

### Phase 3: Improve the CLI

Add arguments such as:

```text
--repo
--base
--head
--files
--format markdown|json
--model
--timeout
--fail-on critical|high|none
```

Choose a stable CLI library and add:

- help text
- validation
- exit codes
- JSON output
- machine-readable progress

### Phase 4: Add GitHub Integration

1. Authenticate with GitHub.
2. Fetch PR metadata and changed files.
3. Map diff line numbers to PR review positions.
4. Post a consolidated summary.
5. Optionally create inline comments.
6. Support idempotency and update existing bot comments.
7. Keep approvals and change requests clearly separated from informational findings.

### Phase 5: Add Tests and Quality Gates

Minimum test coverage:

- environment loading
- missing API key
- provider success
- 503 and general API errors
- each specialist agent
- orchestration success
- partial specialist failure
- aggregation success
- aggregation failure
- diff parsing
- structured JSON parsing
- CLI arguments

Use mocks for all Gemini calls.

## Suggested First Task

Start with a small, dependency-safe implementation:

1. Add a typed `ReviewFinding` and `ReviewReport` model.
2. Add `GEMINI_MODEL`, timeout, and API-key settings.
3. Update `ask_gemini()` to return a small result object or raise a domain exception.
4. Update specialist prompts to return JSON matching the finding model.
5. Validate and normalize JSON responses.
6. Update the orchestrator so partial failures are reported instead of silently converted.
7. Add unit tests for success, malformed JSON, missing key, and partial failure.
8. Keep `main.py` demo behavior working but make it explicitly demo-only.

Do not start GitHub integration until diff parsing and typed review output are stable.

## Prompt for the Next LLM

```text
Continue development of this repository from DEVELOPMENT_HANDOFF.md.

Treat the handoff as the source of truth for current behavior and progress.
Preserve the existing public entry point review_code(code) until a replacement
is explicitly planned.

Work in the following order:
1. Stabilize error handling and configuration.
2. Introduce typed, validated review results.
3. Implement real Git diff input.
4. Add a CLI and tests.
5. Add GitHub PR integration last.

Do not invent features outside this list. Do not expose or log GEMINI_API_KEY.
Use existing repository patterns. Add focused tests for behavior you change.
Before finishing, run the smallest relevant test or syntax-validation command.
```
