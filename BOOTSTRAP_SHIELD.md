# BOOTSTRAP_SHIELD

How to apply SHIELD to another repository.

## Pick An Adoption Mode

| Mode | Use when | What you copy |
|---|---|---|
| Prompt-only | quick exploration, short task, unsure repo | `GUIDE_FIRSTGUY.md`, `PROMPT_PACK.md`, `ONBOARDING.md`, `CHEATSHEET.md`, `tools/prompt-builder/` |
| Full runtime | long-term work, repeated tasks, need reports/handoffs/verification | `control_plane/`, `run_orchestrator.py`, `templates/`, `manifest.yaml`, `DASHBOARD.md`, `GUIDE_FIRSTGUY.md`, `ONBOARDING.md`, `OPERATING_RULES.md`, `CHEATSHEET.md`, `PROMPT_PACK.md`, `ROLE_SKILL_MATRIX.md`, `Skills/` |

If unsure, start Prompt-only.

If this is your first time applying SHIELD to a repo, read `GUIDE_FIRSTGUY.md` first.

## Validation Profiles

Use these add-ons only when you need them.

| Profile | Add these files | What it unlocks |
|---|---|---|
| Runtime core | already covered by `Full runtime` | `compile`, `plan`, `run`, `dashboard` |
| Audit-ready | `tests/fixtures/audit/` and optionally `SYSTEM_AUDIT.md` | `python run_orchestrator.py audit` |
| Prompt-sandbox-ready | `tools/prompt-builder/` | `python run_orchestrator.py prompt-sandbox` |

## Fast Path: Add SHIELD In 10 Steps

Use this when you want the simplest practical path for a new external repo.

1. Clone the target repo and make sure you can run it or at least identify the current failure clearly.
2. Decide whether you need `Prompt-only` or `Full runtime`.
3. Copy the required SHIELD files into the target repo root.
4. Add the SHIELD `.gitignore` rules for `runtime/`, `.hub/`, and `knowledge/compiled/`.
5. Read `GUIDE_FIRSTGUY.md` and choose one scenario: `zero build`, `improve existing repo`, or `solve issue`.
6. Trim `manifest.yaml` to only the roles you plan to use in that repo.
7. Run:

```bash
python run_orchestrator.py compile
```

8. Open the first leadership session: `product-manager-agent` for zero build or improvement, or `qa-lead-agent` for unclear issue triage.
9. Create one small approved task, then run:

```bash
python run_orchestrator.py plan path/to/task.yaml
python run_orchestrator.py run path/to/task.yaml
```

10. Read the outputs before opening more sessions: `DASHBOARD.md`, `.hub/done/`, `runtime/reports/session_reports/`, and `runtime/reports/quick_reports/`.

If the repo should support self-checking of SHIELD itself, also copy the audit fixtures and prompt-builder assets, then run `audit` and `prompt-sandbox`.

## Recommended First Step

Do not start by opening many worker sessions.

Start with Product and CTO:

```text
Product -> CTO -> tasks -> worker roles -> QA/reviewer
```

## Path A: Prompt-Only Adoption

Use this for a cloned repo you are still learning.

1. Clone the target repo.
2. Make the target repo run locally.
3. Read its `README`, configs, docs, and entrypoints.
4. Open a Product session using `PROMPT_PACK.md`.
5. Create a `leadership_brief`.
6. Open CTO only if architecture impact exists.
7. Create 1-3 small tasks.
8. Open worker sessions only for those tasks.
9. End each session with report or handoff.

## Path B: Full Runtime Adoption

Use this when SHIELD should become part of the repo workflow.

Current rule:

```text
SHIELD runtime should live at the target repo root.
```

The current CLI treats the folder containing `run_orchestrator.py` as repo root.

## Files To Copy

Required:

- `control_plane/`
- `run_orchestrator.py`
- `templates/`
- `manifest.yaml`
- `DASHBOARD.md`
- `GUIDE_FIRSTGUY.md`
- `ONBOARDING.md`
- `OPERATING_RULES.md`
- `CHEATSHEET.md`
- `PROMPT_PACK.md`
- `ROLE_SKILL_MATRIX.md`
- `Skills/`

Recommended:

- `CTO_PRODUCT_WORKFLOW.md`
- `SYSTEM_AUDIT.md`
- `tools/prompt-builder/`

Add these when you need stronger validation:

- for `audit`: `tests/fixtures/audit/`
- for `prompt-sandbox`: `tools/prompt-builder/`

Do not copy by default:

- `.skills_pool/`
- `refs_github/`
- generated `runtime/`
- generated `knowledge/compiled/`
- generated `.hub/`

## Ignore Rules

Add to the target repo `.gitignore`:

```gitignore
runtime/state/
runtime/cache/
runtime/sessions/
runtime/reports/
.hub/
knowledge/compiled/
knowledge/memory/
__pycache__/
*.pyc
.env
venv/
```

## Install Minimal Dependency

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pyyaml
```

Install the target repo's own dependencies separately.

## Bootstrap Checklist

1. Confirm target repo builds or at least has a known failure.
2. Read `GUIDE_FIRSTGUY.md` and choose the correct scenario.
3. Create or copy `DASHBOARD.md`.
4. Trim `manifest.yaml` to the roles you will actually use.
5. Run:

```bash
python run_orchestrator.py compile
```

6. Open Product or QA first based on the chosen scenario.
7. Create a small `leadership_brief` or triage summary.
8. Convert one approved task into `task.yaml`.
9. Run:

```bash
python run_orchestrator.py plan path/to/task.yaml
python run_orchestrator.py run path/to/task.yaml
```

If you copied `ROLE_SKILL_MATRIX.md`, `Skills/`, and `tests/fixtures/audit/`, run the serial audit once:

```bash
python run_orchestrator.py audit
```

## Three Common Scenarios

### Zero Build

1. Product defines problem and scope.
2. CTO defines architecture and first slice.
3. Workers implement one vertical slice.
4. QA verifies.

### Improve Existing Repo

1. Product defines improvement value.
2. CTO checks architecture impact.
3. Workers implement small scoped tasks.
4. Reviewer/QA verifies.

### Solve Issue

1. Product or QA clarifies impact and reproduction.
2. CTO triages technical boundary if needed.
3. Worker fixes the assigned task.
4. QA verifies the original issue.

## Common Mistakes

| Wrong | Right |
|---|---|
| Embed runtime before the target repo runs | Make the repo runnable first |
| Ask backend to figure out raw product scope | Product/CTO create tasks first |
| Open many sessions without tasks | Open sessions only after task assignment |
| Keep progress in chat only | Write session reports and handoffs |
| Treat `run` as the whole process | Use `run` after leadership has created tasks |
| Skip reports because command passed | Read session reports and quick reports after every run |
