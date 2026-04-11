# Git Workflow Standard

> Companion to `OPERATING_RULES.md` and the automated orchestrator workflow.

---

## 1. Purpose

This workflow closes the gap between task lifecycle and git lifecycle. 
The orchestrator (`run_orchestrator.py`) tracks execution and verification. Git tracks actual code history, review, and delivery.
Both must move together.

---

## 2. Core Rules

- **One task = one branch**
- **One logical change = one commit**
- **No task is truly done until it is committed**
- If remote/review exists, push + PR before final completion
- Do not mix unrelated task changes on the same branch

---

## 3. Start a Task

Before writing code:

1. Update base branch
   - `git pull --ff-only`
2. Create a task branch
   - Preferred: `codex/<task-id>-<slug>`
   - Example: `codex/TASK-001-freeze-contracts`
3. Prepare your `task.yaml`
4. Start implementation

---

## 4. During the Task

- Commit in small logical increments.
- Prefer commit messages that explain the actual change (Conventional Commits if possible).
- Example: `feat(core): add validator to orchestrator loop`

---

## 5. Before Marking Session Complete

Complete this checklist:

1. Run relevant tests or use `python run_orchestrator.py run path/to/task.yaml`
2. Review `git status`
3. Stage only intended task files
4. Commit task changes
5. If remote/review exists: push branch and create/update PR
6. Ensure orchestrator status is `passed`

---

## 6. Branch Naming

Use:
- lowercase
- short descriptive slug
- task id included (e.g., `TASK-001`)

Avoid:
- `test`, `fix`, `new-branch`
- missing task id

---

## 7. Handoff Expectations

When handing off to another agent or phase:
- mention the branch name
- mention commit hash if useful
- state whether branch is local only or pushed
- state whether PR exists
