# Git Workflow Standard

> Companion to `OPERATING_RULES.md` and `Skills/Global/task-hub/SKILL.md`.

---

## 1. Purpose

This workflow closes the gap between task lifecycle and git lifecycle. 
Task Hub tracks ownership and reporting. Git tracks actual code history, review, and delivery.
Both must move together.

---

## 2. Core Rules

- **One task = one branch**
- **One logical change = one commit**
- **No task is truly done until it is committed**
- If remote/review exists, push + PR before final handoff
- Do not mix unrelated task changes on the same branch

---

## 3. Start a Task

Before writing code:

1. Update base branch
   - `git pull --ff-only`
2. Create a task branch
   - Preferred: `codex/<task-id>-<short-slug>`
   - Example: `codex/task-053-freeze-contracts`
3. Claim the task in Hub
4. Start implementation

---

## 4. During the Task

- Commit in small logical increments.
- Prefer commit messages that explain the actual change (Conventional Commits if possible).
- Example: `feat(hub): add git gates to task protocol`

---

## 5. Before Marking DONE in Hub

Complete this checklist:

1. Run relevant tests
2. Review `git status`
3. Stage only intended task files
4. Commit task changes
5. If remote/review exists: push branch and create/update PR
6. Then update:
   - Hub active/done files
   - `DASHBOARD.md`

### Minimum Gate

If there is code or doc output, the task **should have at least one commit** before it is moved to `done`.

---

## 6. Branch Naming

Use:
- lowercase
- short descriptive slug
- task id included

Avoid:
- `test`, `fix`, `new-branch`
- missing task id

---

## 7. Handoff Expectations

When handing off to another agent:
- mention the branch name
- mention commit hash if useful
- state whether branch is local only or pushed
- state whether PR exists
